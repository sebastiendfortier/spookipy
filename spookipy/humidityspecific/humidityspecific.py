# -*- coding: utf-8 -*-
from ..plugin import Plugin
from ..utils import get_existing_result, get_intersecting_levels, get_plugin_dependencies, initializer, prepare_existing_results, remove_load_data_info
import pandas as pd
import fstpy.all as fstpy
import numpy as np
import sys


class HumiditySpecificError(Exception):
    pass
 
def humidity_specific(uu:np.ndarray,vv:np.ndarray) -> np.ndarray:
    """Computes thw wind modulus from the wind components

    :param uu: U wind component
    :type uu: np.ndarray
    :param vv: V wind component
    :type vv: np.ndarray
    :return: wind modulus
    :rtype: np.ndarray
    """
    return (uu**2 + vv**2)**.5 

class HumiditySpecific(Plugin):
    plugin_mandatory_dependencies_option_1 = {
        'TT':{'nomvar':'TT','unit':'celsius'},
        'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram'}
        }
    plugin_mandatory_dependencies_option_2 = {
        'TT':{'nomvar':'TT','unit':'celsius'},
        'QV':{'nomvar':'QV','unit':'gram_per_kilogram'},
    }
    plugin_mandatory_dependencies_option_3 = {
        'TT':{'nomvar':'TT','unit':'celsius'},
        'TD':{'nomvar':'PX','unit':'celsius'},
        'ES':{'nomvar':'ES','unit':'celsius'},
    }
    plugin_result_specifications = {'HR':{'nomvar':'HR','etiket':'HumiditySpecific','unit':'scalar'}}

    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase='water', temp_phase_switch='',rpn=False):
        self.validate_input()
        
    # might be able to move    
    def validate_input(self):
        if self.df.empty:
            raise  HumiditySpecificError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)  
            
        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies)
            
            # self.df = self.df.query( 'nomvar==%s'%self.plugin_mandatory_dependencies)
            level_intersection_df = get_intersecting_levels(self.df,self.plugin_mandatory_dependencies)
            # print('intersecting levels',level_intersection_df)
            if level_intersection_df.empty:
                raise  HumiditySpecificError('No data to process')
            # if level_intersection_df.empty:
            #     raise HumiditySpecificError('cant find intersecting levels between UU and VV')
            level_intersection_df = fstpy.load_data(level_intersection_df)
            #group by grid/forecast hour    
            # self.fhour_groups = fstpy.get_groups(level_intersection_df,group_by_forecast_hour=True)
            self.fhour_groups = level_intersection_df.groupby(['grid','forecast_hour'])

            

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return prepare_existing_results('HumiditySpecific',self.existing_result_df,self.meta_df)

        sys.stdout.write('HumiditySpecific - compute')
        df_list = []
        for _,current_fhour_group in self.fhour_groups:

            uudf = current_fhour_group.query('nomvar == "UU"').reset_index(drop=True).reset_index(drop=True)
            vvdf = current_fhour_group.query('nomvar == "VV"').reset_index(drop=True).reset_index(drop=True)
            uv_df = vvdf.copy(deep=True)
            #recipe: zap with dict
            for k,v in self.plugin_result_specifications['UV'].items():uv_df[k] = v

            for i in uv_df.index:
                uu = uudf.at[i,'d']
                vv = vvdf.at[i,'d']
                uv_df.at[i,'d']
            df_list.append(uv_df)

        if not len(df_list):
            raise HumiditySpecificError('No results were produced')

        self.meta_df = fstpy.load_data(self.meta_df)
        df_list.append(self.meta_df)    
        # merge all results together
        res_df = pd.concat(df_list,ignore_index=True)

        res_df = remove_load_data_info(res_df)
        res_df = fstpy.metadata_cleanup(res_df)
        
        return res_df
    

