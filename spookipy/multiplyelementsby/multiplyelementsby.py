# -*- coding: utf-8 -*-
from spookipy.utils import validate_nomvar
from spookipy.plugin import Plugin
import pandas as pd
from spookipy.opelementsbyvalue.opelementsbyvalue import OpElementsByValue
from spookipy.utils import initializer, validate_nomvar

def mult_value(a,v):
    return a * v

class MultiplyElementsByError(Exception):
    pass

class MultiplyElementsBy(Plugin):
    @initializer
    def __init__(self, df:pd.DataFrame, value, nomvar_out=''):
        validate_nomvar(nomvar_out, 'MultiplyElementsBy', MultiplyElementsByError)


    def compute(self) -> pd.DataFrame:
        return OpElementsByValue(self.df,
        value = self.value,
        operation_name='MultiplyElementsBy',
        nomvar_out= self.nomvar_out,
        operator = mult_value, 
        exception_class = MultiplyElementsByError).compute() 