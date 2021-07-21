# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
from spookipy.utils import get_intersecting_levels
from spookipy.humidityutils.humidityutils import AEI1, AEI2, AEI3, AEW1, AEW2, AEW3, get_temp_phase_switch
import pandas as pd
import numpy as np
from math import log
import fstpy.all as fstpy

class TemperatureDewPointError(Exception):
    pass

def temperature_dew_point(es,vppr,tt,ice_water_phase_both,temp_phase_switch):
    if es is None:
        vppr = np.where(vppr<10e-15,10e-15,vppr)
        td = np.where( not ice_water_phase_both or (ice_water_phase_both and tt > temp_phase_switch) ,
        ( AEW3 * log(vppr/AEW1) ) / ( AEW2 - log(vppr/AEW1) ),
        ( AEI3 * log(vppr/AEI1) ) / ( AEI2 - log(vppr/AEI1) ))
    else:
        td = np.where(es<0.0, tt, tt-es)
    return td

class TemperatureDewPoint(Plugin):
    plugin_requires = 'nomvar in ["TT","ES","VPPR"]' 
    # plugin_result = {'nomvar':'TD','etiket':'TemperatureDewPoint','unit':'celsius'}
    plugin_result_specifications = {
        'TD':{'nomvar':'TD','etiket':'TemperatureDewPoint','unit':'celsius'}
        }
    def __init__(self,df:pd.DataFrame, ice_water_phase_both=False, temp_phase_switch=-99999,temp_phase_switch_unit='celsius', rpn=False):
        if self.df.empty:
            raise TemperatureDewPointError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)
        
        self.temp_phase_switch = get_temp_phase_switch('TemperatureDewPoint', TemperatureDewPointError, self.ice_water_phase_both, self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)
        self.df = self.df.query(self.plugin_requires).reset_index(drop=True)
        self.df = fstpy.load_data(self.df)
        intersect_ttes_df = get_intersecting_levels(self.df,['TT','ES'])
        intersect_ttvppr_df = get_intersecting_levels(self.df,['TT','VPPR'])
        if intersect_ttes_df.empty and intersect_ttvppr_df.empty:
            sys.stderr.write('TemperatureDewPoint - cant find intersecting levels between TT and ES or VPPR')
            raise TemperatureDewPointError('Cannot find intersecting levels between TT and ES or VPPR')
        elif intersect_ttes_df.empty:
            self.groups= intersect_ttvppr_df.groupby(['grid','forecast_hour'])
        else:
            self.groups= intersect_ttes_df.groupby(['grid','forecast_hour'])

    def validate_input(self):
        pass

    def compute(self) -> pd.DataFrame:
        df_list=[]
        for _, group in self.groups:
            tt_df = group.query( '(nomvar=="TT") and (unit=="celsius")').reset_index(drop=True)
            es_df = group.query( '(nomvar=="ES") and (unit=="celsius")').reset_index(drop=True)
            vppr_df = group.query( '(nomvar=="VPPR") and (unit=="hectoPascal")').reset_index(drop=True)
            td_df = tt_df.copy(deep=True)
            # td_df = fstpy.zap(td_df,**self.plugin_result)
            for k,v in self.plugin_result_specifications['SVP'].items():td_df[k] = v
            for i in td_df.index:
                if es_df.empty:
                    #use vppr
                    #arr[arr > 255] = x
                    vppr_df.at[i,'d'] = vppr_df.at[i,'d'][vppr_df.at[i,'d'] < 10e-15] = 10e-15
                    td_df.at[i,'d'] = np.where( not self.ice_water_phase_both or (self.ice_water_phase_both and tt_df.at[i,'d'] > self.temp_phase_switch) ,
                    ( AEW3 * log(vppr_df.at[i,'d']/AEW1) ) / ( AEW2 - log(vppr_df.at[i,'d']/AEW1) ),
                    ( AEI3 * log(vppr_df.at[i,'d']/AEI1) ) / ( AEI2 - log(vppr_df.at[i,'d']/AEI1) ))
                else:
                    #use es
                    td_df.at[i,'d'] = np.where(es_df.at[i,'d']<0.0, tt_df.at[i,'d'], tt_df.at[i,'d']-es_df.at[i,'d'])

            df_list.append(td_df)
        res = pd.concat(df_list,ignore_index=True)
        return res