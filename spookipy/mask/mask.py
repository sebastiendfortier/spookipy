# -*- coding: utf-8 -*-
import argparse
import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import final_results, initializer
from ..configparsingutils import preprocess_negative_args,check_length_2_to_4,apply_lamda_to_list

class MaskError(Exception):
    pass


class Mask(Plugin):
    """This plug-in creates a mask according to the threshold value(s) given.

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    :param thresholds: List of threshold values to take into account., defaults to None
    :type thresholds: list(float), optional
    :param values: List of values the mask will take (will be used in the same order as the threshold values), defaults to None
    :type values: list(float), optional
    :param operators: List of comparison operators (will be used in the same order as the threshold values), defaults to None
    :type operators: list(str), optional
    :param nomvar_out: nomvar for output result, defaults to None
    :type nomvar_out: str, optional
    :param parallel: execute in parallel, defaults to False
    :type parallel: bool, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            thresholds=None,
            values=None,
            operators=None,
            nomvar_out=None,
            parallel: bool = False):

        self.plugin_result_specifications = {
            'ALL': {'etiket': 'MASK'}
            }
        
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise MaskError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        length = len(self.thresholds)
        if not all(
            len(lst) == length for lst in [
                self.values,
                self.operators]):
            raise MaskError(
                'Threshholds, values and operators lists, must have the same lenght')


        ops = ['>', '>=', '==', '<=', '<', '!=']

        for op in self.operators:
            if op not in ops:
                raise MaskError(f'Operators must have values included in {ops} {op} is an ivalid entry\n')

        
    def compute(self) -> pd.DataFrame:
        
        df_list = []
        # holds data from all the groups

        self.df['etiket'] = 'MASK'
        if not(self.nomvar_out is None):
            self.df['nomvar'] = self.nomvar_out

        df_list = apply_mask(self.df, self.values[::-1], self.operators[::-1], self.thresholds[::-1])

        return final_results(df_list, MaskError, self.meta_df)


    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=Mask.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--thresholds',type=str,required=True, help="List of threshold values to take into account.")
        parser.add_argument('--values',type=str,required=True, help="List of values the mask will take (will be used in the same order as the threshold values).")
        parser.add_argument('--operators',type=str,required=True, help="List of comparison operators (will be used in the same order as the threshold values).")
        parser.add_argument('--outputFieldName',dest='nomvar_out',type=str, help="Option to give the output field a different name from the input field name (works only with 1 input field).")

        parsed_arg = vars(parser.parse_args(preprocess_negative_args(args.split(),["--thresholds","--values"])))

        check_length_2_to_4(parsed_arg['nomvar_out'],error_class=MaskError)

        op_dict = {'GT':'>', 'GE':'>=', 'EQ':'==', 'LE':'<=', 'LT':'<', 'NE':'!='}
        parsed_arg['operators'] = apply_lamda_to_list(parsed_arg['operators'].split(","), lambda a : op_dict[a])
        parsed_arg['values'] = apply_lamda_to_list(parsed_arg['values'].split(","), lambda a : float(a))
        parsed_arg['thresholds'] = apply_lamda_to_list(parsed_arg['thresholds'].split(","), lambda a : float(a))


        return parsed_arg

def lt(value, threshold):
    return (value < threshold)

def le(value, threshold):
    return (value <= threshold)

def eq(value, threshold):
    return (((value >= threshold - 0.4 ) & (value <= threshold + 0.4)))

def ge(value, threshold):
    return (value >= threshold)

def gt(value, threshold):
    return ( value > threshold)

def ne(value, threshold):
    return ( value != threshold)

def apply_mask(df, values, operators, thresholds):
    ops = {'>':gt, '>=':ge, '==':eq, '<=':le, '<':lt, '!=':ne}
    
    results = []
    for row in df.itertuples():
        df.at[row.Index,'d'] = process_array(values, operators, thresholds, ops, df.at[row.Index,'d']).astype('float32')

    results.append(df)

    return results

def process_array(values, operators, thresholds, ops, arr):

    for i in range(len(operators)-1,-1,-1):
        if i == len(operators)-1:
            a = np.where(ops[operators[i]](arr, thresholds[i]), values[i], 0.)
        else:
            a = np.where(ops[operators[i]](arr, thresholds[i]), values[i], a)
    return a

