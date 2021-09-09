# -*- coding: utf-8 -*-

import sys

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils.humidityutils import (get_temp_phase_switch,
                                           validate_humidity_parameters)
from ..plugin.plugin import Plugin
from ..science import (TDPACK_OFFSET_FIX, rpn_vppr_from_hu, rpn_vppr_from_td,
                       vppr_from_hr, vppr_from_hu, vppr_from_qv, vppr_from_td)
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     get_intersecting_levels, initializer)


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

        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])


    def compute(self) -> pd.DataFrame:

        if not self.existing_result_df.empty:
            return existing_results('VapourPressure',self.existing_result_df,self.meta_df)

        sys.stdout.write('VapourPressure - compute\n')
        df_list=[]

        if self.rpn:
            dependencies_list = get_dependencies(self.groups,self.meta_df,'VapourPressure',self.plugin_mandatory_dependencies_rpn,self.plugin_params)
        else:
            dependencies_list = get_dependencies(self.groups,self.meta_df,'VapourPressure',self.plugin_mandatory_dependencies,self.plugin_params)

        for dependencies_df,option in dependencies_list:
            if self.rpn:
                if option==0:
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    hu_df = get_from_dataframe(level_intersection_df,'HU')
                    vppr_df = self.rpn_vapourpressure_from_hu_px(hu_df, level_intersection_df, option)

                elif option==1:
                    vppr_df = self.vapourpressure_from_qv_px(dependencies_df, option, True)

                elif option==2:
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    hu_df = self.compute_hu(level_intersection_df)
                    vppr_df = self.rpn_vapourpressure_from_hu_px(hu_df, level_intersection_df, option)

                elif option==3:
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    td_df = self.compute_td(level_intersection_df)
                    vppr_df = self.rpn_vapourpressure_from_tt_td(td_df, level_intersection_df, option)

                else:
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    td_df = get_from_dataframe(level_intersection_df,'TD')
                    vppr_df = self.rpn_vapourpressure_from_tt_td(td_df, level_intersection_df, option)

            else:
                if option==0:
                    vppr_df = self.vapourpressure_from_hu_px(dependencies_df, option)

                elif option==1:
                    vppr_df = self.vapourpressure_from_qv_px(dependencies_df, option)

                elif option==2:
                    vppr_df = self.vapourpressure_from_hr_svp(dependencies_df, option)

                elif option==3:
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    td_df = self.compute_td(level_intersection_df)
                    vppr_df = self.vapourpressure_from_tt_td(td_df, level_intersection_df, option)

                else:
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    td_df = get_from_dataframe(level_intersection_df,'TD')
                    vppr_df = self.vapourpressure_from_tt_td(td_df, level_intersection_df, option)


            df_list.append(vppr_df)

        return final_results(df_list, VapourPressureError, self.meta_df)

    def vapourpressure_from_hu_px(self, dependencies_df, option):
        sys.stdout.write(f'rpn option {option+1}\n')
        level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
        hu_df = get_from_dataframe(level_intersection_df,'HU')
        hu_df = fstpy.load_data(hu_df)
        level_intersection_df = fstpy.load_data(level_intersection_df)
        px_df = get_from_dataframe(level_intersection_df,'PX')
        vppr_df = create_empty_result(hu_df,self.plugin_result_specifications['VPPR'],all_rows=True)
        for i in vppr_df.index:
            hu = hu_df.at[i,'d']
            px = px_df.at[i,'d']
            vppr_df.at[i,'d'] = vppr_from_hu(hu=hu, px=px).astype(np.float32)
        return vppr_df

    def vapourpressure_from_hr_svp(self, dependencies_df, option):
        sys.stdout.write(f'rpn option {option+1}\n')
        level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
        level_intersection_df = fstpy.load_data(level_intersection_df)
        svp_df = get_from_dataframe(level_intersection_df,'SVP')
        hr_df = get_from_dataframe(level_intersection_df,'HR')
        vppr_df = create_empty_result(svp_df,self.plugin_result_specifications['VPPR'],all_rows=True)
        for i in vppr_df.index:
            hr = hr_df.at[i,'d']
            svp = svp_df.at[i,'d']
            vppr_df.at[i,'d'] = vppr_from_hr(hr=hr, svp=svp).astype(np.float32)
        return vppr_df

    def rpn_vapourpressure_from_tt_td(self, td_df, level_intersection_df, option):
        sys.stdout.write(f'rpn option {option+1}\n')
        td_df = fstpy.load_data(td_df)
        level_intersection_df = fstpy.load_data(level_intersection_df)
        tt_df = get_from_dataframe(level_intersection_df,'TT')
        vppr_df = create_empty_result(tt_df,self.plugin_result_specifications['VPPR'],all_rows=True)
        ttk_df = fstpy.unit_convert(tt_df,'kelvin')
        tdk_df = fstpy.unit_convert(td_df,'kelvin')
        for i in vppr_df.index:
            ttk = ttk_df.at[i,'d']
            tdk = tdk_df.at[i,'d']
            vppr_df.at[i,'d'] = rpn_vppr_from_td(td=tdk, tt=ttk, tpl=(self.temp_phase_switch if self.ice_water_phase!='water' else -40), swph=self.ice_water_phase=='both').astype(np.float32)
        return vppr_df

    def vapourpressure_from_qv_px(self, dependencies_df, option, rpn=False):
        if rpn:
            sys.stdout.write(f'rpn option {option+1}\n')
        else:
            sys.stdout.write(f'option {option+1}\n')
        level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
        level_intersection_df = fstpy.load_data(level_intersection_df)
        qv_df = get_from_dataframe(level_intersection_df,'QV')
        px_df = get_from_dataframe(level_intersection_df,'PX')
        vppr_df = create_empty_result(qv_df,self.plugin_result_specifications['VPPR'],all_rows=True)
        qv_df = fstpy.unit_convert(qv_df,'kilogram_per_kilogram')
        for i in vppr_df.index:
            qv = qv_df.at[i,'d']
            px = px_df.at[i,'d']
            vppr_df.at[i,'d'] = vppr_from_qv(qv=qv, px=px).astype(np.float32)
        return vppr_df

    def vapourpressure_from_tt_td(self, td_df, level_intersection_df, option):
        sys.stdout.write(f'option {option+1}\n')
        td_df = fstpy.load_data(td_df)
        level_intersection_df = fstpy.load_data(level_intersection_df)
        tt_df = get_from_dataframe(level_intersection_df,'TT')
        vppr_df = create_empty_result(tt_df,self.plugin_result_specifications['VPPR'],all_rows=True)
        for i in vppr_df.index:
            tt = tt_df.at[i,'d']
            td = td_df.at[i,'d']
            vppr_df.at[i,'d'] = vppr_from_td(td=td-TDPACK_OFFSET_FIX, tt=tt-TDPACK_OFFSET_FIX, tpl=(self.temp_phase_switch if self.ice_water_phase!='water' else -40), swph=self.ice_water_phase=='both').astype(np.float32)
        return vppr_df

    def rpn_vapourpressure_from_hu_px(self, hu_df, level_intersection_df,option):
        sys.stdout.write(f'rpn option {option+1}\n')
        hu_df = fstpy.load_data(hu_df)
        level_intersection_df = fstpy.load_data(level_intersection_df)
        px_df = get_from_dataframe(level_intersection_df,'PX')
        vppr_df = create_empty_result(px_df,self.plugin_result_specifications['VPPR'],all_rows=True)
        pxpa_df = fstpy.unit_convert(px_df,'pascal')
        for i in vppr_df.index:
            pxpa = pxpa_df.at[i,'d']
            hu = hu_df.at[i,'d']
            vppr_df.at[i,'d'] = rpn_vppr_from_hu(hu=hu, px=pxpa).astype(np.float32)
        return vppr_df

    def compute_hu(self, level_intersection_df):
        from ..humidityspecific import HumiditySpecific
        hu_df = HumiditySpecific(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, temp_phase_switch_unit=self.temp_phase_switch_unit,rpn=True).compute()
        hu_df = get_from_dataframe(hu_df,'HU')
        return hu_df

    def compute_td(self, level_intersection_df):
        from ..temperaturedewpoint import TemperatureDewPoint
        td_df = TemperatureDewPoint(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=self.temp_phase_switch,temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
        td_df = get_from_dataframe(td_df,'TD')
        return td_df
