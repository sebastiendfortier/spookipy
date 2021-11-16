# -*- coding: utf-8 -*-
import logging

import numpy as np
import pandas as pd

from ..opelementsbycolumn import OpElementsByColumn
from ..plugin import Plugin
from ..utils import initializer


class AddElementsByPointError(Exception):
    pass


class AddElementsByPoint(Plugin):
    """Add, for each point, the values of all the fields received

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param nomvar_out: nomvar for output result, defaults to 'ADEP'
    :type nomvar_out: str, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            group_by_forecast_hour: bool=False,
            nomvar_out: str='ADEP'):

        pass

    def compute(self) -> pd.DataFrame:
        logging.info('AddElementsByPoint - compute')
        return OpElementsByColumn(
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
        """method to translate spooki plugin parameters to python plugin parameters

        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        args = {}

        if 'outputFieldName' in kwargs:
            args['nomvar_out'] = kwargs['outputFieldName']

        if 'groupBy' in kwargs and kwargs['groupBy'] == "FORECAST_HOUR":
            args['group_by_forecast_hour'] = True

        return args
