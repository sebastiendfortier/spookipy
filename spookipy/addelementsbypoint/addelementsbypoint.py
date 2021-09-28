# -*- coding: utf-8 -*-
from ..plugin import Plugin
from ..utils import initializer
import pandas as pd
import numpy as np
import logging
from ..opelementsbypoint import OpElementsByPoint


class AddElementsByPointError(Exception):
    pass


class AddElementsByPoint(Plugin):
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            group_by_forecast_hour=False,
            nomvar_out='ADEP'):
        pass

    def compute(self) -> pd.DataFrame:
        logging.info('AddElementsByPoint - compute')
        return OpElementsByPoint(
            self.df,
            operator=np.sum,
            operation_name='AddElementsByPoint',
            exception_class=AddElementsByPointError,
            group_by_forecast_hour=self.group_by_forecast_hour,
            group_by_level=True,
            nomvar_out=self.nomvar_out,
            etiket='ADDEPT').compute()

    @staticmethod
    def parse_config(**kwargs):
        args = {}

        if 'outputFieldName' in kwargs:
            args['nomvar_out'] = kwargs['outputFieldName']

        if 'groupBy' in kwargs and kwargs['groupBy'] == "FORECAST_HOUR":
            args['group_by_forecast_hour'] = True

        return args
