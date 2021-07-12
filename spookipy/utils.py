# -*- coding: utf-8 -*-
import inspect
from functools import wraps
import pandas as pd
import rpnpy.librmn.all as rmn


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
        # tmp_df = df.query('nomvar=="%s"'%nomvar).reset_index(drop=True)
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
        res= df.query('(nomvar=="%s") and (unit=="%s")'%(spec["nomvar"],spec["unit"])).reset_index(drop=True)
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

    firstdf = df.query( 'nomvar == "%s"' % list(plugin_mandatory_dependencies.keys())[0]).reset_index(drop=True)
    if df.empty:
        # print('get_intersecting_levels - no records to intersect')
        raise LevelIntersectionError('get_intersecting_levels - no records to intersect')
    common_levels = set(firstdf.ip1.unique())

    for nomvar,_ in plugin_mandatory_dependencies.items():
        currdf = df.query('nomvar == "%s"' % nomvar).reset_index(drop=True)
        levels = set(currdf.ip1.unique())
        common_levels = common_levels.intersection(levels)
    common_levels = list(common_levels)
    # print('(nomvar in %s) and (ip1 in %s)'%(nomvars,common_levels))
    nomvars = list(plugin_mandatory_dependencies.keys())
    query_res = df.query('(nomvar in %s) and (ip1 in %s)'%(nomvars,common_levels)).reset_index(drop=True)
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

def remove_load_data_info(df):
    #make sure load_data does not execute (does nothing)
    df.loc[:,'path'] = None
    df.loc[:,'key'] = ''

class SelectError(Exception):
    pass

def select_meta(df:pd.DataFrame) -> pd.DataFrame:
    meta_df = df.query('nomvar in ["!!","P0","PT",">>","^^","^>","HY","!!SF"]')
    return meta_df

def select_with_meta(df:pd.DataFrame,nomvar:list) -> pd.DataFrame:
    if df.empty:
        raise SelectError(f'dataframe is empty - nothing to select into')

    results = []

    if len(nomvar) == 0:
        raise SelectError(f'nomvar is empty - nothing to select')

    for var in nomvar:
        res_df = df.query(f'nomvar=="{var}"').reset_index(drop=True)
        if res_df.empty:
            raise SelectError(f'missing {var} in dataframe')
        results.append(res_df)

    meta_df = select_meta(df)

    if not meta_df.empty:
        results.append(meta_df)

    selection_result_df = pd.concat(results,ignore_index=True)   

    selection_result_df = metadata_cleanup(selection_result_df)

    return selection_result_df

    #    kind can take the following values
    #    0, p est en hauteur (m) rel. au niveau de la mer (-20, 000 -> 100, 000)
    #    1, p est en sigma                                (0.0 -> 1.0)
    #    2, p est en pression (mb)                        (0 -> 1100)
    #    3, p est un code arbitraire                      (-4.8e8 -> 1.0e10)
    #    4, p est en hauteur (M) rel. au niveau du sol    (-20, 000 -> 100, 000)
    #    5, p est en coordonnee hybride                   (0.0 -> 1.0)
    #    6, p est en coordonnee theta                     (1 -> 200, 000)
    #    10, p represente le temps en heure               (0.0 -> 1.0e10)
    #    15, reserve (entiers)
    #    17, p represente l'indice x de la matrice de conversion (1.0 -> 1.0e10)
    #        (partage avec kind=1 a cause du range exclusif
    #    21, p est en metres-pression                     (0 -> 1, 000, 000)
    #                                                     fact=1e4
    #        (partage avec kind=5 a cause du range exclusif)


def get_kinds_and_ip1(df:pd.DataFrame) -> dict:
    ip1s = df.ip1.unique()
    kinds = {}
    for ip1 in ip1s:
        (_, kind) = rmn.convertIp(rmn.CONVIP_DECODE, int(ip1))
        if kind not in kinds.keys():
            kinds[kind] = ip1    
    # print(kinds)    
    return kinds

def get_ips(df:pd.DataFrame,sigma=False,hybrid=False) -> list:
    kinds = get_kinds_and_ip1(df)
    ip1_list = []
    if sigma:
        if 1 in kinds.keys():
            ip1_list.append(kinds[1])
    if hybrid:        
        if 5 in kinds.keys():
            ip1_list.append(kinds[5])    
    return ip1_list  

def get_model_ips(df:pd.DataFrame) -> list:
    return get_ips(df,sigma=True,hybrid=True)
    # kinds = get_kinds_and_ip1(df)

    # ip1_list = []
    # if 1 in kinds.keys():
    #     ip1_list.append(kinds[1])
    # if 5 in kinds.keys():
    #     ip1_list.append(kinds[5])    
    # return ip1_list    

def get_sigma_ips(df:pd.DataFrame) -> list:
    return get_ips(df,sigma=True)
    # kinds = get_kinds_and_ip1(df)
    # ip1_list = []
    # if 1 in kinds.keys():
    #     ip1_list.append(kinds[1])
    # return ip1_list    

def get_hybrid_ips(df:pd.DataFrame) -> list:
    return get_ips(df,hybrid=True)
    # kinds = get_kinds_and_ip1(df)
    # ip1_list = []
    # if 5 in kinds.keys():
    #     ip1_list.append(kinds[5])
    # return ip1_list    

# def get_model_ips(df:pd.DataFrame) -> list:
#     ip1s = df.ip1.unique()
#     ip1_list = []
#     for ip1 in ip1s:
#         (_, kind) = rmn.convertIp(rmn.CONVIP_DECODE, int(ip1))
#         if (kind == 1) or (kind == 5):
#             ip1_list.append(ip1)
#     return ip1_list    

# def get_sigma_ips(df:pd.DataFrame) -> list:
#     ip1s = df.ip1.unique()
#     ip1_list = []
#     for ip1 in ip1s:
#         (_, kind) = rmn.convertIp(rmn.CONVIP_DECODE, int(ip1))
#         if (kind == 1):
#             ip1_list.append(ip1)
#     return ip1_list  

# def get_hybrid_ips(df:pd.DataFrame) -> list:
#     ip1s = df.ip1.unique()
#     ip1_list = []
#     for ip1 in ip1s:
#         (_, kind) = rmn.convertIp(rmn.CONVIP_DECODE, int(ip1))
#         if (kind == 5):
#             ip1_list.append(ip1)
#     return ip1_list  

def metadata_cleanup(df:pd.DataFrame):

    if df.empty:
        return df
    
    not_meta_df = df.query('nomvar not in  ["!!","P0","PT",">>","^^","^>","HY","!!SF"]').reset_index(drop=True)
    
    # get deformation fields
    grid_deformation_fields_df = get_grid_deformation_fileds(df,not_meta_df)        

    # get P0's
    p0_fields_df = get_p0_fields(df,not_meta_df)
    
    #get PT's
    pt_fields_df = get_pt_fields(df,not_meta_df)

    #get HY
    hybrid_ips, hy_field_df = get_hy_field_and_hybrid_ips(df,not_meta_df)

    #get !!'s strict
    toctoc_fields_df = get_toctoc_fileds_strict(df,hybrid_ips)


    df = pd.concat([not_meta_df,grid_deformation_fields_df,p0_fields_df,pt_fields_df,hy_field_df,toctoc_fields_df],ignore_index=True)

    return df

def get_toctoc_fileds_strict(df:pd.DataFrame,hybrid_ips:list):
    toctoc_fields_df = pd.DataFrame(dtype=object)
    hybrid_fields_df = pd.DataFrame(dtype=object)

    if len(hybrid_ips):
        hybrid_fields_df = df.query(f'ip1 in {hybrid_ips}').reset_index(drop=True)

    grids = []
    if not hybrid_fields_df.empty:
        grids = hybrid_fields_df.grid.unique()

    df_list = []
    for grid in grids:
        toctoc = df.query(f'(nomvar=="!!") and (grid=="{grid}")')
        if not toctoc.empty:
            toctoc = True
        else:
            toctoc = False
        # toctoc, _, _, _, _, _, _ = fstpy.get_meta_fields_exists(grid)
        if toctoc:
            df_list.append(df.query(f'(nomvar=="!!") and (grid=="grid")'))

    if len(df_list):
        toctoc_fields_df = pd.concat(df_list,ignore_index=True)

    return toctoc_fields_df

def get_hy_field_and_hybrid_ips(df:pd.DataFrame,not_meta_df:pd.DataFrame):
    hy_field_df = pd.DataFrame(dtype=object)
    hybrid_ips = get_hybrid_ips(not_meta_df)
    if len(hybrid_ips):
        hy_field_df = df.query(f'nomvar=="HY"').reset_index(drop=True)

    return hybrid_ips, hy_field_df
    # if len(hybrid_ips):
    #     df.query(f'ip=="HY"').reset_index(drop=True)

    #     #par defaut
    #     else if ( mpds->second->getPdsName() == "!!")
        
    #         # only keep !! if we have at least one pds with a vcode equal to the ig1 value of the !!
    #         int toctocVcode
    #         LEXICALCAST(mpds->second->getOtherInformation().ig1,toctocVcode)
    #         keep = hasPdsWithVcode(toctocVcode)
        
    #     # active par variable globale
    #     else if ( mpds->second->getPdsName() == "!!")
        
    #         # only keep !! if we have at least one pds with a vcode equal to the ig1 value of the !!
    #         int toctocVcode
    #         LEXICALCAST(mpds->second->getOtherInformation().ig1,toctocVcode)
    #         keep = hasPdsWithVcode(toctocVcode)
def get_grid_deformation_fileds(df:pd.DataFrame,not_meta_df:pd.DataFrame):        
    grid_deformation_fields_df = pd.DataFrame(dtype=object)
    all_grids = not_meta_df.grid.unique()

    df_list = []
    for grid in all_grids:
        df_list.append(df.query(f'(nomvar==">>") and (grid=="{grid}")').reset_index(drop=True))
        df_list.append(df.query(f'(nomvar=="^^") and (grid=="{grid}")').reset_index(drop=True))
        df_list.append(df.query(f'(nomvar=="^>") and (grid=="{grid}")').reset_index(drop=True))

    if len(df_list):
        grid_deformation_fields_df = pd.concat(df_list,ignore_index=True)

    return grid_deformation_fields_df   

def get_p0_fields(df:pd.DataFrame,not_meta_df:pd.DataFrame):
    p0_fields_df = pd.DataFrame(dtype=object)
    model_ips = get_model_ips(not_meta_df)
    model_grids = set()
    for ip1 in model_ips:
        model_grids.add(not_meta_df.query(f'ip1=={ip1}').reset_index(drop=True).iloc[0]['grid'])
    
    df_list = []
    for grid in list(model_grids):
        # print(grid)
        df_list.append(df.query(f'(nomvar=="P0") and (grid=="{grid}")').reset_index(drop=True))

    if len(df_list):
        p0_fields_df = pd.concat(df_list,ignore_index=True)

    return p0_fields_df  

def get_pt_fields(df:pd.DataFrame,not_meta_df:pd.DataFrame):
    pt_fields_df = pd.DataFrame(dtype=object)
    sigma_ips = get_sigma_ips(not_meta_df)
    sigma_grids = set()
    for ip1 in sigma_ips:
        sigma_grids.add(not_meta_df.query(f'ip1=={ip1}').reset_index(drop=True).iloc[0]['grid'])
    
    df_list = []
    for grid in list(sigma_grids):
        df_list.append(df.query(f'(nomvar=="PT") and (grid=="{grid}")').reset_index(drop=True))

    if len(df_list):
        pt_fields_df = pd.concat(df_list,ignore_index=True)

    return pt_fields_df    