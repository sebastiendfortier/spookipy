# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
from spookipy.utils import validate_nomvar
import pandas as pd
import fstpy.all as fstpy

class OpElementsByValueError(Exception):
    pass

class OpElementsByValue(Plugin):

    def __init__(self, df:pd.DataFrame, operator, value, operation_name='OpElementsByValue', exception_class = OpElementsByValueError, nomvar_out='', unit=''):
        self.df = df
        self.operator = operator
        self.value = value
        self.operation_name = operation_name
        self.exception_class = exception_class
        self.nomvar_out = nomvar_out
        self.unit = unit
        validate_nomvar(nomvar_out, operation_name, exception_class)
        if self.df.empty:
            raise  exception_class( operation_name + ' - no data to process')
        self.df = fstpy.load_data(self.df)
        self.plugin_result_specifications = {'ALL':{'nomvar':self.nomvar_out,'etiket':self.operation_name,'unit':self.unit}}

    def compute(self) -> pd.DataFrame:
        res_df = self.df.copy(deep=True)
        # res_df = fstpy.zap(res_df, nomvar=self.nomvar_out, etiket=self.operation_name, unit=self.unit)
        for k,v in self.plugin_result_specifications['ALL'].items(): 
            if v!='':
                res_df[k] = v

        res_df['d'] = self.operator(res_df['d'], self.value)
        return res_df 