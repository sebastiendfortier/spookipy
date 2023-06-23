# -*- coding: utf-8 -*-

import operator
import re

import numpy as np

import fstpy
import pandas as pd

from ..plugin import Plugin, PluginParser
from ..utils import (initializer, print_voir, validate_nomvar)

class ReplaceDataIfConditionError(Exception):
    pass

class ReplaceDataIfCondition(Plugin):
    """Pour chaque valeur du champ donné, si elle repond à la condition, on change la valeur par celle fournie

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param condition: Condition
    :type condition: str
    :param value: Substitution value.
    :type value: float
    :param nomvar_out: Output file name (only work with 1 input field)
    :type nomvar_out: str
    :param clear_missing_data: When replacing values, clear the missing data flag.
    :type clear_missing_data: bool
    """

    @initializer
    def __init__(
        self,
        df:pd.DataFrame,
        condition:str,
        value:float,
        nomvar_out:str = None,
        clear_missing_data:bool = False, #TODO
        ):
        self.get_dataframes()
        self.validate_input()
        
    
    def validate_input(self):
        """Checks that the plugin's input are valid

        :raises EmptyDataframeError: The plugin's dataframe is empty, no data to process.
        """
        super().validate_input() # check empty

        if self.nomvar_out is not None:
            validate_nomvar(self.nomvar_out,"ReplaceDataIfCondition",ReplaceDataIfConditionError)
            if len(self.no_meta_df.nomvar.unique()) > 1:
                raise ReplaceDataIfConditionError("ReplaceDataIfConditionError -- MORE THAN ONE INPUT FIELD NAME - CANNOT USE OPTION nomvar_out (outputFieldName)")

        self.condition_operator, self.condition_value = parse_condition(self.condition)
        if self.condition_operator is not None:
            self.condition_operator = operator_lookup_table[self.condition_operator]
            self.condition_value = float(self.condition_value)


    def compute(self) -> pd.DataFrame:
        """Abstract method that should implement the plugin's algorithm.

        :return: dataframe with the results
        :rtype: pd.DataFrame
        """

        self.no_meta_df['d'] = self.no_meta_df.apply(lambda row: replace_data_if_condition(row['d'],self.value,self.condition_operator,self.condition_value), axis=1)

        if self.nomvar_out is not None:
            self.no_meta_df['nomvar'] = self.nomvar_out

        return self.final_results([self.no_meta_df],ReplaceDataIfConditionError)
    
    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=ReplaceDataIfCondition.__name__, parents=[Plugin.base_parser],add_help=False)

        parser.add_argument('--condition','-c',type=str,dest="condition",required=True, help="Condition. \nSupported strings: [ isnan, <_value, >_value, <=_value, >=_value, ==_value  ]\nno spaces allowed between condition and value, use underscore instead of a space")
        parser.add_argument('--value',type=float,dest="value",required=True, help="Substitution value.")
        parser.add_argument('--outputFieldName ',type=str,dest="nomvar_out", help="Option to give the output field a different name from the input field name (works only with 1 input field).")
        parser.add_argument('--clearMissingDataFlag',action='store_true',default=False,dest="clear_missing_data", help="When replacing values, clear the missing data flag.")

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg['nomvar_out'] is not None:
            validate_nomvar(parsed_arg['nomvar_out'],"AddToElement",ReplaceDataIfConditionError)

        parse_condition(parsed_arg['condition'])

        return parsed_arg
    
def parse_condition(condition):
    if condition == 'isnan':
        return None, None
    
    match_operator = "(>=|<=|==|\>|\<)"
    match_optional_underscore = "_*"
    match_float = "(\d+\.?\d?)"
    match_all = match_operator+match_optional_underscore+match_float

    if not re.match(match_all, condition):
        raise ReplaceDataIfConditionError(f"invalid condition - {condition}")
    
    parsed_condition = re.search(match_all,condition)
    
    return (parsed_condition[1],parsed_condition[2])

operator_lookup_table = {
    "<" : operator.lt,
    "<=" : operator.le,
    ">" : operator.gt,
    ">=" : operator.ge,
    "==" : operator.eq,
}

def replace_data_if_condition(arr: np.ndarray, replace_value:float, condition_operator, condition_value:float) -> np.ndarray:
    """Calculates 

    :param arr: data
    :type arr: np.ndarray

    :return: data with replaced value
    :rtype: np.ndarray
    """
    if condition_operator is None:
        return np.where(np.isnan(arr), replace_value, arr)

    return np.where(condition_operator(arr,condition_value), replace_value, arr)

