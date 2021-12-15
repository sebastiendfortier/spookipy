# -*- coding: utf-8 -*-
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import create_empty_result, final_results, get_list_of_forecast_hours, initializer, to_numpy, validate_list_of_nomvar, validate_list_of_times, validate_list_of_tuples_of_times


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
    """
    @initializer
    def __init__(self, df: pd.DataFrame, nomvar=None, forecast_hour_range=None, interval=None, step=None, strictly_positive=False):
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise TimeIntervalDifferenceError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(self.df, ['forecast_hour'])

        if self.nomvar is None or self.forecast_hour_range is None or self.interval is None or self.step is None:
            raise TimeIntervalDifferenceError(
                'One of the mandatory parameter (nomvar, forecast_hour_range, interval, step) is None')

 
        self.check_type_of_params()

        l_fcast = len(self.forecast_hour_range)
        l_int = len(self.interval)
        l_step = len(self.step)
        if l_fcast != l_int or l_fcast != l_step:
            raise TimeIntervalDifferenceError('All list must be the same length')

        for i in range(len(self.interval)):
            if self.interval[i] > self.forecast_hour_range[i][1] - self.forecast_hour_range[i][0]:
                raise TimeIntervalDifferenceError(
                    'The interval must be lower or equal to upper bound minus lower bound of forecast_hour_range.')

        if not isinstance(self.nomvar,list):
            self.nomvar = [self.nomvar]
        for nomvar in self.nomvar:
            if nomvar not in list(self.df.nomvar.unique()):
                raise TimeIntervalDifferenceError(f'Variable {nomvar}, missing from DataFrame!')

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)


        self.df_without_intervals = self.df.loc[(~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])) & (self.df.interval.isna()) & (self.df.nomvar.isin(self.nomvar))].reset_index(drop=True)

        self.df_with_intervals = self.df.loc[(~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])) & (~self.df.interval.isna()) & (self.df.nomvar.isin(self.nomvar))].reset_index(drop=True)


        self.groups_without_interval = self.df_without_intervals.groupby(['grid', 'nomvar'])
        self.groups_with_interval = self.df_with_intervals.groupby(['grid', 'nomvar'])


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
                
                end_df = current_group.loc[(current_group.lower_bound.astype('int32') == b_inf)]
                begin_df = current_group.loc[(current_group.lower_bound.astype('int32') == b_sup)]

                if begin_df.empty or end_df.empty:
                    begin_df = current_group.loc[(current_group.upper_bound.astype('int32') == b_inf)]
                    end_df = current_group.loc[(current_group.upper_bound.astype('int32') == b_sup)]
                    if begin_df.empty or end_df.empty:
                        logging.warning(f'No data found for interval: {int(b_inf/3600)} @ {int(b_sup/3600)}')
                        incomplete = True
                        break

                res_df = self.process(current_group, b_inf, b_sup, begin_df, end_df)

                diffs.append(res_df)

            if not incomplete:
                for df in diffs:
                    df.drop(columns=['lower_bound','upper_bound'])
                    df['interval'] = None
                    df_list.append(df)

        for _, current_group in self.groups_without_interval:
            diffs = []
            incomplete = False
            for forecast_hours in self.forecast_hours:
                b_inf = forecast_hours[0]
                b_sup = forecast_hours[1]

                begin_df = current_group.loc[(current_group.forecast_hour.dt.total_seconds().astype('int32') == b_inf)]
                end_df = current_group.loc[(current_group.forecast_hour.dt.total_seconds().astype('int32') == b_sup)]

                if begin_df.empty or end_df.empty:
                    logging.warning(f'No data found for interval: {int(b_inf/3600)} @ {int(b_sup/3600)}')
                    incomplete = True
                    break

                res_df = self.process(current_group, b_inf, b_sup, begin_df, end_df)

                diffs.append(res_df)

            if not incomplete:
                for df in diffs:
                    df_list.append(df)



        return final_results(df_list, TimeIntervalDifferenceError, self.meta_df)

    def process(self, current_group, b_inf, b_sup, begin_df, end_df):
        begin_arr = begin_df.iloc[0]['d']
        end_arr = end_df.iloc[0]['d']    

        check_for_negative_values(begin_arr, 'input')
        check_for_negative_values(end_arr, 'input')

        if self.strictly_positive:
            begin_arr = np.where(begin_arr < 0., 0., begin_arr)
            end_arr = np.where(end_arr < 0., 0., end_arr)

        # set new ip2, ip3 and npas
        res_df = create_result_container(current_group, b_inf, b_sup)

        res_df.at[0, 'd'] =  end_arr - begin_arr

        check_for_negative_values(res_df.at[0, 'd'], 'output')

        if self.strictly_positive:
            res_df.at[0, 'd'] = np.where(res_df.at[0, 'd'] < 0., 0., res_df.at[0, 'd'])
        return res_df


    def check_type_of_params(self):
        # make sure that nomvar is a list of str
        self.nomvar = validate_list_of_nomvar(self.nomvar, 'TimeIntervalDifference', TimeIntervalDifferenceError)

        # make sure that interval is a list of datetime.timedelta
        self.interval = validate_list_of_times(self.interval, TimeIntervalDifferenceError)

        # make sure that step is a list of datetime.timedelta
        self.step = validate_list_of_times(self.step, TimeIntervalDifferenceError)

        # make sure that forecast_hour_range is a list of tuple of 2 datetime.timedelta
        self.forecast_hour_range = validate_list_of_tuples_of_times(self.forecast_hour_range, TimeIntervalDifferenceError)


def create_result_container(df, b_inf, b_sup):
    deet = df.iloc[0]['deet']
    ip2 = int(b_sup/3600)
    ip3 = int((b_sup-b_inf)/3600)
    npas = int((ip2 * 3600) / deet)
    res_df = create_empty_result(df, {'ip2': ip2, 'ip3': ip3, 'npas': npas})
    return res_df

def check_for_negative_values(arr, location):
    if np.any(np.where(arr < 0.,True,False)):
        logging.warning(f"Found a negative value in the {location}! Probable cause is loss of precision when converting to float computational type")
        logging.warning(f'The lowest found negative value was : {to_numpy(np.min(arr))}')


def get_lower_bound(interval):
    return interval.low*3600

def get_upper_bound(interval):
    return interval.high*3600    