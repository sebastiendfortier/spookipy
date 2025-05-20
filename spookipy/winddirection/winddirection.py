# -*- coding: utf-8 -*-
import logging
import math

import fstpy
import numpy as np
import pandas as pd
from ..rmn_interface import RmnInterface

from ..plugin import Plugin
from ..utils import (
    create_empty_result,
    existing_results,
    get_dependencies,
    get_existing_result,
    get_from_dataframe,
    initializer,
    DependencyError,
)


class WindDirectionError(Exception):
    pass


def wind_direction(uu: np.ndarray, vv: np.ndarray) -> np.ndarray:
    result = np.where((uu == 0.0), np.where(vv >= 0.0, 180.0, 0.0), 270.0 - (180.0 / math.pi) * np.arctan2(vv, uu))
    result = np.fmod(np.fmod(result, 360.0) + 360.0, 360.0)
    return np.where(result == 0.0, 360.0, result)


class WindDirection(Plugin):
    """Calculation of the meteorological wind direction

    :param df: input DataFrame
    :type df: pd.DataFrame
    """

    @initializer
    def __init__(self, df: pd.DataFrame, dependency_check=False, copy_input=False, reduce_df=True):
        self.plugin_mandatory_dependencies = [
            {
                "UU": {"nomvar": "UU", "unit": "knot"},
                "VV": {"nomvar": "VV", "unit": "knot"},
            }
        ]

        self.plugin_result_specifications = {"WD": {"nomvar": "WD", "label": "WNDDIR", "unit": "degree"}}

        self.df = fstpy.metadata_cleanup(df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=["unit", "forecast_hour", "ip_info"])

        # check if result already exists
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(["grid", "datev", "dateo", "vctype"])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results("WindDirection", self.existing_result_df, self.meta_df)

        logging.info("WindDirection - compute")
        df_list = []
        try:
            dependencies_list = get_dependencies(
                self.groups, self.meta_df, "WindDirection", self.plugin_mandatory_dependencies, intersect_levels=True
            )
        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f"{WindDirectionError} - No matching dependencies found")
        else:
            for dependencies_df, _ in dependencies_list:
                grid = dependencies_df.grid.unique()[0]

                pos_df = self.meta_df.loc[
                    ((self.meta_df.nomvar == ">>") | (self.meta_df.nomvar == "^>")) & (self.meta_df.grid == grid)
                ]

                meta_grtyp = ""

                if not pos_df.empty:
                    meta_grtyp = pos_df.grtyp.unique()[0]

                grtyp = dependencies_df.grtyp.unique()[0]

                if grtyp not in ["A", "B", "E", "G", "L", "N", "S", "U", "Y", "Z"]:
                    raise WindDirectionError("Cannot calculate meteorological direction for grid type {grtyp}\n")

                uu_df = get_from_dataframe(dependencies_df, "UU")
                vv_df = get_from_dataframe(dependencies_df, "VV")

                wd_df = create_empty_result(vv_df, self.plugin_result_specifications["WD"], all_rows=True)

                # Creation du df bidon pour UV,necessaire pour l'appel a certaines fonctions.
                uv_df = create_empty_result(vv_df, {"nomvar": "UV", "unit": "knot"}, all_rows=True)

                if grtyp == "Y":
                    if meta_grtyp != "L":
                        raise WindDirectionError(
                            "Only positional records of type: L are supported with grid type: Y.\n"
                        )

                    for i in uu_df.index:
                        uu = uu_df.at[i, "d"].compute()
                        vv = vv_df.at[i, "d"].compute()
                        wd_df.at[i, "d"] = wind_direction(uu, vv)

                elif grtyp == "U":
                    infos_grid = fstpy.define_input_grid(grtyp, dependencies_df, self.meta_df)
                    if len(infos_grid) != 3:
                        raise WindDirectionError(f"Problem with definition of grid of type U")

                    gdid, subgridId1, subgridId2 = infos_grid
                    latGrid1 = RmnInterface.get_lat_lon_from_grid(subgridId1)["lat"]
                    lonGrid1 = RmnInterface.get_lat_lon_from_grid(subgridId1)["lon"]

                    latGrid2 = RmnInterface.get_lat_lon_from_grid(subgridId2)["lat"]
                    lonGrid2 = RmnInterface.get_lat_lon_from_grid(subgridId2)["lon"]

                    wd_df = calc_wd_gridU(
                        subgridId1, subgridId2, uu_df, vv_df, wd_df, uv_df, latGrid1, lonGrid1, latGrid2, lonGrid2
                    )

                    RmnInterface.release_grid(subgridId1)
                    RmnInterface.release_grid(subgridId2)

                else:
                    infos_grid = fstpy.define_input_grid(grtyp, dependencies_df, self.meta_df)
                    gdid, *other = infos_grid
                    lat = RmnInterface.get_lat_lon_from_grid(gdid)["lat"]
                    lon = RmnInterface.get_lat_lon_from_grid(gdid)["lon"]

                    wd_df = calc_wd(gdid, uu_df, vv_df, wd_df, uv_df, lat, lon)

                    RmnInterface.release_grid(gdid)

                df_list.append(wd_df)
        finally:
            return self.final_results(
                df_list,
                WindDirectionError,
                dependency_check=self.dependency_check,
                copy_input=self.copy_input,
                reduce_df=self.reduce_df,
            )


def calc_wd(gdid, uu_df, vv_df, wd_df, uv_df, lat, lon):
    for i in uu_df.index:
        uu = uu_df.at[i, "d"].compute()
        vv = vv_df.at[i, "d"].compute()
        wd = wd_df.at[i, "d"].compute()
        uv = uv_df.at[i, "d"].compute()

        RmnInterface.convert_grid_winds_at_grid_point(gdid, uv, wd, uu, vv, lat, lon, lat.size)
        wd_df.at[i, "d"] = wd

    return wd_df


def calc_wd_gridU(gdid1, gdid2, uu_df, vv_df, wd_df, uv_df, lat1, lon1, lat2, lon2):
    for i in uu_df.index:
        uu = uu_df.at[i, "d"].compute()
        vv = vv_df.at[i, "d"].compute()
        wd = wd_df.at[i, "d"].compute()
        uv = uv_df.at[i, "d"].compute()

        RmnInterface.convert_grid_winds_at_grid_point(
            gdid1,
            uv[:, 0 : int(uv.shape[1] / 2)],
            wd[:, 0 : int(wd.shape[1] / 2)],
            uu[:, 0 : int(uu.shape[1] / 2)],
            vv[:, 0 : int(vv.shape[1] / 2)],
            lat1,
            lon1,
            lat1.size,
        )

        res1 = wd[:, 0 : int(wd.shape[1] / 2)]

        RmnInterface.convert_grid_winds_at_grid_point(
            gdid2,
            uv[:, int(uv.shape[1] / 2) :],
            wd[:, int(wd.shape[1] / 2) :],
            uu[:, int(uu.shape[1] / 2) :],
            vv[:, int(vv.shape[1] / 2) :],
            lat2,
            lon2,
            lat2.size,
        )

        res2 = wd[:, int(wd.shape[1] / 2) :]
        wd_df.at[i, "d"] = np.hstack([res1, res2])

    return wd_df
