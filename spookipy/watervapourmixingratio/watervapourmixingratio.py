# -*- coding: utf-8 -*-
from numpy import float32
from ..humidityutils import calc_water_vapour_mixing_ratio_hu, calc_water_vapour_mixing_ratio_px_vppr, get_temp_phase_switch, validate_humidity_parameters
from ..plugin import Plugin
from ..utils import create_empty_result, get_existing_result, get_intersecting_levels, get_plugin_dependencies, initializer, existing_results, final_results
import pandas as pd
import fstpy.all as fstpy
import sys


class WaterVapourMixingRatioError(Exception):
    pass

class WaterVapourMixingRatio(Plugin):


    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}
        self.plugin_mandatory_dependencies_option_rpn1 = {
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram'},
            }
        self.plugin_mandatory_dependencies_option_1 = {
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_2 = {
            'VPPR':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
        }
        self.plugin_result_specifications = {
            'QV':{'nomvar':'QV','etiket':'WaterVapourMixingRatio','unit':'gram_per_kilogram','nbits':16,'datyp':1}
            }
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise  WaterVapourMixingRatioError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(WaterVapourMixingRatioError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(WaterVapourMixingRatioError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)


        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)
        if self.existing_result_df.empty:
            if self.rpn:
                self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_rpn1)
                self.option=1
            else:
                self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_1,throw_error=False)
                self.option=1
                if self.dependencies_df.empty:
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_2)
                    self.option=2




            #current_fhour_group by grid/forecast hour
            self.fhour_groups = self.dependencies_df.groupby(['grid','forecast_hour'])



    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('WaterVapourMixingRatio',self.existing_result_df,self.meta_df)

        sys.stdout.write('WaterVapourMixingRatio - compute\n')
        df_list = []
        for _, current_fhour_group in self.fhour_groups:

            if self.option==1:
                print('option 1')
                current_fhour_group = fstpy.load_data(current_fhour_group)
                hu_df = current_fhour_group.loc[current_fhour_group.nomvar=='HU'].reset_index(drop=True)

                qv_df = create_empty_result(hu_df,self.plugin_result_specifications['QV'],copy=True)
                for i in qv_df.index:
                    hu = hu_df.at[i,'d']
                    qv_df.at[i,'d'] = calc_water_vapour_mixing_ratio_hu(hu).astype(float32)
            else:
                print('option 2')
                level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_2)
                current_fhour_group = fstpy.load_data(level_intersection_df)
                vppr_df = current_fhour_group.loc[current_fhour_group.nomvar=='VPPR'].reset_index(drop=True)
                px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].reset_index(drop=True)
                qv_df = create_empty_result(vppr_df,self.plugin_result_specifications['QV'],copy=True)
                vppr_df = fstpy.unit_convert(vppr_df,'pascal')
                px_df = fstpy.unit_convert(px_df,'pascal')
                for i in qv_df.index:
                    vppr = vppr_df.at[i,'d']
                    px = px_df.at[i,'d']
                    qv_df.at[i,'d'] = calc_water_vapour_mixing_ratio_px_vppr(px,vppr).astype(float32)

            df_list.append(qv_df)

        return final_results(df_list, WaterVapourMixingRatioError, self.meta_df)
