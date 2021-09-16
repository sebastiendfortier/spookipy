# -*- coding: utf-8 -*-
import copy
import inspect
import sys
from functools import wraps
from inspect import signature
from typing import Tuple

import fstpy.all as fstpy
import numpy as np
import pandas as pd
import rpnpy.librmn.all as rmn
from pandas.core import groupby
import logging

def initializer(func):
    """
    Automatically assigns the parameters.

    >>> class process:
    ...     @initializer
    ...     def __init__(self, cmd, reachable=False, user='root'):
    ...         pass
    >>> p = process('halt', True)
    >>> p.cmd, p.reachable, p.user
    ('halt', True, 'root')
    """
    names, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(func)
    #names, varargs, keywords, defaults = inspect.getfullargspec(func)

    @wraps(func)
    def wrapper(self, *args, **kargs):
        for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
            setattr(self, name, arg)

        for name, default in zip(reversed(names), reversed(defaults)):
            if not hasattr(self, name):
                setattr(self, name, default)

        func(self, *args, **kargs)

    return wrapper

class DependencyError(Exception):
    pass

class LevelIntersectionError(Exception):
    pass

def get_plugin_dependencies(df:pd.DataFrame, plugin_params:dict=None, plugin_mandatory_dependencies:dict=None,throw_error=True) -> pd.DataFrame:
    """Searches for specified dependency in a dataframe. If a plugin can generate the dependency, the plugin params will be applied if not None.
    computable_dependencies = {  
        'RE':WindChill,   
        'TTI':TotalTotalsIndex,  
        'HMX':Humidex,  
        'KI':GeorgeKIndex,  
        'CORP':CoriolisParameter,  
        'CLD':CloudFractionDiagnostic,  
        'UV':WindModulus,  
        'PX':Pressure,  
        'ES':DewPointDepression,  
        'HR':HumidityRelative,  
        'HU':HumiditySpecific,  
        'TD':TemperatureDewPoint,  
        'SVP':SaturationVapourPressure,  
        'VPPR':VapourPressure,  
        'QV':WaterVapourMixingRatio  
        }

    :param df: dataframe to search in
    :type df: pd.DataFrame
    :param plugin_params: parameters to pass to plugin, defaults to None
    :type plugin_params: dict, optional
    :param plugin_mandatory_dependencies: dependencies to find, defaults to None
    :type plugin_mandatory_dependencies: dict, optional
    :param throw_error: raises an error on dependency not found, defaults to True
    :type throw_error: bool, optional
    :raises DependencyError: raised Exception if no dependency is found
    :return: dataframe of results
    :rtype: pd.DataFrame
    """
    from .cloudfractiondiagnostic.cloudfractiondiagnostic import \
        CloudFractionDiagnostic
    from .coriolisparameter.coriolisparameter import CoriolisParameter
    from .dewpointdepression.dewpointdepression import DewPointDepression
    from .georgekindex.georgekindex import GeorgeKIndex
    from .humidex.humidex import Humidex
    from .humidityrelative.humidityrelative import HumidityRelative
    from .humidityspecific.humidityspecific import HumiditySpecific
    from .pressure.pressure import Pressure
    from .saturationvapourpressure.saturationvapourpressure import \
        SaturationVapourPressure
    from .temperaturedewpoint.temperaturedewpoint import TemperatureDewPoint
    from .totaltotalsindex.totaltotalsindex import TotalTotalsIndex
    from .vapourpressure.vapourpressure import VapourPressure
    from .watervapourmixingratio.watervapourmixingratio import \
        WaterVapourMixingRatio
    from .windchill.windchill import WindChill
    from .windmodulus.windmodulus import WindModulus
    # dependencies that can be computer according to the nomvar
    computable_dependencies = {
        'RE':WindChill,
        'TTI':TotalTotalsIndex,
        'HMX':Humidex,
        'KI':GeorgeKIndex,
        'CORP':CoriolisParameter,
        'CLD':CloudFractionDiagnostic,
        'UV':WindModulus,
        'PX':Pressure,
        'ES':DewPointDepression,
        'HR':HumidityRelative,
        'HU':HumiditySpecific,
        'TD':TemperatureDewPoint,
        'SVP':SaturationVapourPressure,
        'VPPR':VapourPressure,
        'QV':WaterVapourMixingRatio
        }
    df_list = []
    # copy the dependencies dict for modification
    pdependencies = copy.deepcopy(plugin_mandatory_dependencies)
    # print('before\n',df[['nomvar','unit','level','ip1_pkind']].to_string())
    # print(plugin_mandatory_dependencies)

    # for each nomvar or label
    for label,desc in pdependencies.items():
        if 'nomvar' in desc.keys():
            nomvar = desc['nomvar']
        else:
            nomvar = label
        # plugin_params = desc.pop('plugin_params') if 'plugin_params' in desc.keys() else None
        # print(f' for {nomvar}',desc)

        # check if select_only is specified, if not the dependency can be computed
        select_only = desc.pop('select_only') if 'select_only' in desc.keys() else False

        # print(f' for {nomvar} select_only:',select_only)

        # if the dependency is computable, try and compute it
        df = compute_dependency(nomvar, computable_dependencies, df, select_only, plugin_params)
            # print('after\n',df[['nomvar','unit','level','ip1_pkind']].to_string())
        # print(f'selecting - {nomvar}')
        # print(df[list(desc)])
        # print(pd.Series(desc))
        #recipe, query with dict

        # find rows that match desc
        tmp_df = df.loc[(df[list(desc)] == pd.Series(desc)).all(axis=1)]

        # if nothing was found
        if tmp_df.empty:
            if throw_error:
                raise DependencyError(f'{plugin_mandatory_dependencies[nomvar]} not found!')
            else:
                return pd.DataFrame(dtype=object)

        # keep found results
        df_list.append(tmp_df)

    res_df = pd.concat(df_list,ignore_index=True)
    # print('res_df\n\n',res_df)
    return res_df

def compute_dependency(nomvar:str, computable_dependencies:dict, df:pd.DataFrame, select_only:bool, plugin_params:dict) -> pd.DataFrame:
    """IF possible, computes a dempendency from a plugin

    :param nomvar: nomvar used to identify the plugin in the dictionnary of computable_dependencies
    :type nomvar: str
    :param computable_dependencies: dictionnary of nomvar:plugin name associations
    :type computable_dependencies: dict
    :param df: dataframe to add results to
    :type df: pd.Dataframe
    :param select_only: if True, will not compute the dependency
    :type select_only: bool
    :param plugin_params: parameters to pass to plugin
    :type plugin_params: dict
    :return: results dataframe
    :rtype: pd.DataFrame
    """
    if (nomvar in computable_dependencies.keys()) and (df.loc[df.nomvar==nomvar].empty) and (select_only==False):

        # get the correcponding plugin instance
        plugin = computable_dependencies[nomvar]

        #  get the plugins parameter signature
        sig = signature(plugin)
        function_keys = []
        for param in sig.parameters:
            function_keys.append(param)
        # print(function_keys)
        # print(f'computing - {nomvar}')

        # run the plugin without parameters
        if plugin_params is None:
            # print('plugin_params is None')
            tmp_df = plugin(df).compute()
        # run the plugin with parameters
        else:
            # print('plugin_params is not None')
            # check if plugin has mathing parameters to the ones defined in plugin_params
            if set(plugin_params.keys()).issubset(function_keys):
                # print('call plugin with params')
                # call plugin with params
                tmp_df = plugin(df,**plugin_params).compute()
            else:
                # print('call plugin without params')
                # call plugin without params
                tmp_df = plugin(df).compute()
        # print('plugin result\n',tmp_df)
        # add computed results to current dataframe
        df = pd.concat([df,tmp_df],ignore_index=True)
    return df

def get_existing_result(df:pd.DataFrame, plugin_result_specifications:dict) -> pd.DataFrame:
    """Looks for the plugin_result_specifications corresponding rows in a dataframe and returns them if found

    :param df: dataframe to look into
    :type df: pd.DataFrame
    :param plugin_result_specifications: column descriptions to look for when searchin in a dataframe
    :type plugin_result_specifications: dict
    :return: if rows are found, returns the corresponding dataframe rows, else it returns an empty dataframe
    :rtype: pd.DataFrame
    """
    df_list = []
    for _,spec in plugin_result_specifications.items():
        res_df = df.loc[(df.nomvar==spec['nomvar']) & (df.unit==spec['unit'])].reset_index(drop=True)

        if not res_df.empty:
            df_list.append(res_df)
        else:
            break
    if len(df_list)==len(plugin_result_specifications):
        return pd.concat(df_list,ignore_index=True)
    else:
        return pd.DataFrame(dtype='object')

def get_intersecting_levels(df:pd.DataFrame, plugin_mandatory_dependencies:dict) -> pd.DataFrame:
    """Gets the records of all intersecting levels for nomvars in list.
    if TT,UU and VV are in the list, the output dataframe will contain all 3
    varaibles at all the intersectiong levels between the 3 variables

    :param df: input dataframe
    :type df: pd.DataFrame
    :param plugin_mandatory_dependencies: dict with of nomvars as keys
    :type nomvars: dict
    :raises LevelIntersectionError: if a problem occurs this exception will be raised
    :return: dataframe subset
    :rtype: pd.DataFrame
    """
    #logger.debug('1',df[['nomvar','surface','level','ip1_kind']])
    if len(plugin_mandatory_dependencies)<=1:
        # print('get_intersecting_levels - not enough nomvars to process')
        raise LevelIntersectionError('Not enough nomvars to process')

    first_df = df.loc[df.nomvar==list(plugin_mandatory_dependencies.keys())[0]]

    if df.empty:
        # print('get_intersecting_levels - no records to intersect')
        raise LevelIntersectionError('No records to intersect')

    common_levels = set(first_df.ip1.unique())

    for nomvar,_ in plugin_mandatory_dependencies.items():
        curr_df = df.loc[df.nomvar==nomvar]
        levels = set(curr_df.ip1.unique())
        common_levels = common_levels.intersection(levels)

    common_levels = list(common_levels)
    # print('(nomvar in %s) and (ip1 in %s)'%(nomvars,common_levels))
    nomvars = list(plugin_mandatory_dependencies.keys())


    res_df = df.loc[(df.nomvar.isin(nomvars)) & (df.ip1.isin(common_levels))].drop_duplicates(subset=['nomvar','typvar','etiket','ni','nj','nk','dateo','ip1','ip2','ip3','deet','npas','ig1','ig2','ig3','ig4'])
        # print('query_res_df\n',query_res_df[['nomvar','typvar','etiket','ni','nj','nk','dateo','ip1','ip2','ip3','grid']].to_string(),len(query_res_df.index))
        # df_list.append(query_res_df)

    # res_df = pd.concat(df_list,ignore_index=True)
    if 'level' not in res_df.columns:
        res_df = fstpy.add_columns(res_df,True, columns=['ip_info'])
    res_df = res_df.sort_values(by='level',ascending=res_df.ascending.unique()[0])
    return res_df


def validate_nomvar(nomvar:str, caller_class:str, error_class:type):
    """Check that a nomvar has between 2 and 4 characters

    :param nomvar: nomvar string
    :type nomvar: str
    :param caller_class: a string that indicates the name of the caller class or method
    :type caller_class: str
    :param error_class: The exception to throw if nomvar is not 4 characters long
    :type error_class: Exception
    :raises error_class: The class of the exception
    """
    if nomvar is None:
        return
    if len(nomvar) < 2:
        raise error_class(caller_class + ' - min 2 char for nomvar')
    if len(nomvar) > 4:
        raise error_class(caller_class + ' - max 4 char for nomvar')

def remove_load_data_info(df):
    #make sure load_data does not execute (does nothing)
    df.loc[:,'file_modification_time'] = None
    df.loc[:,'path'] = None
    df.loc[:,'key'] = ''
    return df


def create_empty_result(df:pd.DataFrame, plugin_result_specifications:dict,all_rows:bool=False) -> pd.DataFrame:
    """Creates a one row dataframe from the model dataframe, id all_rows is True, then copies the entire dataframe.
    The columns in the plugin_result_specifications dict will be modified accordingly.

    :param df: Model dataframe to copy from
    :type df: pd.DataFrame
    :param plugin_result_specifications: a dictionnary of column values to change. ex to change nomvar the dict must contain {'nomvar':'TT'}
    :type plugin_result_specifications: dict
    :param all_rows: if True, will make a copy of the whole dataframe instead of one row, defaults to False
    :type all_rows: bool, optional
    :return: New dataframe modeled on df, sorted by level, if all_rows is True, all rows will be copied instead of one and column values will be changed according to plugin_result_specifications
    :rtype: pd.DataFrame
    """
    if df.empty:
        logging.warning('cant create, model dataframe empty')

    if all_rows:
        res_df = df.copy(deep=True)
    else:
        res_df = df.iloc[0].to_dict()
        res_df = pd.DataFrame([res_df])

    for k,v in plugin_result_specifications.items():
        if (v != '') and (k in res_df.columns):
            res_df.loc[:,k] = v

    if 'level' not in res_df.columns:
        res_df = fstpy.add_columns(res_df,True, columns=['ip_info'])

    res_df = res_df.sort_values(by=['level'],ascending=res_df.ascending.unique()[0])

    return res_df

def get_3d_array(df) -> np.ndarray:
    for i in df.index:
        df.at[i,'d'] = df.at[i,'d'].flatten()
    arr_3d = np.stack(df['d'].to_list())
    return arr_3d

def existing_results(plugin_name:str,df:pd.DataFrame,meta_df:pd.DataFrame) -> pd.DataFrame:
    """Returns a dataframe of the existing results that have been found

    :param plugin_name: Display plugin name for logging
    :type plugin_name: str
    :param df: existing results dataframe
    :type df: pd.DataFrame
    :param meta_df: meta data dataframe
    :type meta_df: pd.DataFrame
    :return: concatenated dataframe of existing results ans meta data with its data loaded
    :rtype: pd.DataFrame
    """
    logging.info(''.join([plugin_name,' - found results']))
    df = fstpy.load_data(df)
    meta_df = fstpy.load_data(meta_df)
    res_df = pd.concat([meta_df,df],ignore_index=True)
    res_df  = remove_load_data_info(res_df)
    return res_df

def final_results(df_list:"list[pd.DataFrame]",error_class:'type',meta_df:pd.DataFrame) -> pd.DataFrame:
    """Returns the final results dataframe, created from the list of dataframes and the meta data

    :param df_list: list of dataframes, one per grouping method in the plugin
    :type df_list: list[pd.DataFrame]
    :param error_class: Exception to raise if list is empty
    :type error_class: Exception
    :param meta_df: meta data dataframe
    :type meta_df: pd.DataFrame
    :raises error_class: error class to raise
    :return: clean and sorted resulting dataframe
    :rtype: pd.DataFrame
    """
    new_list = []
    for df in df_list:
        if not df.empty:
            new_list.append(df)

    if not len(new_list):
        raise error_class('No results were produced')

    meta_df = fstpy.load_data(meta_df)

    new_list.append(meta_df)
    # merge all results together
    res_df = pd.concat(new_list,ignore_index=True)

    res_df = remove_load_data_info(res_df)

    res_df = fstpy.metadata_cleanup(res_df)

    return res_df



def convip(df:pd.DataFrame,style:int=rmn.CONVIP_ENCODE) -> pd.DataFrame:
    """Converts ip1 column of dataframe from new style ips to old style and vice versa

    :param df: A DataFrame
    :type df: pd.DataFrame
    :param style: either rmn.CONVIP_ENCODE or rmn.CONVIP_ENCODE_OLD, defaults to rmn.CONVIP_ENCODE
    :type style: int, optional
    :return: modified Dataframe
    :rtype: pd.DataFrame
    """
    def convertip(ip,style):
        (val, kind) = rmn.convertIp(rmn.CONVIP_DECODE, int(ip))
        if kind != -1:
            return rmn.convertIp(int(style), val, kind)
    vconvertip = np.vectorize(convertip)
    df.loc[~df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]),'ip1'] = vconvertip(df.loc[~df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]),'ip1'].values,style)

    return df

def get_from_dataframe(df:pd.DataFrame, nomvar:str) -> pd.DataFrame:
    """Get a specific variable from a DataFrame and clears the index and sorts the levels according to kind

    :param df: A DataFrame
    :type df: pd.DataFrame
    :param nomvar: nomvar of variable to get
    :type nomvar: str
    :return: Dataframe containing only the requested variable or an empty DataFrame if variable not found
    :rtype: pd.DataFrame
    """
    res_df = df.loc[df.nomvar==nomvar]
    if not(res_df.empty):
        return res_df.sort_values(by=['level'],ascending=res_df.ascending.unique()[0]).reset_index(drop=True)

    return pd.DataFrame(dtype=object)

def find_matching_dependency_option(df:pd.DataFrame,plugin_params:dict,plugin_mandatory_dependencies:'list[dict]',intersect_levels:bool) -> 'Tuple[pd.DataFrame,int]':
    """Searches for dependencies in a dataframe

    :param df: data dataframe to search in
    :type df: pd.DataFrame
    :param plugin_params: plugin parameters to pass on
    :type plugin_params: dict
    :param plugin_mandatory_dependencies: list of dependencies (dictionnaries)
    :type plugin_mandatory_dependencies: list
    :param intersect_levels: finds the intersecting levels for dependencies
    :type intersect_levels: bool, default False
    :return: found dataframe and its index in the list of dependencies or an empty dataframe if nothing was found
    :rtype: tuple
    """
    for i in range(len(plugin_mandatory_dependencies)):
        # print(i,len(plugin_mandatory_dependencies),plugin_mandatory_dependencies[i],(False if i+1 < len(plugin_mandatory_dependencies) else True))
        # dependencies_df = get_plugin_dependencies(df,plugin_params,plugin_mandatory_dependencies[i],throw_error=(False if i+1 < len(plugin_mandatory_dependencies) else True))
        dependencies_df = get_plugin_dependencies(df,plugin_params,plugin_mandatory_dependencies[i],throw_error=False)
        option=i
        if not (dependencies_df.empty):
            logging.info('Found following depency: ')
            for k,v in plugin_mandatory_dependencies[i].items():
                logging.info(f'{k}:{v}')
            if intersect_levels and len(plugin_mandatory_dependencies[i]) > 1:
                dependencies_df = get_intersecting_levels(dependencies_df,plugin_mandatory_dependencies[i])
                if dependencies_df.empty:
                    logging.warning('Intersecting levels requested and not found for this dataframe')
                    return pd.DataFrame(dtype=object), 0
                else:    
                    logging.info('Intersecting levels requested and found')
                
            return dependencies_df, option
            
    return pd.DataFrame(dtype=object), 0

def get_dependencies(groups:groupby.generic.DataFrameGroupBy,meta_df:pd.DataFrame,plugin_name:str,plugin_mandatory_dependencies:'list[dict]',plugin_params:dict=None,intersect_levels:bool=False) -> 'list[Tuple[pd.DataFrame,int]]':
    """For each provided grouping, tries to find the correcponding dependencies

    :param groups: A DataFrameGroupBy object obtained from the groupby method
    :type groups: DataFrameGroupBy
    :param meta_df: meta data dataframe
    :type meta_df: pd.DataFrame
    :param plugin_name: plugin name for logging
    :type plugin_name: str
    :param plugin_mandatory_dependencies: column descriptions to look for in each group
    :type plugin_mandatory_dependencies: list[dict]
    :param plugin_params: plugin paramaters to pass on
    :type plugin_params: dict
    :param intersect_levels: finds the intersecting levels for dependencies
    :type intersect_levels: bool, default False
    :raises DependencyError: if no dependencies are found, raises this error
    :return: list of matching dataframes
    :rtype: list[pd.DataFrame]
    """
    df_list = []
    for _,current_group in groups:
        logging.info(f'{plugin_name} - Checking dependencies')
        dependencies_df, option = find_matching_dependency_option(pd.concat([current_group,meta_df],ignore_index=True),plugin_params,plugin_mandatory_dependencies,intersect_levels)
        if dependencies_df.empty:
            logging.warning(f'{plugin_name} - No matching dependencies found for this group \n%s'%current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']])
            continue
        else:
            logging.info(f'{plugin_name} - Matching dependencies found for this group \n%s'%current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']])
        df_list.append((dependencies_df,option))

    if not df_list:
        raise DependencyError(f'{plugin_name} - No matching dependencies found')
    return df_list
