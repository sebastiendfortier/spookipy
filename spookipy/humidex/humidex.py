# -*- coding: utf-8 -*-
from ..utils import create_empty_result, get_existing_result, get_plugin_dependencies, initializer, prepare_existing_results, remove_load_data_info
from ..plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
import numpy as np
import sys


# Calculates the Humidex (HMX) from the Temperature (TT) and the Temperature Dew Point (TD) and the Satuvation Vapour Pressure (SVP).
# @param vppr  ; Temperature (TT) , Temperature Dew Point (TD), Satuvation Vapour Pressure (SVP)
# @return 		; HMX (celsius)

def humidex(tt:np.ndarray, svp:np.ndarray) -> np.ndarray:
    hmx = tt + (0.55555 * (svp - 10))
    return np.where(hmx > tt, hmx, tt)
    

class HumidexError(Exception):
    pass
class Humidex(Plugin):
    plugin_mandatory_dependencies = {
        'TT':{'nomvar':'TT','unit':'celsius','surface':True},
        'SVP':{'nomvar':'SVP','unit':'hectoPascal','surface':True},
    }
    plugin_result_specifications = {
        'HMX':{'nomvar':'HMX','etiket':'Humidex','unit':'celsius','ip1':0}
        }

    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase='water', temp_phase_switch='',rpn=False):
        self.validate_input()
        
    def validate_input(self):
        if self.df.empty:
            raise HumidexError('No data to process') 

        self.df = fstpy.metadata_cleanup(self.df)
            
        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])     
        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies)
            print('self.dependencies_df',self.dependencies_df['nomvar'].to_string())
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return prepare_existing_results('Humidex',self.existing_result_df,self.meta_df)

        sys.stdout.write('Humidex - compute')
        df_list=[]
        for _, current_fhour_group in self.fhour_groups:
            current_fhour_group = fstpy.load_data(current_fhour_group)
            tt_df = current_fhour_group.query('(nomvar=="TT")').reset_index(drop=True)
            svp_df = current_fhour_group.query('(nomvar=="SVP")').reset_index(drop=True)
            
            hmx_df = create_empty_result(svp_df, self.plugin_result_specifications['HMX'])
            
            for i in hmx_df.index:
                hmx_df.at[i,'d'] = humidex(tt_df,svp_df)

            df_list.append(hmx_df)

        if not len(df_list):
            raise HumidexError('No results were produced')

        self.meta_df = fstpy.load_data(self.meta_df)
        df_list.append(self.meta_df)    
        # merge all results together
        res_df = pd.concat(df_list,ignore_index=True)

        res_df = remove_load_data_info(res_df)
        res_df = fstpy.metadata_cleanup(res_df)

        return res_df