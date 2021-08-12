# -*- coding: utf-8 -*-
from numpy import float32
from ..humidityutils import calc_humidex
from ..utils import create_empty_result, get_existing_result, get_plugin_dependencies, existing_results, final_results
from ..plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
import sys
from ..saturationvapourpressure import SaturationVapourPressure



class HumidexError(Exception):
    pass

class Humidex(Plugin):

    def __init__(self,df:pd.DataFrame):
        self.plugin_mandatory_dependencies = {
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
            'TD':{'nomvar':'TD','unit':'celsius','surface':True},
        }

        self.plugin_result_specifications = {
            'HMX':{'nomvar':'HMX','etiket':'Humidex','unit':'scalar','ip1':0,'surface':True}
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
            self.dependencies_df = get_plugin_dependencies(self.df,{'ice_water_phase':'water'},self.plugin_mandatory_dependencies)
            self.fhour_groups = self.dependencies_df.groupby(['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('Humidex',self.existing_result_df,self.meta_df)

        sys.stdout.write('Humidex - compute\n')
        df_list=[]
        for _, current_fhour_group in self.fhour_groups:
            current_fhour_group = fstpy.load_data(current_fhour_group)
            tt_df = current_fhour_group.loc[current_fhour_group.nomvar=='TT'].reset_index(drop=True)
            td_df = current_fhour_group.loc[current_fhour_group.nomvar=='TD'].reset_index(drop=True)
            if tt_df.empty or td_df.empty:
                continue
            hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],copy=True)
            td_df.loc[:,'nomvar'] = 'TT'
            svp_df = SaturationVapourPressure(pd.concat([td_df,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
            svp_df = svp_df.loc[svp_df.nomvar=='SVP'].reset_index(drop=True)
            for i in td_df.index:
                tt = tt_df.at[i,'d']
                svp = svp_df.at[i,'d']
                hmx_df.at[i,'d'] = calc_humidex(tt,svp).astype(float32)


            df_list.append(hmx_df)

        return final_results(df_list, HumidexError, self.meta_df)
