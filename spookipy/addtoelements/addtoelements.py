# -*- coding: utf-8 -*-
from ..utils import initializer
from ..plugin import Plugin
import pandas as pd
import sys
from ..opelementsbyvalue import OpElementsByValue


def add_value(a, v):
    return a + v

class AddToElementsError(Exception):
    pass

class AddToElements(Plugin):
    @initializer
    def __init__(self, df:pd.DataFrame, value, nomvar_out=None):
        pass

    def compute(self) -> pd.DataFrame:
        sys.stdout.write('AddToElements - compute\n')
        return OpElementsByValue(
            df = self.df,
            operator = add_value,
            value = self.value,
            operation_name='AddToElements',
            exception_class = AddToElementsError,
            nomvar_out= self.nomvar_out
            ).compute()
