# -*- coding: utf-8 -*-
import logging

import pandas as pd

from ..opelementsbyvalue import OpElementsByValue
from ..plugin import Plugin
from ..utils import initializer


def mult_value(a, v):
    return a * v


class MultiplyElementByError(Exception):
    pass


class MultiplyElementBy(Plugin):
    """Multiplies each element of a field by a given value

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    :param value: value to use
    :type value: float
    :param nomvar_out: nomvar for output result, defaults to None
    :type nomvar_out: str, optional
    """
    @initializer
    def __init__(self, df: pd.DataFrame, value, nomvar_out=None):
        pass

    def compute(self) -> pd.DataFrame:
        logging.info('MultiplyElementsBy - compute')
        return OpElementsByValue(self.df,
                                 value=self.value,
                                 operation_name='MultiplyElementsBy',
                                 nomvar_out=self.nomvar_out,
                                 operator=mult_value,
                                 exception_class=MultiplyElementByError,
                                 etiket='MULEBY').compute()
