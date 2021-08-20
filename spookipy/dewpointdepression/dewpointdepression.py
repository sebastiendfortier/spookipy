# -*- coding: utf-8 -*-
import sys

import numpy as np
import fstpy.all as fstpy
import pandas as pd
from ..humidityutils import (
    TDPACK_OFFSET_FIX, get_temp_phase_switch,
    validate_humidity_parameters)

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results,
                     get_existing_result, get_intersecting_levels,
                     get_plugin_dependencies, initializer)
from ..science.science import *

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
            'HR':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
        }



        self.plugin_mandatory_dependencies_option_1 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
            }
        self.plugin_mandatory_dependencies_option_2 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
        }
        self.plugin_mandatory_dependencies_option_3 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'}
        }
        self.plugin_mandatory_dependencies_option_4 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
        }


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
                    self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_params,self.plugin_mandatory_dependencies_option_rpn3)
                    self.option=3
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
        from ..humidityspecific.humidityspecific import HumiditySpecific
        from ..temperaturedewpoint.temperaturedewpoint import TemperatureDewPoint
        if not self.existing_result_df.empty:
            return existing_results('DewPointDepression',self.existing_result_df,self.meta_df)

        sys.stdout.write('DewPointDepression - compute\n')
        df_list=[]
        if self.ice_water_phase == 'water':
            self.temp_phase_switch = -40.
        for _, current_fhour_group in self.fhour_groups:
            if self.rpn:
                print('rpn')
                if self.option==1:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn1)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.loc[level_intersection_df.nomvar=='TT'].reset_index(drop=True)
                    hu_df = level_intersection_df.loc[level_intersection_df.nomvar=='HU'].reset_index(drop=True)
                    px_df = level_intersection_df.loc[level_intersection_df.nomvar=='PX'].reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
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
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn2)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.loc[level_intersection_df.nomvar=='TT'].reset_index(drop=True)
                    qv_df = level_intersection_df.loc[level_intersection_df.nomvar=='QV'].reset_index(drop=True)
                    px_df = level_intersection_df.loc[level_intersection_df.nomvar=='PX'].reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    hu_df = HumiditySpecific(pd.concat([tt_df,qv_df,px_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,rpn=True).compute()
                    hu_df = hu_df.loc[hu_df.nomvar=='HU'].reset_index(drop=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in es_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        pxpa = pxpa_df.at[i,'d']
                        hu = hu_df.at[i,'d']
                        es_df.at[i,'d'] = science.rpn_es_from_hu(tt=ttk,hu=hu,px=pxpa,ni=ni,nj=nj,swph=self.ice_water_phase=='both').astype(np.float32)
                elif self.option==3:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn3)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.loc[level_intersection_df.nomvar=='TT'].reset_index(drop=True)
                    hr_df = level_intersection_df.loc[level_intersection_df.nomvar=='HR'].reset_index(drop=True)
                    px_df = level_intersection_df.loc[level_intersection_df.nomvar=='PX'].reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
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
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_rpn4)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.loc[level_intersection_df.nomvar=='TT'].reset_index(drop=True)
                    td_df = level_intersection_df.loc[level_intersection_df.nomvar=='TD'].reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    tdk_df = fstpy.unit_convert(td_df,'kelvin')
                    for i in es_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        tdk = tdk_df.at[i,'d']
                        es_df.at[i,'d'] = science.es_from_td(tt=ttk-TDPACK_OFFSET_FIX,td=tdk-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)
            else:
                if self.option==1:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_1)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.loc[level_intersection_df.nomvar=='TT'].reset_index(drop=True)
                    hu_df = level_intersection_df.loc[level_intersection_df.nomvar=='HU'].reset_index(drop=True)
                    px_df = level_intersection_df.loc[level_intersection_df.nomvar=='PX'].reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    td_df = TemperatureDewPoint(pd.concat([tt_df,hu_df,px_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    td_df = td_df.loc[td_df.nomvar=='TD'].reset_index(drop=True)
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        td = td_df.at[i,'d']
                        es_df.at[i,'d'] = science.es_from_td(tt=tt-TDPACK_OFFSET_FIX,td=td-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)


                elif self.option==2: # test 9
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_2)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.loc[level_intersection_df.nomvar=='TT'].reset_index(drop=True)
                    qv_df = level_intersection_df.loc[level_intersection_df.nomvar=='QV'].reset_index(drop=True)
                    px_df = level_intersection_df.loc[level_intersection_df.nomvar=='PX'].reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    td_df = TemperatureDewPoint(pd.concat([tt_df,qv_df,px_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    td_df = td_df.loc[td_df.nomvar=='TD'].reset_index(drop=True)
                    qvkgkg_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        td = td_df.at[i,'d']
                        es_df.at[i,'d'] = science.es_from_td(tt=tt-TDPACK_OFFSET_FIX,td=td-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)


                elif self.option==3: #test 5
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_3)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.loc[level_intersection_df.nomvar=='TT'].reset_index(drop=True)
                    hr_df = level_intersection_df.loc[level_intersection_df.nomvar=='HR'].reset_index(drop=True)
                    px_df = level_intersection_df.loc[level_intersection_df.nomvar=='PX'].reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    td_df = TemperatureDewPoint(pd.concat([tt_df,hr_df,px_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    td_df = td_df.loc[td_df.nomvar=='TD'].reset_index(drop=True)
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        td = td_df.at[i,'d']
                        es_df.at[i,'d'] = science.es_from_td(tt=tt-TDPACK_OFFSET_FIX,td=td-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)
                        # es_df.at[i,'d'] = calc_dew_point_depression_td(tt,td).astype(float32)

                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_4)
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = level_intersection_df.loc[level_intersection_df.nomvar=='TT'].reset_index(drop=True)
                    td_df = level_intersection_df.loc[level_intersection_df.nomvar=='TD'].reset_index(drop=True)
                    es_df = create_empty_result(tt_df,self.plugin_result_specifications['ES'],copy=True)
                    for i in es_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        td = td_df.at[i,'d']
                        es_df.at[i,'d'] = science.es_from_td(tt=tt-TDPACK_OFFSET_FIX,td=td-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)

            df_list.append(es_df)

        return final_results(df_list, DewPointDepression, self.meta_df)
