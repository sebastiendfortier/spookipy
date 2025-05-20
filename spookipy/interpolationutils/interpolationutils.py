# -*- coding: utf-8 -*-
import copy
import multiprocessing

import fstpy
from ..comparisonutils import _gt_, _lt_
import numpy as np
import pandas as pd
from ..rmn_interface import RmnInterface
from typing import List, Tuple, Optional
from ..utils import get_split_value, to_dask


def find_index_of_lat_lon_not_in_grid(
    input_grid: int,
    grid_horizontal_dimension: float,
    grid_vertical_dimension: float,
    latitudes: np.ndarray,
    longitudes: np.ndarray,
) -> List[int]:
    """
    Finds the indices of latitude-longitude pairs that are not within the given grid dimensions.

    This function converts latitude-longitude pairs to a coordinate system compatible with the input grid,
    then checks if these coordinates fall within the defined grid bounds. It returns a list of indices
    corresponding to pairs that are outside these bounds.

    :param input_grid: The gridid of the input grid data.
    :type input_grid: int
    :param grid_horizontal_dimension: The horizontal dimension of the grid.
    :type grid_horizontal_dimension: float
    :param grid_vertical_dimension: The vertical dimension of the grid.
    :type grid_vertical_dimension: float
    :param latitudes: A NumPy array of latitudes.
    :type latitudes: numpy.ndarray
    :param longitudes: A NumPy array of longitudes.
    :type longitudes: numpy.ndarray
    :return: A list of indices corresponding to latitude-longitude pairs outside the grid boundaries.
    :rtype: list[int]
    """
    coords = RmnInterface.get_xy_from_lat_lon(input_grid, latitudes.ravel(order="F"), longitudes.ravel(order="F"))

    x_grid_lower_bound = 0.5
    x_grid_upper_bound = grid_horizontal_dimension + 0.5
    y_grid_lower_bound = 0.5
    y_grid_upper_bound = grid_vertical_dimension + 0.5

    # find index of latlon not in input grid limits
    epsilon = 0.00002
    indexes = []
    for i in range(len(latitudes)):
        # need an epsilon
        # ex: for the south pole ezscint can return something like 0.499987 instead of 0.5
        # print("coords['x'][i]",coords['x'][i],"coords['y'][i]",coords['y'][i])
        if (
            _lt_(coords["x"][i], x_grid_lower_bound, epsilon)
            or _gt_(coords["x"][i], x_grid_upper_bound, epsilon)
            or _lt_(coords["y"][i], y_grid_lower_bound, epsilon)
            or _gt_(coords["y"][i], y_grid_upper_bound, epsilon)
        ):
            indexes.append(i)

    return indexes


class ExtrapolationError(Exception):
    pass


def do_extrapolation(
    interpolated_data: np.ndarray,
    data_before_interpolation: np.ndarray,
    indexes: Optional[List[int]],
    extrapolation_type: str,
    extrapolation_value: float,
) -> np.ndarray:
    """
    Performs extrapolation on interpolated data based on the specified type and value.

    This function applies different extrapolation methods to the interpolated data based on the `extrapolation_type` argument. It supports four types of extrapolations: "value", "maximum", "minimum", and "abort".

    :param interpolated_data: The data after interpolation, typically a NumPy array.
    :type interpolated_data: numpy.ndarray
    :param data_before_interpolation: The original data before interpolation, also a NumPy array.
    :type data_before_interpolation: numpy.ndarray
    :param indexes: A list of indices where extrapolation needs to be applied. Can be None.
    :type indexes: Optional[list[int]]
    :param extrapolation_type: The type of extrapolation to apply. Options are "value", "maximum", "minimum", or "abort".
    :type extrapolation_type: str
    :param extrapolation_value: The value to use for extrapolation when `extrapolation_type` is "value". Ignored otherwise.
    :type extrapolation_value: float
    :return: The modified interpolated data with extrapolation applied according to the specified type.
    :rtype: numpy.ndarray
    :raises ExtrapolationError: If the `extrapolation_type` is "abort", raising an error to indicate the process was aborted.
    """
    if extrapolation_type == "value":
        # replace value at latlon outside grid by a fixed value
        for i in indexes:
            interpolated_data[i] = extrapolation_value

    elif extrapolation_type == "maximum":
        min, max = find_min_max(data_before_interpolation)
        max = max + (max - min) * 0.05

        # replace value at latlon outside grid by the max value of the fields
        for i in indexes:
            interpolated_data[i] = max

    elif extrapolation_type == "minimum":
        min, max = find_min_max(data_before_interpolation)
        min = min - (max - min) * 0.05

        # replace value at latlon outside grid by the min value of the fields
        for i in indexes:
            interpolated_data[i] = min

    elif extrapolation_type == "abort":
        raise ExtrapolationError("ABORTED AS REQUESTED BY THE USE OF THE 'extrapolation_type ABORT' OPTION.\n")

    return interpolated_data


def find_min_max(array: np.ndarray) -> Tuple[float, float]:
    """
    Finds the minimum and maximum values in a NumPy array.

    :param array: The NumPy array from which to find the minimum and maximum values.
    :type array: numpy.ndarray
    :return: A tuple containing the minimum and maximum values found in the array.
    :rtype: tuple[float, float]
    """
    return np.min(array), np.max(array)


def keep_intact_hy_field(current_group: pd.DataFrame, no_mod: List[pd.DataFrame]) -> None:
    """
    Filters a group of dataframes to retain those with a specific column ('HY').

    This function iterates through a group of dataframes (`current_group`) and filters them
    based on the presence of a specific column named 'HY'. Only those dataframes that contain the 'HY' column are
    retained and appended to the `no_mod` list.

    :param current_group: A group of dataframes to filter.
    :type current_group: pandas.DataFrame
    :param no_mod: A list to append the filtered dataframes to.
    :type no_mod: list[pandas.DataFrame]
    """
    hy_df = current_group.loc[current_group.nomvar == "HY"].reset_index(drop=True)
    if not hy_df.empty:
        no_mod.append(hy_df)


def keep_toctoc(current_group: pd.DataFrame, results: List[pd.DataFrame]) -> None:
    """
    Filters rows from a DataFrame based on a specific column condition and appends them to a results list.

    This function filters the `current_group` DataFrame to keep only those rows where the `nomvar` column equals '!!'.

    :param current_group: The DataFrame to filter.
    :type current_group: pandas.DataFrame
    :param results: A list to which the filtered DataFrame rows are appended.
    :type results: list[pandas.DataFrame]
    """
    toctoc_df = current_group.loc[current_group.nomvar == "!!"].reset_index(drop=True)
    # we can add toctoc from input grid
    if not toctoc_df.empty:
        results.append(toctoc_df)


def scalar_interpolation(
    df: pd.DataFrame,
    results: List[pd.DataFrame],
    input_grid: int,
    output_grid: int,
    extrapolation_type: str,
    extrapolation_value: float,
    indexes: Optional[List[int]] = None,
) -> None:
    """
    Performs scalar interpolation on a DataFrame and handles extrapolation based on specified criteria.

    :param df: The input DataFrame containing the data to be interpolated.
    :type df: pandas.DataFrame
    :param results: A list to append the processed DataFrames to.
    :type results: list[pandas.DataFrame]
    :param input_grid: The gridid of the input grid data.
    :type input_grid: int
    :param output_grid: The gridid of the output grid data.
    :type output_grid: int
    :param extrapolation_type: The type of extrapolation to apply ("value", "maximum", "minimum", or "abort").
    :type extrapolation_type: str
    :param extrapolation_value: The value to use for extrapolation when `extrapolation_type` is "value".
    :type extrapolation_value: float
    :param indexes: A list of indices where extrapolation needs to be applied. Can be None.
    :type indexes: Optional[list[int]]
    """
    if df.empty:
        return
    # scalar except PT
    int_df = copy.deepcopy(df)

    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)

    int_df_list = np.array_split(int_df, split_value)

    for df, int_df in zip(df_list, int_df_list):
        df = fstpy.compute(df)

        for i in df.index:
            arr = RmnInterface.scalar_interpolation(output_grid, input_grid, df.at[i, "d"])

            # InterpolationHorizontalGrid ne fait jamais d'extrapolation
            if indexes is not None and len(indexes):
                arr = do_extrapolation(arr, df.at[i, "d"], indexes, extrapolation_type, extrapolation_value)

            int_df.at[i, "d"] = to_dask(arr)

        results.append(int_df)


def scalar_interp_with_extrapolation(
    out_grid: int, in_grid: int, data: np.ndarray, indexes: Optional[List[int]], extp_type: str, extp_value: float
) -> np.ndarray:
    """
    Interpolates data between two grids and applies extrapolation based on specified criteria.

    :param out_grid: The gridid of the output grid data.
    :type out_grid: int
    :param in_grid: The gridid of the input grid data.
    :type in_grid: int
    :param data: The data to be interpolated.
    :type data: numpy.ndarray
    :param indexes: A list of indices where extrapolation needs to be applied. Can be None.
    :type indexes: Optional[list[int]]
    :param extp_type: The type of extrapolation to apply ("value", "maximum", "minimum", or "abort").
    :type extp_type: str
    :param extp_value: The value to use for extrapolation when `extp_type` is "value".
    :type extp_value: float
    :return: The interpolated data with extrapolation applied according to the specified type.
    :rtype: numpy.ndarray
    """
    arr = RmnInterface.scalar_interpolation(int(out_grid), int(in_grid), data)
    arr = do_extrapolation(arr, data, indexes.get(), extp_type, extp_value)
    return arr


def scalar_interpolation_parallel(
    df: pd.DataFrame,
    results: List[pd.DataFrame],
    input_grid: int,
    output_grid: int,
    extrapolation_type: str,
    extrapolation_value: float,
    indexes: Optional[List[int]] = None,
) -> None:
    """
    Performs parallel scalar interpolation on a DataFrame and handles extrapolation based on specified criteria.

    :param df: The input DataFrame containing the data to be interpolated.
    :type df: pandas.DataFrame
    :param results: A list to append the processed DataFrames to.
    :type results: list[pandas.DataFrame]
    :param input_grid: The gridid of the input grid data.
    :type input_grid: int
    :param output_grid: The gridid of the output grid data.
    :type output_grid: int
    :param extrapolation_type: The type of extrapolation to apply ("value", "maximum", "minimum", or "abort").
    :type extrapolation_type: str
    :param extrapolation_value: The value to use for extrapolation when `extrapolation_type` is "value".
    :type extrapolation_value: float
    :param indexes: A list of indices where extrapolation needs to be applied. Can be None.
    :type indexes: Optional[list[int]]
    """
    if df.empty:
        return

    # scalar except PT
    int_df = copy.deepcopy(df)

    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)

    int_df_list = np.array_split(int_df, split_value)

    for df, int_df in zip(df_list, int_df_list):
        df = fstpy.compute(df)

        output_grid_arr = [output_grid for _ in range(len(df.index))]
        input_grid_arr = [input_grid for _ in range(len(df.index))]

        # InterpolationHorizontalGrid ne fait jamais d'extrapolation
        if indexes is not None and len(indexes):
            indexes_arr = [
                ListWrapper(indexes) for _ in range(len(df.index))
            ]  # np.full((len(df.index)),ListWrapper(indexes))
            extrapolation_type_arr = [
                extrapolation_type for _ in range(len(df.index))
            ]  # np.full((len(df.index)),extrapolation_type)
            extrapolation_value_arr = [
                extrapolation_value for _ in range(len(df.index))
            ]  # np.full((len(df.index)),extrapolation_value)

        with multiprocessing.Pool() as pool:
            # InterpolationHorizontalGrid ne fait jamais d'extrapolation
            if indexes is not None and len(indexes):
                interp_res = pool.starmap(
                    scalar_interp_with_extrapolation,
                    zip(
                        output_grid_arr,
                        input_grid_arr,
                        df.d.to_list(),
                        indexes_arr,
                        extrapolation_type_arr,
                        extrapolation_value_arr,
                    ),
                )
            else:
                interp_res = pool.starmap(scalar_interp, zip(output_grid_arr, input_grid_arr, df.d.to_list()))

            int_df["d"] = [to_dask(r) for r in interp_res]

        results.append(int_df)


def set_interpolation_type_options(interpolation_type: str) -> None:
    """
    Sets the interpolation degree option based on the specified interpolation type.

    :param interpolation_type: The type of interpolation to set ('nearest', 'bi-linear', or 'bi-cubic').
    :type interpolation_type: str
    """
    if interpolation_type == "nearest":
        RmnInterface.set_interpolation_options("INTERP_DEGREE", "NEAREST")
    elif interpolation_type == "bi-linear":
        RmnInterface.set_interpolation_options("INTERP_DEGREE", "LINEAR")
    elif interpolation_type == "bi-cubic":
        RmnInterface.set_interpolation_options("INTERP_DEGREE", "CUBIC")


def select_input_grid_source_data(
    vect_df: pd.DataFrame, others_df: pd.DataFrame, pt_df: pd.DataFrame
) -> Tuple[pd.DataFrame, str]:
    """
    Selects the source DataFrame for grid data based on availability and assigns the grid type.

    :param vect_df: The first DataFrame to check for data.
    :type vect_df: pandas.DataFrame
    :param others_df: The second DataFrame to check for data.
    :type others_df: pandas.DataFrame
    :param pt_df: The third DataFrame to check for data.
    :type pt_df: pandas.DataFrame
    :return: A tuple containing the selected source DataFrame and the extracted grid type.
    :rtype: Tuple[pandas.DataFrame, str]
    """
    grtyp = ""
    if not vect_df.empty:
        grtyp = vect_df.iloc[0]["grtyp"]
        source_df = vect_df
    elif not others_df.empty:
        grtyp = others_df.iloc[0]["grtyp"]
        source_df = others_df
    elif not pt_df.empty:
        grtyp = pt_df.iloc[0]["grtyp"]
        source_df = pt_df
    else:
        source_df = pd.DataFrame(dtype=object)

    return source_df, grtyp


def scalar_interp(out_grid: int, in_grid: int, data: np.ndarray) -> np.ndarray:
    """
    Performs scalar interpolation from one grid to another.

    :param out_grid: The gridid of the output grid data.
    :type out_grid: int
    :param in_grid: The gridid of the input grid data.
    :type in_grid: int
    :param data: The data to be interpolated.
    :type data: numpy.ndarray
    :return: The interpolated data as a NumPy array.
    :rtype: numpy.ndarray
    """
    arr = RmnInterface.scalar_interpolation(int(out_grid), int(in_grid), data)
    return arr


def vectorial_interpolation(
    vect_df: pd.DataFrame,
    results: List[pd.DataFrame],
    input_grid: int,
    output_grid: int,
    extrapolation_type: str,
    extrapolation_value: float,
    indexes: Optional[List[int]] = None,
) -> None:
    """
    Performs vectorial interpolation on a DataFrame and handles extrapolation based on specified criteria.

    This function processes a DataFrame containing vector components ('UU' and 'VV') separately, sorts them,
    and performs interpolation between input and output grids using `rmn.ezuvint`.
    It then applies extrapolation to the interpolated data if necessary.

    :param vect_df: The input DataFrame containing vector components ('UU' and 'VV').
    :type vect_df: pandas.DataFrame
    :param results: A list to append the processed DataFrames to.
    :type results: list[pandas.DataFrame]
    :param input_grid: The gridid of the input grid data.
    :type input_grid: int
    :param output_grid: The gridid of the output grid data.
    :type output_grid: int
    :param extrapolation_type: The type of extrapolation to apply ("value", "maximum", "minimum", or "abort").
    :type extrapolation_type: str
    :param extrapolation_value: The value to use for extrapolation when `extrapolation_type` is "value".
    :type extrapolation_value: float
    :param indexes: A list of indices where extrapolation needs to be applied. Can be None.
    :type indexes: Optional[list[int]]
    """
    if vect_df.empty:
        return

    uu_df = (
        vect_df.loc[vect_df.nomvar == "UU"]
        .sort_values("level", ascending=vect_df.iloc[0].ascending)
        .reset_index(drop=True)
    )
    vv_df = (
        vect_df.loc[vect_df.nomvar == "VV"]
        .sort_values("level", ascending=vect_df.iloc[0].ascending)
        .reset_index(drop=True)
    )

    if (uu_df.empty) or (vv_df.empty):
        return

    uu_int_df = copy.deepcopy(uu_df)
    vv_int_df = copy.deepcopy(vv_df)

    split_value = get_split_value(uu_df)

    uu_df_list = np.array_split(uu_df, split_value)
    vv_df_list = np.array_split(vv_df, split_value)
    uu_int_df_list = np.array_split(uu_int_df, split_value)
    vv_int_df_list = np.array_split(vv_int_df, split_value)

    for uu_df, vv_df, uu_int_df, vv_int_df in zip(uu_df_list, vv_df_list, uu_int_df_list, vv_int_df_list):
        uu_df = fstpy.compute(uu_df)
        vv_df = fstpy.compute(vv_df)

        for i in uu_df.index:
            (uu, vv) = RmnInterface.vectorial_interpolation(output_grid, input_grid, uu_df.at[i, "d"], vv_df.at[i, "d"])

            # InterpolationHorizontalGrid ne fait jamais d'extrapolation
            if indexes is not None and len(indexes):
                uu = do_extrapolation(uu, uu_int_df.at[i, "d"], indexes, extrapolation_type, extrapolation_value)
                vv = do_extrapolation(vv, vv_int_df.at[i, "d"], indexes, extrapolation_type, extrapolation_value)

            uu_int_df.at[i, "d"] = uu
            vv_int_df.at[i, "d"] = vv

        results.append(uu_int_df)
        results.append(vv_int_df)


def vect_interp(output_grid, input_grid, uu_data, vv_data):
    return RmnInterface.vectorial_interpolation(int(output_grid), int(input_grid), uu_data, vv_data)


def vectorial_interpolation_parallel(
    vect_df: pd.DataFrame,
    results: List[pd.DataFrame],
    input_grid: int,
    output_grid: int,
    extrapolation_type: str,
    extrapolation_value: float,
    indexes: Optional[List[int]] = None,
) -> None:
    """
    Performs parallel vectorial interpolation on a DataFrame and handles extrapolation based on specified criteria.

    :param vect_df: The input DataFrame containing the vectorial data to be interpolated.
    :type vect_df: pandas.DataFrame
    :param results: A list to append the processed DataFrames to.
    :type results: list[pandas.DataFrame]
    :param input_grid: The gridid of the input grid data.
    :type input_grid: int
    :param output_grid: The gridid of the output grid data.
    :type output_grid: int
    :param extrapolation_type: The type of extrapolation to apply ("value", "maximum", "minimum", or "abort").
    :type extrapolation_type: str
    :param extrapolation_value: The value to use for extrapolation when `extrapolation_type` is "value".
    :type extrapolation_value: float
    :param indexes: A list of indices where extrapolation needs to be applied. Can be None.
    :type indexes: Optional[list[int]]
    """
    if vect_df.empty:
        return

    uu_df = (
        vect_df.loc[vect_df.nomvar == "UU"]
        .sort_values("level", ascending=vect_df.iloc[0].ascending)
        .reset_index(drop=True)
    )
    vv_df = (
        vect_df.loc[vect_df.nomvar == "VV"]
        .sort_values("level", ascending=vect_df.iloc[0].ascending)
        .reset_index(drop=True)
    )

    if (uu_df.empty) or (vv_df.empty):
        return

    uu_int_df = copy.deepcopy(uu_df)
    vv_int_df = copy.deepcopy(vv_df)

    split_value = get_split_value(uu_df)

    uu_df_list = np.array_split(uu_df, split_value)
    vv_df_list = np.array_split(vv_df, split_value)
    uu_int_df_list = np.array_split(uu_int_df, split_value)
    vv_int_df_list = np.array_split(vv_int_df, split_value)

    for uu_df, vv_df, uu_int_df, vv_int_df in zip(uu_df_list, vv_df_list, uu_int_df_list, vv_int_df_list):
        uu_df = fstpy.compute(uu_df)
        vv_df = fstpy.compute(vv_df)

        output_grid_arr = [output_grid for _ in range(len(uu_df.index))]
        input_grid_arr = [input_grid for _ in range(len(uu_df.index))]

        # InterpolationHorizontalGrid ne fait jamais d'extrapolation
        if indexes is not None and len(indexes):
            indexes_arr = [ListWrapper(indexes) for _ in range(len(uu_df.index))]
            extrapolation_type_arr = [extrapolation_type for _ in range(len(uu_df.index))]
            extrapolation_value_arr = [extrapolation_value for _ in range(len(uu_df.index))]

        with multiprocessing.Pool() as pool:
            if indexes is not None and len(indexes):
                interp_res = pool.starmap(
                    vect_interp_with_extrapolation,
                    zip(
                        output_grid_arr,
                        input_grid_arr,
                        uu_df.d.to_list(),
                        vv_df.d.to_list(),
                        indexes_arr,
                        extrapolation_type_arr,
                        extrapolation_value_arr,
                    ),
                )
            else:
                interp_res = pool.starmap(
                    vect_interp, zip(output_grid_arr, input_grid_arr, uu_df.d.to_list(), vv_df.d.to_list())
                )

            uu_int_df["d"] = [to_dask(r[0]) for r in interp_res]
            vv_int_df["d"] = [to_dask(r[1]) for r in interp_res]

        results.append(uu_int_df)
        results.append(vv_int_df)


def vect_interp_with_extrapolation(
    out_grid: np.ndarray,
    in_grid: np.ndarray,
    uu_data: np.ndarray,
    vv_data: np.ndarray,
    indexes: List[int],
    extp_type: str,
    extp_value: float,
) -> Tuple[np.ndarray, np.ndarray]:
    (uu, vv) = RmnInterface.vectorial_interpolation(int(out_grid), int(in_grid), uu_data, vv_data)
    uu = do_extrapolation(uu, uu_data, indexes.get(), extp_type, extp_value)
    vv = do_extrapolation(vv, vv_data, indexes.get(), extp_type, extp_value)
    return uu, vv


class ListWrapper:
    """Helper class to hide the list"""

    def __init__(self, indexes):
        self.indexes = indexes

    def get(self):
        return self.indexes
