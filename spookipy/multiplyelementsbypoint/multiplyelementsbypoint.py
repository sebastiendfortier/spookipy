# -*- coding: utf-8 -*-
import logging

import numpy as np
import pandas as pd

from ..opelementsbycolumn import OpElementsByColumn
from ..plugin import Plugin
from ..utils import initializer


class MultiplyElementsByPointError(Exception):
    pass


class MultiplyElementsByPoint(Plugin):
    """Multiplication of the values of all the fields received at each point

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param nomvar_out: nomvar for output result, defaults to 'MUEP'
    :type nomvar_out: str, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            group_by_forecast_hour=False,
            nomvar_out='MUEP'):

        pass

    def compute(self) -> pd.DataFrame:
        logging.info('MultiplyElementsByPoint - compute')
        return OpElementsByColumn(
            self.df,
            operator=np.prod,
            operation_name='MultiplyElementsByPoint',
            exception_class=MultiplyElementsByPointError,
            group_by_forecast_hour=self.group_by_forecast_hour,
            group_by_level=True,
            nomvar_out=self.nomvar_out,
            etiket='MULEPT').compute()
