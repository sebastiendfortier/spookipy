# -*- coding: utf-8 -*-
from ..utils import create_empty_result, final_results, initializer
from ..plugin import Plugin
import pandas as pd
import numpy as np
import fstpy.all as fstpy
from .fmask import fmask


class MaskError(Exception):
    pass


class Mask(Plugin):

    @initializer
    def __init__(self, df:pd.DataFrame, thresholds=None, values=None, operators=None, nomvar_out=None):
        self.plugin_result_specifications = {
            'ALL':{'etiket':'MASK'}
        }
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise  MaskError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        length = len(self.thresholds)
        if not all(len(lst) == length for lst in [self.values, self.operators]):
            raise MaskError('Threshholds, values and operators lists, must have the same lenght')

        ops_str = ['<','<=','==','>=','>','!=']
        self.op_list = []

        for operator in self.operators:
            if operator not in ops_str:
                raise MaskError(f'Operators must have values included in {ops_str}\n')
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


        self.df = fstpy.load_data(self.df)
        self.lenght = length
        self.thresholds = np.flip(self.thresholds).astype(np.float32)
        self.values = np.flip(self.values).astype(np.float32)
        self.op_list = np.flip(self.op_list).astype(np.int32)

    def compute(self) -> pd.DataFrame:
        df_list=[]
        #holds data from all the groups
        res_df = create_empty_result(self.df,self.plugin_result_specifications['ALL'],all_rows=True)
        if not(self.nomvar_out is None):
            res_df['nomvar'] = self.nomvar_out

        for i in res_df.index:
            _ = fmask(slab=res_df.at[i,'d'],ni=res_df.at[i,'d'].shape[0],nj=res_df.at[i,'d'].shape[1],values=self.values,operators=self.op_list,thresholds=self.thresholds,n=self.thresholds.size)
            res_df.at[i,'d'] = res_df.at[i,'d'].astype(np.float32)

        df_list.append(res_df)

        return final_results(df_list, Mask, self.meta_df)
