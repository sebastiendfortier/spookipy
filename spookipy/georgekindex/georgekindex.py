# -*- coding: utf-8 -*-
import logging

import fstpy
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe)


class GeorgeKIndexError(Exception):
    pass


def george_k_index(tt850, tt700, tt500, td850, td700):
    return (tt850 - tt500) + td850 - (tt700 - td700)


class GeorgeKIndex(Plugin):
    """Calculation of the George-K index, a severe weather index used for forecasting thunderstorm

    :param df: input DataFrame
    :type df: pd.DataFrame
    """
    def __init__(self, df: pd.DataFrame):

        self.plugin_mandatory_dependencies = [
            {
                'TT1': {'nomvar': 'TT', 'unit': 'celsius', 'level': 500, 'ip1_pkind': 'mb'},
                'TT2': {'nomvar': 'TT', 'unit': 'celsius', 'level': 700, 'ip1_pkind': 'mb'},
                'TT3': {'nomvar': 'TT', 'unit': 'celsius', 'level': 850, 'ip1_pkind': 'mb'},
                'TD1': {'nomvar': 'TD', 'unit': 'celsius', 'level': 700, 'ip1_pkind': 'mb'},
                'TD2': {'nomvar': 'TD', 'unit': 'celsius', 'level': 850, 'ip1_pkind': 'mb'},
            }
        ]
        self.plugin_result_specifications = {
            'KI': {
                'nomvar': 'KI',
                'etiket': 'GEORKI',
                'unit': 'scalar',
                'ip1': 0}}
        self.df = df
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise GeorgeKIndexError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(self.df, columns=['unit', 'forecast_hour', 'ip_info'])

        # check if result already exists
        self.existing_result_df = get_existing_result(self.df, self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.groups = self.df.groupby(['grid', 'dateo', 'forecast_hour', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'GeorgeKIndex',
                self.existing_result_df,
                self.meta_df)

        logging.info('GeorgeKIndex - compute')
        df_list = []
        dependencies_list = get_dependencies(
            self.groups, self.meta_df, 'GeorgeKIndex', self.plugin_mandatory_dependencies, {
                'ice_water_phase': 'water'})

        for dependencies_df, _ in dependencies_list:

            tt_df = get_from_dataframe(dependencies_df, 'TT')
            td_df = get_from_dataframe(dependencies_df, 'TD')
            tt850_df = tt_df.loc[(tt_df.level == 850)].reset_index(drop=True)
            tt700_df = tt_df.loc[(tt_df.level == 700)].reset_index(drop=True)
            tt500_df = tt_df.loc[(tt_df.level == 500)].reset_index(drop=True)
            td850_df = td_df.loc[(td_df.level == 850)].reset_index(drop=True)
            td700_df = td_df.loc[(td_df.level == 700)].reset_index(drop=True)

            ki_df = create_empty_result(tt850_df, self.plugin_result_specifications['KI'])

            for i in ki_df.index:
                ki_df.at[i,'d'] = george_k_index(tt850_df.at[i,'d'],
                                               tt700_df.at[i,'d'],
                                               tt500_df.at[i,'d'],
                                               td850_df.at[i,'d'],
                                               td700_df.at[i,'d'])
            df_list.append(ki_df)

        return final_results(df_list, GeorgeKIndexError, self.meta_df)
