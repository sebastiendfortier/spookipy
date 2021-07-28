# -*- coding: utf-8 -*-
from ..utils import validate_nomvar
from ..plugin.plugin import Plugin
import pandas as pd
from ..opelementsbyvalue.opelementsbyvalue import OpElementsByValue
from ..utils import initializer, validate_nomvar
import sys

def mult_value(a,v):
    return a * v

class MultiplyElementsByError(Exception):
    pass

class MultiplyElementsBy(Plugin):
    @initializer
    def __init__(self, df:pd.DataFrame, value, nomvar_out=''):
        pass

    def compute(self) -> pd.DataFrame:
        sys.stdout.write('MultiplyElementsBy - compute\n')
        return OpElementsByValue(self.df,
        value = self.value,
        operation_name='MultiplyElementsBy',
        nomvar_out= self.nomvar_out,
        operator = mult_value, 
        exception_class = MultiplyElementsByError).compute() 