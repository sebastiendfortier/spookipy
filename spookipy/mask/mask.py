# -*- coding: utf-8 -*-
from multiprocessing.pool import ThreadPool

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (final_results, get_split_value, initializer, to_dask,
                     to_numpy)
from .f_mask import f_mask


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


        ops = {'>':0, '>=':1, '==':2, '<=':3, '<':4, '!=':5}
        # ops1 = {'>':gt, '>=':ge, '==':eq, '<=':le, '<':lt, '!=':ne}

        self.op_list = [*map(ops.get, self.operators)]

        if None in self.op_list:
            raise MaskError(f'Operators must have values included in {ops.keys()}\n')

        # func_list = []
        # for i in range(len(self.operators)):
        #     op = ops1[self.operators[i]]
        #     threshold = self.thresholds[i]
        #     value = self.values[i]
        #     print(op,threshold,value)
        #     func_list.append(lambda v : ge(v,threshold,value))


        self.lenght = length
        self.thresholdsr = self.thresholds[::-1]
        self.valuesr = self.values[::-1]
        self.op_listr = self.op_list[::-1]
        self.operatorsr = self.operators[::-1]
        # self.op_list1r = self.op_list1[::-1]

    def compute(self) -> pd.DataFrame:
        
        df_list = []
        # holds data from all the groups
        # res_df = create_empty_result(self.df,self.plugin_result_specifications['ALL'],all_rows=True)
        self.df['etiket'] = 'MASK'
        if not(self.nomvar_out is None):
            self.df['nomvar'] = self.nomvar_out

        if self.parallel:
            df_list = apply_mask_parallel(self.df, self.valuesr, self.op_listr, self.thresholdsr)
        else:    
            # df_list = apply_mask(self.df, self.valuesr, self.op_listr, self.thresholdsr)
            df_list = apply_mask_python2(self.df, self.valuesr, self.operatorsr, self.thresholdsr)

        return final_results(df_list, MaskError, self.meta_df)


def lt(value, threshold, replacement):
    return np.where(value < threshold, replacement, np.nan)

def le(value, threshold, replacement):
    return np.where(value <= threshold , replacement, np.nan)

def eq(value, threshold, replacement):
    return np.where(((value >= threshold - 0.4 ) & (value <= threshold + 0.4)), replacement, np.nan)

def ge(value, threshold, replacement):
    return np.where(value >= threshold, replacement, np.nan)

def gt(value, threshold, replacement):
    return np.where( value > threshold, replacement, np.nan)

def ne(value, threshold, replacement):
    return np.where( value != threshold, replacement, np.nan)

def apply_mask_python1(df, values, operators, thresholds):
    ops = {'>':gt, '>=':ge, '==':eq, '<=':le, '<':lt, '!=':ne}

    results = []
    for row in df.itertuples():
        arr_list = []
        for i in range(len(operators)):
            op = ops[operators[i]]
            arr_list.append( op(df.at[row.Index,'d'], thresholds[i], values[i]) )
        a = np.array(arr_list)
        c = np.where(np.isnan(a), 0., 1.)    
        i, j = np.indices(a.shape[1:])
        df.at[row.Index,'d'] = a[c.argmax(axis=0), i, j] 
        df.at[row.Index,'d'][np.isnan(df.at[row.Index,'d'])] = 0.

    results.append(df)

    return results

def lt1(value, threshold):
    return (value < threshold)

def le1(value, threshold):
    return (value <= threshold)

def eq1(value, threshold):
    return (((value >= threshold - 0.4 ) & (value <= threshold + 0.4)))

def ge1(value, threshold):
    return (value >= threshold)

def gt1(value, threshold):
    return ( value > threshold)

def ne1(value, threshold):
    return ( value != threshold)

def apply_mask_python2(df, values, operators, thresholds):
    ops = {'>':gt1, '>=':ge1, '==':eq1, '<=':le1, '<':lt1, '!=':ne1}
    
    results = []
    for row in df.itertuples():
        df.at[row.Index,'d'] = process(values, operators, thresholds, ops, df.at[row.Index,'d'])

    results.append(df)

    return results

def process(values, operators, thresholds, ops, arr):

    for i in range(len(operators)-1,-1,-1):
        if i == len(operators)-1:
            a = np.where(ops[operators[i]](arr, thresholds[i]), values[i], 0.)
        else:
            a = np.where(ops[operators[i]](arr, thresholds[i]), values[i], a)
    return a

def apply_mask(df, values, op_list, thresholds):
    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)
    results = []
    for df in df_list:
        df = fstpy.compute(df)
        for i in df.index:
            ni = df.at[i, 'd'].shape[0]
            nj = df.at[i, 'd'].shape[1]
            arr = f_mask(slab=df.at[i,'d'], ni=ni, nj=nj, values=values, operators=op_list, thresholds=thresholds, n=len(thresholds))
            df.at[i, 'd'] = to_dask(arr)

        results.append(df)
    return results

class ListWrapper:
    def __init__(self, arr):
        self.arr = arr
    def get(self):
        return self.arr

def mask_wrapper(data, values, op_list, thresholds):
    ni = data.shape[0]
    nj = data.shape[1]
    return f_mask(slab=data, ni=ni, nj=nj, values=values.get(), operators=op_list.get(), thresholds=thresholds.get(), n=len(thresholds.get()))


def apply_mask_parallel(df, values, op_list, thresholds):

    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)
    results = []
    for df in df_list:
        df = fstpy.compute(df)
        values_arr = [ListWrapper(values) for _ in range(len(df.index))] # np.full((len(df.index)),ListWrapper(values))
        ops_arr = [ListWrapper(op_list) for _ in range(len(df.index))] # np.full((len(df.index)),ListWrapper(op_list))
        thresholds_arr = [ListWrapper(thresholds) for _ in range(len(df.index))] # np.full((len(df.index)),ListWrapper(thresholds))

        with ThreadPool() as tp:
            filter_results = tp.starmap(mask_wrapper,zip(df.d.to_list(),values_arr,ops_arr,thresholds_arr))

        df['d'] = [to_dask(r) for r in filter_results]

        results.append(df)

    return results


