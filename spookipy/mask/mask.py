# -*- coding: utf-8 -*-
import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import final_results, initializer


class MaskError(Exception):
    pass


class Mask(Plugin):

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
        df.at[row.Index,'d'] = process_array(values, operators, thresholds, ops, df.at[row.Index,'d'])

    results.append(df)

    return results

def process_array(values, operators, thresholds, ops, arr):

    for i in range(len(operators)-1,-1,-1):
        if i == len(operators)-1:
            a = np.where(ops[operators[i]](arr, thresholds[i]), values[i], 0.)
        else:
            a = np.where(ops[operators[i]](arr, thresholds[i]), values[i], a)
    return a

