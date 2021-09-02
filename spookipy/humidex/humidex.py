# -*- coding: utf-8 -*-

import sys

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..science.science import *
from ..utils import (create_empty_result, existing_results, final_results,
                     find_matching_dependency_option, get_existing_result,
                     get_from_dataframe, get_intersecting_levels)


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

        self.df = self.df.loc[self.df.surface==True]
        self.df = pd.concat([self.df,self.meta_df],ignore_index=True)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)
        # print(self.df[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])

    def compute(self) -> pd.DataFrame:
        from ..saturationvapourpressure.saturationvapourpressure import \
            SaturationVapourPressure
        from ..temperaturedewpoint.temperaturedewpoint import \
            TemperatureDewPoint
        if not self.existing_result_df.empty:
            return existing_results('Humidex',self.existing_result_df,self.meta_df)

        sys.stdout.write('Humidex - compute\n')
        df_list=[]
        for _, current_group in self.groups:
            # print('current_group\n',pd.concat([current_group,self.meta_df],ignore_index=True)[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
            sys.stdout.write('Humidex - Checking dependencies\n')
            dependencies_df, option = find_matching_dependency_option(pd.concat([current_group,self.meta_df],ignore_index=True),None,self.plugin_mandatory_dependencies)
            if dependencies_df.empty:
                sys.stdout.write('Humidex - No matching dependencies found for this group \n%s\n'%current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']])
                continue
            else:
                sys.stdout.write('Humidex - Matching dependencies found for this group \n%s\n'%current_group[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']])

            if option==0:
                print('option 1')
                level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                level_intersection_df = fstpy.load_data(level_intersection_df)
                tt_df = get_from_dataframe(level_intersection_df,'TT')
                td_df = get_from_dataframe(level_intersection_df,'TD')
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],all_rows=True)
                # td_df = TemperatureDewPoint(level_intersection_df,ice_water_phase='water').compute()
                rentd_df = td_df
                rentd_df.loc[rentd_df.nomvar=='TD','nomvar'] = 'TT'
                svp_df = SaturationVapourPressure(rentd_df,ice_water_phase='water').compute()
                svp_df = get_from_dataframe(svp_df,'SVP')

                for i in hmx_df.index:
                    tt = tt_df.at[i,'d']
                    ni= tt.shape[0]
                    nj= tt.shape[1]
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = science.hmx_from_svp(tt=tt,svp=svp,ni=ni,nj=nj).astype(np.float32)

            elif option==1:
                print('option 2')
                level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                level_intersection_df = fstpy.load_data(level_intersection_df)
                tt_df = get_from_dataframe(level_intersection_df,'TT')
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],all_rows=True)
                td_df = TemperatureDewPoint(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                rentd_df = td_df
                rentd_df.loc[rentd_df.nomvar=='TD','nomvar'] = 'TT'
                svp_df = SaturationVapourPressure(rentd_df,ice_water_phase='water').compute()
                svp_df = get_from_dataframe(svp_df,'SVP')

                for i in hmx_df.index:
                    tt = tt_df.at[i,'d']
                    ni= tt.shape[0]
                    nj= tt.shape[1]
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = science.hmx_from_svp(tt=tt,svp=svp,ni=ni,nj=nj).astype(np.float32)


            elif option==2:
                print('option 3')
                level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                level_intersection_df = fstpy.load_data(level_intersection_df)
                tt_df = get_from_dataframe(level_intersection_df,'TT')
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],all_rows=True)
                td_df = TemperatureDewPoint(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                rentd_df = td_df
                rentd_df.loc[rentd_df.nomvar=='TD','nomvar'] = 'TT'
                svp_df = SaturationVapourPressure(rentd_df,ice_water_phase='water').compute()
                print('---SaturationVapourPressure',td_df.nomvar.unique())
                svp_df = SaturationVapourPressure(td_df,ice_water_phase='water').compute()
                svp_df = get_from_dataframe(svp_df,'SVP')

                for i in hmx_df.index:
                    tt = tt_df.at[i,'d']
                    ni= tt.shape[0]
                    nj= tt.shape[1]
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = science.hmx_from_svp(tt=tt,svp=svp,ni=ni,nj=nj).astype(np.float32)


            elif option==3:
                print('option 4')
                level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                level_intersection_df = fstpy.load_data(level_intersection_df)
                tt_df = get_from_dataframe(level_intersection_df,'TT')
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],all_rows=True)
                td_df = TemperatureDewPoint(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                rentd_df = td_df
                rentd_df.loc[rentd_df.nomvar=='TD','nomvar'] = 'TT'
                svp_df = SaturationVapourPressure(rentd_df,ice_water_phase='water').compute()
                svp_df = get_from_dataframe(svp_df,'SVP')

                for i in hmx_df.index:
                    tt = tt_df.at[i,'d']
                    ni= tt.shape[0]
                    nj= tt.shape[1]
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = science.hmx_from_svp(tt=tt,svp=svp,ni=ni,nj=nj).astype(np.float32)

            else:
                print('option 5')
                level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                level_intersection_df = fstpy.load_data(level_intersection_df)
                tt_df = get_from_dataframe(level_intersection_df,'TT')
                hmx_df = create_empty_result(tt_df,self.plugin_result_specifications['HMX'],all_rows=True)
                td_df = TemperatureDewPoint(pd.concat([level_intersection_df,self.meta_df],ignore_index=True),ice_water_phase='water').compute()
                rentd_df = td_df
                rentd_df.loc[rentd_df.nomvar=='TD','nomvar'] = 'TT'
                svp_df = SaturationVapourPressure(rentd_df,ice_water_phase='water').compute()
                svp_df = get_from_dataframe(svp_df,'SVP')

                for i in hmx_df.index:
                    tt = tt_df.at[i,'d']
                    ni= tt.shape[0]
                    nj= tt.shape[1]
                    svp = svp_df.at[i,'d']
                    hmx_df.at[i,'d'] = science.hmx_from_svp(tt=tt,svp=svp,ni=ni,nj=nj).astype(np.float32)

            df_list.append(hmx_df)

        return final_results(df_list, HumidexError, self.meta_df)
