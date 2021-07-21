# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
from spookipy.utils import create_empty_result, get_existing_result, get_intersecting_levels, get_plugin_dependencies, initializer, remove_load_data_info
import pandas as pd
import numpy as np
import fstpy.all as fstpy
import sys

class DewPointDepressionError(Exception):
    pass

def dew_point_depression(tt:np.ndarray,td:np.ndarray) -> np.ndarray:
    es = tt - td
    es = np.where(es < 0.0, 0.0 )
    return es

class DewPointDepression(Plugin):
    plugin_mandatory_dependencies_option_1 = {
        'TT':{'nomvar':'TT','unit':'celsius'},
        'TD':{'nomvar':'TD','unit':'celsius'}
        }
    plugin_mandatory_dependencies_option_2 = {
        'PX':{'nomvar':'PX','unit':'hectoPascal'},
        'HR':{'nomvar':'HR','unit':'scalar'},
    }
    plugin_mandatory_dependencies_option_3 = {
        'PX':{'nomvar':'PX','unit':'hectoPascal'},
        'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram'},
    }

    plugin_result_specifications = {'ES':{'nomvar':'ES','etiket':'DewPointDepression','unit':'celsius','nbits':16,'datyp':1}}

    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase='water', temp_phase_switch='',rpn=False):
        self.validate_input()


    # might be able to move    
    def validate_input(self):
        if self.df.empty:
            raise DewPointDepressionError('No data to process') 

        self.df = fstpy.metadata_cleanup(self.df)    

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)    

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.option_1_df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies_option_1)
            self.option_1_df = get_intersecting_levels(self.option_1_df,self.plugin_mandatory_dependencies_option_1)
            if not self.option_1_df.empty:
                self.groups = self.option_1_df.groupby(by=['grid','forecast_hour'])
                return

            self.option_2_df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies_option_2)
            self.option_2_df = get_intersecting_levels(self.option_2_df,self.plugin_mandatory_dependencies_option_2)
            if not self.option_2_df.empty:
                self.groups = self.option_2_df.groupby(by=['grid','forecast_hour'])
                return

            self.option_3_df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies_option_3)
            self.option_3_df = get_intersecting_levels(self.option_3_df,self.plugin_mandatory_dependencies_option_3)
            if not self.option_3_df.empty:
                self.groups = self.option_3_df.groupby(by=['grid','forecast_hour'])
                return
   
            

    def compute(self) -> pd.DataFrame:
        
        if not self.existing_result_df.empty:
            sys.stdout.write('DewPointDepression - found results')
            self.existing_result_df = fstpy.load_data(self.existing_result_df)
            self.meta_df = fstpy.load_data(self.meta_df)
            res_df = pd.concat([self.meta_df,self.existing_result_df],ignore_index=True)
            res_df  = remove_load_data_info(res_df)
            res_df = fstpy.metadata_cleanup(res_df)    
            return res_df
        sys.stdout.write('DewPointDepression - compute')    
        df_list=[]
        for _, group in self.groups:
            if not self.option_1_df.empty: #TT,TD
                 pass

            group = fstpy.load_data(group)
            tt_df = group.query( 'nomvar=="TT"').reset_index(drop=True)
            td_df = group.query( 'nomvar=="TD"').reset_index(drop=True)
            es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
            
            for i in es_df.index:
                #ES = TT - TD  (if ES < 0.0 , ES = 0.0)
                es_df.at[i,'d'] = dew_point_depression( tt_df.at[i,'d'],td_df.at[i,'d'])
                # es_df.at[i,'d'] = tt_df.at[i,'d'] - td_df.at[i,'d']
                # es_df.at[i,'d'] = np.where(es_df.at[i,'d'] < 0.0, 0.0 )
                df_list.append(es_df)

        if not len(df_list):
            raise DewPointDepression('DewPointDepression - no results where produced')

        self.meta_df = fstpy.load_data(self.meta_df)
        df_list.append(self.meta_df)    
        # merge all results together
        res_df = pd.concat(df_list,ignore_index=True)

        res_df = remove_load_data_info(res_df)
        res_df = fstpy.metadata_cleanup(res_df)

        return res_df