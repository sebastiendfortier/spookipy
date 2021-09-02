# -*- coding: utf-8 -*-
import sys

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils.humidityutils import (TDPACK_OFFSET_FIX,
                                           get_temp_phase_switch,
                                           validate_humidity_parameters)
from ..plugin.plugin import Plugin
from ..science.science import *
from ..utils import (create_empty_result, existing_results, final_results,
                     find_matching_dependency_option, get_existing_result,
                     get_from_dataframe, get_intersecting_levels, initializer)


class VapourPressureError(Exception):
    pass

class VapourPressure(Plugin):

    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):

        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}
        self.plugin_mandatory_dependencies_rpn = [
            # HU + PXpa
            {
                'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'}
            },
            # QVkg + PX
            {
                'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'}
            },
            #TT + HR + PX > HUrpn + PXpa
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'}
            },
            # ES + TTk
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'ES':{'nomvar':'ES','unit':'celsius','select_only':True},
            },
            # TDk + TTk
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
            }
        ]
        self.plugin_mandatory_dependencies = [
            # HU + PX
            {
                'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'}
            },
            # QVkg/kg + PX
            {
                'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'}
            },
            # HR + SVP
            {
                'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
                'SVP':{'nomvar':'SVP','unit':'hectoPascal'},
            },
            # ES + TT
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'ES':{'nomvar':'ES','unit':'celsius','select_only':True},
            },
            # TD + TT
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
            }
        ]


        self.plugin_result_specifications = {
            'VPPR':{'nomvar':'VPPR','etiket':'VAPRES','unit':'hectoPascal','nbits':16,'datyp':1}
            }
        self.validate_input()


    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise  VapourPressureError('No data to process')


        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(self.df, decode=True, columns=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(VapourPressureError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(VapourPressureError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].sort_values(by=['level']).reset_index(drop=True)

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)
        # print(self.df[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])


    def compute(self) -> pd.DataFrame:
        from ..humidityspecific.humidityspecific import HumiditySpecific
        if not self.existing_result_df.empty:
            return existing_results('VapourPressure',self.existing_result_df,self.meta_df)

        sys.stdout.write('VapourPressure - compute\n')
        df_list=[]

        for _, current_group in self.groups:
            # print(current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
            if self.rpn:
                sys.stdout.write('VapourPressure - Checking rpn dependencies\n')
                dependencies_df, option = find_matching_dependency_option(pd.concat([current_group,self.meta_df],ignore_index=True),self.plugin_params,self.plugin_mandatory_dependencies_rpn)
            else:
                sys.stdout.write('VapourPressure - Checking dependencies\n')
                dependencies_df, option = find_matching_dependency_option(pd.concat([current_group,self.meta_df],ignore_index=True),self.plugin_params,self.plugin_mandatory_dependencies)
            if dependencies_df.empty:
                sys.stdout.write('VapourPressure - No matching dependencies found for this group \n%s\n'%current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']])
                continue
            else:
                sys.stdout.write('VapourPressure - Matching dependencies found for this group \n%s\n'%current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']])

            if self.rpn:
                print('rpn')
                if option==0:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    hu_df = get_from_dataframe(level_intersection_df,'HU')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    vppr_df = create_empty_result(hu_df,self.plugin_result_specifications['VPPR'],all_rows=True)
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in vppr_df.index:
                        hu = hu_df.at[i,'d']
                        ni = hu.shape[0]
                        nj = hu.shape[1]
                        pxpa = pxpa_df.at[i,'d']
                        vppr_df.at[i,'d'] = science.rpn_vppr_from_hu(hu=hu, px=pxpa, ni=ni, nj=nj).astype(np.float32)

                elif option==1:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    qv_df = get_from_dataframe(level_intersection_df,'QV')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    vppr_df = create_empty_result(qv_df,self.plugin_result_specifications['VPPR'],all_rows=True)
                    qvkgkg_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
                    for i in vppr_df.index:
                        qvkgkg = qvkgkg_df.at[i,'d']
                        px = px_df.at[i,'d']
                        ni = px.shape[0]
                        nj = px.shape[1]
                        vppr_df.at[i,'d'] = science.vppr_from_qv(qv=qvkgkg, px=px, ni=ni, nj=nj).astype(np.float32)


                elif option==2:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    vppr_df = create_empty_result(tt_df,self.plugin_result_specifications['VPPR'],all_rows=True)
                    hu_df = HumiditySpecific(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit,rpn=True).compute()
                    hu_df = get_from_dataframe(hu_df,'HU')
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in vppr_df.index:
                        pxpa = pxpa_df.at[i,'d']
                        hu = hu_df.at[i,'d']
                        ni = hu.shape[0]
                        nj = hu.shape[1]
                        vppr_df.at[i,'d'] = science.rpn_vppr_from_hu(hu=hu, px=pxpa, ni=ni, nj=nj).astype(np.float32)

                elif option==3:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    es_df = get_from_dataframe(level_intersection_df,'ES')
                    vppr_df = create_empty_result(tt_df,self.plugin_result_specifications['VPPR'],all_rows=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    for i in vppr_df.index:
                        tt = tt_df.at[i,'d']
                        ni  =tt.shape[0]
                        nj  =tt.shape[1]
                        ttk = ttk_df.at[i,'d']
                        es = es_df.at[i,'d']
                        td = science.td_es(tt=tt,es=es,ni=ni,nj=nj).astype(np.float32)
                        tdk = fstpy.unit_convert_array(td,'celsius','kelvin')
                        vppr_df.at[i,'d'] = science.rpn_vppr_from_td(td=tdk, tt=ttk, ni=ni, nj=nj, tpl=(self.temp_phase_switch if self.ice_water_phase!='water' else -40), swph=self.ice_water_phase=='both').astype(np.float32)
                else:
                    print('option 5')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = get_from_dataframe(level_intersection_df,'TD')
                    vppr_df = create_empty_result(tt_df,self.plugin_result_specifications['VPPR'],all_rows=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    tdk_df = fstpy.unit_convert(td_df,'kelvin')
                    for i in vppr_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        tdk = tdk_df.at[i,'d']
                        vppr_df.at[i,'d'] = science.rpn_vppr_from_td(td=tdk, tt=ttk, ni=ni, nj=nj, tpl=(self.temp_phase_switch if self.ice_water_phase!='water' else -40), swph=self.ice_water_phase=='both').astype(np.float32)

            else:
                if option==0:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    hu_df = get_from_dataframe(level_intersection_df,'HU')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    vppr_df = create_empty_result(hu_df,self.plugin_result_specifications['VPPR'],all_rows=True)
                    for i in vppr_df.index:
                        hu = hu_df.at[i,'d']
                        ni = hu.shape[0]
                        nj = hu.shape[1]
                        px = px_df.at[i,'d']
                        vppr_df.at[i,'d'] = science.vppr_from_hu(hu=hu, px=px, ni=ni, nj=nj).astype(np.float32)

                elif option==1:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    qv_df = get_from_dataframe(level_intersection_df,'QV')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    vppr_df = create_empty_result(qv_df,self.plugin_result_specifications['VPPR'],all_rows=True)
                    qv_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
                    for i in vppr_df.index:
                        qv = qv_df.at[i,'d']
                        ni = qv.shape[0]
                        nj = qv.shape[1]
                        px = px_df.at[i,'d']
                        vppr_df.at[i,'d'] = science.vppr_from_qv(qv=qv, px=px, ni=ni, nj=nj).astype(np.float32)

                elif option==2:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    svp_df = get_from_dataframe(level_intersection_df,'SVP')
                    hr_df = get_from_dataframe(level_intersection_df,'HR')
                    vppr_df = create_empty_result(svp_df,self.plugin_result_specifications['VPPR'],all_rows=True)
                    for i in vppr_df.index:
                        hr = hr_df.at[i,'d']
                        ni = hr.shape[0]
                        nj = hr.shape[1]
                        svp = svp_df.at[i,'d']
                        vppr_df.at[i,'d'] = science.vppr_from_hr(hr=hr, svp=svp, ni=ni, nj=nj).astype(np.float32)

                elif option==3:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    es_df = get_from_dataframe(level_intersection_df,'ES')
                    vppr_df = create_empty_result(tt_df,self.plugin_result_specifications['VPPR'],all_rows=True)
                    for i in vppr_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        es = es_df.at[i,'d']
                        td = science.td_from_es(tt=tt, es=es, ni=ni, nj=nj).astype(np.float32)
                        vppr_df.at[i,'d'] = science.vppr_from_td(td=td-TDPACK_OFFSET_FIX, tt=tt-TDPACK_OFFSET_FIX, ni=ni, nj=nj, tpl=(self.temp_phase_switch if self.ice_water_phase!='water' else -40), swph=self.ice_water_phase=='both').astype(np.float32)

                else:
                    print('option 5')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = get_from_dataframe(level_intersection_df,'TD')
                    if tt_df.empty or td_df.empty:
                        continue
                    vppr_df = create_empty_result(td_df,self.plugin_result_specifications['VPPR'],all_rows=True)
                    for i in vppr_df.index:
                        tt = tt_df.at[i,'d']
                        ni = tt.shape[0]
                        nj = tt.shape[1]
                        td = td_df.at[i,'d']
                        vppr_df.at[i,'d'] = science.vppr_from_td(td=td-TDPACK_OFFSET_FIX, tt=tt-TDPACK_OFFSET_FIX, ni=ni, nj=nj, tpl=(self.temp_phase_switch if self.ice_water_phase!='water' else -40), swph=self.ice_water_phase=='both').astype(np.float32)


            df_list.append(vppr_df)

        return final_results(df_list, VapourPressureError, self.meta_df)
