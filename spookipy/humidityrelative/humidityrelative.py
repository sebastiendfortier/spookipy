# -*- coding: utf-8 -*-
import sys

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils import get_temp_phase_switch, validate_humidity_parameters
from ..plugin import Plugin
from ..science.science import *
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     get_intersecting_levels,
                     initializer)


class HumidityRelativeError(Exception):
    pass

class HumidityRelative(Plugin):


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
            'TT':{'nomvar':'TT','unit':'celsius'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'TD':{'nomvar':'TD','unit':'celsius','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius'},
                'ES':{'nomvar':'ES','unit':'celsius','select_only':True},
                'PX':{'nomvar':'PX','unit':'hectoPascal'},
            }
        ]

        self.plugin_result_specifications = {
            'HR':{'nomvar':'HR','etiket':'HUMREL','unit':'scalar','nbits':12,'datyp':1}
            }
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise  HumidityRelativeError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(self.df, decode=True, columns=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(HumidityRelativeError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)


        self.temp_phase_switch = get_temp_phase_switch(HumidityRelativeError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)


        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)
        # print(self.df[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])



    def compute(self) -> pd.DataFrame:
        from ..dewpointdepression.dewpointdepression import DewPointDepression
        from ..humidityspecific.humidityspecific import HumiditySpecific
        from ..saturationvapourpressure.saturationvapourpressure import \
            SaturationVapourPressure
        from ..vapourpessure.vapourpessure import VapourPressure
        if not self.existing_result_df.empty:
            return existing_results('HumidityRelative',self.existing_result_df,self.meta_df)

        sys.stdout.write('HumidityRelative - compute\n')
        df_list = []

        if self.rpn:
            dependencies_list = get_dependencies(self.groups,self.meta_df,'HumidityRelative',self.plugin_mandatory_dependencies_rpn,self.plugin_params)
        else:
            dependencies_list = get_dependencies(self.groups,self.meta_df,'HumidityRelative',self.plugin_mandatory_dependencies,self.plugin_params)

        for dependencies_df,option in dependencies_list:
            if self.rpn:
                if option==0:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    hu_df = get_from_dataframe(level_intersection_df,'HU')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],all_rows=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hr_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        pxpa = pxpa_df.at[i,'d']
                        hu = hu_df.at[i,'d']
                        hr_df.at[i,'d'] = science.rpn_hr_from_hu(tt=ttk,hu=hu,px=pxpa,ni=ni,nj=nj,swph=self.ice_water_phase=='both').astype(np.float32)

                elif option==1:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    qv_df = get_from_dataframe(level_intersection_df,'QV')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],all_rows=True)
                    hu_df = HumiditySpecific(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, rpn=True).compute()
                    hu_df = get_from_dataframe(hu_df,'HU')
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hr_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        pxpa = pxpa_df.at[i,'d']
                        hu = hu_df.at[i,'d']
                        hr_df.at[i,'d'] = science.rpn_hr_from_hu(tt=ttk,hu=hu,px=pxpa,ni=ni,nj=nj,swph=self.ice_water_phase=='both').astype(np.float32)

                elif option==2:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    es_df = get_from_dataframe(level_intersection_df,'ES')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],all_rows=True)
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hr_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        pxpa = pxpa_df.at[i,'d']
                        es = es_df.at[i,'d']
                        hr_df.at[i,'d'] = science.rpn_hr_from_es(tt=ttk, es=es, px=pxpa, swph=self.ice_water_phase=='both').astype(np.float32)
                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = get_from_dataframe(level_intersection_df,'TD')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],all_rows=True)
                    es_df = DewPointDepression(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase, temp_phase_switch=self.temp_phase_switch, rpn=True).compute()
                    es_df = get_from_dataframe(es_df,'ES')
                    ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                    pxpa_df = fstpy.unit_convert(px_df,'pascal')
                    for i in hr_df.index:
                        ttk = ttk_df.at[i,'d']
                        ni = ttk.shape[0]
                        nj = ttk.shape[1]
                        pxpa = pxpa_df.at[i,'d']
                        es = es_df.at[i,'d']
                        hr_df.at[i,'d'] = science.rpn_hr_from_es(tt=ttk, es=es, px=pxpa, swph=self.ice_water_phase=='both').astype(np.float32)

            else: # not rpn
                if option==0:
                    print('option 1')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    hu_df = get_from_dataframe(level_intersection_df,'HU')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],all_rows=True)
                    svp_df = SaturationVapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=(self.temp_phase_switch if self.ice_water_phase!='water' else None)).compute()
                    svp_df = get_from_dataframe(svp_df,'SVP')
                    vppr_df = VapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=(self.temp_phase_switch if self.ice_water_phase!='water' else None)).compute()
                    vppr_df = get_from_dataframe(vppr_df,'VPPR')
                    for i in hr_df.index:
                        svp = svp_df.at[i,'d']
                        ni = svp.shape[0]
                        nj = svp.shape[1]
                        vppr = vppr_df.at[i,'d']
                        hr_df.at[i,'d'] = science.hr_from_svp_vppr(svp=svp,vppr=vppr,ni=ni,nj=nj).astype(np.float32)

                elif option==1:
                    print('option 2')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    qv_df = get_from_dataframe(level_intersection_df,'QV')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],all_rows=True)
                    svp_df = SaturationVapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=(self.temp_phase_switch if self.ice_water_phase!='water' else None)).compute()
                    svp_df = get_from_dataframe(svp_df,'SVP')
                    vppr_df = VapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=(self.temp_phase_switch if self.ice_water_phase!='water' else None)).compute()
                    vppr_df = get_from_dataframe(vppr_df,'VPPR')

                    for i in hr_df.index:
                        svp = svp_df.at[i,'d']
                        ni = svp.shape[0]
                        nj = svp.shape[1]
                        vppr = vppr_df.at[i,'d']
                        hr_df.at[i,'d'] = science.hr_from_svp_vppr(svp=svp,vppr=vppr,ni=ni,nj=nj).astype(np.float32)

                elif option==2:
                    print('option 3')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    td_df = get_from_dataframe(level_intersection_df,'TD')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],all_rows=True)
                    svp_df = SaturationVapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=(self.temp_phase_switch if self.ice_water_phase!='water' else None)).compute()
                    svp_df = get_from_dataframe(svp_df,'SVP')
                    vppr_df = VapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=(self.temp_phase_switch if self.ice_water_phase!='water' else None)).compute()
                    vppr_df = get_from_dataframe(vppr_df,'VPPR')

                    for i in hr_df.index:
                        svp = svp_df.at[i,'d']
                        ni = svp.shape[0]
                        nj = svp.shape[1]
                        vppr = vppr_df.at[i,'d']
                        hr_df.at[i,'d'] = science.hr_from_svp_vppr(svp=svp,vppr=vppr,ni=ni,nj=nj).astype(np.float32)
                else:
                    print('option 4')
                    level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                    level_intersection_df = fstpy.load_data(level_intersection_df)
                    tt_df = get_from_dataframe(level_intersection_df,'TT')
                    es_df = get_from_dataframe(level_intersection_df,'ES')
                    px_df = get_from_dataframe(level_intersection_df,'PX')
                    hr_df = create_empty_result(tt_df,self.plugin_result_specifications['HR'],all_rows=True)
                    svp_df = SaturationVapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=(self.temp_phase_switch if self.ice_water_phase!='water' else None)).compute()
                    svp_df = get_from_dataframe(svp_df,'SVP')
                    vppr_df = VapourPressure(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase=self.ice_water_phase,temp_phase_switch=(self.temp_phase_switch if self.ice_water_phase!='water' else None)).compute()
                    vppr_df = get_from_dataframe(vppr_df,'VPPR')
                    for i in hr_df.index:
                        svp = svp_df.at[i,'d']
                        ni = svp.shape[0]
                        nj = svp.shape[1]
                        vppr = vppr_df.at[i,'d']
                        hr_df.at[i,'d'] = science.hr_from_svp_vppr(svp=svp,vppr=vppr,ni=ni,nj=nj).astype(np.float32)

            df_list.append(hr_df)


        return final_results(df_list, HumidityRelativeError, self.meta_df)
