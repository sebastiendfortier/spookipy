# -*- coding: utf-8 -*-

import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd
import copy

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe)


class PercentileToPercentageError(Exception):
    pass


def field_to_percentage(arr: np.ndarray, arg: str) -> float:
    """returns a float that represents the likelyhood of the threshold exceedence

    :param arr: the list gathered from the 3d numpy array's vertical axis
    :type arr: list
    :param arg: the stored parsed command line arguments
    :type arg: arg.Namespace
    :return: a float that represents the percentage value of the threshold exceedence
    :rtype: float
    """
    steps = np.array(arg.ps.split(',')).astype(int)

    # Check for if the threshold is between two percentiles, if it is then run a linear fit calcullation to find the value
    equal_to = np.where(arr == arg.th)
    smaller_than = np.where(arr < arg.th)
    greater_than = np.where(arr > arg.th)

    if len(equal_to[0]) > 0:
        risk = ((equal_to[0][0] + equal_to[0][-1]) * steps[2]) / 2
    elif (len(smaller_than[0]) > 0) & (len(greater_than[0]) > 0):
        risk = ((greater_than[0][0] * steps[2]) - (smaller_than[0][-1] * steps[2])) / (arr[greater_than[0][0]] -
                                                                                       arr[smaller_than[0][-1]]) * (arg.th - arr[smaller_than[0][-1]]) + (smaller_than[0][-1] * steps[2])

    # Check for the edge cases where the threshold does not lie in the middle
    if arg.op == 'ge':
        if arr[0] > arg.th:
            risk = 100
        elif arr[-1] < arg.th:
            risk = 0.0
        elif (len(smaller_than[0]) > 0) & (len(greater_than[0]) > 0):
            risk = 100 - risk
        else:
            risk = 0.0

    # The Less Than or Equal to case
    else:
        if arr[0] > arg.th:
            risk = 0.0
        elif arr[-1] < arg.th:
            risk = 100
        else:
            risk = 0.0
    return risk


def sort_etiket(col: pd.Series) -> pd.Series:
    """returns a new mapped series that contains only the integer values to be sorted

    :param col: the etiket column of the data fram
    :type col: panda.Series
    :return: a panda series that only contains the number part of the etiket
    :rtype: panda.Series
    """

    col = col.map(lambda field: list(field))
    for i in range(len(col.index)):
        num = ""
        for x in range(len(col.iloc[i])):
            if col.iloc[i][x].isnumeric():
                num += str(col.iloc[i][x])
        col.iloc[i] = num
    return col.map(lambda field: int(field))


class PercentileToPercentage(Plugin):
    """Writes a new field with with the percentile exceedence percentage from the input percentiles

    :param df: input data frame
    :type df: pd.Dataframe
    :param th: the threshold values, defaults to 0.3
    :type th: float, optional
    :param op: the operator, defaults to ge
    :type op: str, optional
    :param ed: the output etiket name, defaults to GE0_____PALL
    :type ed: str, optional
    :param nv: the nomvar for input data frame, defaults to SSH
    :type nv: str, optional
    :param tv: the typvar for input data frame, defaults to P@
    :type tv: str, optional
    :param ps: Indicates the Start;End;Step for the percentile steps, defaults to 0,100,5
    :type ps: str, optional
    """

    def __init__(self, df: pd.DataFrame, threshold: float = 0.3, operator: str = 'ge', etiket: str = 'GE0_____PALL', nomvar: str = 'SSH', typvar: str = 'P@', percentile_step: str = '0,100,5'):
        self.df = df
        self.th = threshold
        self.op = operator
        self.ed = etiket
        self.tv = typvar
        self.nv = nomvar
        self.ps = percentile_step
        self.validate_input()

    # Validate input data
    def validate_input(self):
        if self.df.empty:
            raise PercentileToPercentageError('No data to process')

        # Ensure that the selected nomvar is present
        self.nomvar_df = self.df.loc[self.df.nomvar == self.nv]
        if self.nomvar_df.empty:
            raise PercentileToPercentageError('Input nomvar is not found')

        # Ensure that the selected typvar is present
        self.typvar_df = self.df.loc[self.df.typvar == self.tv]
        if self.typvar_df.empty:
            raise PercentileToPercentageError('Input typvar is not found')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(
            self.df, columns=[
                'forecast_hour'])

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

    def compute(self) -> pd.DataFrame:
        """Writes the new field and metadata with the updated threshold exceedence percentage returned from field to percentage function to the
        parsed destination file from the command line. 

        :param arg: the stored parsed command line arguments
        :type arg: arg.Namespace
        """
        df = self.df
        df_field = fstpy.compute(df.loc[(df.typvar == self.tv) & (
            df.nomvar == self.nv) & (df.etiket.str.startswith('C'))])

        # Since nv and tv is verified, if df is still empty then etiket does not start with C
        if df_field.empty:
            raise("Etiket does not indicate percentile")

        df_all_mask = df.loc[df.typvar.isin(['@@', '!@'])]
        df_msk = fstpy.compute(df_all_mask.loc[(df_all_mask.nomvar == self.nv)
                               & (df_all_mask.etiket.str.startswith('C'))])
        df_field_grouped = df_field.groupby(['forecast_hour'], as_index=False)

        df_output = []
        for (forecast_hour), df_group in df_field_grouped:

            # Find the masks associated with the current group of data
            df_msk_group = df_msk.loc[df_msk['forecast_hour'] == forecast_hour]

            # Checking for validity of etiket field
            if len(self.ed[-12:-10]) != 2 and len(self.ed[-12:-10]) != 0:
                raise Exception("The start of the etiket name can only have either 2 or 0 characters.")
            if len(self.ed[-10:-4]) == 0:
                raise Exception("Etiket name does not have 6 character before the last four chracters.")
            if (self.ed[-4] != "N") and (self.ed[-4] != "P") and (self.ed[-4] != "X"):
                print("The letter before 'ALL' is not N, P or X")
            if self.ed[-3:] != "ALL":
                raise Exception("Etiket name does not end in 'ALL'.")

            # Rewrite the etiket field name to the validated input name
            mask = copy.deepcopy(df_msk_group.iloc[0].to_dict())
            mask['etiket'] = self.ed
            mask = pd.DataFrame([mask])

            # Select a row of data to update the field to the exceedence percentage
            df_group = df_group.sort_values('etiket', key=sort_etiket)
            group_field_stacked = np.stack(df_group['d'])
            percentile_field = np.apply_along_axis(field_to_percentage, 0, group_field_stacked, self)
            percentile_field = np.where(mask['d'].iloc[0] == 0.0, 0, percentile_field)

            data = copy.deepcopy(df_group.iloc[0].to_dict())
            data['etiket'] = self.ed
            data['d'] = percentile_field
            data['nbits'] = 32
            data["datyp"] = 5
            data = pd.DataFrame([data])
            data["d"] = data["d"].map(lambda f: f.astype(np.float32))
            df_output.append(data)
            df_output.append(mask)

        return final_results(df_output, PercentileToPercentageError, self.meta_df)
