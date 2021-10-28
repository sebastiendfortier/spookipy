# -*- coding: utf-8 -*-
import datetime
import logging

import dask.array as da
import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, final_results, initializer, to_numpy,
                     validate_nomvar)


class TimeIntervalMinMaxError(Exception):
    pass


class TimeIntervalMinMax(Plugin):

    @initializer
    def __init__(self, df: pd.DataFrame, nomvar=None, min=False, max=False, forecast_hour_range=None, interval=None, step=None, nomvar_min='MIN', nomvar_max='MAX'):
        """ Computes the time interval difference between groups of begin@end forecast_hour
        :param df: Input dataframe
        :type df: pd.DataFrame
        :param nomvar: Target nomvar of the difference
        :type nomvar: str or list of str
        :param forecast_hour_range: 
        :type forecast_hour_range: datetime.timedelta or list of datetime.timedelta
        :param interval:List of the time intervals between inputs within each time range.
        :type interval:datetime.timedelta or list of datetime.timedelta
        :param step: List of the time steps between successive start times within each time range
        :type step: datetime.timedelta or list of datetime.timedelta
        """

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise TimeIntervalMinMaxError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(self.df, ['forecast_hour'])

        if (self.nomvar is None) or (self.forecast_hour_range is None):
            raise TimeIntervalMinMaxError(
                'One of the mandatory parameter (nomvar, forecast_hour_range, interval, step) is None')

        self.nomvar = validate_list_of_str(self.nomvar)
        l_nomvar = len(self.nomvar)

        
        validate_nomvar(
            self.nomvar_min,
            'TimeIntervalMinMax',
            TimeIntervalMinMaxError)

        validate_nomvar(
            self.nomvar_max,
            'TimeIntervalMinMax',
            TimeIntervalMinMaxError)

        if (not self.min) and (not self.max):
            self.min = True
            self.max = True



        self.forecast_hour_range = validate_list_of_tuples_of_times(self.forecast_hour_range)
        l_fcast = len(self.forecast_hour_range)

        if self.step is None:
           self.step = [datetime.timedelta(hours=i)  for i in range(l_fcast)]
        else:
            self.step = validate_list_of_times(self.step)

        if self.interval is None:
           self.interval = [(i[1] - i[0])  for i in self.forecast_hour_range]
        else:
            self.interval = validate_list_of_times(self.interval)   

        l_int = len(self.interval)
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


        self.groups_without_interval = self.df_without_intervals.groupby(['grid', 'nomvar'])
        self.groups_with_interval = self.df_with_intervals.groupby(['grid', 'nomvar'])


    def compute(self) -> pd.DataFrame:
        logging.info('TimeIntervalMinMax - compute\n')

        self.list_of_forecast_hours()

        print( self.forecast_hours)
        if len(self.forecast_hours) == 0:
            raise TimeIntervalMinMaxError('Unable to calculate intervals with provided parameters')

        # print(self.groups)
        df_list = []

        for _, current_group in self.groups_with_interval:
            # print(f"\ncurrent_group\n {current_group[['nomvar','typvar','etiket','ni','nj','nk', 'dateo', 'ip1','ip2','ip3','deet','npas', 'datev', 'forecast_hour', 'interval']].to_string()}")
            
            current_group['lower_bound'] = current_group['interval'].map(get_lower_bound)
            current_group['upper_bound'] = current_group['interval'].map(get_upper_bound)
            # print(f"\nlower\n {current_group.lower_bound.astype('int32').sort_values()}\n")
            # print(f"\nupper\n {current_group.upper_bound.astype('int32').sort_values()}\n")
            
            diffs = []
            incomplete = False
            for forecast_hours in self.forecast_hours:
                b_inf = forecast_hours[0]
                b_sup = forecast_hours[1]
                # print(b_inf,b_sup)    
                
                end_df = current_group.loc[(current_group.lower_bound.astype('int32') == b_inf)]
                begin_df = current_group.loc[(current_group.lower_bound.astype('int32') == b_sup)]

                if begin_df.empty or end_df.empty:
                    # print('not found in lower bound')
                    begin_df = current_group.loc[(current_group.upper_bound.astype('int32') == b_inf)]
                    end_df = current_group.loc[(current_group.upper_bound.astype('int32') == b_sup)]
                    if begin_df.empty or end_df.empty:
                        # print('not found in upper bound')
                        logging.warning(f'No data found for interval: {int(b_inf/3600)} @ {int(b_sup/3600)}')
                        incomplete = True
                        break
                # else:
                #     logging.info('found matches')

                res_df = self.process(current_group, b_inf, b_sup, begin_df, end_df)

                diffs.append(res_df)

            if not incomplete:
                for df in diffs:
                    df.drop(columns=['lower_bound','upper_bound'])
                    df['interval'] = None
                    df_list.append(df)

        for _, current_group in self.groups_without_interval:
            # print(current_group[['nomvar','typvar','etiket','ni','nj','nk', 'dateo', 'ip1','ip2','ip3','deet','npas', 'datev', 'forecast_hour', 'interval']].to_string())
            # print(f"{current_group.forecast_hour.dt.total_seconds().astype('int32').sort_values()}\n")
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



        return final_results(df_list, TimeIntervalMinMaxError, self.meta_df)

    def process(self, current_group, b_inf, b_sup, begin_df, end_df):
        begin_arr = begin_df.iloc[0]['d']
        end_arr = end_df.iloc[0]['d']    

        # set new ip2, ip3 and npas
        min_df = create_result_container(current_group, b_inf, b_sup)
        max_df = create_result_container(current_group, b_inf, b_sup)

        arr3d = da.stack([end_arr,begin_arr])
        results = []
        if self.min:
            min_df.at[0, 'd'] =  np.min(arr3d, axis=0)
            results.append(min_df)
        if self.max:    
            max_df.at[0, 'd'] =  np.max(arr3d, axis=0)
            results.append(max_df)

        res_df = pd.concat(results, ignore_index=True)

        return res_df


    # def check_type_of_params(self):
    #     # make sure that nomvar is a list of str
    #     self.nomvar = validate_list_of_str(self.nomvar)

    #     # make sure that interval is a list of datetime.timedelta
    #     self.interval = validate_list_of_times(self.interval)

    #     # make sure that step is a list of datetime.timedelta
    #     self.step = validate_list_of_times(self.step)

    #     # make sure that forecast_hour_range is a list of tuple of 2 datetime.timedelta
    #     self.forecast_hour_range = validate_list_of_tuples_of_times(self.forecast_hour_range)

    def bornes(self):
        self.borne_inf = []
        self.borne_sup = []
        for i in range(len(self.forecast_hour_range)):
            self.borne_inf.append(self.forecast_hour_range[i][0])
            self.borne_sup.append(self.forecast_hour_range[i][1])

    def list_of_forecast_hours(self):
        self.bornes()
        self.forecast_hours = []
        for i in range(len(self.interval)):
            j = self.borne_inf[i].total_seconds()  
            while int(j + self.interval[i].total_seconds()) <=  int(self.borne_sup[i].total_seconds()):
                b_inf = int(j)
                b_sup = int(j + self.interval[i].total_seconds())
                self.forecast_hours.append((b_inf,b_sup))
                # print('binf\tb_sup')
                # print(f'{int(b_inf/3600)}\t{int(b_sup/3600)}')
                j = j + self.step[i].total_seconds()

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

def validate_list_of_str(param):
    if isinstance(param, str):
        param = [param]
    if not isinstance(param, list):
        raise TimeIntervalMinMaxError(f'{str(param)} needs to be a list of str')
    for n in param:
        if not isinstance(n, str):
            raise TimeIntervalMinMaxError(f'{str(param)} needs to be a list of str')
    return param        


def validate_list_of_times(param):
    if isinstance(param, datetime.timedelta):
        param = [param]
    if not isinstance(param, list):
        raise TimeIntervalMinMaxError(f'{str(param)} needs to be a list of datetime.timedelta')
    for n in param:
        if not isinstance(n, datetime.timedelta):
            raise TimeIntervalMinMaxError(f'{str(param)} needs to be a list of datetime.timedelta')
        if n == datetime.timedelta():
            raise TimeIntervalMinMaxError('value is not valid') 
    return param

def validate_list_of_tuples_of_times(param):
    if isinstance(param, tuple) and len(param) == 2:
        param = [param]
    if not isinstance(param, list):
        raise TimeIntervalMinMaxError(f'{str(param)} is not a list, {str(param)} needs to be a list of tuple of 2 datetime.timedelta')
    for n in param:
        if not isinstance(n, tuple) or len(n) != 2:
            raise TimeIntervalMinMaxError(
                f'{str(param)} does not contain tuple of 2 elements, {str(param)} needs to be a list of tuple of 2 datetime.timedelta')
        if not isinstance(n[0], datetime.timedelta) or not isinstance(n[1], datetime.timedelta):
            raise TimeIntervalMinMaxError(
                f'{str(param)} needs to be a list of tuple of 2 datetime.timedelta')
        if n[0] >= n[1]:
            raise TimeIntervalMinMaxError(f'{str(param)} value is not valid')  
    return param        

def get_lower_bound(interval):
    return interval.low*3600

def get_upper_bound(interval):
    return interval.high*3600    
