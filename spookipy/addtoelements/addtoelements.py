# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
import pandas as pd
from spookipy.opelementsbyvalue.opelementsbyvalue import OpElementsByValue


def add_value(a, v):
    return a + v

class AddToElementsError(Exception):
    pass

class AddToElements(Plugin):

    def __init__(self, df:pd.DataFrame, value, nomvar_out=''):
        self.df = df
        self.value = value
        self.nomvar_out = nomvar_out


    def compute(self) -> pd.DataFrame:
        return OpElementsByValue(
            df = self.df,
            operator = add_value, 
            value = self.value,
            operation_name='AddToElements',
            exception_class = AddToElementsError,
            nomvar_out= self.nomvar_out
            ).compute() 
