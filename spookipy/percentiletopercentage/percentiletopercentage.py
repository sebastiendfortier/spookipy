# -*- coding: utf-8 -*-

import fstpy.all as fstpy
import numpy as np
import pandas as pd
import copy
import re
import os   
from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe, initializer)


class PercentileToPercentageError(Exception):
    pass

def field_to_percentage_ge(arr: np.ndarray, arg: str) -> float:
    """returns a float that represents the likelyhood of the threshold exceedence

    :param arr: the list gathered from the 3d numpy array's vertical axis
    :type arr: list
    :param arg: the stored parsed command line arguments
    :type arg: arg.Namespace
    :return: a float that represents the percentage value of the threshold exceedence
    :rtype: float
    """
    if arr[0] >= arg.threshold:
        return 100.
    elif arr[-1] <= arg.threshold:
        return 0.

    equal_to = np.where(arr == arg.threshold)
    smaller_than = np.where(arr < arg.threshold)
    greater_than = np.where(arr > arg.threshold)

    return((100 - (equal_to[0][0] + equal_to[0][-1]) * arg.percentile_step / 2) if ((equal_to[0]).size > 0) else (100 - (((greater_than[0][0] * arg.percentile_step) - (smaller_than[0][-1] * arg.percentile_step)) / (arr[greater_than[0][0]] -
                                                                                arr[smaller_than[0][-1]]) * (arg.threshold - arr[smaller_than[0][-1]]) + (smaller_than[0][-1] * arg.percentile_step))))

def field_to_percentage_le(arr: np.ndarray, arg: str) -> float:
    """returns a float that represents the likelyhood of the threshold exceedence

    :param arr: the list gathered from the 3d numpy array's vertical axis
    :type arr: list
    :param arg: the stored parsed command line arguments
    :type arg: arg.Namespace
    :return: a float that represents the percentage value of the threshold exceedence
    :rtype: float
    """
    if arr[0] >= arg.threshold:
        return 0.
    elif arr[-1] <= arg.threshold:
        return 100.

    equal_to = np.where(arr == arg.threshold)
    smaller_than = np.where(arr < arg.threshold)
    greater_than = np.where(arr > arg.threshold)

    return((equal_to[0][0] + equal_to[0][-1]) * arg.percentile_step / 2 if ((equal_to[0]).size > 0) else (((greater_than[0][0] * arg.percentile_step) - (smaller_than[0][-1] * arg.percentile_step)) / (arr[greater_than[0][0]] -
                                                                                arr[smaller_than[0][-1]]) * (arg.threshold - arr[smaller_than[0][-1]]) + (smaller_than[0][-1] * arg.percentile_step)))


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
    :param percentile_step: Indicates the increment value for the percentile steps, defaults to 5
    :type percentile_step: int, optional
    """
    @initializer
    def __init__(self, df: pd.DataFrame, threshold: float = 0.3, operator: str = 'ge', etiket: str = 'GE0_____PALL', nomvar: str = 'SSH', typvar: str = 'P@', percentile_step: int = 5):
        super().__init__(df)
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

        if not isinstance(self.percentile_step,int):
            raise PercentileToPercentageError(f'Unexpected value, should be a list of ints containing Start;End;Step, provided {self.percentile_step}')

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

        df_list = []
        for (forecast_hour), group_df in self.groups:

            # Find the masks associated with the current group of data
            msk_group_df = self.msk_df.loc[self.msk_df['forecast_hour'] == forecast_hour]

            # Rewrite the etiket field name to the validated input name
            mask_df = create_empty_result(msk_group_df,{'etiket':self.etiket})

            # Select a row of data to update the field to the exceedence percentage
            group_df = fstpy.compute(group_df)
            group_df['percentile'] = group_df['etiket'].map(lambda f:  int(re.sub('[^0-9]+','',f)))
            group_df = group_df.sort_values('percentile')
            group_field_stacked = np.stack(group_df['d'])
            
            if self.operator == 'ge':
                percentile_field = np.apply_along_axis(field_to_percentage_ge, 0, group_field_stacked, self)
            else:
                percentile_field = np.apply_along_axis(field_to_percentage_le, 0, group_field_stacked, self)
            percentile_field = np.where(mask_df['d'].iloc[0] == 0.0, 0, percentile_field)

            data_df = create_empty_result(group_df,{'etiket':self.etiket})

            data_df['d'] = [percentile_field.astype(np.float32)]

            df_list.append(data_df)
            df_list.append(mask_df)

        return final_results(df_list, PercentileToPercentageError, self.meta_df)