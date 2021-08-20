# -*- coding: utf-8 -*-

from ..utils import create_empty_result, get_existing_result, get_intersecting_levels, get_plugin_dependencies, existing_results, final_results
from ..plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
import sys
import numpy as np
from ..science.science import *


class HumidexError(Exception):
    pass

class Humidex(Plugin):

    def __init__(self,df:pd.DataFrame):
        self.plugin_mandatory_dependencies_option_1 = {
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True,'surface':True},
        }

        self.plugin_mandatory_dependencies_option_2 = {
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True,'surface':True},
        }
        self.plugin_mandatory_dependencies_option_3 = {
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True,'surface':True},
        }
        self.plugin_mandatory_dependencies_option_4 = {
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
            'TD':{'nomvar':'TD','unit':'celsius','select_only':True,'surface':True},
        }
        self.plugin_mandatory_dependencies_option_5 = {
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
            'ES':{'nomvar':'ES','unit':'celsius','select_only':True,'surface':True},
        }
        self.plugin_result_specifications = {
            'HMX':{'nomvar':'HMX','etiket':'HUMIDX','unit':'scalar','ip1':0,'surface':True,'surface':True}
        }

        self.df = df

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise HumidexError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])

        # print(self.df[['nomvar','typvar','etiket','unit','surface','grid','forecast_hour']].sort_values(by=['grid','nomvar']).to_string())
        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        self.df = self.df.loc[self.df.surface==True]
        self.df = pd.concat([self.df,self.meta_df],ignore_index=True)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,None,self.plugin_mandatory_dependencies_option_1,throw_error=False)
            self.option=1
            if self.dependencies_df.empty:
                self.dependencies_df = get_plugin_dependencies(self.df,None,self.plugin_mandatory_dependencies_option_2,throw_error=False)
                self.option=2
            if self.dependencies_df.empty:
                self.dependencies_df = get_plugin_dependencies(self.df,None,self.plugin_mandatory_dependencies_option_3,throw_error=False)
                self.option=3
            if self.dependencies_df.empty:
                self.dependencies_df = get_plugin_dependencies(self.df,None,self.plugin_mandatory_dependencies_option_4,throw_error=False)
                self.option=4
            if self.dependencies_df.empty:
                self.dependencies_df = get_plugin_dependencies(self.df,None,self.plugin_mandatory_dependencies_option_5)
                self.option=5
            self.fhour_groups = self.dependencies_df.groupby(['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        from ..saturationvapourpressure.saturationvapourpressure import SaturationVapourPressure
        from ..temperaturedewpoint.temperaturedewpoint import TemperatureDewPoint
        if not self.existing_result_df.empty:
            return existing_results('Humidex',self.existing_result_df,self.meta_df)

        sys.stdout.write('Humidex - compute\n')
        df_list=[]
        for _, current_fhour_group in self.fhour_groups:
            print('current_fhour_group\n',current_fhour_group)
            if self.option==1:
                print('option 1')
                level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_1)
                current_fhour_group = fstpy.load_data(level_intersection_df)
                tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].sort_values(by=['level']).reset_index(drop=True)
                hu_df = current_fhour_group.loc[current_fhour_group.nomvar=='HU'].sort_values(by=['level']).reset_index(drop=True)
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],copy=True)
                td_df = TemperatureDewPoint(current_fhour_group,ice_water_phase='water').compute()
                rentd_df = td_df
                rentd_df.loc[rentd_df.nomvar=='TD','nomvar'] == 'TT'
                svp_df = SaturationVapourPressure(rentd_df,ice_water_phase='water').compute()
                svp_df = svp_df.loc[svp_df.nomvar=='SVP'].sort_values(by=['level']).reset_index(drop=True)

                for i in hr_df.index:
                    tt = tt_df.at[i,'d']
                    ni= tt.shape[0]
                    nj= tt.shape[1]
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = science.hmx_from_svp(tt=tt,svp=svp,ni=ni,nj=nj).astype(np.float32)


            elif self.option==2:
                print('option 2')
                level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_2)
                current_fhour_group = fstpy.load_data(level_intersection_df)
                tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].sort_values(by=['level']).reset_index(drop=True)
                hr_df = current_fhour_group.loc[current_fhour_group.nomvar=='HR'].sort_values(by=['level']).reset_index(drop=True)
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],copy=True)
                td_df = TemperatureDewPoint(current_fhour_group,ice_water_phase='water').compute()
                rentd_df = td_df
                rentd_df.loc[rentd_df.nomvar=='TD','nomvar'] == 'TT'
                svp_df = SaturationVapourPressure(rentd_df,ice_water_phase='water').compute()
                svp_df = svp_df.loc[svp_df.nomvar=='SVP'].sort_values(by=['level']).reset_index(drop=True)

                for i in hr_df.index:
                    tt = tt_df.at[i,'d']
                    ni= tt.shape[0]
                    nj= tt.shape[1]
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = science.hmx_from_svp(tt=tt,svp=svp,ni=ni,nj=nj).astype(np.float32)


            elif self.option==3:
                print('option 3')
                level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_3)
                current_fhour_group = fstpy.load_data(level_intersection_df)
                tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].sort_values(by=['level']).reset_index(drop=True)
                qv_df = current_fhour_group.loc[current_fhour_group.nomvar=='QV'].sort_values(by=['level']).reset_index(drop=True)
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],copy=True)
                td_df = TemperatureDewPoint(current_fhour_group,ice_water_phase='water').compute()
                rentd_df = td_df
                rentd_df.loc[rentd_df.nomvar=='TD','nomvar'] == 'TT'
                svp_df = SaturationVapourPressure(rentd_df,ice_water_phase='water').compute()
                svp_df = svp_df.loc[svp_df.nomvar=='SVP'].sort_values(by=['level']).reset_index(drop=True)

                for i in hr_df.index:
                    tt = tt_df.at[i,'d']
                    ni= tt.shape[0]
                    nj= tt.shape[1]
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = science.hmx_from_svp(tt=tt,svp=svp,ni=ni,nj=nj).astype(np.float32)
            elif self.option==4:
                print('option 4')
                level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_4)
                current_fhour_group = fstpy.load_data(level_intersection_df)
                tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].sort_values(by=['level']).reset_index(drop=True)
                td_df = current_fhour_group.loc[current_fhour_group.nomvar=='TD'].sort_values(by=['level']).reset_index(drop=True)
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],copy=True)
                td_df = TemperatureDewPoint(current_fhour_group,ice_water_phase='water').compute()
                rentd_df = td_df
                rentd_df.loc[rentd_df.nomvar=='TD','nomvar'] == 'TT'
                svp_df = SaturationVapourPressure(rentd_df,ice_water_phase='water').compute()
                svp_df = svp_df.loc[svp_df.nomvar=='SVP'].sort_values(by=['level']).reset_index(drop=True)

                for i in hr_df.index:
                    tt = tt_df.at[i,'d']
                    ni= tt.shape[0]
                    nj= tt.shape[1]
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = science.hmx_from_svp(tt=tt,svp=svp,ni=ni,nj=nj).astype(np.float32)

            else:
                print('option 5')
                level_intersection_df = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies_option_5)
                current_fhour_group = fstpy.load_data(level_intersection_df)
                tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].sort_values(by=['level']).reset_index(drop=True)
                es_df = current_fhour_group.loc[current_fhour_group.nomvar=='ES'].sort_values(by=['level']).reset_index(drop=True)
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],copy=True)
                td_df = TemperatureDewPoint(current_fhour_group,ice_water_phase='water').compute()
                rentd_df = td_df
                rentd_df.loc[rentd_df.nomvar=='TD','nomvar'] == 'TT'
                svp_df = SaturationVapourPressure(rentd_df,ice_water_phase='water').compute()
                svp_df = svp_df.loc[svp_df.nomvar=='SVP'].sort_values(by=['level']).reset_index(drop=True)

                for i in hr_df.index:
                    tt = tt_df.at[i,'d']
                    ni= tt.shape[0]
                    nj= tt.shape[1]
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = science.hmx_from_svp(tt=tt,svp=svp,ni=ni,nj=nj).astype(np.float32)

            df_list.append(hmx_df)

        return final_results(df_list, HumidexError, self.meta_df)
