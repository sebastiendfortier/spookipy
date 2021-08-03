# -*- coding: utf-8 -*-
import sys

from numpy import float32
import fstpy.all as fstpy
import pandas as pd
from ..humidityutils.humidityutils import (
    TDPACK_OFFSET_FIX, calc_dew_point_depression_td, get_temp_phase_switch,
    rpn_calc_dew_point_depression_hr, rpn_calc_dew_point_depression_hu,
    validate_humidity_parameters)

from ..plugin.plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results,
                     get_existing_result, get_intersecting_levels,
                     get_plugin_dependencies, initializer)


class DewPointDepressionError(Exception):
    pass

class DewPointDepression(Plugin):


    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}
        self.plugin_mandatory_dependencies_option_rpn1 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
            }
        self.plugin_mandatory_dependencies_option_rpn2 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
        }
        self.plugin_mandatory_dependencies_option_rpn3 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
        }
        self.plugin_mandatory_dependencies_option_rpn4 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
        }

        self.plugin_mandatory_dependencies_option_1 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
            }
        self.plugin_mandatory_dependencies_option_2 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_3 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_4 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
        }


        self.plugin_result_specifications = {
            'ES':{'nomvar':'ES','etiket':'DewPointDepression','unit':'celsius','nbits':16,'datyp':1}
        }
        self.validate_input()


    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise DewPointDepressionError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(DewPointDepressionError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(DewPointDepressionError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        #check if result already exists
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
        from ..all import HumiditySpecific,TemperatureDewPoint
        if not self.existing_result_df.empty:
            return existing_results('DewPointDepression',self.existing_result_df,self.meta_df)

        sys.stdout.write('DewPointDepression - compute\n')
        df_list=[]
        for _, current_fhour_group in self.fhour_groups:
            if self.rpn:
                print('rpn')
                if self.option==1:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn1)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( 'nomvar=="TT"').reset_index(drop=True)
                    hu_df = level_intersection_df.query( 'nomvar=="HU"').reset_index(drop=True)
                    px_df = level_intersection_df.query( 'nomvar=="PX"').reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    tt_df = fstpy.unit_convert(tt_df,'kelvin')
                    px_df = fstpy.unit_convert(px_df,'pascal')
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']
                        px = px_df.at[i,'d']
                        hu = hu_df.at[i,'d']
                        es_df.at[i,'d'] = rpn_calc_dew_point_depression_hu(tt,hu,px,self.ice_water_phase=='both').astype(float32)
                elif self.option==2:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn2)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( 'nomvar=="TT"').reset_index(drop=True)
                    qv_df = level_intersection_df.query( 'nomvar=="QV"').reset_index(drop=True)
                    px_df = level_intersection_df.query( 'nomvar=="PX"').reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    hu_df = HumiditySpecific(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,rpn=True).compute()
                    hu_df = hu_df.loc[hu_df.nomvar=='HU'].reset_index(drop=True)
                    tt_df = fstpy.unit_convert(tt_df,'kelvin')
                    px_df = fstpy.unit_convert(px_df,'pascal')
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']
                        px = px_df.at[i,'d']
                        hu = hu_df.at[i,'d']
                        es_df.at[i,'d'] = rpn_calc_dew_point_depression_hu(tt,hu,px,self.ice_water_phase=='both').astype(float32)
                elif self.option==3:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn3)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( 'nomvar=="TT"').reset_index(drop=True)
                    hr_df = level_intersection_df.query( 'nomvar=="HR"').reset_index(drop=True)
                    px_df = level_intersection_df.query( 'nomvar=="PX"').reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    tt_df = fstpy.unit_convert(tt_df,'kelvin')
                    px_df = fstpy.unit_convert(px_df,'pascal')
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']
                        px = px_df.at[i,'d']
                        hr = hr_df.at[i,'d']
                        es_df.at[i,'d'] = rpn_calc_dew_point_depression_hr(tt,hr,px,self.ice_water_phase=='both').astype(float32)
                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn4)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( 'nomvar=="TT"').reset_index(drop=True)
                    td_df = level_intersection_df.query( 'nomvar=="TD"').reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    tt_df = fstpy.unit_convert(tt_df,'kelvin')
                    td_df = fstpy.unit_convert(td_df,'kelvin')
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        td = td_df.at[i,'d']-TDPACK_OFFSET_FIX
                        es_df.at[i,'d'] = calc_dew_point_depression_td(tt,td).astype(float32)
            else:
                if self.option==1:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_1)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( 'nomvar=="TT"').reset_index(drop=True)
                    hu_df = level_intersection_df.query( 'nomvar=="HU"').reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    td_df = TemperatureDewPoint(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    td_df = td_df.loc[td_df.nomvar=='TD'].reset_index(drop=True)
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        td = td_df.at[i,'d']-TDPACK_OFFSET_FIX
                        es_df.at[i,'d'] = calc_dew_point_depression_td(tt,td).astype(float32)


                elif self.option==2:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_2)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( 'nomvar=="TT"').reset_index(drop=True)
                    qv_df = level_intersection_df.query( 'nomvar=="QV"').reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    td_df = TemperatureDewPoint(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    td_df = td_df.loc[td_df.nomvar=='TD'].reset_index(drop=True)
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        td = td_df.at[i,'d']-TDPACK_OFFSET_FIX
                        es_df.at[i,'d'] = calc_dew_point_depression_td(tt,td).astype(float32)


                elif self.option==3:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_3)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( 'nomvar=="TT"').reset_index(drop=True)
                    hr_df = level_intersection_df.query( 'nomvar=="HR"').reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    td_df = TemperatureDewPoint(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    td_df = td_df.loc[td_df.nomvar=='TD'].reset_index(drop=True)
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        td = td_df.at[i,'d']-TDPACK_OFFSET_FIX
                        es_df.at[i,'d'] = calc_dew_point_depression_td(tt,td).astype(float32)

                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_4)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( 'nomvar=="TT"').reset_index(drop=True)
                    td_df = level_intersection_df.query( 'nomvar=="TD"').reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        td = td_df.at[i,'d']-TDPACK_OFFSET_FIX
                        es_df.at[i,'d'] = calc_dew_point_depression_td(tt,td).astype(float32)

            df_list.append(es_df)

        return final_results(df_list, DewPointDepression, self.meta_df)
