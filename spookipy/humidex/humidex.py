# -*- coding: utf-8 -*-
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin

from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result,
                     get_from_dataframe)

from ..science import hmx_from_svp

class HumidexError(Exception):
    pass

class Humidex(Plugin):

    def __init__(self,df:pd.DataFrame):
        self.plugin_mandatory_dependencies = [
            {
                'TT':{'nomvar':'TT','unit':'celsius','surface':True},
                'TD':{'nomvar':'TD','unit':'celsius','select_only':True,'surface':True},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius','surface':True},
                'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True,'surface':True},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius','surface':True},
                'HR':{'nomvar':'HR','unit':'scalar','select_only':True,'surface':True},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius','surface':True},
                'QV':{'nomvar':'QV','unit':'gram_per_kilogram','select_only':True,'surface':True},
            },
            {
                'TT':{'nomvar':'TT','unit':'celsius','surface':True},
                'ES':{'nomvar':'ES','unit':'celsius','select_only':True,'surface':True},
            }
        ]

        self.plugin_result_specifications = {
            'HMX':{'nomvar':'HMX','etiket':'HUMIDX','unit':'scalar','ip1':0,'surface':True,'surface':True}
        }

        self.df = df

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise HumidexError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(self.df, decode=True, columns=['unit','forecast_hour','ip_info'])

        # print(self.df[['nomvar','typvar','etiket','unit','surface','grid','forecast_hour']].sort_values(by=['grid','nomvar']).to_string())
        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        # select surface only
        self.df = self.df.loc[self.df.surface==True]

        self.df = pd.concat([self.df,self.meta_df],ignore_index=True)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('Humidex',self.existing_result_df,self.meta_df)

        logging.info('Humidex - compute\n')
        df_list=[]
        dependencies_list = get_dependencies(self.groups,self.meta_df,'Humidex',self.plugin_mandatory_dependencies,intersect_levels=True)

        for dependencies_df,option in dependencies_list:
            if option==0:
                # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                td_df = get_from_dataframe(dependencies_df,'TD')
                hmx_df = self.humidex_from_tt_svp(dependencies_df,td_df,option)

            else:
                # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                td_df = self.compute_td(dependencies_df)
                hmx_df = self.humidex_from_tt_svp(dependencies_df,td_df,option)

            df_list.append(hmx_df)

        return final_results(df_list, HumidexError, self.meta_df)

    def humidex_from_tt_svp(self, dependencies_df, td_df, option):
        from ..saturationvapourpressure.saturationvapourpressure import \
            SaturationVapourPressure
        logging.info(f'option {option+1}\n')
        td_df = fstpy.load_data(td_df)
        dependencies_df = fstpy.load_data(dependencies_df)
        tt_df = get_from_dataframe(dependencies_df,'TT')
        hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],all_rows=True)
        rentd_df = td_df
        rentd_df.loc[rentd_df.nomvar=='TD','nomvar'] = 'TT'
        svp_df = SaturationVapourPressure(rentd_df,ice_water_phase='water').compute()
        svp_df = get_from_dataframe(svp_df,'SVP')

        for i in hmx_df.index:
            tt = tt_df.at[i,'d']
            svp = svp_df.at[i,'d']
            hmx_df.at[i,'d'] = hmx_from_svp(tt=tt,svp=svp).astype(np.float32)
        return hmx_df

    def compute_td(self, dependencies_df):
        from ..temperaturedewpoint.temperaturedewpoint import \
            TemperatureDewPoint
        td_df = TemperatureDewPoint(pd.concat([dependencies_df,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
        return td_df
