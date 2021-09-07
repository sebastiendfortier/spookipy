# -*- coding: utf-8 -*-

import sys

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils import (TDPACK_OFFSET_FIX, get_temp_phase_switch,
                             validate_humidity_parameters)
from ..plugin import Plugin
from ..science.science import *
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result,
                     get_from_dataframe, get_intersecting_levels, initializer)


class HumiditySpecificError(Exception):
    pass

class HumiditySpecific(Plugin):


    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}
        self.plugin_mandatory_dependencies_rpn = [
            {
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
            },
            {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'ES':{'nomvar':'ES','unit':'celsius','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            }
        ]
        self.plugin_mandatory_dependencies = [
            {
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
            },
            {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'ES':{'nomvar':'ES','unit':'celsius','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
            'TT':{'nomvar':'TT','unit':'celsius'},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            }
        ]




        self.plugin_result_specifications = {
            'HU':{'nomvar':'HU','etiket':'HUMSPF','unit':'kilogram_per_kilogram','nbits':16,'datyp':1}
            }
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise  HumiditySpecificError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(self.df, decode=True, columns=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(HumiditySpecificError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(HumiditySpecificError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)


        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)
        # print(self.df[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])


    def compute(self) -> pd.DataFrame:
        from ..vapourpessure.vapourpessure import VapourPressure
        if not self.existing_result_df.empty:
            return existing_results('HumiditySpecific',self.existing_result_df,self.meta_df)

        sys.stdout.write('HumiditySpecific - compute\n')
        df_list = []

        if self.rpn:
            dependencies_list = get_dependencies(self.groups,self.meta_df,'HumiditySpecific',self.plugin_mandatory_dependencies_rpn,self.plugin_params)
        else:
            dependencies_list = get_dependencies(self.groups,self.meta_df,'HumiditySpecific',self.plugin_mandatory_dependencies,self.plugin_params)

        for dependencies_df,option in dependencies_list:
            if self.rpn:
                print('rpn')
                if option==0:
                    print('option 1')
                    dependencies_df = fstpy.load_data(dependencies_df)
                    qv_df = get_from_dataframe(dependencies_df,'QV')
                    hu_df = create_empty_result(qv_df,self.plugin_result_specifications['HU'],all_rows=True)
                    qvkgkg_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
                    for i in hu_df.index:
                        qvkgkg = qvkgkg_df.at[i,'d']
                        ni = qvkgkg.shape[0]
                        nj = qvkgkg.shape[1]
                        hu_df.at[i,'d'] = science.hu_from_qv(qv=qvkgkg,ni=ni,nj=nj).astype(np.float32)

                elif option==1:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    hr_df = get_from_dataframe(level_intersection_df,'HR')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hu_df = create_empty_result(tt_df,self.plugin_result_specifications['HU'],all_rows=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hu_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        pxpa = pxpa_df.at[i,'d']
                        hr = hr_df.at[i,'d']
                        hu_df.at[i,'d'] = science.rpn_hu_from_hr(tt=ttk, hr=hr, px=pxpa, ni=ni, nj=nj, swph=self.ice_water_phase=='both').astype(np.float32)

                elif option==2: #test 11
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    es_df = get_from_dataframe(level_intersection_df,'ES')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hu_df = create_empty_result(tt_df,self.plugin_result_specifications['HU'],all_rows=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hu_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        es = es_df.at[i,'d']
                        pxpa = pxpa_df.at[i,'d']
                        hu_df.at[i,'d'] = science.rpn_hu_from_es(tt=ttk, es=es, px=pxpa, ni=ni, nj=nj, swph=self.ice_water_phase=='both').astype(np.float32)

                else: #test 13
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = get_from_dataframe(level_intersection_df,'TD')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hu_df = create_empty_result(tt_df,self.plugin_result_specifications['HU'],all_rows=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    tdk_df = fstpy.unit_convert(td_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hu_df.index:
                        ttk = ttk_df.at[i,'d']
                        tt = tt_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        tdk = tdk_df.at[i,'d']
                        td = td_df.at[i,'d']
                        pxpa = pxpa_df.at[i,'d']
                        es = science.es_from_td(tt=tt-TDPACK_OFFSET_FIX,td=td-TDPACK_OFFSET_FIX,ni=ni,nj=nj).astype(np.float32)
                        # hu_df.at[i,'d'] = science.rpn_hu_from_es(tt=ttk, es=esk, px=pxpa, ni=ni, nj=nj, swph=self.ice_water_phase=='both').astype(np.float32)
                        hu_df.at[i,'d'] = science.rpn_hu_from_es(tt=ttk, es=es, px=pxpa, ni=ni, nj=nj, swph=self.ice_water_phase=='both').astype(np.float32)

            else:
                if option==0:
                    print('option 1')
                    dependencies_df = fstpy.load_data(dependencies_df)
                    qv_df = get_from_dataframe(dependencies_df,'QV')
                    hu_df = create_empty_result(qv_df,self.plugin_result_specifications['HU'],all_rows=True)
                    qvkgkg_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
                    for i in hu_df.index:
                        qvkgkg = qvkgkg_df.at[i,'d']
                        ni = qvkgkg.shape[0]
                        nj = qvkgkg.shape[1]
                        hu_df.at[i,'d'] = science.hu_from_qv(qv=qvkgkg,ni=ni,nj=nj).astype(np.float32)

                elif option==1:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hu_df = create_empty_result(px_df,self.plugin_result_specifications['HU'],all_rows=True)
                    vppr_df = VapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = get_from_dataframe(vppr_df,'VPPR')
                    # px_df = fstpy.unit_convert(px_df,'pascal')
                    # vppr_df = fstpy.unit_convert(vppr_df,'pascal')
                    for i in hu_df.index:
                        px = px_df.at[i,'d']
                        ni = px.shape[0]
                        nj = px.shape[1]
                        vppr = vppr_df.at[i,'d']
                        hu_df.at[i,'d'] = science.hu_from_vppr(vppr=vppr,px=px,ni=ni,nj=nj).astype(np.float32)

                elif option==2:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hu_df = create_empty_result(px_df,self.plugin_result_specifications['HU'],all_rows=True)
                    vppr_df = VapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = get_from_dataframe(vppr_df,'VPPR')
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
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hu_df = create_empty_result(px_df,self.plugin_result_specifications['HU'],all_rows=True)
                    vppr_df = VapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
                    vppr_df = get_from_dataframe(vppr_df,'VPPR')
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
