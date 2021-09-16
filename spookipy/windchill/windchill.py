# -*- coding: utf-8 -*-
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result,
                     get_from_dataframe)


class WindChillError(Exception):
    pass

def wind_chill(tt:np.ndarray,uv:np.ndarray) ->np.ndarray:
    """Calculates the wind chill

    :param tt: surface temperature
    :type tt: np.ndarray
    :param uv: surface wind modulus
    :type uv: np.ndarray
    :return: wind chill
    :rtype: np.ndarray
    """
    return np.where( (tt <= 0) & (uv >= 5), 13.12 + 0.6215 * tt + ( 0.3965 * tt - 11.37) * ( uv**0.16 ), tt)

class WindChill(Plugin):

    def __init__(self,df:pd.DataFrame):
        self.plugin_mandatory_dependencies =[ {
            'UV':{'nomvar':'UV','unit':'knot','surface':True},
            'TT':{'nomvar':'TT','unit':'celsius','surface':True},
        }]

        self.plugin_result_specifications = {
            'RE':{'nomvar':'RE','etiket':'WNDCHL','unit':'celsius','ip1':0}
            }
        self.df = df
        self.validate_input()


    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise  WindChillError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(self.df,True, columns=['unit','ip_info','forecast_hour'])

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])


    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('WindChill',self.existing_result_df,self.meta_df)

        logging.info('WindChill - compute')
        #holds data from all the groups
        df_list = []
        dependencies_list = get_dependencies(self.groups,self.meta_df,'WindChill',self.plugin_mandatory_dependencies)
        for dependencies_df,_ in dependencies_list:
            dependencies_df = fstpy.load_data(dependencies_df)
            tt_df = get_from_dataframe(dependencies_df,'TT')
            uv_df = get_from_dataframe(dependencies_df,'UV')
            uv_df = fstpy.unit_convert(uv_df,'kilometer_per_hour')
            re_df = create_empty_result(tt_df,self.plugin_result_specifications['RE'])

            for i in re_df.index:
                tt = tt_df.at[i,'d']
                uv = uv_df.at[i,'d']
                re_df.at[i,'d'] = wind_chill(tt,uv)

            df_list.append(re_df)

        return final_results(df_list,WindChillError, self.meta_df)
