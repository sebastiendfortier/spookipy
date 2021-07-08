# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
import pandas as pd
import numpy as np
from math import exp
from rpnpy.utils.tdpack import FOEWA, FOEW
from spookipy.humidityutils.humidityutils import get_temp_phase_switch, TDPACK_OFFSET_FIX, AEW1, AEW2, AEW3, AEI1, AEI2, AEI3


class SaturationVapourPressureError(Exception):
    pass

class SaturationVapourPressure(Plugin):
    plugin_requires = 'nomvar =="TT"' 
    plugin_result_specifications = {'SVP':{'nomvar':'SVP','etiket':'SaturationVapourPressure','unit':'hectoPascal'}}
    
    def __init__(self,df:pd.DataFrame, ice_water_phase_both=False, temp_phase_switch=-99999,temp_phase_switch_unit='celsius', rpn=False):
        if df.empty:
            raise SaturationVapourPressureError('SaturationVapourPressure' + ' - no data to process') 
        self.temp_phase_switch = get_temp_phase_switch('SaturationVapourPressure', SaturationVapourPressureError, self.ice_water_phase_both, self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)
        self.df = self.df.query(self.plugin_requires).reset_index(drop=True)
        self.df = fstpy.load_data(self.df)
        self.groups= df.groupby(by=['grid','forecast_hour'])
        
    def compute(self) -> pd.DataFrame:
        kelvin = fstpy.get_unit_by_name('kelvin')
        celsius = fstpy.get_unit_by_name('celsius')
        self.celsius_to_kelvin = fstpy.get_converter(celsius,kelvin)
        svpdfs=[]
        for _, group in self.groups:
            tt_df = group.query( '(nomvar=="TT") and (unit=="celsius")').reset_index(drop=True)
            svp_df = tt_df.copy(deep=True)
            # svp_df = fstpy.zap(svp_df,**self.plugin_result_specifications)
            for k,v in self.plugin_result_specifications['SVP'].items():svp_df[k] = v
            if self.rpn:
                tt_df['d'] = self.celsius_to_kelvin(tt_df['d'])
                svp_df['d'] =np.where( not self.ice_water_phase_both or (self.ice_water_phase_both and tt_df['d'] > self.temp_phase_switch),
                FOEWA(tt_df['d']) / 100.0, 
                FOEW(tt_df['d']) / 100.0)
            else:
                tt_df['d'] = tt_df['d']-TDPACK_OFFSET_FIX
                svp_df['d'] = np.where( not self.ice_water_phase_both or (self.ice_water_phase_both and tt_df['d'] > self.temp_phase_switch)), 
                AEW1 * exp((AEW2 * tt_df['d']) / (AEW3 + tt_df['d'])), 
                AEI1 * exp((AEI2 * tt_df['d']) / (AEI3 + tt_df['d']))
            svpdfs.append(svp_df)
        res = pd.concat(svpdfs,ignore_index=True)
        return res


    
    