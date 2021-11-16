# -*- coding: utf-8 -*-
import logging

import numpy as np
import pandas as pd

from ..opelementsbycolumn import OpElementsByColumn
from ..plugin import Plugin
from ..utils import initializer


class ArithmeticMeanByPointError(Exception):
    pass


class ArithmeticMeanByPoint(Plugin):
    """Arithmetic mean for each point of all the fields received

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param nomvar_out: nomvar for output result, defaults to 'MEAN'
    :type nomvar_out: str, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            group_by_forecast_hour=False,
            nomvar_out='MEAN'):
        pass

    def compute(self) -> pd.DataFrame:
        logging.info('ArithmeticMeanByPoint - compute')
        return OpElementsByColumn(
            self.df,
            operator=np.mean,
            operation_name='ArithmeticMeanByPoint',
            exception_class=ArithmeticMeanByPointError,
            group_by_forecast_hour=self.group_by_forecast_hour,
            group_by_level=True,
            nomvar_out=self.nomvar_out,
            etiket='MEANPT').compute()
