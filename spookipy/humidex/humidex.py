# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
import pandas as pd
import fstpy.all as fstpy

class HumidexError(Exception):
    pass
class Humidex(Plugin):
    plugin_requires = 'nomvar in ["TT","TD"]' 
    plugin_result_specifications = {'HMX':{'nomvar':'HMX','etiket':'Humidex','unit':'celsius'}}

    def __init__(self,df:pd.DataFrame, ice_water_phase='water', temp_phase_switch='',rpn=False):
        self.df = df
        self.ice_water_phase = ice_water_phase
        self.temp_phase_switch = temp_phase_switch
        self.rpn = rpn
        if df.empty:
            raise HumidexError('Humidex - no data to process') 
        self.df = self.df.query(self.plugin_requires)
        self.df = fstpy.load_data(self.df)
        self.groups= df.groupby(by=['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        tddfs=[]
        for _, group in self.groups:
            tt850df = group.query( '(nomvar=="TT") and (level==850) and (pkind=="mb")')
            tt700df = group.query( '(nomvar=="TT") and (level==700) and (pkind=="mb")')
            tt500df = group.query( '(nomvar=="TT") and (level==500) and (pkind=="mb")')
            td850df = group.query( '(nomvar=="TD") and (level==850) and (pkind=="mb")')
            td700df = group.query( '(nomvar=="TD") and (level==700) and (pkind=="mb")')
            hmx_df = fstpy.create_1row_df_from_model(tt850df)
            # hmx_df = fstpy.zap(hmx_df,**self.plugin_result_specifications)
            for k,v in self.plugin_result_specifications['HMX'].items():hmx_df[k] = v
            hmx_df.iloc[0]['d'] = (tt850df.iloc[0]['d'] - tt500df.iloc[0]['d']) + td850df.iloc[0]['d'] - (tt700df.iloc[0]['d'] - td700df.iloc[0]['d'])
            tddfs.append(hmx_df)
        res = pd.concat(tddfs,ignore_index=True)
        return res