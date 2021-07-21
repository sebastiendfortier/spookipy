# -*- coding: utf-8 -*-
from spookipy.utils import initializer
from spookipy.plugin import Plugin
import pandas as pd
import sys
from spookipy.opelementsbyvalue.opelementsbyvalue import OpElementsByValue


def add_value(a, v):
    return a + v

class AddToElementsError(Exception):
    pass

class AddToElements(Plugin):
    @initializer
    def __init__(self, df:pd.DataFrame, value, nomvar_out=''):
        pass

    def compute(self) -> pd.DataFrame:
        sys.stdout.write('AddToElements - compute')
        return OpElementsByValue(
            df = self.df,
            operator = add_value, 
            value = self.value,
            operation_name='AddToElements',
            exception_class = AddToElementsError,
            nomvar_out= self.nomvar_out
            ).compute() 
