# -*- coding: utf-8 -*-
from numpy import float32
from ..temperaturedewpoint import TemperatureDewPoint
from ..humidityutils import calc_humidex
from ..utils import create_empty_result, get_existing_result, get_intersecting_levels, get_plugin_dependencies, existing_results, final_results
from ..plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
import sys
from ..saturationvapourpressure import SaturationVapourPressure



class HumidexError(Exception):
    pass

class Humidex(Plugin):

    def __init__(self,df:pd.DataFrame):
        self.plugin_mandatory_dependencies_option_1 = {
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
            'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','surface':True,'select_only':True},
        }

        self.plugin_mandatory_dependencies_option_2 = {
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
            'HR':{'nomvar':'HR','unit':'scalar','surface':True,'select_only':True},
        }


        self.plugin_mandatory_dependencies_option_3 = {
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
            'QV':{'nomvar':'QV','unit':'gram_per_kilogram','surface':True,'select_only':True},
        }


        self.plugin_mandatory_dependencies_option_4 = {
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
            'TD':{'nomvar':'TD','unit':'celsius','surface':True,'select_only':True}
        }

        self.plugin_mandatory_dependencies_option_5 = {
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
            'ES':{'nomvar':'ES','unit':'celsius','surface':True,'select_only':True}
        }

        self.plugin_result_specifications = {
            'HMX':{'nomvar':'HMX','etiket':'Humidex','unit':'scalar','ip1':0}
        }

        self.df = df

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise HumidexError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])

        print(self.df[['nomvar','typvar','etiket','unit','surface','grid','forecast_hour']].sort_values(by=['grid','nomvar']).to_string())
        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)


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
        if not self.existing_result_df.empty:
            return existing_results('Humidex',self.existing_result_df,self.meta_df)

        sys.stdout.write('Humidex - compute\n')
        df_list=[]
        for _, current_fhour_group in self.fhour_groups:
            if self.option==1:
                print('option 1')
                current_fhour_group = fstpy.load_data(current_fhour_group)
                if len(current_fhour_group.index) != 2:
                    continue
                tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],copy=True)
                td_df = TemperatureDewPoint(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                td_df = td_df.loc[td_df.nomvar=='TD'].reset_index(drop=True)
                tttd_df = td_df.copy(deep=True)
                tttd_df.loc[:,'nomvar'] = 'TT'
                svp_df = SaturationVapourPressure(pd.concat([tttd_df,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                svp_df = svp_df.loc[svp_df.nomvar=='SVP'].reset_index(drop=True)
                for i in td_df.index:
                    tt = tt_df.at[i,'d']
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = calc_humidex(tt,svp).astype(float32)

            elif self.option==2:
                print('option 2')
                current_fhour_group = fstpy.load_data(current_fhour_group)
                if len(current_fhour_group.index) != 2:
                    continue
                tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],copy=True)
                td_df = TemperatureDewPoint(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                td_df = td_df.loc[td_df.nomvar=='TD'].reset_index(drop=True)
                tttd_df = td_df.copy(deep=True)
                tttd_df.loc[:,'nomvar'] = 'TT'
                svp_df = SaturationVapourPressure(pd.concat([tttd_df,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                svp_df = svp_df.loc[svp_df.nomvar=='SVP'].reset_index(drop=True)
                for i in td_df.index:
                    tt = tt_df.at[i,'d']
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = calc_humidex(tt,svp).astype(float32)
            elif self.option==3:
                print('option 3')
                current_fhour_group = fstpy.load_data(current_fhour_group)
                if len(current_fhour_group.index) != 2:
                    continue
                tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],copy=True)
                td_df = TemperatureDewPoint(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                td_df = td_df.loc[td_df.nomvar=='TD'].reset_index(drop=True)
                tttd_df = td_df.copy(deep=True)
                tttd_df.loc[:,'nomvar'] = 'TT'
                svp_df = SaturationVapourPressure(pd.concat([tttd_df,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                svp_df = svp_df.loc[svp_df.nomvar=='SVP'].reset_index(drop=True)
                for i in td_df.index:
                    tt = tt_df.at[i,'d']
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = calc_humidex(tt,svp).astype(float32)
            elif self.option==4:
                print('option 4')
                current_fhour_group = fstpy.load_data(current_fhour_group)
                if len(current_fhour_group.index) != 2:
                    continue
                tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                td_df = current_fhour_group.loc[current_fhour_group.nomvar=='TD'].reset_index(drop=True)
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],copy=True)
                tttd_df = td_df.copy(deep=True)
                tttd_df.loc[:,'nomvar'] = 'TT'
                svp_df = SaturationVapourPressure(pd.concat([tttd_df,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                svp_df = svp_df.loc[svp_df.nomvar=='SVP'].reset_index(drop=True)
                for i in td_df.index:
                    tt = tt_df.at[i,'d']
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = calc_humidex(tt,svp).astype(float32)
            else:
                print('option 5')
                current_fhour_group = fstpy.load_data(current_fhour_group)
                if len(current_fhour_group.index) != 2:
                    continue
                tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],copy=True)
                td_df = TemperatureDewPoint(pd.concat([current_fhour_group,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                td_df = td_df.loc[td_df.nomvar=='TD'].reset_index(drop=True)
                tttd_df = td_df.copy(deep=True)
                tttd_df.loc[:,'nomvar'] = 'TT'
                svp_df = SaturationVapourPressure(pd.concat([tttd_df,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                svp_df = svp_df.loc[svp_df.nomvar=='SVP'].reset_index(drop=True)
                for i in td_df.index:
                    tt = tt_df.at[i,'d']
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = calc_humidex(tt,svp).astype(float32)

            df_list.append(hmx_df)

        return final_results(df_list, HumidexError, self.meta_df)
