# -*- coding: utf-8 -*-
import logging
from multiprocessing.pool import ThreadPool

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (final_results, get_split_value, initializer, to_dask, validate_nomvar)
from .f_stenfilt import f_stenfilt


class FilterDigitalError(Exception):
    pass


class FilterDigital(Plugin):

    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            filter: list,
            repetitions: int = 1,
            nomvar_out=None,
            parallel: bool = False):

        self.plugin_result_specifications = {
            'ALL': {'filtered': True}
            # 'etiket':'FLTRDG',
        }

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise FilterDigitalError('No data to process')

        validate_nomvar(self.nomvar_out, 'FilterDigital', FilterDigitalError)

        if not len(self.filter):
            raise FilterDigitalError('Filter must contain at least 1 value')

        if len(self.filter) % 2 == 0:
            raise FilterDigitalError('Filter lenght must be odd, not even')

        if not (self.repetitions > 0):
            raise FilterDigitalError('Repetitions must be a positive integer')

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

    def compute(self) -> pd.DataFrame:
        logging.info('FilterDigital - compute')

        # if not (self.nomvar_out is None):
        #     self.plugin_result_specifications['ALL']['nomvar'] = self.nomvar_out

        # self.df = fstpy.compute(self.df)

        if not (self.nomvar_out is None):
            self.df['nomvar'] = self.nomvar_out
        self.df['filtered'] = True

        # new_df = create_empty_result(self.df,self.plugin_result_specifications['ALL'],all_rows=True)

        filter_len = len(self.filter)

        filter_arr = np.array(self.filter, dtype=np.int32, order='F')

        if self.parallel:
            df_list = apply_filter_parallel(self.df, self.repetitions, filter_arr, filter_len)
        else:    
            df_list = apply_filter(self.df, self.repetitions, filter_arr, filter_len)


        return final_results(df_list, FilterDigitalError, self.meta_df)

def apply_filter(df, repetitions, filter_arr, filter_len):
    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)
    results = []
    for df in df_list:
        df = fstpy.compute(df)
        for i in df.index:
            ni = df.at[i, 'd'].shape[0]
            nj = df.at[i, 'd'].shape[1]
            arr = f_stenfilt(slab=df.at[i,'d'],ni=ni,nj=nj,npass=repetitions,list=filter_arr,l=filter_len)
            df.at[i, 'd'] = to_dask(arr)

        results.append(df)
    return results

class ListWrapper:
    def __init__(self, arr):
        self.arr = arr
    def get(self):
        return self.arr

def filter_wrapper(data,repetitions,filter_arr,filter_len):
    ni = data.shape[0]
    nj = data.shape[1]
    return f_stenfilt(slab=data,ni=ni,nj=nj,npass=repetitions,list=filter_arr.get(),l=filter_len)

def apply_filter_parallel(df, repetitions, filter, filter_len):

    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)
    results = []
    for df in df_list:
        df = fstpy.compute(df)
        
        repetitions_arr = [repetitions for _ in range(len(df.index))]
        filter_arr = [ListWrapper(filter) for _ in range(len(df.index))]
        filter_len_arr = [filter_len for _ in range(len(df.index))]

        with ThreadPool() as tp:
            filter_results = tp.starmap(filter_wrapper,zip(df.d.to_list(),repetitions_arr,filter_arr,filter_len_arr))

        df['d'] = [to_dask(r) for r in filter_results]

        results.append(df)

    return results