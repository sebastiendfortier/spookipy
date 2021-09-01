# -*- coding: utf-8 -*-
import sys

import numpy as np
import fstpy.all as fstpy
import pandas as pd
from ..humidityutils import (
    TDPACK_OFFSET_FIX, get_temp_phase_switch,
    validate_humidity_parameters)

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results, find_matching_dependency_option,
                     get_existing_result, get_from_dataframe, get_intersecting_levels,
                     initializer)
from ..science.science import *

class DewPointDepressionError(Exception):
    pass

class DewPointDepression(Plugin):


    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}
        self.plugin_mandatory_dependencies_rpn = [
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'}
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'}
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'}
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
            }
        ]
        self.plugin_mandatory_dependencies = [
            {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
            },
            {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
            },
            {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
            },
            {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
            }
        ]


        self.plugin_result_specifications = {
            'ES':{'nomvar':'ES','etiket':'DEWPTD','unit':'celsius','nbits':16,'datyp':1}
        }
        self.validate_input()


    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise DewPointDepressionError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(self.df, decode=True, columns=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(DewPointDepressionError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(DewPointDepressionError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            if self.rpn:
                self.dependencies_df,self.option = find_matching_dependency_option(self.df,self.plugin_params,self.plugin_mandatory_dependencies_rpn)

            else:
                self.dependencies_df,self.option = find_matching_dependency_option(self.df,self.plugin_params,self.plugin_mandatory_dependencies)
                # for i in range(len(self.plugin_mandatory_dependencies)):
                #     self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies[i],throw_error=(False if i-1 < len(self.plugin_mandatory_dependencies) else True))
                #     self.option=i
                #     if not (self.dependencies_df.empty):
                #         break
                # self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_1,throw_error=False)
                # self.option=1
                # if self.dependencies_df.empty:
                #     self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_2,throw_error=False)
                #     self.option=2
                # if self.dependencies_df.empty:
                #     self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_3,throw_error=False)
                #     self.option=3
                # if self.dependencies_df.empty:
                #     self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_4)
                #     self.option=4

            self.fhour_groups = self.dependencies_df.groupby(['grid','forecast_hour'])





    def compute(self) -> pd.DataFrame:
        from ..humidityspecific.humidityspecific import HumiditySpecific
        from ..temperaturedewpoint.temperaturedewpoint import TemperatureDewPoint
        if not self.existing_result_df.empty:
            return existing_results('DewPointDepression',self.existing_result_df,self.meta_df)

        sys.stdout.write('DewPointDepression - compute\n')
        df_list=[]
        for _, current_fhour_group in self.fhour_groups:
            if self.rpn:
                print('rpn')
                if self.option==0:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_rpn[self.option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    hu_df = get_from_dataframe(level_intersection_df,'HU')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],all_rows=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in es_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        pxpa = pxpa_df.at[i,'d']
                        hu = hu_df.at[i,'d']
                        es_df.at[i,'d'] = science.rpn_es_from_hu(tt=ttk,hu=hu,px=pxpa,ni=ni,nj=nj,swph=self.ice_water_phase=='both').astype(np.float32)
                elif self.option==1:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_rpn[self.option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    qv_df = get_from_dataframe(level_intersection_df,'QV')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],all_rows=True)
                    hu_df = HumiditySpecific(level_intersection_df,ice_water_phase=self.ice_water_phase,rpn=True).compute()
                    hu_df = get_from_dataframe(hu_df,'HU')
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in es_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        pxpa = pxpa_df.at[i,'d']
                        hu = hu_df.at[i,'d']
                        es_df.at[i,'d'] = science.rpn_es_from_hu(tt=ttk,hu=hu,px=pxpa,ni=ni,nj=nj,swph=self.ice_water_phase=='both').astype(np.float32)
                elif self.option==2:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_rpn[self.option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    hr_df = get_from_dataframe(level_intersection_df,'HR')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],all_rows=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in es_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        pxpa = pxpa_df.at[i,'d']
                        hr = hr_df.at[i,'d']
                        es_df.at[i,'d'] = science.rpn_es_from_hr(tt=ttk,hr=hr,px=pxpa,ni=ni,nj=nj,swph=self.ice_water_phase=='both').astype(np.float32)
                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_rpn[self.option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = get_from_dataframe(level_intersection_df,'TD')
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],all_rows=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    tdk_df = fstpy.unit_convert(td_df,'kelvin')
                    for i in es_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        tdk = tdk_df.at[i,'d']
                        es_df.at[i,'d'] = science.es_from_td(tt=ttk-TDPACK_OFFSET_FIX,td=tdk-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)
            else:
                if self.option==0:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies[self.option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    hu_df = get_from_dataframe(level_intersection_df,'HU')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],all_rows=True)
                    td_df = TemperatureDewPoint(level_intersection_df,ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    td_df = get_from_dataframe(td_df,'TD')
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        td = td_df.at[i,'d']
                        es_df.at[i,'d'] = science.es_from_td(tt=tt-TDPACK_OFFSET_FIX,td=td-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)


                elif self.option==1: # test 9
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies[self.option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    qv_df = get_from_dataframe(level_intersection_df,'QV')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],all_rows=True)
                    td_df = TemperatureDewPoint(level_intersection_df,ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    td_df = get_from_dataframe(td_df,'TD')
                    # qvkgkg_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        td = td_df.at[i,'d']
                        es_df.at[i,'d'] = science.es_from_td(tt=tt-TDPACK_OFFSET_FIX,td=td-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)


                elif self.option==2: #test 5
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies[self.option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    hr_df = get_from_dataframe(level_intersection_df,'HR')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],all_rows=True)
                    td_df = TemperatureDewPoint(level_intersection_df,ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    td_df = get_from_dataframe(td_df,'TD')
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        td = td_df.at[i,'d']
                        es_df.at[i,'d'] = science.es_from_td(tt=tt-TDPACK_OFFSET_FIX,td=td-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)
                        # es_df.at[i,'d'] = calc_dew_point_depression_td(tt,td).astype(float32)

                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies[self.option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = get_from_dataframe(level_intersection_df,'TD')
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],all_rows=True)
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        td = td_df.at[i,'d']
                        es_df.at[i,'d'] = science.es_from_td(tt=tt-TDPACK_OFFSET_FIX,td=td-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)

            df_list.append(es_df)

        return final_results(df_list, DewPointDepression, self.meta_df)
