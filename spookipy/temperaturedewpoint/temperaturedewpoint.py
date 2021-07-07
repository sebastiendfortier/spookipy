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
    plugin_result_specifications = {'TD':{'nomvar':'TD','etiket':'TemperatureDewPoint','unit':'celsius'}}
    def __init__(self,df:pd.DataFrame, ice_water_phase_both=False, temp_phase_switch=-99999,temp_phase_switch_unit='celsius', rpn=False):
        if self.df.empty:
            raise TemperatureDewPointError('TemperatureDewPoint - no data to process')

        self.temp_phase_switch = get_temp_phase_switch('TemperatureDewPoint', TemperatureDewPointError, self.ice_water_phase_both, self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)
        self.df = self.df.query(self.plugin_requires)
        self.df = fstpy.load_data(self.df)
        intersect_ttes_df = get_intersecting_levels(self.df,['TT','ES'])
        intersect_ttvppr_df = get_intersecting_levels(self.df,['TT','VPPR'])
        if intersect_ttes_df.empty and intersect_ttvppr_df.empty:
            sys.stderr.write('TemperatureDewPoint - cant find intersecting levels between TT and ES or VPPR')
            raise TemperatureDewPointError('cant find intersecting levels between TT and ES or VPPR')
        elif intersect_ttes_df.empty:
            self.groups= intersect_ttvppr_df.groupby(['grid','forecast_hour'])
        else:
            self.groups= intersect_ttes_df.groupby(['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        td_dfs=[]
        for _, group in self.groups:
            tt_df = group.query( '(nomvar=="TT") and (unit=="celsius")')
            esdf = group.query( '(nomvar=="ES") and (unit=="celsius")')
            vpprdf = group.query( '(nomvar=="VPPR") and (unit=="hectoPascal")')
            td_df = tt_df.copy(deep=True)
            # td_df = fstpy.zap(td_df,**self.plugin_result)
            for k,v in self.plugin_result_specifications['SVP'].items():td_df[k] = v
            for i in td_df.index:
                if esdf.empty:
                    #use vppr
                    #arr[arr > 255] = x
                    vpprdf.at[i,'d'] = vpprdf.at[i,'d'][vpprdf.at[i,'d'] < 10e-15] = 10e-15
                    td_df.at[i,'d'] = np.where( not self.ice_water_phase_both or (self.ice_water_phase_both and tt_df.at[i,'d'] > self.temp_phase_switch) ,
                    ( AEW3 * log(vpprdf.at[i,'d']/AEW1) ) / ( AEW2 - log(vpprdf.at[i,'d']/AEW1) ),
                    ( AEI3 * log(vpprdf.at[i,'d']/AEI1) ) / ( AEI2 - log(vpprdf.at[i,'d']/AEI1) ))
                else:
                    #use es
                    td_df.at[i,'d'] = np.where(esdf.at[i,'d']<0.0, tt_df.at[i,'d'], tt_df.at[i,'d']-esdf.at[i,'d'])

            td_dfs.append(td_df)
        res = pd.concat(td_dfs,ignore_index=True)
        return res