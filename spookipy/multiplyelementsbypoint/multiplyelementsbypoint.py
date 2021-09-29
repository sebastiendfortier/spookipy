# -*- coding: utf-8 -*-
import logging

import numpy as np
import pandas as pd

from ..opelementsbypoint import OpElementsByPoint
from ..plugin import Plugin
from ..utils import initializer


class MultiplyElementsByPointError(Exception):
    pass


class MultiplyElementsByPoint(Plugin):

    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            group_by_forecast_hour=False,
            nomvar_out='MUEP'):
        pass

    def compute(self) -> pd.DataFrame:
        logging.info('MultiplyElementsByPoint - compute')
        return OpElementsByPoint(
            self.df,
            operator=np.prod,
            operation_name='MultiplyElementsByPoint',
            exception_class=MultiplyElementsByPointError,
            group_by_forecast_hour=self.group_by_forecast_hour,
            group_by_level=True,
            nomvar_out=self.nomvar_out,
            etiket='MULEPT').compute()
