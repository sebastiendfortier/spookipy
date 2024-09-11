# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd
import dask.array as da

from spookipy.configparsingutils.configparsingutils import apply_lambda_to_list

from ..plugin import Plugin, PluginParser
from ..science import hmx_from_svp
from ..utils import (create_empty_result, existing_results, parse_and_validate_condition, 
                     parse_condition, OPERATOR_LOOKUP_TABLE, LABEL_OPERATOR_LOOKUP_TABLE,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer, find_common_levels)


class ArithmeticPercentageExceedingThresholdsByPointError(Exception):
    pass


class ArithmeticPercentageExceedingThresholdsByPoint(Plugin):
    """ArithmeticPercentageExceedingThresholdsByPoint calculation. 

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param thresholds: list of thresholds to calculate
    :type thresholds: list[str]
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """

    @initializer
    def __init__(
            self, 
            df: pd.DataFrame,
            thresholds: 'list[str]',
            ignore_mask = False,
            copy_input  = False,
            reduce_df   = True,
            ):
        
        super().__init__(self.df)
        self.validate_thresholds()
        self.prepare_groups()

    def validate_thresholds(self):
        self.parsed_thresholds = []
        for t in self.thresholds:
            operator, value = parse_and_validate_condition(t, ArithmeticPercentageExceedingThresholdsByPointError)
            self.parsed_thresholds.append((operator, value))

    def prepare_groups(self):
        # group by grid, dateo-v
        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=['etiket','ip_info','flags'])

        self.groups = self.no_meta_df.groupby(
            ['grid', 'datev', 'dateo', 'nomvar'])

    def compute(self) -> pd.DataFrame:

        df_list = []
        for _, df_group in self.groups:
            # create empty container here?
            common_level_df = find_common_levels(df_group,list_nomvar=df_group.ensemble_member.unique(),column_to_match='ensemble_member')
            level_groups = common_level_df.groupby('level')# ensemble_groups = self.no_meta_df.groupby(['ensemble_member'])
            amount_of_member = len(df_group.ensemble_member.unique())
            for l,level_df in level_groups:
                data = level_df['d']
                all_ensemble_data = np.stack(data, axis=0)
                if type(all_ensemble_data) == da.core.Array:
                    all_ensemble_data = all_ensemble_data.compute()
                # all_ensemble_data_result = np.percentile(all_ensemble_data, self.percentiles, axis=0, interpolation=self.method)

                for threshold in self.parsed_thresholds:
                    all_ensemble_data_result = np.sum(threshold[0](all_ensemble_data,threshold[1]), axis=0)
                    all_ensemble_data_result = all_ensemble_data_result / amount_of_member * 100
                    threshold_res_df = create_empty_result(
                        level_df,
                        {"label": make_label(threshold), "ensemble_member":"ALL",
                         "ensemble_extra_info": True, # add ! to typvar
                         "unit": "percent"
                         },
                        )
                    threshold_res_df['d'] = [all_ensemble_data_result]
                    df_list.append(threshold_res_df)

        r = self.final_results(df_list, ArithmeticPercentageExceedingThresholdsByPointError,
                                      copy_input       = self.copy_input,
                                      reduce_df        = self.reduce_df)

        return r


    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=ArithmeticPercentageExceedingThresholdsByPoint.__name__, parents=[Plugin.base_parser],add_help=False)
        # should we add the option to chose what to group by??? like the others
        # # add option to group on member and allow a list of multiple group by
        # parser.add_argument('--groupBy',type=str,choices=['FORECAST_HOUR','FIELD_NAME'],dest='group_by', help="Option to group fields by attribute when performing calculation.")
        parser.add_argument('--thresholds', required=True, type=str,help='Supported strings: [ isnan, <_value, >_value, <=_value, >=_value, ==_value  ]\nno spaces allowed between condition and value, use underscore instead of a space \n Ex: --thresholds >10,<15.8')
        parser.add_argument('--ignore_mask', action='store_true', default=False, help="Par défaut , on vérifie s'il y a un masque à tenir compte dans les calcul. Cette option ignore les masques.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['thresholds'] = parsed_arg['thresholds'].split(",")
        # just a check to make sure it's valide
        for t in parsed_arg['thresholds']:
            parse_and_validate_condition(t)

        return parsed_arg


def make_label(threshold)->str :
    threshold_operator = threshold[0]
    threshold_number = str(threshold[1])

    threshold_operator = LABEL_OPERATOR_LOOKUP_TABLE[threshold_operator]
    
    # Check if the number is an integer (i.e., does not contain a decimal point)
    if '.' in threshold_number:
        threshold_number = threshold_number.rstrip('0')
        # Check if the string ends with a decimal point and remove it if necessary
        if threshold_number.endswith('.'):
            threshold_number = threshold_number[:-1]
    
    label = threshold_operator + threshold_number + "_____"
    
    return label[:6]
