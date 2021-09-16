# -*- coding: utf-8 -*-
from numpy import float32
from ..utils import create_empty_result, get_existing_result, existing_results, final_results
from ..plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
import logging
import math
import numpy as np


def coriolis_parameter(lat_2d:np.ndarray) -> np.ndarray:
    """computes the coriolis parameter for each latitude obtained from gdll (2d grid size latitudes)

    :param lat_2d: latitudes obtained from gdll (2d grid size latitudes)
    :type lat_2d: np.ndarray
    :return: coriolis parameter
    :rtype: np.ndarray
    """
    # 2 * omega = 0.00014584
    return 0.00014584 * np.sin(lat_2d * (math.pi/180)).astype(float32)

class CoriolisParameterError(Exception):
    pass

class CoriolisParameter(Plugin):

    def __init__(self,df:pd.DataFrame):

        self.plugin_result_specifications = {
            'CORP':{'nomvar':'CORP','etiket':'CORIOP','unit':'divergence','ip1':0,'ip2':0,'ip3':0,'datyp':134,'nbits':12}
        }

        self.df = df

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise CoriolisParameterError('No data to process')

        self.df = fstpy.add_columns(self.df,True, columns=['unit'])

        self.df = fstpy.metadata_cleanup(self.df)

        # print(self.df[['nomvar','typvar','etiket','unit','surface','grid','forecast_hour']].sort_values(by=['grid','nomvar']).to_string())
        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        self.groups = self.df.groupby(['grid'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('CoriolisParameter',self.existing_result_df,self.meta_df)

        logging.info('CoriolisParameter - compute')
        df_list=[]
        for _, current_group in self.groups:
            latlon_df = fstpy.get_2d_lat_lon(current_group)
            lat_df = latlon_df.loc[latlon_df.nomvar=='LA'].reset_index(drop=True)
            if lat_df.empty:
                logging.warning('Cannot find "LA" field in this group - skipping')
                continue
            # remove meta
            current_group = current_group.loc[~current_group.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)
            if current_group.empty:
                logging.warning('Cannot find "LON" field in this group - skipping')
                continue

            corp_df = create_empty_result(lat_df,self.plugin_result_specifications['CORP'])
            corp_df = adjust_column_values(current_group, corp_df)

            for i in corp_df.index:
                corp_df.at[i,'d'] = coriolis_parameter(lat_df.at[i,'d']).astype(float32)

            df_list.append(corp_df)

        return final_results(df_list, CoriolisParameterError, self.meta_df)

def adjust_column_values(current_group, corp_df):
    corp_df.loc[:,'typvar'] = current_group.typvar.unique()[0]
    corp_df.loc[:,'grtyp'] = current_group.grtyp.unique()[0]
    corp_df.loc[:,'ig1'] = current_group.ig1.unique()[0]
    corp_df.loc[:,'ig2'] = current_group.ig2.unique()[0]
    corp_df.loc[:,'ig3'] = current_group.ig3.unique()[0]
    corp_df.loc[:,'ig4'] = current_group.ig4.unique()[0]
    return corp_df
