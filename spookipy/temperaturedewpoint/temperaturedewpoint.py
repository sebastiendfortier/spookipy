# -*- coding: utf-8 -*-
from numpy import float32
from ..plugin import Plugin
from ..utils import create_empty_result, get_existing_result, get_intersecting_levels, get_plugin_dependencies, initializer, existing_results, final_results
from ..humidityutils import TDPACK_OFFSET_FIX, calc_temperature_dew_point_es, calc_temperature_dew_point_vppr, get_temp_phase_switch, validate_humidity_parameters
import pandas as pd
import fstpy.all as fstpy
import sys

class TemperatureDewPointError(Exception):
    pass


class TemperatureDewPoint(Plugin):


    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}
        self.plugin_mandatory_dependencies_option_rpn1 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
        }
        self.plugin_mandatory_dependencies_option_rpn2 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
        }
        self.plugin_mandatory_dependencies_option_rpn3 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
        }
        self.plugin_mandatory_dependencies_option_rpn4 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'ES':{'nomvar':'ES','unit':'celsius','select_only':True}
        }
        self.plugin_mandatory_dependencies_option_1 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
        }
        self.plugin_mandatory_dependencies_option_2 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
        }
        self.plugin_mandatory_dependencies_option_3 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
        }
        self.plugin_mandatory_dependencies_option_4 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'ES':{'nomvar':'ES','unit':'celsius','select_only':True}
        }
        self.plugin_result_specifications = {
            'TD':{'nomvar':'TD','etiket':'TemperatureDewPoint','unit':'celsius'}
            }
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise TemperatureDewPointError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(TemperatureDewPointError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)


        self.temp_phase_switch = get_temp_phase_switch(TemperatureDewPointError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)

        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)
        if self.existing_result_df.empty:
            if self.rpn:
                self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_rpn1,throw_error=False)
                self.option=1
                if self.dependencies_df.empty:
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_rpn2,throw_error=False)
                    self.option=2
                if self.dependencies_df.empty:
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_rpn3,throw_error=False)
                    self.option=3
                if self.dependencies_df.empty:
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_rpn4)
                    self.option=4
            else:
                self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_1,throw_error=False)
                self.option=1
                if self.dependencies_df.empty:
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_2,throw_error=False)
                    self.option=2
                if self.dependencies_df.empty:
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_3,throw_error=False)
                    self.option=3
                if self.dependencies_df.empty:
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_4)
                    self.option=4

            self.fhour_groups = self.dependencies_df.groupby(['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        from ..all import DewPointDepression, SaturationVapourPressure, VapourPressure
        if not self.existing_result_df.empty:
            return existing_results('TemperatureDewPoint',self.existing_result_df,self.meta_df)

        sys.stdout.write('TemperatureDewPoint - compute\n')
        df_list=[]
        for _, current_fhour_group in self.fhour_groups:
            if self.rpn:
                print('rpn')
                if self.option==1:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn1)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],copy=True)
                    es_df = DewPointDepression(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit,rpn=True).compute()
                    es_df = es_df.loc[es_df.nomvar=='ES'].reset_index(drop=True)
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        es = es_df.at[i,'d']
                        td_df.at[i,'d'] = calc_temperature_dew_point_es(tt, es).astype(float32)

                elif self.option==2:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn2)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],copy=True)
                    es_df = DewPointDepression(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit,rpn=True).compute()
                    es_df = es_df.loc[es_df.nomvar=='ES'].reset_index(drop=True)
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        es = es_df.at[i,'d']
                        td_df.at[i,'d'] = calc_temperature_dew_point_es(tt, es).astype(float32)

                elif self.option==3:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn3)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],copy=True)
                    es_df = DewPointDepression(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit,rpn=True).compute()
                    es_df = es_df.loc[es_df.nomvar=='ES'].reset_index(drop=True)
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        es = es_df.at[i,'d']
                        td_df.at[i,'d'] = calc_temperature_dew_point_es(tt, es).astype(float32)

                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn4)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    es_df = level_intersection_df.query( '(nomvar=="ES")').reset_index(drop=True)
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],copy=True)
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        es = es_df.at[i,'d']
                        td_df.at[i,'d'] = calc_temperature_dew_point_es(tt, es).astype(float32)

            else:
                if self.option==1:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_1)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],copy=True)
                    vppr_df = VapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = vppr_df.loc[vppr_df.nomvar=='VPPR']
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        vppr = vppr_df.at[i,'d']
                        td_df.at[i,'d'] = calc_temperature_dew_point_vppr(tt,vppr,self.temp_phase_switch,self.ice_water_phase=='both').astype(float32)

                elif self.option==2:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_2)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],copy=True)
                    vppr_df = VapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = vppr_df.loc[vppr_df.nomvar=='VPPR']
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        vppr = vppr_df.at[i,'d']
                        td_df.at[i,'d'] = calc_temperature_dew_point_vppr(tt,vppr,self.temp_phase_switch,self.ice_water_phase=='both').astype(float32)

                elif self.option==3:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_3)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],copy=True)
                    svp_df = SaturationVapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    svp_df = svp_df.loc[svp_df.nomvar=='SVP']
                    vppr_df = VapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = vppr_df.loc[vppr_df.nomvar=='VPPR']
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        vppr = vppr_df.at[i,'d']
                        td_df.at[i,'d'] = calc_temperature_dew_point_vppr(tt,vppr,self.temp_phase_switch,self.ice_water_phase=='both').astype(float32)

                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_4)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    es_df = level_intersection_df.query( '(nomvar=="ES")').reset_index(drop=True)
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],copy=True)
                    vppr_df = VapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = vppr_df.loc[vppr_df.nomvar=='VPPR']
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        vppr = vppr_df.at[i,'d']
                        td_df.at[i,'d'] = calc_temperature_dew_point_vppr(tt,vppr,self.temp_phase_switch,self.ice_water_phase=='both').astype(float32)

            df_list.append(td_df)

        return final_results(df_list,TemperatureDewPointError, self.meta_df)
