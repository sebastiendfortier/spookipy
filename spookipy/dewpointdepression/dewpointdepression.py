# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
from spookipy.utils import get_existing_result, get_intersecting_levels, get_plugin_dependencies
import pandas as pd
import numpy as np
import fstpy.all as fstpy

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

    def __init__(self,df:pd.DataFrame, ice_water_phase='water', temp_phase_switch='',rpn=False):
        self.df = df
        self.ice_water_phase = ice_water_phase
        self.temp_phase_switch = temp_phase_switch
        self.rpn = rpn
        self.validate_input()


    # might be able to move    
    def validate_input(self):
        if self.df.empty:
            raise DewPointDepressionError('DewPointDepression - no data to process') 
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
            return self.existing_result_df
        esdfs=[]
        for _, group in self.groups:
            if not self.option_1_df.empty: #TT,TD
                 pass

            group = fstpy.load_data(group)
            tt_df = group.query( 'nomvar=="TT"').reset_index(drop=True)
            tddf = group.query( 'nomvar=="TD"').reset_index(drop=True)
            esdf = tt_df.copy(deep=True)
            # esdf = fstpy.zap(esdf,**self.plugin_result_specifications['ES'])
            for k,v in self.plugin_result_specifications['ES'].items():esdf[k] = v
            for i in esdf.index:
                #ES = TT - TD  (if ES < 0.0 , ES = 0.0)
                esdf.at[i,'d'] = dew_point_depression( tt_df.at[i,'d'],tddf.at[i,'d'])
                # esdf.at[i,'d'] = tt_df.at[i,'d'] - tddf.at[i,'d']
                # esdf.at[i,'d'] = np.where(esdf.at[i,'d'] < 0.0, 0.0 )
                esdfs.append(esdf)
        res = pd.concat(esdfs,ignore_index=True)
        return res