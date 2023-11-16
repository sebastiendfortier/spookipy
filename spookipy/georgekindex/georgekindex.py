# -*- coding: utf-8 -*-
import logging
import fstpy
import pandas as pd
from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, initializer,
                     get_dependencies, get_existing_result, get_from_dataframe)


class GeorgeKIndexError(Exception):
    pass


def george_k_index(tt850, tt700, tt500, td850, td700):
    return (tt850 - tt500) + td850 - (tt700 - td700)


class GeorgeKIndex(Plugin):
    """Calculation of the George-K index, a severe weather index used for forecasting thunderstorm

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional 
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """
    computable_plugin = "KI"
    @initializer
    def __init__(
            self, 
            df: pd.DataFrame,
            copy_input = False,
            reduce_df  = True):

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
                'nomvar'  : 'KI',
                'label'   : 'GEORKI',
                'unit'    : 'scalar',
                'level'   : 0,
                'ip1_kind': 2}
                }

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):

        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=['unit', 'forecast_hour', 'ip_info'])

        # check if result already exists
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)
        self.groups = self.no_meta_df.groupby(['grid', 'datev', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'GeorgeKIndex',
                self.existing_result_df,
                self.meta_df)

        logging.info('GeorgeKIndex - compute')
        df_list = []
        dependencies_list = get_dependencies(
                                self.groups, self.meta_df, 'GeorgeKIndex', 
                                self.plugin_mandatory_dependencies, 
                                {'ice_water_phase': 'water'})

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

        return self.final_results(df_list, 
                                  GeorgeKIndexError, 
                                  copy_input = self.copy_input,
                                  reduce_df  = self.reduce_df)
