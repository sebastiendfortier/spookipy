# -*- coding: utf-8 -*-
from ..utils import initializer, final_results
from ..opelementsbyvalue import OpElementsByValue
from ..plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
import logging


def set_value(a,v):
    a[:]=v
    return a

def set_series_value(a:pd.Series, v):
    return a.apply(set_value,args=(v,))

class SetConstantValueError(Exception):
    pass

class SetConstantValue(Plugin):

    @initializer
    def __init__(self, df:pd.DataFrame, value=0, nomvar_out=None, min_index=False, max_index=False, nb_levels=False, bi_dimensionnal=False):
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise SetConstantValueError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(self.df,True, columns=['unit','forecast_hour','ip_info'])

        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.groups=self.df.groupby(by=['grid','nomvar','dateo','forecast_hour'])

        l = [self.min_index,self.max_index,self.nb_levels]

        lcount = l.count(True)

        if lcount > 1:
            raise SetConstantValueError('Too many options selected, you can only choose one option at a time in %s' % ['min_index','max_index','nb_levels'])
        if self.min_index:
            self.value=0


    def compute(self) -> pd.DataFrame:
        logging.info('SetConstantValue - compute')
        df_list = []
        for _,current_group in self.groups:
            if self.max_index:
                self.value=len(current_group.index)-1
            if self.nb_levels:
                self.value=len(current_group.index)

            res_df= OpElementsByValue(current_group,
            value = self.value,
            operation_name='SetConstantValue',
            nomvar_out= self.nomvar_out,
            operator = set_series_value,
            unit = 'scalar' ,
            exception_class = SetConstantValueError,
            etiket='SETVAL').compute()
            if self.bi_dimensionnal:
                res_df.drop(res_df.index[1:], inplace=True)
                res_df.loc[:,'ip1'] = 0
            df_list.append(res_df)

        return final_results(df_list,SetConstantValueError, self.meta_df)
