# -*- coding: utf-8 -*-
from ..plugin import Plugin
from .humidityutils.humidityutils import AEI1, AEI2, AEI3, AEW1, AEW2, AEW3, TDPACK_OFFSET_FIX
from ..utils import get_existing_result, get_intersecting_levels, get_plugin_dependencies, initializer, prepare_existing_results, remove_load_data_info
import pandas as pd
import numpy as np
from math import exp
import fstpy.all as fstpy
from rpnpy.utils.tdpack import FOEWA, FOEW
import sys

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
            raise  VapourPressureError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True) 
            
        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies)
            
            # self.df = self.df.query( 'nomvar==%s'%self.plugin_mandatory_dependencies).reset_index(drop=True)
            level_intersection_df = get_intersecting_levels(self.df,self.plugin_mandatory_dependencies)
            # print('intersecting levels',level_intersection_df)
            if level_intersection_df.empty:
                raise  VapourPressureError('No data to process')
            # if level_intersection_df.empty:
            #     raise VapourPressureError('cant find intersecting levels between UU and VV')
            level_intersection_df = fstpy.load_data(level_intersection_df)
            #group by grid/forecast hour    
            # self.fhour_groups = fstpy.get_groups(level_intersection_df,group_by_forecast_hour=True)
            self.fhour_groups = level_intersection_df.groupby(['grid','forecast_hour'])


    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return prepare_existing_results('VapourPressure',self.existing_result_df,self.meta_df) 

        sys.stdout.write('VapourPressure - compute')
        df_list=[]
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
        
        if not len(df_list):
            raise VapourPressureError('No results were produced')

        self.meta_df = fstpy.load_data(self.meta_df)

        df_list.append(self.meta_df)    
        # merge all results together
        res_df = pd.concat(df_list,ignore_index=True)
        
        res_df = remove_load_data_info(res_df)
        res_df = fstpy.metadata_cleanup(res_df)
        
        return res_df

