# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results,
                     get_dependencies, get_existing_result, get_from_dataframe, initializer)


class TotalTotalsIndexError(Exception):
    pass


def total_totals_index(
        tt850: np.ndarray,
        tt500: np.ndarray,
        td850: np.ndarray) -> np.ndarray:
    return tt850 + td850 - 2 * tt500


class TotalTotalsIndex(Plugin):
    computable_plugin = "TTI"
    @initializer
    def __init__(self, df: pd.DataFrame, copy_input=False):

        self.plugin_mandatory_dependencies = [
            {
                'TT1': {'nomvar': 'TT', 'unit': 'celsius', 'level': 850, 'ip1_pkind': 'mb'},
                'TT2': {'nomvar': 'TT', 'unit': 'celsius', 'level': 500, 'ip1_pkind': 'mb'},
                'OTHERS': {'level': 850, 'ip1_pkind': 'mb'},
            }
        ]

        self.plugin_result_specifications = {
            'TTI': {
                'nomvar': 'TTI',
                'label' : 'TOTALI',
                'unit'  : 'celsius',
                'ip1'   : 0,
                'level' : 0}
        }
        
        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
    
        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=[
                'unit', 'forecast_hour', 'ip_info'])
        
        # check if result already exists
        self.existing_result_df = get_existing_result(
            self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(
            ['grid', 'datev', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        from .. import TemperatureDewPoint
        if not self.existing_result_df.empty:
            return existing_results(
                'TotalTotalsIndex',
                self.existing_result_df,
                self.meta_df)

        logging.info('TotalTotalsIndex - compute')
        df_list = []
        dependencies_list = get_dependencies(
            self.groups,
            self.meta_df,
            'TotalTotalsIndex',
            self.plugin_mandatory_dependencies)

        for dependencies_df, _ in dependencies_list:

            tt_df = get_from_dataframe(dependencies_df, 'TT')
            tt850_df = tt_df.loc[(tt_df.level == 850)].reset_index(drop=True)
            tt500_df = tt_df.loc[(tt_df.level == 500)].reset_index(drop=True)
            td_df = TemperatureDewPoint(
                dependencies_df, ice_water_phase='water').compute()
            td_df = get_from_dataframe(td_df, 'TD')
            td850_df = td_df.loc[(td_df.level == 850)].reset_index(drop=True)

            tti_df = create_empty_result(
                td850_df, self.plugin_result_specifications['TTI'])

            for i in tti_df.index:
                tti_df.at[i, 'd'] = total_totals_index(
                    tt850_df.at[i, 'd'], tt500_df.at[i, 'd'], td850_df.at[i, 'd'])
            df_list.append(tti_df)

        return self.final_results(df_list, 
                                  TotalTotalsIndexError, 
                                  copy_input = self.copy_input)
