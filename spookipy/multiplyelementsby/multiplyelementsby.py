# -*- coding: utf-8 -*-
import logging

import pandas as pd

from ..opelementsbyvalue import OpElementsByValue
from ..plugin import Plugin
from ..utils import initializer


def mult_value(a, v):
    return a * v


class MultiplyElementsByError(Exception):
    pass


class MultiplyElementsBy(Plugin):
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
                                 exception_class=MultiplyElementsByError,
                                 etiket='MULEBY').compute()
