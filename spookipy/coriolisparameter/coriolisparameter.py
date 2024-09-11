# -*- coding: utf-8 -*-
import logging
import math

import fstpy
import numpy as np
import pandas as pd
import warnings

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, 
                     get_existing_result, initializer)

class CoriolisParameterError(Exception):
    pass

def coriolis_parameter(lat_2d: np.ndarray) -> np.ndarray:
    """computes the coriolis parameter for each latitude obtained from gdll (2d grid size latitudes)

    :param lat_2d: latitudes obtained from gdll (2d grid size latitudes)
    :type lat_2d: np.ndarray
    :return: coriolis parameter
    :rtype: np.ndarray
    """
    # 2 * omega = 0.00014584
    return 0.00014584 * np.sin(lat_2d * (math.pi / 180)).astype('float32')


class CoriolisParameterError(Exception):
    pass


class CoriolisParameter(Plugin):
    """Calculation of the Coriolis parameter

    :param df: input DataFrame
    :type df: pd.DataFrame
    """
    computable_plugin = "CORP"
    @initializer
    def __init__(self, 
                 df: pd.DataFrame,
                 copy_input = False,
                 reduce_df  = True
                 ):
        
        self.plugin_result_specifications = {
            'CORP': {
                'nomvar'  : 'CORP',
                'label'   : 'CORIOP',
                'unit'    : 'divergence',
                'level'   : 0,
                'ip1_kind': 2,
                'ip2_dec' : 0,
                'ip3_dec' : 0,
                'npas'    : 0,
                'datyp'   : 134,
                'nbits'   : 12}}

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):

        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=['ip_info'])

        # check if result already exists
        self.existing_result_df = get_existing_result(
            self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby('grid')

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'CoriolisParameter',
                self.existing_result_df,
                self.meta_df)

        logging.info('CoriolisParameter - compute')
        df_list = []
        for _, current_group in self.groups:
 
            latlon_df = fstpy.get_2d_lat_lon_df(pd.concat([ current_group,
                                                            self.meta_df ],
                                                            ignore_index=True))
            lat_df    = latlon_df.loc[latlon_df.nomvar =='LA'].reset_index(drop=True)

            if lat_df.empty:
                logging.warning(
                    'Cannot find "LA" field in this group - skipping')
                continue

            corp_df = create_empty_result(
                current_group, self.plugin_result_specifications['CORP'])
            
            corp_df = adjust_column_values(current_group, corp_df)

            for i in corp_df.index:
                corp_df.at[i, 'd'] = coriolis_parameter(lat_df.at[i, 'd']).astype('float32')

            df_list.append(corp_df)

        return self.final_results(df_list, CoriolisParameterError,
                                  copy_input = self.copy_input,
                                  reduce_df  = self.reduce_df)


def adjust_column_values(current_group, corp_df):
    # Suppression d'un future warning de pandas; dans notre cas, on veut conserver le meme comportement
    # meme avec le nouveau comportement a venir. On encapsule la suppression du warning pour ce cas seulement.
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=FutureWarning)
        corp_df.loc[:, 'typvar'] = current_group.typvar.unique()[0]
        corp_df.loc[:, 'grtyp']  = current_group.grtyp.unique()[0]
        corp_df.loc[:, 'ig1']    = current_group.ig1.unique()[0]
        corp_df.loc[:, 'ig2']    = current_group.ig2.unique()[0]
        corp_df.loc[:, 'ig3']    = current_group.ig3.unique()[0]
        corp_df.loc[:, 'ig4']    = current_group.ig4.unique()[0]

    return corp_df
