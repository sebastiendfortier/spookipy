# -*- coding: utf-8 -*-
from numpy import float32
from ..plugin.plugin import Plugin
import pandas as pd
from math import exp
from ..utils import create_empty_result, get_existing_result, get_plugin_dependencies, initializer, existing_results, final_results
from spookipy.humidityutils.humidityutils import calc_saturation_vapour_pressure, get_temp_phase_switch, TDPACK_OFFSET_FIX, rpn_calc_saturation_vapour_pressure, validate_humidity_parameters
import fstpy.all as fstpy
import sys



class SaturationVapourPressureError(Exception):
    pass

class SaturationVapourPressure(Plugin):
    plugin_mandatory_dependencies = {
        'TT':{'nomvar':'TT','unit':'celsius'},
    }

    plugin_result_specifications = {
        'SVP':{'nomvar':'SVP','etiket':'SaturationVapourPressure','unit':'hectoPascal','nbits':16,'datyp':1},
        }

    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise SaturationVapourPressureError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(SaturationVapourPressureError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)


        self.temp_phase_switch = get_temp_phase_switch(SaturationVapourPressureError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)


        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies)
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('SaturationVapourPressure',self.existing_result_df,self.meta_df)

        sys.stdout.write('SaturationVapourPressure - compute\n')
        df_list=[]
        for _, current_fhour_group in self.fhour_groups:
            current_fhour_group = fstpy.load_data(current_fhour_group)
            tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
            svp_df = create_empty_result(tt_df,self.plugin_result_specifications['SVP'],copy=True)

            if self.rpn:
                print('rpn')
                print('option 1')
                tt_df = fstpy.unit_convert(tt_df,'kelvin')
                for i in svp_df.index:
                    tt = tt_df.at[i,'d']
                    svp_df.at[i,'d'] = rpn_calc_saturation_vapour_pressure(tt,self.temp_phase_switch,self.ice_water_phase=='both').astype(float32)
            else:
                print('option 1')
                for i in tt_df.index:
                    tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                    svp_df.at[i,'d'] = calc_saturation_vapour_pressure(tt,self.temp_phase_switch,self.ice_water_phase=='both').astype(float32)

            df_list.append(svp_df)


        return final_results(df_list,SaturationVapourPressureError, self.meta_df)
