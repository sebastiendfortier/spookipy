# -*- coding: utf-8 -*-

from ..humidityutils import TDPACK_OFFSET_FIX, get_temp_phase_switch, validate_humidity_parameters
from ..plugin import Plugin
from ..utils import create_empty_result, get_existing_result, get_intersecting_levels, get_plugin_dependencies, initializer, existing_results, final_results
import pandas as pd
import fstpy.all as fstpy
import sys
import numpy as np
from ..science.science import *

class HumiditySpecificError(Exception):
    pass

class HumiditySpecific(Plugin):


    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}
        self.plugin_mandatory_dependencies_option_rpn1 = {
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
            }
        self.plugin_mandatory_dependencies_option_rpn2 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
            }
        self.plugin_mandatory_dependencies_option_rpn3 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'ES':{'nomvar':'ES','unit':'celsius','select_only':True},
            }
        self.plugin_mandatory_dependencies_option_rpn4 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
            }
        self.plugin_mandatory_dependencies_option_1 = {
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
            }
        self.plugin_mandatory_dependencies_option_2 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_3 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'ES':{'nomvar':'ES','unit':'celsius','select_only':True},
        }
        self.plugin_mandatory_dependencies_option_4 = {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
        }


        self.plugin_result_specifications = {
            'HU':{'nomvar':'HU','etiket':'HUMSPF','unit':'kilogram_per_kilogram','nbits':16,'datyp':1}
            }
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise  HumiditySpecificError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(HumiditySpecificError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(HumiditySpecificError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)


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
        from ..vapourpessure.vapourpessure import VapourPressure
        if not self.existing_result_df.empty:
            return existing_results('HumiditySpecific',self.existing_result_df,self.meta_df)

        sys.stdout.write('HumiditySpecific - compute\n')
        df_list = []
        if self.ice_water_phase == 'water':
            self.temp_phase_switch = -40.
        for _, current_fhour_group in self.fhour_groups:
            if self.rpn:
                print('rpn')
                if self.option==1:
                    print('option 1')
                    current_fhour_group = fstpy.load_data(current_fhour_group)
                    qv_df = current_fhour_group.loc[current_fhour_group.nomvar=='QV'].reset_index(drop=True)
                    hu_df = create_empty_result(qv_df,self.plugin_result_specifications['HU'],copy=True)
                    qvkgkg_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
                    for i in hu_df.index:
                        qvkgkg = qvkgkg_df.at[i,'d']
                        ni = qvkgkg.shape[0]
                        nj = qvkgkg.shape[1]
                        hu_df.at[i,'d'] = science.hu_from_qv(qv=qvkgkg,ni=ni,nj=nj).astype(np.float32)

                elif self.option==2:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_2)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].sort_values(by=['level']).reset_index(drop=True)
                    hr_df = current_fhour_group.loc[current_fhour_group.nomvar=='HR'].sort_values(by=['level']).reset_index(drop=True)
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].sort_values(by=['level']).reset_index(drop=True)

                    hu_df = create_empty_result(tt_df,self.plugin_result_specifications['HU'],copy=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hu_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        pxpa = pxpa_df.at[i,'d']
                        hr = hr_df.at[i,'d']
                        hu_df.at[i,'d'] = science.rpn_hu_from_hr(tt=ttk, hr=hr, px=pxpa, ni=ni, nj=nj, swph=self.ice_water_phase=='both').astype(np.float32)

                elif self.option==3:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_3)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].sort_values(by=['level']).reset_index(drop=True)
                    es_df = current_fhour_group.loc[current_fhour_group.nomvar=='ES'].sort_values(by=['level']).reset_index(drop=True)
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].sort_values(by=['level']).reset_index(drop=True)
                    hu_df = create_empty_result(tt_df,self.plugin_result_specifications['HU'],copy=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hu_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        es = es_df.at[i,'d']
                        pxpa = pxpa_df.at[i,'d']
                        hu_df.at[i,'d'] = science.rpn_hu_from_es(tt=ttk, es=es, px=pxpa, ni=ni, nj=nj, swph=self.ice_water_phase=='both').astype(np.float32)

                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_4)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].sort_values(by=['level']).reset_index(drop=True)
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].sort_values(by=['level']).reset_index(drop=True)
                    td_df = current_fhour_group.loc[current_fhour_group.nomvar=='TD'].sort_values(by=['level']).reset_index(drop=True)
                    hu_df = create_empty_result(tt_df,self.plugin_result_specifications['HU'],copy=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    tdk_df = fstpy.unit_convert(td_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hu_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        tdk = tdk_df.at[i,'d']
                        pxpa = pxpa_df.at[i,'d']
                        es = science.es_from_td(tt=ttk-TDPACK_OFFSET_FIX,td=tdk-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)
                        hu_df.at[i,'d'] = science.rpn_hu_from_es(tt=ttk, es=es, px=pxpa, ni=ni, nj=nj, swph=self.ice_water_phase=='both').astype(np.float32)

            else:
                if self.option==1:
                    print('option 1')
                    current_fhour_group = fstpy.load_data(current_fhour_group)
                    qv_df = current_fhour_group.loc[current_fhour_group.nomvar=='QV'].reset_index(drop=True)
                    hu_df = create_empty_result(qv_df,self.plugin_result_specifications['HU'],copy=True)
                    qvkgkg_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
                    for i in hu_df.index:
                        qvkgkg = qvkgkg_df.at[i,'d']
                        ni = qvkgkg.shape[0]
                        nj = qvkgkg.shape[1]
                        hu_df.at[i,'d'] = science.hu_from_qv(qv=qvkgkg,ni=ni,nj=nj).astype(np.float32)

                elif self.option==2:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_2)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True).sort_values(by=['level'])
                    hr_df = current_fhour_group.loc[current_fhour_group.nomvar=='HR'].reset_index(drop=True).sort_values(by=['level'])
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].reset_index(drop=True).sort_values(by=['level'])
                    vppr_df = VapourPressure(pd.concat([tt_df,hr_df,px_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = vppr_df.loc[vppr_df.nomvar=='VPPR'].reset_index(drop=True).sort_values(by=['level'])
                    hu_df = create_empty_result(px_df,self.plugin_result_specifications['HU'],copy=True)
                    # px_df = fstpy.unit_convert(px_df,'pascal')
                    # vppr_df = fstpy.unit_convert(vppr_df,'pascal')
                    for i in hu_df.index:
                        px = px_df.at[i,'d']
                        ni = px.shape[0]
                        nj = px.shape[1]
                        vppr = vppr_df.at[i,'d']
                        hu_df.at[i,'d'] = science.hu_from_vppr(vppr=vppr,px=px,ni=ni,nj=nj).astype(np.float32)

                elif self.option==3:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_3)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].sort_values(by=['level']).reset_index(drop=True)
                    es_df = current_fhour_group.loc[current_fhour_group.nomvar=='ES'].sort_values(by=['level']).reset_index(drop=True)
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].sort_values(by=['level']).reset_index(drop=True)
                    vppr_df = VapourPressure(pd.concat([tt_df,es_df,px_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = vppr_df.loc[vppr_df.nomvar=='VPPR'].sort_values(by=['level']).reset_index(drop=True)
                    hu_df = create_empty_result(px_df,self.plugin_result_specifications['HU'],copy=True)
                    # px_df = fstpy.unit_convert(px_df,'pascal')
                    # vppr_df = fstpy.unit_convert(vppr_df,'pascal')
                    for i in hu_df.index:
                        px = px_df.at[i,'d']
                        ni = px.shape[0]
                        nj = px.shape[1]
                        vppr = vppr_df.at[i,'d']
                        hu_df.at[i,'d'] = science.hu_from_vppr(vppr=vppr,px=px,ni=ni,nj=nj).astype(np.float32)

                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_4)
                    current_fhour_group = fstpy.load_data(level_intersection_df)
                    tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                    px_df = current_fhour_group.loc[current_fhour_group.nomvar=='PX'].reset_index(drop=True)
                    td_df = current_fhour_group.loc[current_fhour_group.nomvar=='TD'].reset_index(drop=True)
                    vppr_df = VapourPressure(pd.concat([tt_df,px_df,td_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = vppr_df.loc[vppr_df.nomvar=='VPPR'].reset_index(drop=True)
                    hu_df = create_empty_result(px_df,self.plugin_result_specifications['HU'],copy=True)
                    # px_df = fstpy.unit_convert(px_df,'pascal')
                    # vppr_df = fstpy.unit_convert(vppr_df,'pascal')
                    for i in hu_df.index:
                        px = px_df.at[i,'d']
                        ni = px.shape[0]
                        nj = px.shape[1]
                        vppr = vppr_df.at[i,'d']
                        hu_df.at[i,'d'] = science.hu_from_vppr(vppr=vppr,px=px,ni=ni,nj=nj).astype(np.float32)

            df_list.append(hu_df)

        return final_results(df_list, HumiditySpecificError, self.meta_df)
