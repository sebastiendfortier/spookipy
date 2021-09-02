# -*- coding: utf-8 -*-
import sys
from math import exp

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils import (TDPACK_OFFSET_FIX, get_temp_phase_switch,
                             validate_humidity_parameters)
from ..plugin import Plugin
from ..science.science import *
from ..utils import (create_empty_result, existing_results, final_results, find_matching_dependency_option,
                     get_existing_result, get_from_dataframe,
                     initializer)


class SaturationVapourPressureError(Exception):
    pass

class SaturationVapourPressure(Plugin):


    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}
        self.plugin_mandatory_dependencies = [
            {
            'TT':{'nomvar':'TT','unit':'celsius'}
            }
        ]
        self.plugin_result_specifications = {
            'SVP':{'nomvar':'SVP','etiket':'SVPRES','unit':'hectoPascal','nbits':16,'datyp':1},
        }
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise SaturationVapourPressureError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(self.df, decode=True, columns=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(SaturationVapourPressureError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(SaturationVapourPressureError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)
        # print(self.df[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('SaturationVapourPressure',self.existing_result_df,self.meta_df)

        sys.stdout.write('SaturationVapourPressure - compute\n')
        df_list=[]

        for _, current_group in self.groups:
            # print(current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
            sys.stdout.write('SaturationVapourPressure - Checking rpn dependencies\n')
            dependencies_df, _ = find_matching_dependency_option(pd.concat([current_group,self.meta_df],ignore_index=True),self.plugin_params,self.plugin_mandatory_dependencies)
            if dependencies_df.empty:
                sys.stdout.write('SaturationVapourPressure - No matching dependencies found for this group \n%s\n'%current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']])
                continue
            else:
                sys.stdout.write('SaturationVapourPressure - Matching dependencies found for this group \n%s\n'%current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']])


            dependencies_df = fstpy.load_data(dependencies_df)
            tt_df = get_from_dataframe(dependencies_df,'TT')
            svp_df = create_empty_result(tt_df,self.plugin_result_specifications['SVP'],all_rows=True)

            if self.rpn:
                print('rpn')
                print('option 1')
                ttk_df = fstpy.unit_convert(tt_df,'kelvin')
                for i in svp_df.index:
                    ttk = ttk_df.at[i,'d']
                    ni = ttk.shape[0]
                    nj = ttk.shape[1]
                    svp_df.at[i,'d'] = science.rpn_svp_from_tt(tt=ttk, ni=ni.shape[0], nj=nj, tpl=(self.temp_phase_switch if self.ice_water_phase!='water' else -40), swph=self.ice_water_phase=='both').astype(np.float32)
            else:
                print('option 1')
                for i in tt_df.index:
                    tt = tt_df.at[i,'d']
                    ni = tt.shape[0]
                    nj = tt.shape[1]
                    svp_df.at[i,'d'] = science.svp_from_tt(tt=tt-TDPACK_OFFSET_FIX, ni=ni, nj=nj, tpl=(self.temp_phase_switch if self.ice_water_phase!='water' else -40), swph=self.ice_water_phase=='both').astype(np.float32)

            df_list.append(svp_df)


        return final_results(df_list,SaturationVapourPressureError, self.meta_df)
