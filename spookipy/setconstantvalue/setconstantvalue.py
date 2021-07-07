# -*- coding: utf-8 -*-
from spookipy.opelementsbyvalue.opelementsbyvalue import OpElementsByValue
from spookipy.plugin import Plugin
import pandas as pd


def set_value(a,v):
    a[:]=v
    return a

def set_series_value(a:pd.Series, v):
    return a.apply(set_value,args=(v,))

class SetConstantValueError(Exception):
    pass

class SetConstantValue(Plugin):
    def __init__(self, df:pd.DataFrame, value=0, nomvar_out='', min_index=False, max_index=False, nb_levels=False, bi_dimensionnal=False):
        if self.df.empty:
            raise  SetConstantValueError( 'SetConstantValue' + ' - no data to process')
        l = [min_index,max_index,nb_levels]
        lcount = l.count(True)
        if lcount != 0:
            if lcount != 1:
                raise SetConstantValueError('SetConstantValue - too many options selected, you can only choose one option at a time in %s' % ['min_index','max_index','nb_levels'])
            elif min_index:
                self.value=0
            elif max_index:
                self.value=len(df.index)-1
            else:
                self.value=len(df.index)
                

    def compute(self) -> pd.DataFrame:
        res_df= OpElementsByValue(self.df,
        value = self.value,
        operation_name='SetConstantValue',
        nomvar_out= self.nomvar_out,
        operator = set_series_value,
        unit = 'scalar' ,
        exception_class = SetConstantValueError).compute() 
        if self.bi_dimensionnal:
            res_df.drop(res_df.index[1:], inplace=True)
        return res_df