# -*- coding: utf-8 -*-
import logging
from typing import Final

import numpy as np
import pandas as pd

from ..opelementsbycolumn import OpElementsByColumn
from ..plugin import Plugin
from ..utils import initializer

ETIKET: Final[str] =  'SUBEVY'
class SubtractElementsVerticallyError(Exception):
    pass


class SubtractElementsVertically(Plugin):
    """From a field value for a chosen level (either the lowest or the highest), subtract the values from all the other levels of the same field.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param nomvar_out: nomvar for output result
    :type nomvar_out: str, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            direction: str='ascending',
            nomvar_out: str = None):

        pass

    def compute(self) -> pd.DataFrame:
        logging.info('SubtractElementsVertically - compute')
        return OpElementsByColumn(
            self.df,
            operator=np.sum,
            operation_name='SubtractElementsVertically',
            exception_class=SubtractElementsVerticallyError,
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
