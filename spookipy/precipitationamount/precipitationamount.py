# -*- coding: utf-8 -*-
import argparse
import logging
from typing import Final
import pandas as pd
from ..timeintervaldifference.timeintervaldifference import TimeIntervalDifference
from ..plugin import Plugin, PluginParser
from ..utils import final_results, initializer, validate_nomvar
from ..configparsingutils import apply_lambda_to_list, convert_time_range, convert_time

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
    def __init__(self, df: pd.DataFrame, nomvar=None, forecast_hour_range=None, interval=None, step=None):
        super().__init__(df)
        # self.validate_nomvar()

    def compute(self) -> pd.DataFrame:
        logging.info('PrecipitationAmount - compute\n')
        df = TimeIntervalDifference(self.df, nomvar=self.nomvar,
                                       forecast_hour_range=self.forecast_hour_range,
                                       interval=self.interval,
                                       step=self.step,
                                       strictly_positive=True).compute()
        df['label'] = ETIKET

        return final_results([df], PrecipitationAmountError, self.meta_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=PrecipitationAmount.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--fieldName',required=True,type=str,dest='nomvar', help="List of field names.")
        parser.add_argument('--interval',required=True,type=str, help="List of each time range used for the minimum/maximum calculation")
        parser.add_argument('--rangeForecastHour',required=True,type=str,dest='forecast_hour_range', help="List of time ranges in hours.")
        parser.add_argument('--step',required=True,type=str, help="List of the time steps in hours between successive start times within each time range.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['interval'] = apply_lambda_to_list(parsed_arg['interval'].split(','), lambda a: convert_time(a))
        parsed_arg['step'] = apply_lambda_to_list(parsed_arg['step'].split(','), lambda a: convert_time(a))
        parsed_arg['forecast_hour_range'] = apply_lambda_to_list(parsed_arg['forecast_hour_range'].split(','), lambda a: convert_time_range(a))

        parsed_arg['nomvar'] = parsed_arg['nomvar'].split(',')
        apply_lambda_to_list(parsed_arg['nomvar'],lambda a : validate_nomvar(a,"PrecipitationAmount",PrecipitationAmountError))

        return parsed_arg
