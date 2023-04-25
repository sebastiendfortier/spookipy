# -*- coding: utf-8 -*-
import argparse
import datetime
import logging

import dask.array as da
import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin, PluginParser
from ..utils import (create_empty_result, final_results, get_list_of_forecast_hours, 
                     initializer, to_numpy, validate_list_of_nomvar, validate_list_of_times, 
                     validate_list_of_tuples_of_times, validate_nomvar)
from ..configparsingutils import apply_lambda_to_list, convert_time_range, convert_time

class TimeIntervalMinMaxError(Exception):
    pass

class TimeIntervalMinMax(Plugin):
    """Calculation of the minimum/maximum of a field whitin a specified time frame

    :param df: Input dataframe
    :type df: pd.DataFrame
    :param nomvar: Target nomvar(s) for the computation of min max
    :type nomvar: str or list of str
    :param min: get the minimum, defaults to False
    :type min: bool, optional
    :param max: get the maximum, defaults to False
    :type max: bool, optional
    :param forecast_hour_range: List of forecast hour ranges, tuple of 2 values
    :type forecast_hour_range: tuple(datetime.timedelta, datetime.timedelta) or list of tuple(datetime.timedelta, datetime.timedelta)
    :param interval: List of the time intervals between inputs within each time range.
    :type interval: datetime.timedelta or list of datetime.timedelta
    :param step: List of the time steps between successive start times within each time range
    :type step: datetime.timedelta or list of datetime.timedelta    
    :param nomvar_min: nomvar of min result field, defaults to None
    :type nomvar_min: str or list of str, optional
    :param nomvar_max: nomvar of min result field, defaults to None
    :type nomvar_max: str or list of str, optional
    """
    @initializer
    def __init__(self, df: pd.DataFrame, 
                 nomvar:str=None, min:bool=False, max:bool=False, 
                 forecast_hour_range=None, interval=None, step=None, 
                 nomvar_min=None, nomvar_max=None):
        
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise TimeIntervalMinMaxError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(self.df, ['forecast_hour'])

        if (self.nomvar is None) or (self.forecast_hour_range is None):
            raise TimeIntervalMinMaxError(
                'One of the mandatory parameter (nomvar, forecast_hour_range) is None')

        self.nomvar = validate_list_of_nomvar(self.nomvar, 'TimeIntervalMinMax', TimeIntervalMinMaxError)
        l_nomvar = len(self.nomvar)

        if (self.min is None) and (self.max is None):
            self.min = True
            self.max = True

        if self.min & (self.nomvar_min is None):
            self.nomvar_min = [''.join(['V',str(i),'MN']) for i in range(1,l_nomvar+1)]

        if self.max & (self.nomvar_max is None):
            self.nomvar_max = [''.join(['V',str(i),'MX']) for i in range(1,l_nomvar+1)]

        if self.min:
            self.nomvar_min = validate_list_of_nomvar(self.nomvar_min, 'TimeIntervalMinMax', TimeIntervalMinMaxError)
            l_nbmin = len(self.nomvar_min)
            if l_nomvar != l_nbmin:
                raise TimeIntervalMinMaxError('There must be the same number of output nomvar as there are inputs')
            self.df['nomvar_min'] = None
            for nomvar,nomvar_min in zip(self.nomvar,self.nomvar_min):
                self.df.loc[self.df.nomvar==nomvar,'nomvar_min'] = nomvar_min
        if self.max:    
            self.nomvar_max = validate_list_of_nomvar(self.nomvar_max, 'TimeIntervalMinMax', TimeIntervalMinMaxError)
            l_nbmax = len(self.nomvar_max)
            if l_nomvar != l_nbmax:
                raise TimeIntervalMinMaxError('There must be the same number of output nomvar as there are inputs')
            self.df['nomvar_max'] = None
            for nomvar,nomvar_max in zip(self.nomvar,self.nomvar_max):
                self.df.loc[self.df.nomvar==nomvar,'nomvar_max'] = nomvar_max    


        self.forecast_hour_range = validate_list_of_tuples_of_times(self.forecast_hour_range, TimeIntervalMinMaxError)
        l_fcast = len(self.forecast_hour_range)

        if self.step is None:
           self.step = [datetime.timedelta(hours=1)  for i in range(l_fcast)]
        else:
            self.step = validate_list_of_times(self.step, TimeIntervalMinMaxError)

        if self.interval is None:
           self.interval = [(i[1] - i[0])  for i in self.forecast_hour_range]
        else:
            self.interval = validate_list_of_times(self.interval, TimeIntervalMinMaxError)   

        l_int  = len(self.interval)
        l_step = len(self.step)
        
        if l_fcast != l_int or l_fcast != l_step:
            raise TimeIntervalMinMaxError('All list must be the same length')

        for i in range(len(self.interval)):
            if self.interval[i] > self.forecast_hour_range[i][1] - self.forecast_hour_range[i][0]:
                raise TimeIntervalMinMaxError(
                    'The interval must be lower or equal to upper bound minus lower bound of forecast_hour_range.')

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df_without_intervals = self.df.loc[(~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])) & (self.df.interval.isna()) & (self.df.nomvar.isin(self.nomvar))].reset_index(drop=True)

        self.df_with_intervals = self.df.loc[(~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])) & (~self.df.interval.isna()) & (self.df.nomvar.isin(self.nomvar))].reset_index(drop=True)

        self.groups_without_interval = self.df_without_intervals.groupby(['grid', 'nomvar','ip1_kind'])
        self.groups_with_interval    = self.df_with_intervals.groupby(['grid', 'nomvar','ip1_kind'])


    def compute(self) -> pd.DataFrame:
        logging.info('TimeIntervalMinMax - compute\n')

        self.forecast_hours = get_list_of_forecast_hours(self.forecast_hour_range, self.interval, self.step)

        if len(self.forecast_hours) == 0:
            raise TimeIntervalMinMaxError('Unable to calculate intervals with provided parameters')
        df_list = []
        for _, current_group in self.groups_with_interval:
            
            current_group['lower_bound'] = current_group['interval'].map(get_lower_bound)
            current_group['upper_bound'] = current_group['interval'].map(get_upper_bound)
            
            diffs = []
            incomplete = False
            for forecast_hours in self.forecast_hours:
                b_inf = forecast_hours[0]
                b_sup = forecast_hours[1]
                
                interval_df = current_group.loc[current_group.lower_bound.astype('int32').between(b_inf,b_sup, inclusive='both')]

                if interval_df.empty:
                    interval_df = current_group.loc[current_group.upper_bound.astype('int32').between(b_inf,b_sup, inclusive='both')]
                    if interval_df.empty:
                        logging.warning(f'No data found for interval: {int(b_inf/3600)} @ {int(b_sup/3600)}')
                        incomplete = True
                        break
                
                res_df = self.process(current_group, interval_df, b_inf, b_sup)

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
        
                interval_df = current_group.loc[current_group.forecast_hour.dt.total_seconds().astype('int32').between(b_inf,b_sup, inclusive='both')]

                if interval_df.empty:
                    logging.warning(f'No data found for interval: {int(b_inf/3600)} @ {int(b_sup/3600)}')
                    incomplete = True
                    break
                
                res_df = self.process(current_group, interval_df, b_inf, b_sup)

                diffs.append(res_df)

            if not incomplete:
                for df in diffs:
                    df_list.append(df)


        return final_results(df_list, TimeIntervalMinMaxError, self.meta_df)

    def process(self, current_group, interval_df, b_inf, b_sup):
        arr3d = da.stack(interval_df['d'])
        results = []
        if self.min:
            # set new ip2, ip3 and npas
            nomvar_min = current_group.iloc[0].nomvar_min
            min_df = create_result_container(current_group, b_inf, b_sup, nomvar_min)
            min_df.at[0, 'd'] =  np.min(arr3d, axis=0)
            results.append(min_df)
        if self.max:    
            # set new ip2, ip3 and npas
            nomvar_max = current_group.iloc[0].nomvar_max
            max_df = create_result_container(current_group, b_inf, b_sup, nomvar_max)
            max_df.at[0, 'd'] =  np.max(arr3d, axis=0)
            results.append(max_df)

        res_df = pd.concat(results, ignore_index=True)

        return res_df

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=TimeIntervalMinMax.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--fieldName',required=True,type=str,dest='nomvar', help="List of field names.")
        parser.add_argument('--interval',type=str, help="List of each time range used for the minimum/maximum calculation")
        parser.add_argument('--rangeForecastHour',required=True,type=str,dest='forecast_hour_range', help="List of time ranges in hours.")
        parser.add_argument('--step',type=str, help="List of the time steps in hours between successive start times within each time range.")
        parser.add_argument('--outputFieldNameMax',type=str,dest='nomvar_max',help="List of names of maximum field.")
        parser.add_argument('--outputFieldNameMin',type=str,dest='nomvar_min',help="List of names if minimum fields.")
        parser.add_argument('--type',type=str,required=True,choices=["MIN","MAX","BOTH"], help="Calculation of minimum and/or maximum.")

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg['type'] == "MIN":
            parsed_arg['min'] = True
        elif parsed_arg['type'] == "MAX":
            parsed_arg['max'] = True
        else:
            parsed_arg['min'] = True
            parsed_arg['max'] = True

        if parsed_arg['interval'] is not None:
            parsed_arg['interval'] = apply_lambda_to_list(parsed_arg['interval'].split(','), lambda a: convert_time(a))
        if parsed_arg['step'] is not None:
            parsed_arg['step'] = apply_lambda_to_list(parsed_arg['step'].split(','), lambda a: convert_time(a))
        parsed_arg['forecast_hour_range'] = apply_lambda_to_list(parsed_arg['forecast_hour_range'].split(','), lambda a: convert_time_range(a))

        parsed_arg['nomvar'] = parsed_arg['nomvar'].split(',')
        apply_lambda_to_list(parsed_arg['nomvar'],lambda a : validate_nomvar(a,"TimeIntervalMinMax",TimeIntervalMinMaxError))

        if parsed_arg['nomvar_max'] is not None:
            parsed_arg['nomvar_max'] = parsed_arg['nomvar_max'].split(',')
            apply_lambda_to_list(parsed_arg['nomvar_max'],lambda a : True if a is None else validate_nomvar(a,"TimeIntervalMinMax",TimeIntervalMinMaxError))
        if parsed_arg['nomvar_min'] is not None:
            parsed_arg['nomvar_min'] = parsed_arg['nomvar_min'].split(',')
            apply_lambda_to_list(parsed_arg['nomvar_min'],lambda a : True if a is None else validate_nomvar(a,"TimeIntervalMinMax",TimeIntervalMinMaxError))

        return parsed_arg

def create_result_container(df, b_inf, b_sup, nomvar):
    deet = df.iloc[0]['deet']
    npas = int(b_sup / deet)
    # npas = int((ip2 * 3600) / deet)

    inter  = fstpy.Interval('ip2', b_inf, b_sup, 10)
    res_df = create_empty_result(df, {'nomvar':nomvar, 'label':'TIMNMX',
                                      'interval':inter, 'npas': npas})
    return res_df

def check_for_negative_values(arr, location):
    if np.any(np.where(arr < 0.,True,False)):
        logging.warning(f"Found a negative value in the {location}! Probable cause is loss of precision when converting to float computational type")
        logging.warning(f'The lowest found negative value was : {to_numpy(np.min(arr))}')


def get_lower_bound(interval):
    return interval.low*3600

def get_upper_bound(interval):
    return interval.high*3600
