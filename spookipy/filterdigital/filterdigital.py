# -*- coding: utf-8 -*-
from numpy import float32
from ..utils import create_empty_result, final_results, initializer, validate_nomvar
from ..plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
import sys
import numpy as np
from .stenfilt import filtre

class FilterDigitalError(Exception):
    pass

class FilterDigital(Plugin):

    @initializer
    def __init__(self,df:pd.DataFrame,filter:list,repetitions:int=1,nomvar_out=None):

        self.plugin_result_specifications = {
            'ALL':{'filtered':True}
            # 'etiket':'FLTRDG',
        }

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise FilterDigitalError('No data to process')

        validate_nomvar(self.nomvar_out,'FilterDigital',FilterDigitalError)

        if not len(self.filter):
            raise FilterDigitalError('Filter must contain at least 1 value')

        if len(self.filter)%2==0:
            raise FilterDigitalError('Filter lenght must be odd, not even')

        if not (self.repetitions > 0):
            raise FilterDigitalError('Repetitions must be a positive integer')

        # self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

    def compute(self) -> pd.DataFrame:
        sys.stdout.write('FilterDigital - compute\n')

        if not (self.nomvar_out is None):
            self.plugin_result_specifications['ALL']['nomvar'] = self.nomvar_out

        self.df = fstpy.load_data(self.df)

        new_df = create_empty_result(self.df,self.plugin_result_specifications['ALL'],copy=True)

        df_list=[]

        filter_len = len(self.filter)
        filter = np.array(self.filter,dtype=np.int32,order='F')
        for i in new_df.index:
            ni = new_df.at[i,'d'].shape[0]
            nj = new_df.at[i,'d'].shape[1]
            filtre(slab=new_df.at[i,'d'],ni=ni,nj=nj,npass=self.repetitions,list=filter,l=filter_len)

        df_list.append(new_df)

        return final_results(df_list, FilterDigitalError, self.meta_df)
