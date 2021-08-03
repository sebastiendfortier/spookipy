# -*- coding: utf-8 -*-
from numpy import float32
from ..humidityutils.humidityutils import calc_humidity_relative_svp_vppr, get_temp_phase_switch, rpn_calc_humidity_relative_es, rpn_calc_humidity_relative_hu, validate_humidity_parameters
from ..plugin.plugin import Plugin
from ..utils import create_empty_result, get_existing_result, get_intersecting_levels, get_plugin_dependencies, initializer, existing_results, final_results
import pandas as pd
import fstpy.all as fstpy
import sys


class HumidityRelativeError(Exception):
    pass

class HumidityRelative(Plugin):


    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}

        self.plugin_mandatory_dependencies_option_rpn1 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_rpn2 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_rpn3 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
        }
        self.plugin_mandatory_dependencies_option_rpn4 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'ES':{'nomvar':'ES','unit':'celsius','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
        }
        self.plugin_mandatory_dependencies_option_1 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_2 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_3 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_4 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'ES':{'nomvar':'ES','unit':'celsius','select_only':True},
        }


        self.plugin_result_specifications = {
            'HR':{'nomvar':'HR','etiket':'HumidityRelative','unit':'scalar','nbits':12,'datyp':1}
            }
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise  HumidityRelativeError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(HumidityRelativeError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)


        self.temp_phase_switch = get_temp_phase_switch(HumidityRelativeError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

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

            #current_fhour_group by grid/forecast hour
            self.fhour_groups = self.dependencies_df.groupby(['grid','forecast_hour'])



    def compute(self) -> pd.DataFrame:
        from ..all import VapourPressure, SaturationVapourPressure, HumiditySpecific, DewPointDepression
        if not self.existing_result_df.empty:
            return existing_results('HumidityRelative',self.existing_result_df,self.meta_df)

        sys.stdout.write('HumidityRelative - compute\n')
        df_list = []
        for _, current_fhour_group in self.fhour_groups:
            if self.rpn:
                if self.option==1:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn1)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].reset_index(drop=True)
                    hu_df = current_fhour_group.loc[current_fhour_group.nomvar=='HU'].reset_index(drop=True)
                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],copy=True)
                    tt_df = fstpy.unit_convert(tt_df,'kelvin')
                    px_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hr_df.index:
                        tt = tt_df.at[i,'d']
                        px = px_df.at[i,'d']
                        hu = hu_df.at[i,'d']
                        hr_df.at[i,'d'] = rpn_calc_humidity_relative_hu(hu, tt, px, self.ice_water_phase=='both').astype(float32)
                        # hr_df.at[i,'d'] = calc_humidity_relative_svp_vppr(svp,vppr)

                elif self.option==2:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn2)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].reset_index(drop=True)

                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],copy=True)
                    hu_df = HumiditySpecific(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,rpn=True).compute()
                    hu_df = hu_df.loc[hu_df.nomvar=='HU'].reset_index(drop=True)
                    tt_df = fstpy.unit_convert(tt_df,'kelvin')
                    px_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hr_df.index:
                        tt = tt_df.at[i,'d']
                        px = px_df.at[i,'d']
                        hu = hu_df.at[i,'d']
                        hr_df.at[i,'d'] = rpn_calc_humidity_relative_hu(hu, tt, px, self.ice_water_phase=='both').astype(float32)
                        # hr_df.at[i,'d'] = calc_humidity_relative_svp_vppr(svp,vppr)

                elif self.option==3:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn3)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].reset_index(drop=True)

                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],copy=True)
                    es_df = DewPointDepression(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,rpn=True).compute()
                    es_df = es_df.loc[es_df.nomvar=='ES'].reset_index(drop=True)
                    tt_df = fstpy.unit_convert(tt_df,'kelvin')
                    px_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hr_df.index:
                        tt = tt_df.at[i,'d']
                        px = px_df.at[i,'d']
                        es = es_df.at[i,'d']
                        hr_df.at[i,'d'] = rpn_calc_humidity_relative_es(es, tt, px, self.ice_water_phase=='both').astype(float32)
                        # hr_df.at[i,'d'] = calc_humidity_relative_svp_vppr(svp,vppr)
                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn4)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].reset_index(drop=True)
                    es_df = current_fhour_group.loc[current_fhour_group.nomvar=='ES'].reset_index(drop=True)

                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],copy=True)
                    tt_df = fstpy.unit_convert(tt_df,'kelvin')
                    es_df = fstpy.unit_convert(es_df,'kelvin')
                    px_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hr_df.index:
                        tt = tt_df.at[i,'d']
                        px = px_df.at[i,'d']
                        es = es_df.at[i,'d']
                        hr_df.at[i,'d'] = rpn_calc_humidity_relative_es(es, tt, px, self.ice_water_phase=='both').astype(float32)
                        # hr_df.at[i,'d'] = calc_humidity_relative_svp_vppr(svp,vppr)
            else: # not rpn
                if self.option==1:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_1)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].reset_index(drop=True)
                    hu_df = current_fhour_group.loc[current_fhour_group.nomvar=='HU'].reset_index(drop=True)
                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],copy=True)
                    svp_df = SaturationVapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch).compute()
                    svp_df = svp_df.loc[svp_df.nomvar=='SVP'].reset_index(drop=True)
                    vppr_df = VapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch).compute()
                    vppr_df = vppr_df.loc[vppr_df.nomvar=='VPPR'].reset_index(drop=True)
                    for i in hr_df.index:
                        svp = svp_df.at[i,'d']
                        vppr = vppr_df.at[i,'d']
                        hr_df.at[i,'d'] = calc_humidity_relative_svp_vppr(svp,vppr).astype(float32)
                elif self.option==2:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_2)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].reset_index(drop=True)

                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],copy=True)
                    svp_df = SaturationVapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch).compute()
                    svp_df = svp_df.loc[svp_df.nomvar=='SVP'].reset_index(drop=True)
                    vppr_df = VapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch).compute()
                    vppr_df = vppr_df.loc[vppr_df.nomvar=='VPPR'].reset_index(drop=True)

                    for i in hr_df.index:
                        svp = svp_df.at[i,'d']
                        vppr = vppr_df.at[i,'d']
                        hr_df.at[i,'d'] = calc_humidity_relative_svp_vppr(svp,vppr).astype(float32)
                elif self.option==3:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_3)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)

                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],copy=True)
                    svp_df = SaturationVapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch).compute()
                    svp_df = svp_df.loc[svp_df.nomvar=='SVP'].reset_index(drop=True)
                    vppr_df = VapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch).compute()
                    vppr_df = vppr_df.loc[vppr_df.nomvar=='VPPR'].reset_index(drop=True)

                    for i in hr_df.index:
                        svp = svp_df.at[i,'d']
                        vppr = vppr_df.at[i,'d']
                        hr_df.at[i,'d'] = calc_humidity_relative_svp_vppr(svp,vppr).astype(float32)
                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_4)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                    es_df = current_fhour_group.loc[current_fhour_group.nomvar=='ES'].reset_index(drop=True)

                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],copy=True)
                    svp_df = SaturationVapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch).compute()
                    svp_df = svp_df.loc[svp_df.nomvar=='SVP'].reset_index(drop=True)
                    vppr_df = VapourPressure(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch).compute()
                    vppr_df = vppr_df.loc[vppr_df.nomvar=='VPPR'].reset_index(drop=True)
                    for i in hr_df.index:
                        svp = svp_df.at[i,'d']
                        vppr = vppr_df.at[i,'d']
                        hr_df.at[i,'d'] = calc_humidity_relative_svp_vppr(svp,vppr).astype(float32)

            df_list.append(hr_df)


        return final_results(df_list, HumidityRelativeError, self.meta_df)
