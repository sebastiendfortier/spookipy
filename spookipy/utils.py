# -*- coding: utf-8 -*-
import copy
import datetime
import inspect
import logging
import math
from functools import wraps
from inspect import signature
from typing import Tuple, Final
import operator
import re

import dask.array as da
import fstpy
from   fstpy.utils import vectorize
from   fstpy.std_vgrid import vctype_dict
from   fstpy.dataframe_utils import convert_cols_to_boolean_dtype, safe_concatenate
import numpy as np
import pandas as pd
import rpnpy.librmn.all as rmn
from   pandas.core import groupby
import warnings
    
class DataframeColumnError(Exception):
    pass
class DependencyError(Exception):
    pass
class LevelIntersectionError(Exception):
    pass

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
    names, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(
        func)
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

def explicit_params_checker(func):
    varnames = inspect.getfullargspec(func)[0]
    @wraps(func)
    def wrapper(self, *args, **kargs):
        setattr(self, 'explicit_params', set(list(varnames[:len(args)]) + list(kargs.keys())))
        return func(self, *args, **kargs)
    return wrapper

def get_computable_dependencies():
    import sys
    import spookipy
    spookipy_members = inspect.getmembers(sys.modules["spookipy"], inspect.isclass)
    plugin_dict ={p[1].computable_plugin:p[1] for p in spookipy_members if issubclass(p[1],spookipy.Plugin) and p[1].computable_plugin is not None}
    return plugin_dict

def get_plugin_dependencies(
        df: pd.DataFrame,
        plugin_params: dict = None,
        plugin_mandatory_dependencies: dict = None,
        throw_error=True) -> pd.DataFrame:
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
        'VT':TemperatureVirtual,
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
    # dependencies that can be computer according to the nomvar
    computable_dependencies = get_computable_dependencies()

    df_list = []
    # copy the dependencies dict for modification
    pdependencies = copy.deepcopy(plugin_mandatory_dependencies)
    # print('before\n',df[['nomvar','unit','level','ip1_pkind']].to_string())
    # print(plugin_mandatory_dependencies)

    # for each nomvar or label
    for label, desc in pdependencies.items():
        if 'nomvar' in desc.keys():
            nomvar = desc['nomvar']
        else:
            nomvar = label
        # plugin_params = desc.pop('plugin_params') if 'plugin_params' in desc.keys() else None
        # print(f' for {nomvar}',desc)

        # check if select_only is specified, if not the dependency can be
        # computed
        select_only = desc.pop('select_only') if 'select_only' in desc.keys() else False

        # if the dependency is computable, try and compute it
        df = compute_dependency(
            nomvar,
            computable_dependencies,
            df,
            select_only,
            plugin_params)
        # print('after\n',df[['nomvar','unit','level','ip1_pkind']].to_string())
        # print(f'selecting - {nomvar}')
        # print(df[list(desc)])
        # print(pd.Series(desc))
        # recipe, query with dict

        # find rows that match desc
        destination_unit = desc.pop('unit') if 'unit' in desc.keys() else None

        tmp_df = df.loc[(df[list(desc)] == pd.Series(desc)).all(axis=1)]

        # if nothing was found
        if tmp_df.empty:
            if throw_error:
                raise DependencyError(f'{plugin_mandatory_dependencies[nomvar]} not found!')
            else:
                return pd.DataFrame(dtype=object)

        else:
            # do the unit conversion
            if not (destination_unit is None):
                tmp_df = fstpy.unit_convert(tmp_df, destination_unit)

        # keep found results
        df_list.append(tmp_df)

    res_df = safe_concatenate(df_list)

    return res_df

def compute_dependency(
        nomvar: str,
        computable_dependencies: dict,
        df: pd.DataFrame,
        select_only: bool,
        plugin_params: dict) -> pd.DataFrame:
    """IF possible, computes a dependency from a plugin

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
    logger = logging.getLogger('root') 
    if not(df.loc[df.nomvar == nomvar].empty):
        logging.debug(f'\t {nomvar} - Found ')
    elif (nomvar in computable_dependencies.keys()) and (select_only == False):
    # if (nomvar in computable_dependencies.keys()) and (
    #         df.loc[df.nomvar == nomvar].empty) and (select_only == False):

        # get the correcponding plugin instance
        plugin = computable_dependencies[nomvar]

        #  get the plugins parameter signature
        sig = signature(plugin)
        function_keys = []
        for param in sig.parameters:
            function_keys.append(param)

        plugin_params_only_dep_check = {}
        plugin_params_only_dep_check["dependency_check"] = True
        plugin_params_only_dep_check["reduce_df"]        = False
        # run the plugin without parameters but with the bool for the dependency
        if plugin_params is None:
            logging.debug(f'\n 1 - pluginsParams is None ---- {plugin=} {plugin_params_only_dep_check=}\n')
            tmp_df = plugin(df, **plugin_params_only_dep_check).compute()
            
        # run the plugin with parameters
        else:
            # check if plugin has matching parameters to the ones defined in
            # plugin_params
            plugin_params["dependency_check"] = True
            plugin_params["reduce_df"]        = False
            if set(plugin_params.keys()).issubset(function_keys):
                logging.debug(f'\n 2 -  pluginsParams is not None ---- {plugin=} {plugin_params=}\n')
                # call plugin with params
                tmp_df = plugin(df, **plugin_params).compute()
            else:
                logging.debug(f'\n 3- {plugin=} {plugin_params_only_dep_check=} {plugin_params=}\n')
                # call plugin without params
                tmp_df = plugin(df, **plugin_params_only_dep_check).compute()
                
        logging.debug(f'\t Resultats calcules pour {nomvar} ! \n')
        if not tmp_df.empty:
            # Conversion des colonnes a boolean pour eviter warning "object-dtype columns with all-bool values ..."
            tmp_df = convert_cols_to_boolean_dtype(tmp_df)
            if logger.isEnabledFor(logging.DEBUG):
                message = (f' Resultats calcules pour {nomvar}: ')
                logging.debug(f'{print_style_voir(tmp_df, message)}')
        else:
            logging.debug(f'\t Pas de resultats calcules pour {nomvar}  !!! \n')

        # Conversion des colonnes a boolean pour eviter warning "object-dtype columns with all-bool values ..."
        df = convert_cols_to_boolean_dtype(df)
        df = safe_concatenate([df, tmp_df])
    else:
        logging.debug(f'\t Compute_dependency - {nomvar} ne peut etre calcule!  \n\n')

    return df

def get_existing_result(
        df: pd.DataFrame,
        plugin_result_specifications: dict) -> pd.DataFrame:
    """Looks for the plugin_result_specifications corresponding rows in a dataframe and returns them if found

    :param df: dataframe to look into
    :type df: pd.DataFrame
    :param plugin_result_specifications: column descriptions to look for when searchin in a dataframe
    :type plugin_result_specifications: dict
    :return: if rows are found, returns the corresponding dataframe rows, else it returns an empty dataframe
    :rtype: pd.DataFrame
    """
    df_list = []
    for _, spec in plugin_result_specifications.items():
        res_df = df.loc[(df.nomvar == spec['nomvar']) & (
            df.unit == spec['unit'])].reset_index(drop=True)

        if not res_df.empty:
            df_list.append(res_df)
        else:
            break
    if len(df_list) == len(plugin_result_specifications):
        return safe_concatenate(df_list)
    else:
        return pd.DataFrame(dtype='object')

def find_intersecting_levels(df: pd.DataFrame) -> pd.DataFrame:
    """Finds the records of all intersecting levels from a dataframe.

    The input data must be grouped by grid. 

    :param df: input dataframe, must contain the ip_info
    :type df: pd.DataFrame
    :return: dataframe subset
    :rtype: pd.DataFrame
    """

    list_nomvar = df.nomvar.unique()

    # Un seul champ? Pas d'intersection a trouver
    if len(list_nomvar) == 1:
        return df

    res_df = find_common_levels(df, list_nomvar)

    return res_df

def get_intersecting_levels(df: pd.DataFrame,
                            list_nomvar: list) -> pd.DataFrame:
    """Gets the records of all intersecting levels for nomvars in a list from plugin_mandatory_dependency dict.
    The input data must be grouped by grid and ip1_kind info.  
    If TT,UU and VV are in the list, the output dataframe will contain all 3
    variables at all the intersecting levels between the 3 variables

    :param df: input dataframe, must contain the ip_info
    :type df: pd.DataFrame
    :param list_nomvar: list of nomvars 
    :type nomvars: list
    :raises LevelIntersectionError: if a problem occurs this exception will be raised
    :return: dataframe subset
    :rtype: pd.DataFrame
    """
    
    # On recoit la liste des dependances qui se doivent d'etre presentes.
    if df.loc[df.nomvar == list_nomvar[0]].empty:
        raise LevelIntersectionError('No records to intersect')

    res_df = find_common_levels(df, list_nomvar)

    return res_df

def find_common_levels(df: pd.DataFrame,
                       list_nomvar: list,
                       column_to_match: str = 'nomvar') -> pd.DataFrame:
    """Finds all common levels for fields in list_nomvar in the dataframe.

    The input data must be grouped by grid. 

    :param df: input dataframe, must contain the ip_info
    :type df: pd.DataFrame
    :return: dataframe subset
    :rtype: pd.DataFrame
    """

    df.sort_values(by=[column_to_match,'level'])
    first_df           = df.loc[df[column_to_match] == list_nomvar[0]]
    common_levels      = set(first_df.level.unique())

    for nomvar in list_nomvar:
        curr_df        = df.loc[df[column_to_match] == nomvar]
        levels         = set(curr_df.level.unique())
        common_levels  = common_levels.intersection(levels)

    common_levels = list(common_levels)

    df.sort_values(by=[column_to_match,'typvar','level'])
    df['typvar_char1'] = df.apply(lambda row: row['typvar'] if len(row['typvar']) < 2 else row['typvar'][0], axis=1)

    res_df             = df.loc[(df[column_to_match].isin(list_nomvar)) & 
                                (df.level.isin(common_levels))]
    res_df = res_df.drop_duplicates(
                                subset=[
                                        column_to_match, 'typvar_char1','etiket', 'ni', 'nj', 'nk', 'dateo', 
                                        'ip1', 'ip2', 'ip3', 'deet', 'npas', 'ig1', 'ig2', 'ig3', 'ig4'
                                       ])
    
    res_df = res_df.drop(columns=['typvar_char1'])

    if not res_df.empty:
        res_df = res_df.sort_values(by='level',ascending=res_df.ascending.unique()[0])

    return res_df


def validate_list_of_nomvar(nomvar: 'str|list', caller_class: str, error_class: type):
    if isinstance(nomvar, str):
        nomvar = [nomvar]
    if not isinstance(nomvar, list):
        raise error_class(f'{caller_class} - {str(nomvar)} needs to be a list of str')
    for n in nomvar:
        validate_nomvar(n, caller_class, error_class)
    return nomvar   

def validate_nomvar(nomvar: str, caller_class: str, error_class: type):
    """Check that a nomvar has between 2 and 4 characters

    :param nomvar: nomvar string
    :type nomvar: str
    :param caller_class: a string that indicates the name of the caller class or method
    :type caller_class: str
    :param error_class: The exception to throw if nomvar is not 4 characters long
    :type error_class: Exception
    :raises error_class: The class of the exception

    >>> class MyError(Exception):
    ...     pass
    >>> validate_nomvar('TOTO','MyClass',MyError) # doctest: +IGNORE_EXCEPTION_DETAIL
    >>> validate_nomvar('','MyClass',MyError) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    MyError: MyClass - min 2 char for nomvar
    >>> validate_nomvar('T','MyClass',MyError) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    MyError: MyClass - min 2 char for nomvar    
    >>> validate_nomvar('TOTOTO','MyClass',MyError) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    MyError: MyClass - max 4 char for nomvar    
    >>> validate_nomvar(None,'MyClass',MyError) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    MyError: MyClass - nomvar must be a string    
    """
    if not isinstance(nomvar,str):
        raise error_class(caller_class + ' - nomvar must be a string')
    if len(nomvar) < 2:
        raise error_class(caller_class + ' - min 2 char for nomvar')
    if len(nomvar) > 4:
        raise error_class(caller_class + ' - max 4 char for nomvar')


def create_empty_result(df: pd.DataFrame, plugin_result_specifications: dict, all_rows: bool = False) -> pd.DataFrame:
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
        logging.error('\t Cant create, model dataframe empty \n')
        raise DataframeColumnError(f'In create_empty_result - Model dataframe is empty!')

    # df = df.drop('d', axis=1)
    if all_rows:
        res_df = copy.deepcopy(df)
    else:
        res_df = df.iloc[0].to_dict()
        res_df = pd.DataFrame([res_df])

    res_df = fstpy.add_columns(res_df, columns=['etiket'])
    
    # set to default parameters
    res_df['run'] = '__'
    res_df['implementation'] = 'X'
    res_df['etiket_format'] = ''


    for k, v in plugin_result_specifications.items():
        if (k in res_df.columns):
            # Suppression d'un future warning de pandas; dans notre cas, on veut conserver le meme comportement
            # meme avec le nouveau comportement a venir. On encapsule la suppression du warning pour ce cas seulement.
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=FutureWarning)
                res_df.loc[:, k] = v
        else:
            raise DataframeColumnError(f'In create_empty_result - Column "{k}" not found in dataframe!')

    # au lieu de faire un drop des colonnes de flag, il faudrait faire une réduction de colonne
    flag_col = [x for x in ['multiple_modifications','zapped','filtered','interpolated','bounded','unit_converted'] if x in res_df.columns]
    res_df = res_df.drop(flag_col,axis=1)

    # if only one char leave it, if 2 char remove the second unless it's ! (ensemble extra info)
    res_df['typvar'] = res_df.apply(lambda row: row['typvar'] if len(row['typvar']) < 2 or row['typvar'][1] in ['!','@'] else row['typvar'][0], axis=1)

    res_df['etiket'] = res_df.apply(lambda row: fstpy.create_encoded_standard_etiket(
                                                                row['label'], 
                                                                row['run'], 
                                                                row['implementation'], 
                                                                row['ensemble_member'], 
                                                                row['etiket_format'],
                                                                ), axis=1)

    if 'level' not in res_df.columns:
        res_df = fstpy.add_columns(res_df, columns=['ip_info'])

    res_df = res_df.sort_values(
        by=['level'],
        ascending=res_df.ascending.mode()[0]).reset_index(drop=True)

    return res_df

def define_time_interval_infos(df: pd.DataFrame, b_inf: int, b_sup: int):
    """ Creates a dictionnary with values to use for the creation of a result dataframe with 
        a time interval.
    
    :param df: input dataframe
    :type df: pd.DataFrame
    :b_inf: borne inferieure 
    :rtype: int
    :b_sup: borne superieure 
    :rtype: int
    :return: a dictionnary containing the values for the creation of a df with a time interval object
    :rtype: dict
    """
    deet          = df.iloc[0]['deet']
    npas          = int(b_sup / deet)
    b_sup_hour    = b_sup/3600.0
    b_inf_hour    = b_inf/3600.0
    ip2           = int(b_sup_hour)
    ip3           = int(b_sup_hour-b_inf_hour)
    kind          = int(df.iloc[0].ip2_kind)
    forecast_hour = fstpy.get_forecast_hour(deet,npas)

    inter         = fstpy.Interval('ip2', b_inf_hour, b_sup_hour, kind)

    info_inter    = {'ip2': ip2, 'ip3': ip3, 'npas': npas, 'forecast_hour': forecast_hour, 'interval':inter }

    return info_inter

def get_3d_array(df: pd.DataFrame, flatten:bool=False, reverse:bool=False) -> np.ndarray:
    """stacks the arrays of the 'd' row of a dataframe

    :param df: input dataframe
    :type df: pd.DataFrame
    :param flatten: flattens the arrays, defaults to False
    :type flatten: bool, optional
    :param reverse: reverse stacking order, defaults to False
    :type reverse: bool, optional
    :return: a 3d array of the 'd' column
    :rtype: np.ndarray
    """
    if reverse:
        df.reindex(index=df.index[::-1])
    if flatten:    
        for row in df.itertuples():
            df.at[row.Index,'d'] = row.d.flatten()

    arr_3d = np.stack(df['d'].to_list())
    return arr_3d


def existing_results(
        plugin_name: str,
        df: pd.DataFrame,
        meta_df: pd.DataFrame) -> pd.DataFrame:
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
    logging.info(''.join([plugin_name, ' - found results']))

    res_df = safe_concatenate([meta_df, df])

    return res_df


def convip(df: pd.DataFrame, style: int = rmn.CONVIP_ENCODE, ip_str:str='ip1') -> pd.DataFrame:
    """Converts ip1 column of dataframe from new style ips to old style and vice versa

    :param df: A DataFrame
    :type df: pd.DataFrame
    :param style: either rmn.CONVIP_ENCODE or rmn.CONVIP_ENCODE_OLD, defaults to rmn.CONVIP_ENCODE
    :type style: int, optional
    :return: modified Dataframe
    :rtype: pd.DataFrame
    """
    def convertip(ip, style):
        (val, kind) = rmn.convertIp(rmn.CONVIP_DECODE, int(ip))

        if (ip_str == 'ip2'):
            kind = 10
        if kind != -1:
            return rmn.convertIp(int(style), val, kind)

    vconvertip = np.vectorize(convertip)
    df.loc[~df.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"]), ip_str] = vconvertip(
        df.loc[~df.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"]), ip_str].values, style)

    return df

def get_from_dataframe(df: pd.DataFrame, nomvar: str) -> pd.DataFrame:
    """Get a specific variable from a DataFrame and clears the index and sorts the levels according to kind

    :param df: A DataFrame
    :type df: pd.DataFrame
    :param nomvar: nomvar of variable to get
    :type nomvar: str
    :return: Dataframe containing only the requested variable or an empty DataFrame if variable not found
    :rtype: pd.DataFrame
    """
    res_df = df.loc[df.nomvar == nomvar]
    
    if not(res_df.empty):
        if len(res_df.ascending.mode()) > 1 and res_df.vctype.mode()[0] != vctype_dict['HYBRID_5005']:
            raise Exception(f"There's a problem with the ascending column of {nomvar}, there should only be one unique value.")
        return res_df.sort_values(
            by=['level'],
            ascending=res_df.ascending.mode()[0]).reset_index(
            drop=True)

    return pd.DataFrame(dtype=object)

def find_matching_dependency_option(
        df: pd.DataFrame,
        plugin_params: dict,
        plugin_mandatory_dependencies: 'list[dict]',
        intersect_levels: bool) -> 'Tuple[pd.DataFrame,int]':
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
        logging.debug(f'\t (Option {i+1} de {len(plugin_mandatory_dependencies)},{plugin_mandatory_dependencies[i]} ')
        # print(i,len(plugin_mandatory_dependencies),plugin_mandatory_dependencies[i],(False if i+1 < len(plugin_mandatory_dependencies) else True))
        # dependencies_df = get_plugin_dependencies(df,plugin_params,plugin_mandatory_dependencies[i],throw_error=(False if i+1 < len(plugin_mandatory_dependencies) else True))
        dependencies_df = get_plugin_dependencies(
            df, plugin_params, plugin_mandatory_dependencies[i], throw_error=False)
        option = i
        if not (dependencies_df.empty):
            logging.info('\t Found following depency: ')
            for k, v in plugin_mandatory_dependencies[i].items():
                logging.info(f'\t {k}:{v}')
            if intersect_levels and len(plugin_mandatory_dependencies[i]) > 1:
                list_nomvar = [value['nomvar'] for value in plugin_mandatory_dependencies[i].values()]
                dependencies_df = get_intersecting_levels(
                    dependencies_df, list_nomvar)
                if dependencies_df.empty:
                    logging.warning(
                        '\t Intersecting levels requested and not found for this dataframe')
                    return pd.DataFrame(dtype=object), 0
                else:
                    logging.info('\t Intersecting levels requested and found')

            return dependencies_df, option

    return pd.DataFrame(dtype=object), 0


def get_dependencies(
        groups: groupby.generic.DataFrameGroupBy,
        meta_df: pd.DataFrame,
        plugin_name: str,
        plugin_mandatory_dependencies: 'list[dict]',
        plugin_params: dict = None,
        intersect_levels: bool = False, 
        throw_error: bool = True,
        dependency_check = False) -> 'list[Tuple[pd.DataFrame,int]]':
    """For each provided grouping, tries to find the correcponding dependencies
       When intersect_levels is True, the input should have been grouped with ip1_kind
       before the call.

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
    :param throw_error: raises an error on dependency not found, defaults to True
    :type throw_error: bool, optional
    :return: list of matching dataframes
    :rtype: list[pd.DataFrame]
    """

    logger = logging.getLogger('root')  
    df_list = []
    # nb_group = len(groups)
    # print(f'\n Get_dependencies - Nbre groupes = {nb_group}')
    no_groupe = 0

    for _, current_group in groups:

        no_groupe += 1
        logging.debug(f'\t  ************************ Boucle sur les groupes - Groupe no {no_groupe} pour {plugin_name} ************************ \n ')
        logging.info(f'{plugin_name} - Checking dependencies')

        if dependency_check:
            logging.debug(f'\t Pas besoin de cleaner metadata - sous-plugin ! \n\n')
            new_df = safe_concatenate([current_group, meta_df])
            dependencies_df, option = find_matching_dependency_option(new_df, plugin_params, 
                                        plugin_mandatory_dependencies, intersect_levels)
        else:
            new_df= safe_concatenate([current_group, meta_df])
            new_df = fstpy.metadata_cleanup(new_df)
            dependencies_df, option = find_matching_dependency_option(
                                        new_df, plugin_params, 
                                        plugin_mandatory_dependencies, intersect_levels)
        
        if dependencies_df.empty:
            logging.info(f'{plugin_name} - No matching dependencies found for this group \n%s' %
                            current_group[['nomvar', 'typvar', 'etiket', 'dateo', 'ip1_kind', 'grid']])
            if logger.isEnabledFor(logging.DEBUG):
                logging.debug(f'{plugin_name} - {print_style_voir(current_group, " No matching dependencies found for this group: ")}')
            continue
        else:
            logging.info(f'{plugin_name} - Matching dependencies found for this group \n%s' %
                        current_group[['nomvar', 'typvar', 'etiket', 'dateo', 'ip1_kind', 'grid']])
            if logger.isEnabledFor(logging.DEBUG):
                logging.debug(f'{plugin_name} - {print_style_voir(current_group, " Matching dependencies found for this group: ")}')
        df_list.append((dependencies_df, option))

    if not df_list and throw_error:
        raise DependencyError(
            f'{plugin_name} - No matching dependencies found')

    logging.debug(f'\t  ************************ Fin de boucle sur les groupes pour {plugin_name} ************************ \n ')
    return df_list
            
def create_result_container(df: pd.DataFrame, plugin_result_specifications: dict, nomvar: str, all_rows: bool=False) -> pd.DataFrame:
    """Creates a result container dataframe from model contained in the dataframe

    :param df: input model dataframe
    :type df: pd.DataFrame
    :param plugin_result_specifications: dict of column name:values to modify the container
    :type plugin_result_specifications: dict
    :param nomvar: nomvar to look for in model dataframe
    :type nomvar: str
    :param all_rows: if True, will create a dataframe with the same number
                     of levels as the model, otherwise the container will 
                     have only one row, defaults to False
    :type all_rows: bool, optional
    :return: a dataframe to contain the result of an operation
    :rtype: pd.DAtaFrame
    """
    var_df = get_from_dataframe(df, nomvar)
    res_df = create_empty_result(var_df, plugin_result_specifications[nomvar], all_rows)
    return res_df    
    
class ConversionError(Exception):
    pass

def to_numpy(arr: "np.ndarray|da.core.Array") -> np.ndarray:
    """If the array is of numpy type, no op, else compute de daks array to get a numpy array

    :param arr: array to convert
    :type arr: np.ndarray|da.core.Array
    :raises ConversionError: Raised if not a numpy or dask array
    :return: a numpy array
    :rtype: np.ndarray
    """
    if arr is None:
        return arr
    if isinstance(arr, da.core.Array):   
        return arr.compute()  
    elif isinstance(arr,np.ndarray):    
        return arr    
    else:
        raise ConversionError('to_numpy - Array is not an array of type numpy or dask')    

def to_dask(arr:"np.ndarray|da.core.Array") -> da.core.Array:
    """If the array is of dask type, no op, else comvert array to dask array

    :param arr: array to convert
    :type arr: np.ndarray|da.core.Array
    :raises ConversionError: Raised if not a numpy or dask array
    :return: a dask array
    :rtype:da.core.Array
    """
    if arr is None:
        return arr
    if isinstance(arr, da.core.Array):   
        return arr
    elif isinstance(arr, np.ndarray):   
        return da.from_array(arr).astype(np.float32)        
    else:    
        raise ConversionError('to_dask - Array is not an array of type numpy or dask')       


def reshape_arrays(df:pd.DataFrame) -> pd.DataFrame:
    """reshapes the arrays of the 'd' column to correspond to ni, nj columns

    :param df: input dataframe
    :type df: pd.DataFrame
    :return: dataframe with reshaped arrays
    :rtype: pd.DataFrame
    """
    for row in df.itertuples():
        df.at[row.Index,'d'] = row.d.reshape((row.ni,row.nj))
    return df    

def dataframe_arrays_to_dask(df:pd.DataFrame) -> pd.DataFrame:
    """converts all the arrays of the 'd' column to dask arrays

    :param df: input dataframe
    :type df: pd.DataFrame
    :return: dataframe with dask arrays
    :rtype: pd.DataFrame
    """
    for row in df.itertuples():
        df.at[row.Index,'d'] = to_dask(row.d)
    return df    

def get_split_value(df:pd.DataFrame) -> float:
    """gets the optimal number of rows for reading fst file records

    :param df: input dataframe
    :type df: pd.DataFrame
    :return: split value
    :rtype: float
    """
    num_rows = fstpy.get_num_rows_for_reading(df)
    return math.ceil(len(df.index)/num_rows)

def get_encoded_ips_height(val1, val2, val3, kind):

    (ip2,_) = rmn.convertIp(rmn.CONVIP_DECODE, int(val2))

    rp1a = rmn.FLOAT_IP(val1, val3, int(kind))
    rp2a = rmn.FLOAT_IP(ip2,  ip2, rmn.KIND_HOURS)
    rp3a = rmn.FLOAT_IP(val1,  val3, int(kind))
    (val1_encode, val2_encode, val3_encode) = rmn.EncodeIp(rp1a, rp2a, rp3a)

    return (val1_encode, val2_encode, val3_encode)

def get_encoded_ips_time(val2, val3):

    rp1a = rmn.FLOAT_IP(0., 0., rmn.LEVEL_KIND_PMB)
    rp2a = rmn.FLOAT_IP( val2, val3, rmn.TIME_KIND_HR)
    rp3a = rmn.FLOAT_IP( val2, val3, rmn.TIME_KIND_HR)
    (_, val2_encode, val3_encode) = rmn.EncodeIp(rp1a, rp2a, rp3a)

    return (val2_encode, val3_encode)

# def encode_ip1_and_ip3(df):
#     for row in df.itertuples():
#         if row.nomvar in ['>>', '^^', '^>', '!!', 'P0', 'PT']:
#             continue

#         ip1 = row.ip1
#         ip2 = row.ip2
#         ip3 = row.ip3

#         (rp1, rp2, rp3) = rmn.DecodeIp(ip1, ip2, ip3)
#         rp1a = rmn.FLOAT_IP(rp1.v1,rp1.v1, rp1.kind)
#         rp2a = rmn.FLOAT_IP( 0., 0., rmn.TIME_KIND_HR)
#         rp3a = rmn.FLOAT_IP( rp3.v1, rp3.v1, rp1.kind)

#         (ip1, ip2,  ip3) = rmn.EncodeIp(rp1a, rp2a, rp3a)
#         df.at[row.Index,'ip1'] = ip1
#         df.at[row.Index,'ip3'] = ip3

#     return df 

def encode_ip_when_interval(df:pd.DataFrame) -> pd.DataFrame:
    # Fonction temporaire, utilise dans les tests de regression, en attendant d'avoir un 
    # writer a la facon spooki.  
    """encode les valeurs des IP des champs pour lesquels il existe un objet interval; sinon n'encode pas.
    :param df: input DataFrame
    :type df: pd.DataFrame
    :return: output DataFrame
    :rtype: pd.DataFrame
    """

    if 'level' not in df.columns:
        df = fstpy.add_columns(df, 'ip_info')

    for row in df.itertuples():
        if row.nomvar in ['>>', '^^', '^>', '!!','HY']:
            continue

        (ip2,_) = rmn.convertIp(rmn.CONVIP_DECODE, int(row.ip2))
        inter = row.interval

        # if inter is not None and not math.isnan(inter):
        if isinstance(inter,fstpy.Interval):
            # print(f' Interval pour nomvar {row.nomvar}  = \n {inter} \n\n')
            if inter.ip == 'ip1':
                (val1_enc, val2_enc, val3_enc) = get_encoded_ips_height (inter.low, ip2, inter.high, inter.kind )
                df.at[row.Index,'ip1'] = val1_enc
                df.at[row.Index,'ip3'] = val3_enc
            else:
                val2 = (inter.high)
                val3 = (inter.low)
                (val2_enc, val3_enc) = get_encoded_ips_time (val2, val3)
                df.at[row.Index,'ip2'] = val2_enc
                df.at[row.Index,'ip3'] = val3_enc

    return df

def encode_ip2_and_ip3_height(df:pd.DataFrame) -> pd.DataFrame:
    """encode ip2 and ip3 to new style

    :param df: input DataFrame
    :type df: pd.DataFrame
    :return: output DataFrame
    :rtype: pd.DataFrame
    """
    if 'level' not in df.columns:
        df = fstpy.add_columns(df, 'ip_info')

    for row in df.itertuples():
        if row.nomvar in ['>>', '^^', '^>', '!!','HY']:
            continue

        inter = row.interval
        if inter is None:
            (ip1,interval_kind) = rmn.convertIp(rmn.CONVIP_DECODE, int(row.ip1))
            (ip3,_)             = rmn.convertIp(rmn.CONVIP_DECODE, int(row.ip3))
        else:
            ip1           = row.interval.low
            ip3           = row.interval.high
            interval_kind = row.interval.kind

        (ip2,_) = rmn.convertIp(rmn.CONVIP_DECODE, int(row.ip2))
        (val1_enc, val2_enc, val3_enc) = get_encoded_ips_height (ip1, ip2, ip3, interval_kind)

        df.at[row.Index,'ip1'] = val1_enc
        df.at[row.Index,'ip2'] = val2_enc
        df.at[row.Index,'ip3'] = val3_enc
    return df

def decode_ip_info(nomvar:str, ip1: int, ip2: int, ip3: int):
    """A partir des ips encodes, retourne la valeur du ip1,
       la valeur de la borne sup de l'objet interval ainsi
       que le delta de l'objet interval. Fonction utilisee
       dans les tests de regression pour fins de compatibilite,
       particulierement avec l'utilisation des intervalles de temps.

    :param ip1: encoded value stored in ip1
    :type ip1 : int
    :param ip2: encoded value stored in ip2
    :type ip2 : int
    :param ip3: encoded value stored in ip3
    :type ip3 : int
    :return: level value, ip2 and ip3 from the interval object
    :rtype: float, int, int
    """

    i1, i2, i3 = fstpy.decode_ip123(nomvar, ip1, ip2, ip3) 
    interval   = fstpy.get_interval(ip1, ip2, ip3, i1, i2, i3)
    ip2        = interval.high
    ip3        = interval.delta()

    return i1['v1'],  ip2,  ip3

VDECODE_IP_INFO: Final = vectorize(decode_ip_info, otypes=['float32', 'int32', 'int32'])

def decode_ip2(nomvar:str, ip1: int, ip2: int, ip3: int):
    """A partir des ips encodes, retourne la valeur du ip2.
       Fonction utilisee dans les tests de regression pour 
       fins de compatibilite, particulierement avec l'utilisation 
       des intervalles de temps.

    :param ip1: encoded value stored in ip1
    :type ip1 : int
    :param ip2: encoded value stored in ip2
    :type ip2 : int
    :param ip3: encoded value stored in ip3
    :type ip3 : int
    :return: ip2 decoded value
    :rtype:  int
    """

    i1, i2, i3 = fstpy.decode_ip123(nomvar, ip1, ip2, ip3) 

    return i2['v1']

VDECODE_IP2_INFO: Final = vectorize(decode_ip2, otypes=['int32'])

def validate_list_of_times(param:'list(datetime.timedelta)|datetime.timedelta', exception_class:type) -> 'list(datetime.timedelta)|datetime.timedelta':
    """validate a list of time deltas

    :param param: time delta object
    :type param: list(datetime.timedelta)|datetime.timedelta
    :param exception_class: excpetion to raise
    :type exception_class: type
    :raises exception_class: raised exception
    :return: valid time delta object(s)
    :rtype: list(datetime.timedelta)|datetime.timedelta
    """
    if isinstance(param, datetime.timedelta):
        param = [param]
    if not isinstance(param, list):
        raise exception_class(f'{str(param)} needs to be a list of datetime.timedelta')
    for n in param:
        if not isinstance(n, datetime.timedelta):
            raise exception_class(f'{str(param)} needs to be a list of datetime.timedelta')
        if n == datetime.timedelta():
            raise exception_class('value is not valid') 
    return param

def validate_list_of_tuples_of_times(param:'list(Tuple(datetime.timedelta,datetime.timedelta))|Tuple(datetime.timedelta,datetime.timedelta)', exception_class:type) -> 'list(Tuple(datetime.timedelta,datetime.timedelta))|Tuple(datetime.timedelta,datetime.timedelta)':
    """validate a list of tuples of 2 time deltas

    :param param: tuple of time delta objects
    :type param: list(Tuple(datetime.timedelta,datetime.timedelta))|Tuple(datetime.timedelta,datetime.timedelta)
    :param exception_class: excpetion to raise
    :type exception_class: type
    :raises exception_class: raised exception
    :return: valid tuple(s) of 2 time delta object(s)
    :rtype: list(Tuple(datetime.timedelta,datetime.timedelta))|Tuple(datetime.timedelta,datetime.timedelta)
    """
    if isinstance(param, tuple) and len(param) == 2:
        param = [param]
    if not isinstance(param, list):
        raise exception_class(f'{str(param)} is not a list, {str(param)} needs to be a list of tuple of 2 datetime.timedelta')
    for n in param:
        if not isinstance(n, tuple) or len(n) != 2:
            raise exception_class(
                f'{str(param)} does not contain tuple of 2 elements, {str(param)} needs to be a list of tuple of 2 datetime.timedelta')
        if not isinstance(n[0], datetime.timedelta) or not isinstance(n[1], datetime.timedelta):
            raise exception_class(
                f'{str(param)} needs to be a list of tuple of 2 datetime.timedelta')
        if n[0] >= n[1]:
            raise exception_class(f'{str(param)} value is not valid')  
    return param       

def get_bounds(forecast_hour_range:'list(Tuple(datetime.timedelta, datetime.timedelta))') -> 'Tuple(list(datetime.timedelta), list(datetime.timedelta))':
    """Get the lower and upper bounds from the forecast_hour_range(s) as seperate lists

    :param forecast_hour_range: a forecast hour range
    :type forecast_hour_range: list(Tuple(datetime.datetime, datetime.datetime))
    :return: a list of lower bounds and a list of upper bounds
    :rtype: Tuple(list(datetime.datetime), list(datetime.datetime))
    """
    borne_inf = []
    borne_sup = []
    for i in range(len(forecast_hour_range)):
        borne_inf.append(forecast_hour_range[i][0])
        borne_sup.append(forecast_hour_range[i][1])
    return borne_inf, borne_sup

def get_list_of_forecast_hours(forecast_hour_range:'list(Tuple(datetime.timedelta, datetime.timedelta))', interval:'list(datetime.timedelta)', step:'list(datetime.timedelta)') -> 'list(datetime.timedelta)':
    """Build a list of forecast hours from  the range, the interval and the step

    :param forecast_hour_range: list of forecast hour ranges
    :type forecast_hour_range: list(Tuple(datetime.timedelta, datetime.timedelta))
    :param interval: intervals
    :type interval: list(datetime.timedelta)
    :param step: steps
    :type step: list(datetime.timedelta)
    :return: the list of computed forecast hours
    :rtype: list(datetime.timedelta)
    """
    borne_inf, borne_sup = get_bounds(forecast_hour_range)
    forecast_hours = []
    for i in range(len(interval)):
        j = borne_inf[i].total_seconds()  
        while int(j + interval[i].total_seconds()) <=  int(borne_sup[i].total_seconds()):
            b_inf = int(j)
            b_sup = int(j + interval[i].total_seconds())
            forecast_hours.append((b_inf,b_sup))
            j = j + step[i].total_seconds()
    return forecast_hours   

def get_0_ip1(model_ip1:int) -> int:
    """get an ip1 of 0 with the same encoding and kind as the model ip1

    :param model_ip1: model ip1 to derive encoding and kind from
    :type model_ip1: int
    :return: ip1 of 0 with right encoding and kind
    :rtype: int
    """
    _, kind = rmn.convertIp(rmn.CONVIP_DECODE, int(model_ip1))
    if model_ip1 >= 32768:
        ip1 = rmn.convertIp(rmn.CONVIP_ENCODE, 0., kind)
    else:
        ip1 = rmn.convertIp(rmn.CONVIP_ENCODE_OLD, 0., kind)
    return ip1


def modify_5005_record(df:pd.DataFrame):
    # modify the dataframe itself, no return value

    # add column surfacelevelfor5005 with none everywhere
    df['levelfor5005'] = -999
    df['kindfor5005'] = -999
    # split in two those with flag 5005 (and vctype and HYBRID_5005) and not
    mask = (df['vctype']==fstpy.VerticalCoordType.HYBRID_5005) & df['flag5005']
    df_5005 = df.loc[mask]

    group_nomvar = df_5005.groupby(by='nomvar')

    for _, grouped_df in group_nomvar:
        idx = grouped_df.loc[grouped_df['ip1_kind']==4].index
        if idx.empty:
            continue
        level = df['level'].loc[idx]
        df.loc[idx,'levelfor5005'] = level
        kind = df['ip1_kind'].loc[idx]
        df.loc[idx,'kindfor5005'] = kind
        df.loc[idx,'level'] = 1.0
        df.loc[idx,'ip1_kind'] = 5 # is this an ok assumption?

def restore_5005_record(df:pd.DataFrame):
    # modify the dataframe itself, no return value
    # find places where the surfacelevelfor5005 column is and restore level and kind
    if 'levelfor5005' in df.columns:
        df['level'] = df.apply(lambda row: row['level'] if row['levelfor5005'] == -999 else row['levelfor5005'], axis=1)

    if 'kindfor5005' in df.columns:
        df['ip1_kind'] = df.apply(lambda row: row['ip1_kind'] if row['kindfor5005'] == -999 else row['kindfor5005'], axis=1)

def print_voir(df: pd.DataFrame, message: str = ""):
    """Impression du contenu du dataframe style <voir>

    :param df: dataframe dont on veut voir les valeurs
    :type df: pd.DataFrame
    :return: code retour
    :rtype: int
    """
    message_log = print_style_voir(df, message)
    print(message_log)

def print_style_voir(df: pd.DataFrame, message: str) -> str:
    """Impression du contenu du dataframe style <voir> dans une string

    :param df: dataframe dont on veut voir les valeurs
    :type df: pd.DataFrame
    :return: code retour
    :rtype: int
    """
    df=df.sort_values(by=['ig1','nomvar'])
    df=df.reset_index()
 
    ligne1 = "\n***************************************************************************************************************************************\n"
    info   = df[['nomvar','typvar','etiket','ni','nj','nk','dateo','ip1','ip2','ip3','deet','npas','datyp','nbits','grtyp','ig1','ig2','ig3','ig4']].to_string()
    ligne2 = "\n***************************************************************************************************************************************\n\n"

    message_log = "".join([message, ligne1, info, ligne2])
    return message_log



def parse_condition(condition, error: 'type' = Exception, only_operator = False):
    if condition == 'isnan':
        return None, None
    
    match_operator = r"(>=|<=|==|\>|\<)"

    if only_operator:
        if not re.match(match_operator, condition):
            raise error(f"invalid condition - {condition}")

        parsed_condition = re.search(match_operator,condition)
        # print(parsed_condition)
        return parsed_condition[1]


    match_optional_underscore = "_*"
    match_float = r"(\d+(\.\d*)?)$"
    match_all = match_operator+match_optional_underscore+match_float

    if not re.match(match_all, condition):
        raise error(f"invalid condition - {condition}")
    
    parsed_condition = re.search(match_all,condition)
    
    return (parsed_condition[1],parsed_condition[2])

def parse_and_validate_condition(condition, error: 'type' = Exception):
    condition_operator, condition_value = parse_condition(condition, error)
    if condition_operator is not None:
        condition_operator = OPERATOR_LOOKUP_TABLE[condition_operator]
        condition_value = float(condition_value)
    return condition_operator, condition_value

OPERATOR_LOOKUP_TABLE = {
    "<" : operator.lt,
    "<=" : operator.le,
    ">" : operator.gt,
    ">=" : operator.ge,
    "==" : operator.eq,
    "!=" : operator.ne,
}

LABEL_OPERATOR_LOOKUP_TABLE = {
    operator.lt : "LT",
    operator.le : "LE",
    operator.gt : "GT",
    operator.ge : "GE",
    operator.eq : "EQ",
    operator.ne : "NE",
}
