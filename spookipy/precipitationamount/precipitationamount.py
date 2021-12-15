# -*- coding: utf-8 -*-
import logging
from typing import Final
import pandas as pd
from ..timeintervaldifference.timeintervaldifference import TimeIntervalDifference
from ..plugin import Plugin
from ..utils import final_results, initializer

ETIKET: Final[str] = 'PCPAMT'

class PrecipitationAmountError(Exception):
    pass

class PrecipitationAmount(Plugin):
    """Calculate precipitation accumulations for given time intervals.
    
    :param df: Input dataframe
    :type df: pd.DataFrame
    :param nomvar: Target nomvar(s) for the computation of differences
    :type nomvar: str or list of str
    :param forecast_hour_range: List of forecast hour ranges, tuple of 2 values
    :type forecast_hour_range: tuple(datetime.timedelta, datetime.timedelta) or list of tuple(datetime.timedelta, datetime.timedelta)
    :param interval: List of the time intervals between inputs within each time range.
    :type interval: datetime.timedelta or list of datetime.timedelta
    :param step: List of the time steps between successive start times within each time range
    :type step: datetime.timedelta or list of datetime.timedelta
    """
    @initializer
    def __init__(self, df: pd.DataFrame, nomvar=None, forecast_hour_range=None, interval=None, step=None, strictly_positive=False):
        super().__init__(df)
        # self.validate_nomvar()

    def compute(self) -> pd.DataFrame:
        logging.info('PrecipitationAmount - compute\n')
        df = TimeIntervalDifference(self.df, nomvar=self.nomvar,
                                       forecast_hour_range=self.forecast_hour_range,
                                       interval=self.interval,
                                       step=self.step,
                                       strictly_positive=True).compute()
        df['etiket'] = ETIKET

        return final_results([df], PrecipitationAmountError, self.meta_df)