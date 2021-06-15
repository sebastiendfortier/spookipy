# -*- coding: utf-8 -*-

import pandas as pd

class DependencyError(Exception):
    pass

class LevelIntersectionError(Exception):
    pass

def get_plugin_dependencies(df:pd.DataFrame, plugin_mandatory_dependencies:dict) -> pd.DataFrame:
    from spookipy.windmodulus.windmodulus import WindModulus
    from spookipy.humidityspecific.humidityspecific import HumiditySpecific
    from spookipy.humidityrelative.humidityrelative import HumidityRelative
    from spookipy.temperaturedewpoint.temperaturedewpoint import TemperatureDewPoint
    from spookipy.windmodulus.windmodulus import WindModulus
    from fstpy.pressure import Pressure
    computable_dependencies = {
        'UV':WindModulus,
        'PX':Pressure,
        'HR':HumidityRelative,
        'HU':HumiditySpecific,
        'TD':TemperatureDewPoint,
        }
    results = []
    for nomvar,desc in plugin_mandatory_dependencies.items():
        #recipe, query with dict
        tmp_df = df.loc[(df[list(desc)] == pd.Series(desc)).all(axis=1)]
        # tmp_df = df.query('nomvar=="%s"'%nomvar)
        # print('query equality',tmp_df1.equals(tmp_df))
        # print('tmp_df',tmp_df,'results',results,sep='\n')
        if tmp_df.empty:
            if nomvar in computable_dependencies.keys():
                plugin = computable_dependencies[nomvar] 
            else:
                plugin = None    
            if plugin == None:
                raise DependencyError(f'get_plugin_dependencies - {plugin_mandatory_dependencies[nomvar]} not found!')
            else:
                # print('-------',df)
                tmp_df = plugin(df).compute()
                # print('tmp_df',tmp_df)
        # print('\nappending\n',tmp_df)        
        results.append(tmp_df)

    res_df = pd.concat(results,ignore_index=True)
    # print('res_df\n\n',res_df)
    return res_df

def get_existing_result(df:pd.DataFrame, plugin_result_specifications) -> pd.DataFrame:
    results = []
    for _,spec in plugin_result_specifications.items():
        res= df.query('(nomvar=="%s") and (unit=="%s")'%(spec["nomvar"],spec["unit"]))
        if not res.empty:
            results.append(res)
        else:
            break
    if len(results)==len(plugin_result_specifications):    
        return pd.concat(results,ignore_index=True)    
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
        raise LevelIntersectionError('not enough nomvars to process')

    firstdf = df.query( 'nomvar == "%s"' % list(plugin_mandatory_dependencies.keys())[0])
    if df.empty:
        # print('get_intersecting_levels - no records to intersect')
        raise LevelIntersectionError('get_intersecting_levels - no records to intersect')
    common_levels = set(firstdf.ip1.unique())

    for nomvar,_ in plugin_mandatory_dependencies.items():
        currdf = df.query('nomvar == "%s"' % nomvar)
        levels = set(currdf.ip1.unique())
        common_levels = common_levels.intersection(levels)
    common_levels = list(common_levels)
    # print('(nomvar in %s) and (ip1 in %s)'%(nomvars,common_levels))
    nomvars = list(plugin_mandatory_dependencies.keys())
    query_res = df.query('(nomvar in %s) and (ip1 in %s)'%(nomvars,common_levels))
    # print('query_res',query_res)  
    if query_res.empty:
        # print('get_intersecting_levels - no intersecting levels found')
        return pd.DataFrame(dtype='object')
      
    return query_res            


def validate_nomvar(nomvar:str, caller_class:str, error_class:Exception):
    """Check that a nomvar only has 4 characters

    :param nomvar: nomvar string
    :type nomvar: str
    :param caller_class: a string that indicates the name of the caller class or method
    :type caller_class: str
    :param error_class: The exception to throw if nomvar is not 4 characters long
    :type error_class: Exception
    :raises error_class: The class of the exception
    """
    if len(nomvar) > 4:
        raise error_class(caller_class + ' - max 4 char for nomvar')
