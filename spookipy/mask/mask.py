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

        ops_str = ['<', '<=', '==', '>=', '>', '!=']
        self.op_list = []

        for operator in self.operators:
            if operator not in ops_str:
                raise MaskError(
                    f'Operators must have values included in {ops_str}\n')
            if operator == '>':
                self.op_list.append(0)
            elif operator == '>=':
                self.op_list.append(1)
            elif operator == '==':
                self.op_list.append(2)
            elif operator == '<=':
                self.op_list.append(3)
            elif operator == '<':
                self.op_list.append(4)
            else:
                self.op_list.append(5)

        self.lenght = length
        self.thresholds = np.flip(self.thresholds).astype(np.float32)
        self.values = np.flip(self.values).astype(np.float32)
        self.op_list = np.flip(self.op_list).astype(dtype=np.int32)

    def compute(self) -> pd.DataFrame:
        df_list = []
        # holds data from all the groups
        # res_df = create_empty_result(self.df,self.plugin_result_specifications['ALL'],all_rows=True)
        self.df['etiket'] = 'MASK'
        if not(self.nomvar_out is None):
            self.df['nomvar'] = self.nomvar_out

        if self.parallel:
            df_list = apply_mask_parallel(self.df, self.values, self.op_list, self.thresholds)
        else:    
            df_list = apply_mask(self.df, self.values, self.op_list, self.thresholds)


        return final_results(df_list, MaskError, self.meta_df)

def apply_mask(df, values, op_list, thresholds):
    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)
    results = []
    for df in df_list:
        df = fstpy.compute(df)
        for i in df.index:
            ni = df.at[i, 'd'].shape[0]
            nj = df.at[i, 'd'].shape[1]
            arr = f_mask(slab=df.at[i,'d'], ni=ni, nj=nj, values=values, operators=op_list, thresholds=thresholds, n=thresholds.size)
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
    return f_mask(slab=data, ni=ni, nj=nj, values=values.get(), operators=op_list.get(), thresholds=thresholds.get(), n=thresholds.get().size)


def apply_mask_parallel(df, values, op_list, thresholds):

    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)
    results = []
    for df in df_list:
        df = fstpy.compute(df)
        values_arr = [ListWrapper(values) for _ in range(len(df.index))] #np.full((len(df.index)),ListWrapper(values))
        ops_arr = [ListWrapper(op_list) for _ in range(len(df.index))] #np.full((len(df.index)),ListWrapper(op_list))
        thresholds_arr = [ListWrapper(thresholds) for _ in range(len(df.index))] #np.full((len(df.index)),ListWrapper(thresholds))

        with ThreadPool() as tp:
            filter_results = tp.starmap(mask_wrapper,zip(df.d.to_list(),values_arr,ops_arr,thresholds_arr))

        df['d'] = [to_dask(r) for r in filter_results]

        results.append(df)

    return results
