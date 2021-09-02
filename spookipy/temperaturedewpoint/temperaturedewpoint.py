# -*- coding: utf-8 -*-
import sys

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils import (TDPACK_OFFSET_FIX,
                             get_temp_phase_switch,
                             validate_humidity_parameters)
from ..plugin import Plugin
from ..science.science import *
from ..utils import (create_empty_result, existing_results, final_results, find_matching_dependency_option,
                     get_existing_result, get_from_dataframe, get_intersecting_levels,
                     initializer)


class TemperatureDewPointError(Exception):
    pass


class TemperatureDewPoint(Plugin):


    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}
        self.plugin_mandatory_dependencies_rpn = [
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'ES':{'nomvar':'ES','unit':'celsius','select_only':True}
            }
        ]
        self.plugin_mandatory_dependencies = [
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'ES':{'nomvar':'ES','unit':'celsius','select_only':True}
            }
        ]

        self.plugin_result_specifications = {
            'TD':{'nomvar':'TD','etiket':'DEWPTT','unit':'celsius'}
            }
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise TemperatureDewPointError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(self.df, decode=True, columns=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(TemperatureDewPointError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)


        self.temp_phase_switch = get_temp_phase_switch(TemperatureDewPointError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)
        # print(self.df[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])

    def compute(self) -> pd.DataFrame:
        from ..dewpointdepression.dewpointdepression import DewPointDepression
        from ..vapourpessure.vapourpessure import VapourPressure
        if not self.existing_result_df.empty:
            return existing_results('TemperatureDewPoint',self.existing_result_df,self.meta_df)

        sys.stdout.write('TemperatureDewPoint - compute\n')
        df_list=[]

        for _, current_group in self.groups:
            # print(current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
            if self.rpn:
                sys.stdout.write('TemperatureDewPoint - Checking rpn dependencies\n')
                dependencies_df, option = find_matching_dependency_option(pd.concat([current_group,self.meta_df],ignore_index=True),self.plugin_params,self.plugin_mandatory_dependencies_rpn)
            else:
                sys.stdout.write('TemperatureDewPoint - Checking dependencies\n')
                dependencies_df, option = find_matching_dependency_option(pd.concat([current_group,self.meta_df],ignore_index=True),self.plugin_params,self.plugin_mandatory_dependencies)
            if dependencies_df.empty:
                sys.stdout.write('TemperatureDewPoint - No matching dependencies found for this group \n%s\n'%current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']])
                continue
            else:
                sys.stdout.write('TemperatureDewPoint - Matching dependencies found for this group \n%s\n'%current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']])

            if self.rpn:
                print('rpn')
                if option==0:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],all_rows=True)
                    es_df = DewPointDepression(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit,rpn=True).compute()
                    es_df = get_from_dataframe(es_df,'ES')
                    # ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        es = es_df.at[i,'d']
                        td_df.at[i,'d'] = science.td_from_es(tt=tt-TDPACK_OFFSET_FIX, es=es, ni=ni, nj=nj).astype(np.float32)

                elif option==1:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],all_rows=True)
                    es_df = DewPointDepression(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit,rpn=True).compute()
                    es_df = get_from_dataframe(es_df,'ES')
                    # ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    # pxpa_df = fstpy.unit_convert(px_df,'kelvin')
                    # qvkgkg_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        es = es_df.at[i,'d']
                        td_df.at[i,'d'] = science.td_from_es(tt=tt-TDPACK_OFFSET_FIX, es=es, ni=ni, nj=nj).astype(np.float32)

                elif option==2:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],all_rows=True)
                    es_df = DewPointDepression(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit,rpn=True).compute()
                    es_df = get_from_dataframe(es_df,'ES')
                    # ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    # pxpa_df = fstpy.unit_convert(px_df,'kelvin')
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        es = es_df.at[i,'d']
                        td_df.at[i,'d'] = science.td_from_es(tt=tt-TDPACK_OFFSET_FIX, es=es, ni=ni, nj=nj).astype(np.float32)

                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    es_df = get_from_dataframe(level_intersection_df,'ES')
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],all_rows=True)
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']#
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        es = es_df.at[i,'d']
                        # td_df.at[i,'d'] = science.td_from_es(tt=tt-TDPACK_OFFSET_FIX, es=es, ni=ni, nj=nj).astype(np.float32)
                        td_df.at[i,'d'] = science.td_from_es(tt=tt, es=es, ni=ni, nj=nj).astype(np.float32)
                        # td_df.at[i,'d'] = calc_temperature_dew_point_es(tt, es).astype(float32)

            else:
                if option==0: #9 12
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],all_rows=True)
                    vppr_df = VapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = get_from_dataframe(vppr_df,'VPPR')
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        vppr = vppr_df.at[i,'d']
                        td_df.at[i,'d'] = science.td_from_vppr(tt=tt-TDPACK_OFFSET_FIX,vppr=vppr,ni=ni,nj=nj,tpl=(self.temp_phase_switch if self.ice_water_phase!='water' else -40),swph=self.ice_water_phase=='both').astype(np.float32)

                elif option==1: # 11
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],all_rows=True)
                    vppr_df = VapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = get_from_dataframe(vppr_df,'VPPR')
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        vppr = vppr_df.at[i,'d']
                        td_df.at[i,'d'] = science.td_from_vppr(tt=tt-TDPACK_OFFSET_FIX,vppr=vppr,ni=ni,nj=nj,tpl=(self.temp_phase_switch if self.ice_water_phase!='water' else -40),swph=self.ice_water_phase=='both').astype(np.float32)

                elif option==2: #7
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],all_rows=True)
                    vppr_df = VapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = get_from_dataframe(vppr_df,'VPPR')
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        vppr = vppr_df.at[i,'d']
                        td_df.at[i,'d'] = science.td_from_vppr(tt=tt-TDPACK_OFFSET_FIX,vppr=vppr,ni=ni,nj=nj,tpl=(self.temp_phase_switch if self.ice_water_phase!='water' else -40),swph=self.ice_water_phase=='both').astype(np.float32)

                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    es_df = get_from_dataframe(level_intersection_df,'ES')
                    td_df = create_empty_result(tt_df,self.plugin_result_specifications['TD'],all_rows=True)
                    for i in td_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        es = es_df.at[i,'d']
                        # td_df.at[i,'d'] = science.td_from_es(tt=tt-TDPACK_OFFSET_FIX, es=es, ni=ni, nj=nj).astype(np.float32)
                        td_df.at[i,'d'] = science.td_from_es(tt=tt, es=es, ni=ni, nj=nj).astype(np.float32)

            df_list.append(td_df)

        return final_results(df_list,TemperatureDewPointError, self.meta_df)
