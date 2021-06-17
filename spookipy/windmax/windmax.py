# -*- coding: utf-8 -*-
from typing import Tuple
import pandas as pd
import numpy as np
from spookipy.utils import get_existing_result, get_plugin_dependencies
import fstpy.all as fstpy
from spookipy.plugin.plugin import Plugin


class WindMaxError(Exception):
    pass

def wind_max(uu_3d:np.ndarray,vv_3d:np.ndarray,uv_3d:np.ndarray,px_3d:np.ndarray) -> Tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray]:
    """Computes the maximum values by column for uu,vv,uv and px

    :param uu_3d: flattened then stacked uu wind component arrays. the array is actually 2d (rows(flattened 2d grid) by levels)
    :type uu_3d: np.ndarray
    :param vv_3d: flattened then stacked vv wind component arrays. the array is actually 2d (rows(flattened 2d grid) by levels)
    :type vv_3d: np.ndarray
    :param uv_3d: flattened then stacked uv wind modulus arrays. the array is actually 2d (rows(flattened 2d grid) by levels)
    :type uv_3d: np.ndarray
    :param px_3d: flattened then stacked px pressure arrays. the array is actually 2d (rows(flattened 2d grid) by levels)
    :type px_3d: np.ndarray
    :return: uu_max,vv_max,uv_max,px_max
    :rtype: Tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray]
    """
    # max index
    uvmax = np.expand_dims(np.argmax(uv_3d,axis=0),axis=0)

    # match index
    uu_max = np.take_along_axis(uu_3d,uvmax,axis=0)
    vv_max = np.take_along_axis(vv_3d,uvmax,axis=0)
    uv_max = np.take_along_axis(uv_3d,uvmax,axis=0)
    px_max = np.take_along_axis(px_3d,uvmax,axis=0)
    return uu_max,vv_max,uv_max,px_max
    

class WindMax(Plugin):
    plugin_mandatory_dependencies = {
        'UV':{'nomvar':'UV','unit':'knot'},
        'UU':{'nomvar':'UU','unit':'knot'},
        'VV':{'nomvar':'VV','unit':'knot'},
    }
    plugin_result_specifications = {
        'UV':{'nomvar':'UV','etiket':'WindMax','unit':'knot'},
        'PX':{'nomvar':'PX','etiket':'WindMax','unit':'hectoPascal'},
        'UU':{'nomvar':'UU','etiket':'WindMax','unit':'knot'},
        'VV':{'nomvar':'VV','etiket':'WindMax','unit':'knot'},
        }
    
    def __init__(self,df:pd.DataFrame):
        self.df = df
        # print('df1\n',df)
        self.validate_input()
        
    # might be able to move    
    def validate_input(self):
        if self.df.empty:
            raise  WindMaxError( "WindMax" + ' - no data to process')
        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies)
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','forecast_hour'])


    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return self.existing_result_df
        #holds data from all the groups
        results = []
        
        for index,current_fhour_group in self.fhour_groups:
            # print('current_fhour_group',current_fhour_group)
            press_meta_df = self.df.query('(nomvar in ["P0","PT","!!","HY"]) and (grid=="%s")'%index[0])

            uu_df = current_fhour_group.query('nomvar=="UU"')
            uu_df = fstpy.load_data(uu_df)
            uu_res_df = create_empty_result(uu_df,self.plugin_result_specifications['UU'])

            vv_df = current_fhour_group.query('nomvar=="VV"')
            vv_df = fstpy.load_data(vv_df)
            vv_res_df = create_empty_result(vv_df,self.plugin_result_specifications['VV'])

            uv_df = current_fhour_group.query('nomvar=="UV"')
            uv_res_df = create_empty_result(uv_df,self.plugin_result_specifications['UV'])
            
            px_df = fstpy.Pressure(pd.concat([uv_df,press_meta_df],ignore_index=True)).compute()
            px_res_df = create_empty_result(px_df,self.plugin_result_specifications['PX'])

            uu_3d = get_3d_array(uu_df)
            vv_3d = get_3d_array(vv_df)
            px_3d = get_3d_array(px_df)
            uv_3d = get_3d_array(uv_df)


            uu_res_df.at[0,'d'],vv_res_df.at[0,'d'],uv_res_df.at[0,'d'],px_res_df.at[0,'d'] = wind_max(uu_3d,vv_3d,uv_3d,px_3d)

            results.append(uu_res_df)
            results.append(vv_res_df)
            results.append(uv_res_df)
            results.append(px_res_df)
        # merge all results together
        result = pd.concat(results,ignore_index=True)
        return result

def get_3d_array(df):
    for i in df.index:
        df.at[i,'d'] = df.at[i,'d'].flatten()
    arr_3d = np.stack(df['d'].to_list())
    return arr_3d

def create_empty_result(df, plugin_result_specifications):
    res_df = fstpy.create_1row_df_from_model(df)
    res_df['ip1'] = 0
    for k,v in plugin_result_specifications.items():
        res_df[k] = v
    return res_df


