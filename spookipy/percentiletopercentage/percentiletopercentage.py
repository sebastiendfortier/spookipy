# -*- coding: utf-8 -*-

import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd
import copy
import re
from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe, initializer)


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
    steps = arg.percentile_step

    # Check for if the threshold is between two percentiles, if it is then run a linear fit calcullation to find the value
    equal_to = np.where(arr == arg.threshold)
    smaller_than = np.where(arr < arg.threshold)
    greater_than = np.where(arr > arg.threshold)

    if(equal_to[0]).size > 0:
        risk = ((equal_to[0][0] + equal_to[0][-1]) * steps[2]) / 2
    elif ((smaller_than[0]).size > 0) & ((greater_than[0]).size > 0):
        risk = ((greater_than[0][0] * steps[2]) - (smaller_than[0][-1] * steps[2])) / (arr[greater_than[0][0]] -
                                                                                       arr[smaller_than[0][-1]]) * (arg.threshold - arr[smaller_than[0][-1]]) + (smaller_than[0][-1] * steps[2])

    # Check for the edge cases where the threshold does not lie in the middle
    if arg.operator == 'ge':
        if arr[0] > arg.threshold:
            risk = 100
        elif arr[-1] < arg.threshold:
            risk = 0.0
        elif ((smaller_than[0]).size > 0) & ((greater_than[0]).size > 0):
            risk = 100 - risk
        else:
            risk = 0.0

    # The Less Than or Equal to case
    else:
        if arr[0] > arg.threshold:
            risk = 0.0
        elif arr[-1] < arg.threshold:
            risk = 100
        else:
            risk = 0.0
    return risk


# def field_to_percentage2(arr: np.ndarray, arg: str) -> float:
#     """returns a float that represents the likelyhood of the threshold exceedence

#     :param arr: the list gathered from the 3d numpy array's vertical axis
#     :type arr: list
#     :param arg: the stored parsed command line arguments
#     :type arg: arg.Namespace
#     :return: a float that represents the percentage value of the threshold exceedence
#     :rtype: float
#     """
#     steps = np.array(arg.percentile_step.split(',')).astype(int)

#     # Check for if the threshold is between two percentiles, if it is then run a linear fit calcullation to find the value
#     prec = np.roll(arr,-1)
#     risk = np.where(
#         arr == arg.threshold, ((arr+prec)*steps[-1])/2, 
#         np.where((arr < arg.threshold) & (arr > arg.threshold), ,arr)
#         )
#     smaller_than = np.where(arr < arg.threshold)
#     greater_than = np.where(arr > arg.threshold)

#     if len(equal_to[0]) > 0:
#         risk = ((equal_to[0][0] + equal_to[0][-1]) * steps[2]) / 2
#     elif (len(smaller_than[0]) > 0) & (len(greater_than[0]) > 0):
#         risk = ((greater_than[0][0] * steps[2]) - (smaller_than[0][-1] * steps[2])) / 
#                (arr[greater_than[0][0]] - arr[smaller_than[0][-1]]) * (arg.threshold - arr[smaller_than[0][-1]]) + (smaller_than[0][-1] * steps[2])

#     # Check for the edge cases where the threshold does not lie in the middle
#     if arg.operator == 'ge':
#         if arr[0] > arg.threshold:
#             risk = 100
#         elif arr[-1] < arg.threshold:
#             risk = 0.0
#         elif (len(smaller_than[0]) > 0) & (len(greater_than[0]) > 0):
#             risk = 100 - risk
#         else:
#             risk = 0.0

#     # The Less Than or Equal to case
#     else:
#         if arr[0] > arg.threshold:
#             risk = 0.0
#         elif arr[-1] < arg.threshold:
#             risk = 100
#         else:
#             risk = 0.0
#     return risk

# def sort_etiket(col: pd.Series) -> pd.Series:
#     """returns a new mapped series that contains only the integer values to be sorted

#     :param col: the etiket column of the data fram
#     :type col: panda.Series
#     :return: a panda series that only contains the number part of the etiket
#     :rtype: panda.Series
#     """

#     col = col.map(lambda field: list(field))
#     for i in range(len(col.index)):
#         num = ''
#         for x in range(len(col.iloc[i])):
#             if col.iloc[i][x].isnumeric():
#                 num += str(col.iloc[i][x])
#         col.iloc[i] = num
#     return col.map(lambda field: int(field))


class PercentileToPercentage(Plugin):
    """Writes a new field with with the percentile exceedence percentage from the input percentiles

    :param df: input data frame
    :type df: pd.Dataframe
    :param threshold: the threshold values, defaults to 0.3
    :type threshold: float, optional
    :param operator: the operator, defaults to ge
    :type operator: str, optional
    :param etiket: the output etiket name, defaults to GE0_____PALL
    :type etiket: str, optional
    :param nomvar: the nomvar for input data frame, defaults to SSH
    :type nomvar: str, optional
    :param typvar: the typvar for input data frame, defaults to P@
    :type typvar: str, optional
    :param percentile_step: Indicates the Start;End;Step for the percentile steps, defaults to 0,100,5
    :type percentile_step: str, optional
    """
    @initializer
    def __init__(self, df: pd.DataFrame, threshold: float = 0.3, operator: str = 'ge', etiket: str = 'GE0_____PALL', nomvar: str = 'SSH', typvar: str = 'P@', percentile_step: list = [0,100,5]):
        super().__init__(df)
        # self.df = df
        # self.threshold = threshold
        # self.operator = operator
        # self.etiket = etiket
        # self.tv = typvar
        # self.nv = nomvar
        # self.percentile_step = percentile_step
        self.validate_parameters()
        self.prepare_groups()

    # Validate input data
    def validate_parameters(self):

        # Ensure that the selected nomvar is present
        if self.nomvar not in self.no_meta_df.nomvar.unique():
            raise PercentileToPercentageError('Input nomvar is not found')

        # Ensure that the selected typvar is present
        if self.typvar not in self.no_meta_df.typvar.unique():
            raise PercentileToPercentageError('Input typvar is not found')

        # Ensure that the selected etiket is present
        if self.no_meta_df.etiket.str.startswith('C').empty:
            raise PercentileToPercentageError('Etiket does not indicate percentiles')

        if not isinstance(self.percentile_step,list):
            raise PercentileToPercentageError(f'Unexpected value, should be a list of ints containing Start;End;Step, provided {self.percentile_step}')

        if len(self.percentile_step) != 3:
            raise PercentileToPercentageError(f'Wrong number of values, should be a list of ints containing Start;End;Step, provided {self.percentile_step}')
        # self.df = fstpy.metadata_cleanup(self.df)

        # self.meta_df = self.df.loc[self.df.nomvar.isin(
        #     ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=['forecast_hour'])


        ###

        # I think this will break if etiket is not 12 chars long, maybe make sure

        ###
        if len(self.etiket) != 12:
            raise PercentileToPercentageError('Etiket parameter must have 12 characters')
        # Checking for validity of etiket field
        if len(self.etiket[-12:-10]) != 2 and len(self.etiket[-12:-10]) != 0:
            raise PercentileToPercentageError('The start of the etiket name can only have either 2 or 0 characters.')

        if len(self.etiket[-10:-4]) == 0:
            raise PercentileToPercentageError('Etiket name does not have 6 character before the last four chracters.')

        if (self.etiket[-4] != 'N') and (self.etiket[-4] != 'P') and (self.etiket[-4] != 'X'):
            raise PercentileToPercentageError('The letter before "ALL" is not N, P or X')

        if self.etiket[-3:] != 'ALL':
            raise PercentileToPercentageError('Etiket name does not end in "ALL".')

        # remove meta data from DataFrame
        # self.df = self.df.loc[~self.df.nomvar.isin(
        #     ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

    def prepare_groups(self):
        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=['forecast_hour'])

        field_df = self.no_meta_df.loc[(self.no_meta_df.typvar == self.typvar) & (self.no_meta_df.nomvar == self.nomvar) & (self.no_meta_df.etiket.str.startswith('C'))]

        if field_df.empty:
            raise PercentileToPercentageError('No data matching typvar, nomvar and percentile criterias found')

        all_mask_df = self.no_meta_df.loc[self.no_meta_df.typvar.isin(['@@', '!@'])]
        
        self.msk_df = all_mask_df.loc[(all_mask_df.nomvar == self.nomvar)& (all_mask_df.etiket.str.startswith('C'))]

        self.groups = field_df.groupby(['forecast_hour'], as_index=False)

    def compute(self) -> pd.DataFrame:
        """Writes the new field and metadata with the updated threshold exceedence percentage returned from field to percentage function to the
        parsed destination file from the command line. 

        :param arg: the stored parsed command line arguments
        :type arg: arg.Namespace
        """
        # df = self.df
        # field_df = fstpy.compute(df.loc[(df.typvar == self.tv) & (
        #     df.nomvar == self.nv) & (df.etiket.str.startswith('C'))])

        # # Since nv and tv is verified, if df is still empty then etiket does not start with C
        # if field_df.empty:
        #     raise("Etiket does not indicate percentile")

        # all_mask_df = df.loc[df.typvar.isin(['@@', '!@'])]
        # msk_df = fstpy.compute(all_mask_df.loc[(all_mask_df.nomvar == self.nv)
        #                        & (all_mask_df.etiket.str.startswith('C'))])
        # groups = field_df.groupby(['forecast_hour'], as_index=False)

        df_list = []
        for (forecast_hour), group_df in self.groups:

            # Find the masks associated with the current group of data
            msk_group_df = self.msk_df.loc[self.msk_df['forecast_hour'] == forecast_hour]


            # Rewrite the etiket field name to the validated input name
            mask_df = create_empty_result(msk_group_df,{'etiket':self.etiket})
            # mask = copy.deepcopy(msk_group_df.iloc[0].to_dict())
            # mask['etiket'] = self.etiket
            # mask = pd.DataFrame([mask])

            # Select a row of data to update the field to the exceedence percentage
            group_df['percentile'] = group_df['etiket'].map(lambda f:  int(re.sub('[^0-9]+','',f)))
            group_df = group_df.sort_values('percentile')
            group_field_stacked = np.stack(group_df['d'])
            percentile_field = np.apply_along_axis(field_to_percentage, 0, group_field_stacked, self)
            percentile_field = np.where(mask_df['d'].iloc[0] == 0.0, 0, percentile_field)

            data_df = create_empty_result(group_df,{'etiket':self.etiket})
            # print(data_df1[fstpy.BASE_COLUMNS].drop(columns='d').to_string())
            # data_df = copy.deepcopy(group_df.iloc[0].to_dict())
            # data_df['etiket'] = self.etiket
            data_df['d'] = [percentile_field.astype(np.float32)]
            # print(percentile_field.shape)
            # data_df['nbits'] = 32
            # data_df['datyp'] = 5
            # data_df = pd.DataFrame([data_df])
            # print(data_df[fstpy.BASE_COLUMNS].drop(columns='d').to_string())
            # assert(False)
            # data_df['d'] = data_df['d'].map(lambda f: f.astype(np.float32))
            df_list.append(data_df)
            df_list.append(mask_df)

        return final_results(df_list, PercentileToPercentageError, self.meta_df)
