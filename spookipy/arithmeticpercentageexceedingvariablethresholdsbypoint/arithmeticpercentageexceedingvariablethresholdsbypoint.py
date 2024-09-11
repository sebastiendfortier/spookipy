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
                     initializer, find_common_levels, validate_nomvar)


class ArithmeticPercentageExceedingVariableThresholdsByPointError(Exception):
    pass


class ArithmeticPercentageExceedingVariableThresholdsByPoint(Plugin):
    """ArithmeticPercentageExceedingVariableThresholdsByPoint calculation. 

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
            threshold_operator: str,
            threshold_nomvar: str,
            threshold_label: str,
            ignore_mask = False,
            copy_input  = False,
            reduce_df   = True,
            ):
        
        super().__init__(self.df)
        self.validate_thresholds()
        self.prepare_groups()

    def validate_thresholds(self):
        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=['etiket','ip_info','flags'])
        
        self.parsed_threshold_operator = OPERATOR_LOOKUP_TABLE[parse_condition(self.threshold_operator,ArithmeticPercentageExceedingVariableThresholdsByPointError,only_operator=True)]
        
        threshold_mask = (self.no_meta_df.nomvar == self.threshold_nomvar) & (self.no_meta_df.label == self.threshold_label)
        self.threshold_df = self.no_meta_df[threshold_mask]
        if self.threshold_df.empty:
            raise ArithmeticPercentageExceedingVariableThresholdsByPointError(
                f"Could not find the threshold variable with name {self.threshold_nomvar} and label {self.threshold_label}")


    def prepare_groups(self):
        # group by grid, dateo-v

        self.groups = self.no_meta_df.groupby(
            ['grid', 'datev', 'dateo', 'nomvar'])

    def compute(self) -> pd.DataFrame:

        df_list = []
        for _, df_group in self.groups:
            # create empty container here?
            common_level_df = find_common_levels(df_group,list_nomvar=df_group.ensemble_member.unique(),column_to_match='ensemble_member')
            level_groups = common_level_df.groupby('level')# ensemble_groups = self.no_meta_df.groupby(['ensemble_member'])
            amount_of_member = len(df_group.ensemble_member.unique())-1
            for l,level_df in level_groups:
                threshold_mask = (level_df.nomvar == self.threshold_nomvar) & (level_df.label == self.threshold_label)
                threshold_df = level_df[threshold_mask].reset_index()
                other_df = level_df[~threshold_mask]

                if threshold_df.empty:
                    # warning
                    continue
                comps = []
                for x in other_df.d:
                    # comp here
                    # add it to array
                    comps.append(self.parsed_threshold_operator(x,threshold_df.loc[0,'d']))
                    # x
                counts_above_threshold = np.sum(comps, axis=0)
                percent_threshold = counts_above_threshold / amount_of_member * 100
                # sum the comp
                # put it in the empty

                threshold_res_df = create_empty_result(
                        level_df,
                        {"label": make_label(self.parsed_threshold_operator, self.threshold_label), "ensemble_member":"ALL",
                         "ensemble_extra_info": True, # add ! to typvar
                         "unit": "percent"
                         },
                        )
                threshold_res_df['d'] = [percent_threshold]
                df_list.append(threshold_res_df)


        r = self.final_results(df_list, ArithmeticPercentageExceedingVariableThresholdsByPointError,
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
        parser = PluginParser(prog=ArithmeticPercentageExceedingVariableThresholdsByPoint.__name__, parents=[Plugin.base_parser],add_help=False)
        # should we add the option to chose what to group by??? like the others
        # # add option to group on member and allow a list of multiple group by
        # parser.add_argument('--groupBy',type=str,choices=['FORECAST_HOUR','FIELD_NAME'],dest='group_by', help="Option to group fields by attribute when performing calculation.")
        parser.add_argument('--thresholdFileVarName', required=True, dest='threshold_nomvar', type=str,help='Nom de la varible à utiliser pour le threshold')
        parser.add_argument('--thresholdFileVarLabel', required=True, dest='threshold_label', type=str,help='Label de la varible à utiliser pour le threshold')
        parser.add_argument('--thresholdFileOperator', required=True, dest='threshold_operator', type=str, choices=['<=','>=','>','<','==','!='], help='Opérateur de comparaison, choix supportés [<=,>=,>,<,==,!=]. Ex: --thresholdFileOperator <=')
        parser.add_argument('--ignore_mask', action='store_true', default=False, help="Par défaut , on vérifie s'il y a un masque à tenir compte dans les calcul. Cette option ignore les masques.")

        parsed_arg = vars(parser.parse_args(args.split()))

        # just a check to make sure it's valide
        validate_nomvar(parsed_arg['threshold_nomvar'],ArithmeticPercentageExceedingVariableThresholdsByPoint.__name__,ArithmeticPercentageExceedingVariableThresholdsByPointError)

        return parsed_arg



def make_label(threshold_operator, threshold_nomvar)->str :
    threshold_operator = LABEL_OPERATOR_LOOKUP_TABLE[threshold_operator]
    
    label = threshold_operator + threshold_nomvar + "_____"
    
    return label[:6]
