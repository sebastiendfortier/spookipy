# -*- coding: utf-8 -*-
import logging

import numpy as np
import pandas as pd

from ..opelementsbypoint import OpElementsByPoint
from ..plugin import Plugin
from ..utils import initializer


class ArithmeticMeanByPointError(Exception):
    pass


class ArithmeticMeanByPoint(Plugin):
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            group_by_forecast_hour=False,
            nomvar_out='MEAN'):
        pass

    def compute(self) -> pd.DataFrame:
        logging.info('ArithmeticMeanByPoint - compute')
        return OpElementsByPoint(
            self.df,
            operator=np.mean,
            operation_name='ArithmeticMeanByPoint',
            exception_class=ArithmeticMeanByPointError,
            group_by_forecast_hour=self.group_by_forecast_hour,
            group_by_level=True,
            nomvar_out=self.nomvar_out,
            etiket='MEANPT').compute()
