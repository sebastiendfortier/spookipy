# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin, PluginParser
from ..utils import (create_empty_result, define_time_interval_infos, get_list_of_forecast_hours, initializer,
                     validate_list_of_nomvar, validate_list_of_times, validate_list_of_tuples_of_times, 
                     validate_nomvar)
from ..configparsingutils import apply_lambda_to_list, convert_time_range, convert_time

class TimeIntervalDifferenceError(Exception):
    pass

class TimeIntervalDifference(Plugin):
    """ Computes the time interval difference between groups of begin@end forecast_hour
    
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
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """
    @initializer
    def __init__(self, 
                 df: pd.DataFrame, 
                 nomvar              = None, 
                 forecast_hour_range = None, 
                 interval            = None, 
                 step                = None, 
                 strictly_positive   = False,
                 reduce_df           = True):
        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):

        self.no_meta_df = fstpy.add_columns(self.no_meta_df, ['forecast_hour'])

        if self.nomvar is None or self.forecast_hour_range is None or self.interval is None or self.step is None:
            raise TimeIntervalDifferenceError(
                'One of the mandatory parameter (nomvar, forecast_hour_range, interval, step) is None')

 
        self.check_type_of_params()

        l_fcast = len(self.forecast_hour_range)
        l_int   = len(self.interval)
        l_step  = len(self.step)
        if l_fcast != l_int or l_fcast != l_step:
            raise TimeIntervalDifferenceError('All list must be the same length')

        for i in range(len(self.interval)):
            if self.interval[i] > self.forecast_hour_range[i][1] - self.forecast_hour_range[i][0]:
                raise TimeIntervalDifferenceError(
                    'The interval must be lower or equal to upper bound minus lower bound of forecast_hour_range.')

        for nomvar in self.nomvar:
            if nomvar not in list(self.no_meta_df.nomvar.unique()):
                raise TimeIntervalDifferenceError(f'Variable {nomvar}, missing from DataFrame!')

        self.df_without_intervals = self.no_meta_df.loc[(self.no_meta_df.interval.isna())  & (self.no_meta_df.nomvar.isin(self.nomvar))].reset_index(drop=True)
        self.df_with_intervals    = self.no_meta_df.loc[(~self.no_meta_df.interval.isna()) & (self.no_meta_df.nomvar.isin(self.nomvar))].reset_index(drop=True)

        self.groups_without_interval = self.df_without_intervals.groupby(['grid', 'nomvar','ip1_kind'])
        self.groups_with_interval    = self.df_with_intervals.groupby(['grid', 'nomvar','ip1_kind'])


    def compute(self) -> pd.DataFrame:
        logging.info('TimeIntervalDifference - compute\n')

        self.forecast_hours = get_list_of_forecast_hours(self.forecast_hour_range, self.interval, self.step)

        if len(self.forecast_hours) == 0:
            raise TimeIntervalDifferenceError('Unable to calculate intervals with provided parameters')

        df_list = []

        for _, current_group in self.groups_with_interval:
           
            current_group['lower_bound'] = current_group['interval'].map(get_lower_bound)
            current_group['upper_bound'] = current_group['interval'].map(get_upper_bound)
            
            diffs = []
            incomplete = False
            for forecast_hours in self.forecast_hours:
                b_inf = forecast_hours[0]
                b_sup = forecast_hours[1]
                
                end_df   = current_group.loc[(current_group.lower_bound.astype('int32') == b_inf)]
                begin_df = current_group.loc[(current_group.lower_bound.astype('int32') == b_sup)]

                if begin_df.empty or end_df.empty:
                    begin_df = current_group.loc[(current_group.upper_bound.astype('int32') == b_inf)]
                    end_df   = current_group.loc[(current_group.upper_bound.astype('int32') == b_sup)]
                    if begin_df.empty or end_df.empty:
                        logging.warning(f'No data found for interval: {int(b_inf/3600)} @ {int(b_sup/3600)}')
                        incomplete = True
                        break

                res_df = self.process(current_group, b_inf, b_sup, begin_df, end_df)

                diffs.append(res_df)

            if not incomplete:
                for df in diffs:
                    df.drop(columns=['lower_bound','upper_bound'])
                    df_list.append(df)

        for _, current_group in self.groups_without_interval:
            diffs = []
            incomplete = False
            for forecast_hours in self.forecast_hours:
                b_inf = forecast_hours[0]
                b_sup = forecast_hours[1]

                begin_df = current_group.loc[(current_group.forecast_hour.dt.total_seconds().astype('int32') == b_inf)]
                end_df   = current_group.loc[(current_group.forecast_hour.dt.total_seconds().astype('int32') == b_sup)]

                if begin_df.empty or end_df.empty:
                    logging.warning(f'No data found for interval: {int(b_inf/3600)} @ {int(b_sup/3600)}')
                    incomplete = True
                    break

                res_df = self.process(current_group, b_inf, b_sup, begin_df, end_df)

                diffs.append(res_df)

            if not incomplete:
                for df in diffs:
                    df_list.append(df)

        return self.final_results(df_list, 
                                  TimeIntervalDifferenceError, 
                                  copy_input = False,
                                  reduce_df  = self.reduce_df)

    def process(self, current_group, b_inf, b_sup, begin_df, end_df):
        begin_arr = begin_df.iloc[0]['d']
        end_arr   = end_df.iloc[0]['d']    

        check_for_negative_values(begin_arr, 'input')
        check_for_negative_values(end_arr, 'input')

        if self.strictly_positive:
            begin_arr = np.where(begin_arr < 0., 0., begin_arr)
            end_arr   = np.where(end_arr < 0., 0., end_arr)

        # set new ip2, ip3 and npas
        res_df = create_result_container(current_group, b_inf, b_sup)

        res_df.at[0, 'd'] =  end_arr - begin_arr

        check_for_negative_values(res_df.at[0, 'd'], 'output')

        if self.strictly_positive:
            res_df.at[0, 'd'] = np.where(res_df.at[0, 'd'] < 0., 0., res_df.at[0, 'd'])
        return res_df


    def check_type_of_params(self):
        # make sure that nomvar is a list of str
        self.nomvar   = validate_list_of_nomvar(self.nomvar, 'TimeIntervalDifference', TimeIntervalDifferenceError)

        # make sure that interval is a list of datetime.timedelta
        self.interval = validate_list_of_times(self.interval, TimeIntervalDifferenceError)

        # make sure that step is a list of datetime.timedelta
        self.step    = validate_list_of_times(self.step, TimeIntervalDifferenceError)

        # make sure that forecast_hour_range is a list of tuple of 2 datetime.timedelta
        self.forecast_hour_range = validate_list_of_tuples_of_times(self.forecast_hour_range, TimeIntervalDifferenceError)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=TimeIntervalDifference.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--fieldName',required=True,type=str,dest='nomvar', help="List of field names.")
        parser.add_argument('--interval',required=True,type=str, help="List of the time intervals between inputs within each time range.")
        parser.add_argument('--rangeForecastHour',required=True,type=str,dest='forecast_hour_range', help="List of time ranges.")
        parser.add_argument('--step',required=True,type=str, help="List of the time steps between successive start times within each time range.")
        parser.add_argument('--strictlyPositive',action='store_true',dest='strictly_positive',default=False, help="Checks that input and output values are strictly positive.\nThis option also changes the negative values to 0.\nIf said condition is observed a warning will be displayed.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['interval'] = apply_lambda_to_list(parsed_arg['interval'].split(','), lambda a: convert_time(a))
        parsed_arg['step']     = apply_lambda_to_list(parsed_arg['step'].split(','), lambda a: convert_time(a))
        parsed_arg['forecast_hour_range'] = apply_lambda_to_list(parsed_arg['forecast_hour_range'].split(','), lambda a: convert_time_range(a))

        parsed_arg['nomvar']   = parsed_arg['nomvar'].split(',')
        apply_lambda_to_list(parsed_arg['nomvar'],lambda a : validate_nomvar(a,"TimeIntervalDifference",TimeIntervalDifferenceError))

        return parsed_arg

def create_result_container(df, b_inf, b_sup):

    info_inter = define_time_interval_infos(df, b_inf, b_sup)
    res_df     = create_empty_result(df, info_inter)

    return res_df

def check_for_negative_values(arr, location):
    if np.any(np.where(arr < 0.,True,False)):
        logging.warning(f"Found a negative value in the {location}! Probable cause is loss of precision when converting to float computational type")
        logging.warning(f'The lowest found negative value was : {np.min(arr)}')


def get_lower_bound(interval):
    return interval.low*3600

def get_upper_bound(interval):
    return interval.high*3600    
