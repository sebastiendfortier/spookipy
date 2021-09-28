# -*- coding: utf-8 -*-
from ..utils import final_results, initializer, to_dask, to_numpy
from ..plugin import Plugin
import pandas as pd
import numpy as np
import fstpy.all as fstpy
from .f_mask import f_mask
import dask.array as da


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
            nomvar_out=None):
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

        for i in self.df.index:
            ni = self.df.at[i, 'd'].shape[0]
            nj = self.df.at[i, 'd'].shape[1]
            self.df.at[i, 'd'] = to_numpy(self.df.at[i, 'd'])

            _ = f_mask(slab=self.df.at[i,
                                       'd'],
                       ni=ni,
                       nj=nj,
                       values=self.values,
                       operators=self.op_list,
                       thresholds=self.thresholds,
                       n=self.thresholds.size)
            self.df.at[i, 'd'] = to_dask(self.df.at[i, 'd'])

        df_list.append(self.df)

        return final_results(df_list, Mask, self.meta_df)
