# -*- coding: utf-8 -*-
from spookipy.plugin.plugin import Plugin
from spookipy.utils import get_existing_result, get_intersecting_levels, get_plugin_dependencies
import pandas as pd
import fstpy.all as fstpy
import numpy as np


class WindModulusError(Exception):
    pass
 
def wind_modulus(uu:np.ndarray,vv:np.ndarray) -> np.ndarray:
    """Computes the wind modulus from the wind components

    :param uu: U wind component
    :type uu: np.ndarray
    :param vv: V wind component
    :type vv: np.ndarray
    :return: wind modulus
    :rtype: np.ndarray
    """
    return (uu**2 + vv**2)**.5 

class WindModulus(Plugin):
    plugin_mandatory_dependencies = {
        'UU':{'nomvar':'UU','unit':'knot'},
        'VV':{'nomvar':'VV','unit':'knot'},
    }
    plugin_result_specifications = {'UV':{'nomvar':'UV','etiket':'WindModulus','unit':'knot'}}

    def __init__(self,df:pd.DataFrame):
        self.df = df
        #ajouter forecast_hour et unit
        self.validate_input()
        
    # might be able to move    
    def validate_input(self):
        if self.df.empty:
            raise  WindModulusError( "WindModulus" + ' - no data to process')
        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies)
            
            # self.df = self.df.query( 'nomvar==%s'%self.plugin_mandatory_dependencies)
            level_intersection_df = get_intersecting_levels(self.df,self.plugin_mandatory_dependencies)
            # print('intersecting levels',level_intersection_df)
            if level_intersection_df.empty:
                raise  WindModulusError( "WindModulus" + ' - no data to process')
            # if level_intersection_df.empty:
            #     raise WindModulusError('cant find intersecting levels between UU and VV')
            level_intersection_df = fstpy.load_data(level_intersection_df)
            #group by grid/forecast hour    
            # self.fhour_groups = fstpy.get_groups(level_intersection_df,group_by_forecast_hour=True)
            self.fhour_groups = level_intersection_df.groupby(['grid','forecast_hour'])

            

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return self.existing_result_df
        results = []

        for _,current_fhour_group in self.fhour_groups:
            # current_fhour_group = current_fhour_group.reset_index(drop=True)
            # print('-1-','\n',current_fhour_group[['nomvar','level','forecast_hour']])        
            uudf = current_fhour_group.query('nomvar == "UU"').reset_index(drop=True)
            vvdf = current_fhour_group.query('nomvar == "VV"').reset_index(drop=True)
            uv_df = vvdf.copy(deep=True)
            #recipe: zap with dict
            for k,v in self.plugin_result_specifications['UV'].items():uv_df[k] = v
            # uv_df = fstpy.zap(uv_df, **self.plugin_result_specifications['UV'])
            # print('---uv_df---\n',uv_df[['nomvar','etiket','unit']])
            # test = uv_df.replace(self.plugin_result_specifications['UV'])
            # print('---test---\n',test[['nomvar','etiket','unit']])
            # print('equality',uv_df.equals(test))
            for i in uv_df.index:
                uu = uudf.at[i,'d']
                vv = vvdf.at[i,'d']
                uv_df.at[i,'d'] = wind_modulus(uu,vv)
            results.append(uv_df)
        # merge all results together
        result = pd.concat(results, ignore_index=True)
        return result
    

