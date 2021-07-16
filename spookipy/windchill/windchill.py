# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
from spookipy.utils import create_empty_result, get_existing_result, get_plugin_dependencies, remove_load_data_info
import pandas as pd
import numpy as np
import fstpy.all as fstpy


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
            raise  WindChillError( 'WindChil - no data to process')
        
        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','ip_info','forecast_hour'])
      

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies)
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','forecast_hour'])


    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            self.existing_result_df = fstpy.load_data(self.existing_result_df)
            self.meta_df = fstpy.load_data(self.meta_df)
            res_df = pd.concat([self.meta_df,self.existing_result_df],ignore_index=True)
            res_df  = remove_load_data_info(res_df)
            return res_df
        #holds data from all the groups
        df_list = []
        for _,current_fhour_group in self.fhour_groups:
            current_fhour_group = fstpy.load_data(current_fhour_group)
            
            #print('-1-','\n',current_fhour_group[['nomvar','level','fhour']])        
            tt_df = current_fhour_group.query('nomvar == "TT"').reset_index(drop=True)
            uv_df = current_fhour_group.query('nomvar == "UV"').reset_index(drop=True)
            uv_df = fstpy.unit_convert(uv_df,'kilometer_per_hour')
            re_df = create_empty_result(tt_df,self.plugin_result_specifications['RE'])
            
            for i in re_df.index:
                tt = (tt_df.at[i,'d'])
                uv = (uv_df.at[i,'d'])
                re_df.at[i,'d'] = wind_chill(tt,uv)

            df_list.append(re_df)

        if not len(df_list):
            raise WindChillError('WindChill - no results where produced')

        self.meta_df = fstpy.load_data(self.meta_df)

        df_list.append(self.meta_df)    
        # merge all results together
        res_df = pd.concat(df_list,ignore_index=True)

        res_df = remove_load_data_info(res_df)
        res_df = fstpy.metadata_cleanup(res_df)

        return res_df

