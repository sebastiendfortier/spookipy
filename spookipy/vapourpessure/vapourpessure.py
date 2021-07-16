# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
from spookipy.humidityutils.humidityutils import AEI1, AEI2, AEI3, AEW1, AEW2, AEW3, TDPACK_OFFSET_FIX
from spookipy.utils import get_existing_result, get_intersecting_levels, get_plugin_dependencies, initializer
import pandas as pd
import numpy as np
from math import exp
import fstpy.all as fstpy
from rpnpy.utils.tdpack import FOEWA, FOEW

class VapourPressureError(Exception):
    pass

class VapourPressure(Plugin):
    plugin_mandatory_dependencies_option_1 = {
        'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram'},
        'PX':{'nomvar':'PX','unit':'hectoPascal'},
    }
    plugin_mandatory_dependencies_option_2 = {
        'QV':{'nomvar':'QV','unit':'gram_per_kilogram'},
        'PX':{'nomvar':'PX','unit':'hectoPascal'},
    }
    plugin_mandatory_dependencies_option_3 = {
        'HR':{'nomvar':'HR','unit':'scalar'},
        'SVP':{'nomvar':'SVP','unit':'hectoPascal'},
    }
    plugin_mandatory_dependencies_option_4 = {
        'TT':{'nomvar':'TT','unit':'celsius'},
        'TD':{'nomvar':'TD','unit':'celsius'},
        'ES':{'nomvar':'ES','unit':'celsius'},
    }
    plugin_mandatory_dependencies_option_5 = {
        'TT':{'nomvar':'TT','unit':'celsius'},
        'TD':{'nomvar':'PX','unit':'celsius'},
    }

    plugin_result_specifications = {
        'VPPR':{'nomvar':'VPPR','etiket':'VapourPressure','unit':'hectoPascal'}
        }
    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase='water', temp_phase_switch='',rpn=False):
        self.validate_input()

    # might be able to move    
    def validate_input(self):
        if self.df.empty:
            raise  VapourPressureError( 'VapourPressure - no data to process')
        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies)
            
            # self.df = self.df.query( 'nomvar==%s'%self.plugin_mandatory_dependencies).reset_index(drop=True)
            level_intersection_df = get_intersecting_levels(self.df,self.plugin_mandatory_dependencies)
            # print('intersecting levels',level_intersection_df)
            if level_intersection_df.empty:
                raise  VapourPressureError( 'VapourPressure - no data to process')
            # if level_intersection_df.empty:
            #     raise VapourPressureError('cant find intersecting levels between UU and VV')
            level_intersection_df = fstpy.load_data(level_intersection_df)
            #group by grid/forecast hour    
            # self.fhour_groups = fstpy.get_groups(level_intersection_df,group_by_forecast_hour=True)
            self.fhour_groups = level_intersection_df.groupby(['grid','forecast_hour'])


    def compute(self) -> pd.DataFrame:
        vpprdfs=[]
        for _, group in self.groups:
            tddf = group.query( '(nomvar=="TD") and (unit=="celsius")').reset_index(drop=True)
            tt_df = group.query( '(nomvar=="TT") and (unit=="celsius")').reset_index(drop=True)
            vpprdf = tddf.copy(deep=True)
            # vpprdf = fstpy.zap(vpprdf,**self.plugin_result)
            for k,v in self.plugin_result_specifications['ALL'].items(): vpprdf[k] = v
            if self.rpn:
                tt_df['d'] = self.celsius_to_kelvin(tt_df['d'])
                tddf['d'] = self.celsius_to_kelvin(tddf['d'])
                vpprdf['d'] = np.where( (not self.ice_water_phase_both) or (self.ice_water_phase_both and (tt_df['d'] > self.temp_phase_switch)),
                FOEWA(tddf['d']) / 100.0,
                FOEW(tddf['d']) / 100.0)
            else:
                tt_df['d'] = tt_df['d']-TDPACK_OFFSET_FIX
                tddf['d'] = tddf['d']-TDPACK_OFFSET_FIX
                vpprdf['d'] = np.where( (not self.ice_water_phase_both) or (self.ice_water_phase_both and (tt_df['d'] > self.temp_phase_switch)),
                AEW1 * exp((AEW2 * tddf['d']) / (AEW3 + tddf['d'])),
                AEI1 * exp((AEI2 * tddf['d']) / (AEI3 + tddf['d'])))
        res = pd.concat(vpprdfs,ignore_index=True)
        return res

