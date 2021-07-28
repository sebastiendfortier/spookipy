# -*- coding: utf-8 -*-
from ..plugin.plugin import Plugin
from ..utils import create_empty_result, get_existing_result, get_plugin_dependencies, existing_results, final_results
import pandas as pd
import numpy as np
import fstpy.all as fstpy
import sys

class WindChillError(Exception):
    pass

def wind_chill(tt:np.ndarray,uv:np.ndarray) ->np.ndarray:
    """Calculates the wind chill

    :param tt: surface temperature
    :type tt: np.ndarray
    :param uv: surface wind modulus
    :type uv: np.ndarray
    :return: wind chill
    :rtype: np.ndarray
    """
    return np.where( (tt <= 0) & (uv >= 5), 13.12 + 0.6215 * tt + ( 0.3965 * tt - 11.37) * ( uv**0.16 ), tt)

class WindChill(Plugin):
    plugin_mandatory_dependencies = {
        'UV':{'nomvar':'UV','unit':'knot','surface':True},
        'TT':{'nomvar':'TT','unit':'celsius','surface':True},
    }

    plugin_result_specifications = {
        'RE':{'nomvar':'RE','etiket':'WindChill','unit':'celsius','ip1':0}
        }
    
    def __init__(self,df:pd.DataFrame):
        self.df = df
        self.validate_input()
        
        
    # might be able to move    
    def validate_input(self):
        if self.df.empty:
            raise  WindChillError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)    
        
        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','ip_info','forecast_hour'])
      

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,None,self.plugin_mandatory_dependencies)
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','forecast_hour'])


    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('WindChill',self.existing_result_df,self.meta_df) 

        sys.stdout.write('WindChill - compute\n')    
        #holds data from all the groups
        df_list = []
        for _,current_fhour_group in self.fhour_groups:
            current_fhour_group = fstpy.load_data(current_fhour_group)
            tt_df = current_fhour_group.query('nomvar == "TT"').reset_index(drop=True)
            uv_df = current_fhour_group.query('nomvar == "UV"').reset_index(drop=True)
            uv_df = fstpy.unit_convert(uv_df,'kilometer_per_hour')
            re_df = create_empty_result(tt_df,self.plugin_result_specifications['RE'])
            
            for i in re_df.index:
                tt = (tt_df.at[i,'d'])
                uv = (uv_df.at[i,'d'])
                re_df.at[i,'d'] = wind_chill(tt,uv)

            df_list.append(re_df)

        return final_results(df_list,WindChillError, self.meta_df)


