# -*- coding: utf-8 -*-
from ..plugin import Plugin
import pandas as pd
import numpy as np
from math import exp
from rpnpy.utils.tdpack import FOEWA, FOEW
from ..utils import create_empty_result, get_existing_result, get_plugin_dependencies, initializer, remove_load_data_info
from spookipy.humidityutils.humidityutils import get_temp_phase_switch, TDPACK_OFFSET_FIX, AEW1, AEW2, AEW3, AEI1, AEI2, AEI3
import fstpy.all as fstpy

class SaturationVapourPressureError(Exception):
    pass

class SaturationVapourPressure(Plugin):
    plugin_mandatory_dependencies = {
        'TT':{'nomvar':'TT','unit':'celsius'},
    }
    
    plugin_result_specifications = {
        'SVP':{'nomvar':'SVP','etiket':'SaturationVapourPressure','unit':'hectoPascal','nbits':16,'datyp':1},
        }

    valid_units = ['celsius','kelvin']

    valid_phases = ['water','both']

    vfoewa = np.vectorize(FOEWA,otypes=['float32'])
    vfoew = np.vectorize(FOEW,otypes=['float32'])

    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase='water', temp_phase_switch=-99999,temp_phase_switch_unit='celsius', rpn=False):
        self.validate_input()
        
    def validate_input(self):
        if self.df.empty:
            raise SaturationVapourPressureError('No data to process') 

        self.df = fstpy.metadata_cleanup(self.df)    

        # if self.ice_water_phase == 'both':
        #     if self.temp_phase_switch==-99999:
        #         raise SaturationVapourPressureError(f'SaturationVapourPressure - cant use ice_water_phase="both" without defining temp_phase_switch and temp_phase_switch_unit')     

        if self.temp_phase_switch_unit not in self.valid_units:
            raise SaturationVapourPressureError(f'Invalid unit {self.temp_phase_switch_unit} not in {self.valid_units}') 

        if self.ice_water_phase not in self.valid_phases:
            raise SaturationVapourPressureError(f'Invalid unit {self.ice_water_phase} not in {self.valid_phases}') 

        self.temp_phase_switch = get_temp_phase_switch('SaturationVapourPressure', SaturationVapourPressureError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])     
        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies)
            # print('self.dependencies_df\n',self.dependencies_df)
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            self.existing_result_df = fstpy.load_data(self.existing_result_df)
            self.meta_df = fstpy.load_data(self.meta_df)
            res_df = pd.concat([self.meta_df,self.existing_result_df],ignore_index=True)
            res_df  = remove_load_data_info(res_df)
            return res_df

        df_list=[]
        for _, current_fhour_group in self.fhour_groups:
            current_fhour_group = fstpy.load_data(current_fhour_group)

            tt_df = current_fhour_group.query( '(nomvar=="TT")').reset_index(drop=True)
            svp_df = create_empty_result(tt_df,self.plugin_result_specifications['SVP'],copy=True)

            ice_water_phase_both=(self.ice_water_phase=='both')
            if self.rpn:
                for i in tt_df.index:
                    tt_df.at[i,'d'] = fstpy.unit_convert_array(tt_df.at[i,'d'], 'celsius','kelvin')#self.celsius_to_kelvin(tt_df.at[i,'d'])
                    tt = tt_df.at[i,'d']
                    svp_df.at[i,'d'] = np.where( not ice_water_phase_both or (ice_water_phase_both and tt > self.temp_phase_switch),
                    self.vfoewa(tt) / 100.0, self.vfoew(tt) / 100.0)
            else:
                for i in tt_df.index:
                    tt_df.at[i,'d'] = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                    tt = tt_df.at[i,'d']

                    if not ice_water_phase_both:
                        svp_df.at[i,'d'] = np.exp((tt * AEW2) / (tt + AEW3)) * AEW1
                        # svp_df.at[i,'d'] = aew1 * np.exp((aew2 * tt) / (aew3 + tt))
                    elif ice_water_phase_both:
                        svp_df.at[i,'d'] = np.where(tt > self.temp_phase_switch, np.exp((tt * AEW2) / (tt + AEW3)) * AEW1, np.exp((tt * AEI2) / (tt + AEI3)) * AEI1)
                        # svp_df.at[i,'d'] = np.where(tt > self.temp_phase_switch, aew1 * np.exp((aew2 * tt) / (aew3 + tt)), aei1 * np.exp((aei2 * tt) / (aei3 + tt)))
                    # svp_df.at[i,'d'] = np.where( np.invert(wpboth) or (wpboth and tt > self.temp_phase_switch)), 
                    # aew1 * np.exp((aew2 * tt) / (aew3 + tt)), 
                    # aei1 * np.exp((aei2 * tt) / (aei3 + tt))
            df_list.append(svp_df)

        if not len(df_list):
            raise SaturationVapourPressureError('No results were produced')

        self.meta_df = fstpy.load_data(self.meta_df)
        df_list.append(self.meta_df)    
        # merge all results together
        res_df = pd.concat(df_list,ignore_index=True)

        res_df = remove_load_data_info(res_df)
        res_df = fstpy.metadata_cleanup(res_df)
        print(res_df[['nomvar','d']])
        return res_df


    
    