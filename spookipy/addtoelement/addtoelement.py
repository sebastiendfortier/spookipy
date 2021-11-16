# -*- coding: utf-8 -*-
import logging

import pandas as pd

from ..opelementsbyvalue import OpElementsByValue
from ..plugin import Plugin
from ..utils import initializer


def add_value(a, v):
    return a + v

class AddToElementError(Exception):
    pass

class AddToElement(Plugin):
    """Add a given number to each element of a field

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param value: value to add to field
    :type value: float
    :param nomvar_out: nomvar for output result, defaults to None
    :type nomvar_out: str, optional
    """
    @initializer
    def __init__(self, df: pd.DataFrame, value:float, nomvar_out:str=None):
        pass

    def compute(self) -> pd.DataFrame:
        logging.info('AddToElement - compute')
        return OpElementsByValue(
            df=self.df,
            operator=add_value,
            value=self.value,
            operation_name='AddToElement',
            exception_class=AddToElementError,
            nomvar_out=self.nomvar_out,
            etiket='ADDTOE').compute()
