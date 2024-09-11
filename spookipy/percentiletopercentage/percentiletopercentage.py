# -*- coding: utf-8 -*-

import fstpy
import numpy as np
import pandas as pd
import re 
from ..plugin import Plugin, PluginParser
from ..utils import create_empty_result, initializer


class PercentileToPercentageError(Exception):
    pass

def calculate_percentage(arr: np.ndarray, threshold: float, percentile_step: list) -> float:
    """Calculate the percentage value of the threshold exceedence.

    :param arr: The list gathered from the 3D numpy array's vertical axis.
    :type arr: np.ndarray
    :param threshold: The threshold value that the field compares to.
    :type threshold: float
    :param percentile_step: A list representing percentile steps.
    :type percentile_step: list
    :return: A float that represents the percentage value of the threshold exceedence.
    :rtype: float
    """

    equal_to     = np.where(arr == threshold)
    smaller_than = np.where(arr < threshold)
    greater_than = np.where(arr > threshold)

    # Calculate the average of the first and last elements of equal_to if it's not empty
    if equal_to[0].size > 0:
        avg_percentile_step = (percentile_step[equal_to[0][0]] + percentile_step[equal_to[0][-1]]) / 2
        result =  avg_percentile_step
    else:
        # Calculate the interpolated percentile step otherwise
        diff_percentile_step = percentile_step[greater_than[0][0]] - percentile_step[smaller_than[0][-1]]
        diff_arr = arr[greater_than[0][0]] - arr[smaller_than[0][-1]]
        interpolated_percentile_step = diff_percentile_step / diff_arr * (threshold - arr[smaller_than[0][-1]]) + percentile_step[smaller_than[0][-1]]
        result = interpolated_percentile_step

    return result

def field_to_percentage_ge(arr: np.ndarray, threshold: float, percentile_step: list) -> float:
    """returns a float that represents the likelyhood of the threshold exceedence

    :param arr: the list gathered from the 3d numpy array's vertical axis
    :type arr: list
    :param threshold: the threshold value that the field compares to
    :type threshold: float
    :param percentile_step: 
    :type percentile_step: list
    :return: a float that represents the percentage value of the threshold exceedence
    :rtype: float
    """
    if arr[0] >= threshold:
        return 100.
    elif arr[-1] <= threshold:
        return 0.
    
    result = calculate_percentage(arr, threshold, percentile_step)

    return 100 - result 

def field_to_percentage_le(arr: np.ndarray, threshold: float, percentile_step: list) -> float:
    """returns a float that represents the likelyhood of the threshold exceedence

    :param arr: the list gathered from the 3d numpy array's vertical axis
    :type arr: list
    :param threshold: the threshold value that the field compares to
    :type threshold: float
    :param percentile_step: 
    :type percentile_step: list
    :return: a float that represents the percentage value of the threshold exceedence
    :rtype: float
    """
    if arr[0] >= threshold:
        return 0.
    elif arr[-1] <= threshold:
        return 100.

    result = calculate_percentage(arr, threshold, percentile_step)

    return result


class PercentileToPercentage(Plugin):
    """Writes a new field with with the percentile exceedence percentage from the input percentiles

    :param df: Input dataframe
    :type df: pd.Dataframe
    :param threshold: Threshold value, defaults to 0.3
    :type threshold: float, optional
    :param operator: Operator, defaults to ge
    :type operator: str, optional
    :param label: Output label name, defaults to STG1__
    :type label: str, optional
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """
    @initializer
    def __init__(self, 
                 df:        pd.DataFrame,  
                 threshold: float = 0.3, 
                 operator:  str = 'ge', 
                 label:     str = 'STG1__', 
                 reduce_df = True):
        
        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.validate_parameters()
        self.prepare_groups()

    # Validate input data
    def validate_parameters(self):
        
        if len(self.label) > 6:
            raise PercentileToPercentageError(f'Label parameter must have 6 characters maximum! label = "{self.label}"')

    def prepare_groups(self):
        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=['forecast_hour', 'etiket'])

        # Selection des champs de donnees, on exclut les masques
        # S'assurer que les labels contiennent au moins un digit car sinon le map causera une erreur
        field_df = self.no_meta_df.loc[ 
                                        (~self.no_meta_df.typvar.isin(['@@', '!@'])) &
                                        (self.no_meta_df.label.str.contains(r'\d'))
                                        ]

        if field_df.empty:
            raise PercentileToPercentageError(f'PercentileToPercentage - no data to process')

        self.msk_df = self.no_meta_df.loc[
                                        (self.no_meta_df.typvar.isin(['@@', '!@'])) &  
                                        (self.no_meta_df.label.str.contains(r'\d'))
                                        ]

        self.groups     = field_df.groupby('forecast_hour', as_index=False)

    def compute(self) -> pd.DataFrame:
        df_list = []

        for forecast_hour, group_df in self.groups:
            group_df               = fstpy.compute(group_df)
            group_df['percentile'] = group_df['label'].map(lambda f:  int(re.sub('[^0-9]+','',f)))
            group_df               = group_df.sort_values('percentile')
            group_field_stacked    = np.stack(group_df['d'])
            percentiles            = group_df['percentile'].tolist()

            if self.operator == 'ge':
                percentile_field = np.apply_along_axis(field_to_percentage_ge, 0, 
                                                       group_field_stacked, self.threshold, percentiles)
            else:
                percentile_field = np.apply_along_axis(field_to_percentage_le, 0, 
                                                       group_field_stacked, self.threshold, percentiles)
                
            # Find the masks associated with the current group of data
            msk_group_df = self.msk_df.loc[self.msk_df['forecast_hour'] == forecast_hour]

            # Creation du champs mask et du champs de donnees
            mask_df = create_empty_result(msk_group_df,{'label':self.label})
            data_df = create_empty_result(group_df,    {'label':self.label})
        
            percentile_field     = np.where(mask_df['d'].iloc[0] == 0.0, 0, percentile_field)
            data_df['d']         = [percentile_field.astype(np.float32)]

            df_list.append(data_df)
            df_list.append(mask_df)


        return self.final_results(df_list, 
                                  PercentileToPercentageError, 
                                  copy_input = False,
                                  reduce_df  = self.reduce_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """

        parser = PluginParser(prog=PercentileToPercentage.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--label',    type=str, default="STG1__", help="Label of the output field.")
        parser.add_argument('--threshold',type=float, default=0.3, help="Threshold value.")
        parser.add_argument('--operator', type=str, default="ge",help="Comparison operator.")

        parsed_arg = vars(parser.parse_args(args.split()))

        return parsed_arg
