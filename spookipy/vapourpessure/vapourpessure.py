# -*- coding: utf-8 -*-
from spookipy.saturationvapourpressure.saturationvapourpressure import SaturationVapourPressure
from spookipy.humidityspecific.humidityspecific import HumiditySpecific
from ..plugin.plugin import Plugin
from ..humidityutils.humidityutils import TDPACK_OFFSET_FIX, calc_temperature_dew_point_es, calc_vapour_pressure_hr, calc_vapour_pressure_hu, calc_vapour_pressure_qv, calc_vapour_pressure_td, get_temp_phase_switch, rpn_calc_vapour_pressure_hu, rpn_calc_vapour_pressure_td, validate_humidity_parameters
from ..utils import create_empty_result, get_existing_result, get_intersecting_levels, get_plugin_dependencies, initializer, existing_results, final_results
import pandas as pd
import fstpy.all as fstpy
import sys

class VapourPressureError(Exception):
    pass

class VapourPressure(Plugin):

    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}
        self.plugin_mandatory_dependencies_option_rpn1 = { 
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
        }
        self.plugin_mandatory_dependencies_option_rpn2 = {
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
            'ES':{'nomvar':'ES','unit':'celsius','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_rpn5 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_1 = { 
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
        }
        self.plugin_mandatory_dependencies_option_2 = { 
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
        }
        self.plugin_mandatory_dependencies_option_3 = { 
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_4 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'ES':{'nomvar':'ES','unit':'celsius','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_5 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
        }
        self.plugin_result_specifications = {
            'VPPR':{'nomvar':'VPPR','etiket':'VapourPressure','unit':'hectoPascal','nbits':16,'datyp':1}
            }
        self.validate_input()

    # might be able to move    
    def validate_input(self):
        if self.df.empty:
            raise  VapourPressureError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)    

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])     

        validate_humidity_parameters(VapourPressureError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(VapourPressureError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)

        
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
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_rpn4,throw_error=False)
                    self.option=4
                if self.dependencies_df.empty:
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_rpn5)
                    self.option=5
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
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_4,throw_error=False)
                    self.option=4
                if self.dependencies_df.empty:
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_5)
                    self.option=5


            
        #current_fhour_group by grid/forecast hour    
        self.fhour_groups = self.dependencies_df.groupby(['grid','forecast_hour'])


    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('VapourPressure',self.existing_result_df,self.meta_df) 

        sys.stdout.write('VapourPressure - compute\n')
        df_list=[]
        for _, current_fhour_group in self.fhour_groups:
            if self.rpn:
                print('rpn')
                if self.option==1:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn1)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    hu_df = level_intersection_df.query( '(nomvar=="HU")').reset_index(drop=True)
                    px_df = level_intersection_df.query( '(nomvar=="PX")').reset_index(drop=True)
                    vppr_df = create_empty_result(hu_df,self.plugin_result_specifications['VPPR'],copy=True)
                    px_df = fstpy.unit_convert(px_df,'pascal')
                    for i in vppr_df.index:
                        hu = hu_df.at[i,'d']
                        px = px_df.at[i,'d']
                        vppr_df.at[i,'d'] = rpn_calc_vapour_pressure_hu(hu, px)

                elif self.option==2:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn2)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    qv_df = level_intersection_df.query( '(nomvar=="QV")').reset_index(drop=True)
                    px_df = level_intersection_df.query( '(nomvar=="PX")').reset_index(drop=True)
                    vppr_df = create_empty_result(qv_df,self.plugin_result_specifications['VPPR'],copy=True)
                    qv_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
                    for i in vppr_df.index:
                        qv = qv_df.at[i,'d']
                        px = px_df.at[i,'d']
                        vppr_df.at[i,'d'] = calc_vapour_pressure_qv(qv, px)

                elif self.option==3:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn3)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( 'nomvar=="TT"').reset_index(drop=True)
                    hr_df = level_intersection_df.query( 'nomvar=="HR"').reset_index(drop=True)
                    px_df = level_intersection_df.query( '(nomvar=="PX")').reset_index(drop=True)
                    vppr_df = create_empty_result(tt_df,self.plugin_result_specifications['VPPR'],copy=True)
                    hu_df = HumiditySpecific(pd.concat([tt_df,hr_df,px_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,rpn=True).compute()
                    hu_df = hu_df.loc[hu_df.nomvar=='HU'].reset_index(drop=True)
                    px_df = fstpy.unit_convert(px_df,'pascal')
                    for i in vppr_df.index:
                        hu =  hu_df.at[i,'d']
                        px = px_df.at[i,'d']
                        vppr_df.at[i,'d'] = rpn_calc_vapour_pressure_hu(hu, px)

                elif self.option==4:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn4)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    es_df = level_intersection_df.query( '(nomvar=="ES")').reset_index(drop=True)
                    vppr_df = create_empty_result(es_df,self.plugin_result_specifications['VPPR'],copy=True)
                    tt_df = fstpy.unit_convert(tt_df,'kelvin')
                    for i in vppr_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        es = es_df.at[i,'d']
                        vppr_df.at[i,'d'] = calc_temperature_dew_point_es(tt, es)
                else:
                    print('option 5')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn5)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    td_df = level_intersection_df.query( '(nomvar=="TD")').reset_index(drop=True)
                    vppr_df = create_empty_result(tt_df,self.plugin_result_specifications['VPPR'],copy=True)
                    tt_df = fstpy.unit_convert(tt_df,'kelvin')
                    td_df = fstpy.unit_convert(td_df,'kelvin')
                    for i in vppr_df.index:
                        tt = tt_df.at[i,'d']
                        td = td_df.at[i,'d']
                        vppr_df.at[i,'d'] = rpn_calc_vapour_pressure_td(td, tt, self.temp_phase_switch, self.ice_water_phase=='both')

            else:
                if self.option==1:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_1)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    hu_df = level_intersection_df.query( '(nomvar=="HU")').reset_index(drop=True)
                    px_df = level_intersection_df.query( '(nomvar=="PX")').reset_index(drop=True)
                    vppr_df = create_empty_result(hu_df,self.plugin_result_specifications['VPPR'],copy=True)
                    for i in vppr_df.index:
                        hu = hu_df.at[i,'d']
                        px = px_df.at[i,'d']
                        vppr_df.at[i,'d'] = calc_vapour_pressure_hu(hu, px)

                elif self.option==2:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_2)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    qv_df = level_intersection_df.query( '(nomvar=="QV")').reset_index(drop=True)
                    px_df = level_intersection_df.query( '(nomvar=="PX")').reset_index(drop=True)
                    vppr_df = create_empty_result(qv_df,self.plugin_result_specifications['VPPR'],copy=True)
                    qv_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
                    for i in vppr_df.index:
                        qv = qv_df.at[i,'d']
                        px = px_df.at[i,'d']
                        vppr_df.at[i,'d'] = calc_vapour_pressure_qv(qv, px)

                elif self.option==3:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_3)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( 'nomvar=="TT"').reset_index(drop=True)
                    hr_df = level_intersection_df.query( 'nomvar=="HR"').reset_index(drop=True)
                    vppr_df = create_empty_result(tt_df,self.plugin_result_specifications['VPPR'],copy=True)
                    svp_df = SaturationVapourPressure(pd.concat([tt_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    svp_df = svp_df.loc[svp_df.nomvar=='SVP'].reset_index(drop=True)
                    for i in vppr_df.index:
                        hr = hr_df.at[i,'d']
                        svp = svp_df.at[i,'d']
                        vppr_df.at[i,'d'] = calc_vapour_pressure_hr(hr,svp)

                elif self.option==4:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_4)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    es_df = level_intersection_df.query( '(nomvar=="ES")').reset_index(drop=True)
                    # print('level_intersection_df 4\n',level_intersection_df)
                    vppr_df = create_empty_result(es_df,self.plugin_result_specifications['VPPR'],copy=True)
                    for i in vppr_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        es = es_df.at[i,'d']
                        vppr_df.at[i,'d'] = calc_temperature_dew_point_es(tt, es)
                else:
                    print('option 5')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_5)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.query( '(nomvar=="TT")').reset_index(drop=True)
                    td_df = level_intersection_df.query( '(nomvar=="TD")').reset_index(drop=True)
                    # print('level_intersection_df 5\n',level_intersection_df)
                    vppr_df = create_empty_result(tt_df,self.plugin_result_specifications['VPPR'],copy=True)
                    for i in vppr_df.index:
                        tt = tt_df.at[i,'d']-TDPACK_OFFSET_FIX
                        td = td_df.at[i,'d']
                        vppr_df.at[i,'d'] = calc_vapour_pressure_td(td, tt, self.temp_phase_switch, self.ice_water_phase=='both')


            df_list.append(vppr_df)        

        return final_results(df_list, VapourPressureError, self.meta_df)
        