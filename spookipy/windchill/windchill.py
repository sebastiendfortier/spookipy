# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer, DependencyError)

class WindChillError(Exception):
    pass


def wind_chill(tt: np.ndarray, uv: np.ndarray) -> np.ndarray:
    """Calculates the wind chill

    :param tt: surface temperature
    :type tt: np.ndarray
    :param uv: surface wind modulus
    :type uv: np.ndarray
    :return: wind chill
    :rtype: np.ndarray
    """
    return np.where((tt <= 0) & (uv >= 5), 13.12 + 0.6215 *
                    tt + (0.3965 * tt - 11.37) * (uv**0.16), tt)


class WindChill(Plugin):
    """Calculation of the equivalent temperature associated to the wind chill factor at the surface

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param dependency_check: Indicates the plugin is being called from another one who checks dependencies , defaults to False
    :type dependency_check: bool, optional   
    """
    computable_plugin = "RE"
    @initializer
    def __init__(
        self, 
        df: pd.DataFrame,
        dependency_check=False,
        copy_input=False):

        self.plugin_mandatory_dependencies = [
                {
                'UV': {'nomvar': 'UV', 'unit': 'kilometer_per_hour', 'surface': True},
                'TT': {'nomvar': 'TT', 'unit': 'celsius', 'surface': True},
                }
            ]
        self.plugin_result_specifications = {
            'RE': {
                'nomvar': 'RE',
                'label': 'WNDCHL',
                'unit': 'celsius',
                'ip1': 0}}

        self.df = fstpy.metadata_cleanup(self.df)      
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):

        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=['unit', 'ip_info', 'forecast_hour'])

        # check if result already exists
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(['grid', 'datev', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:   
            return existing_results(
                    'WindChill',
                    self.existing_result_df,
                    self.meta_df)

        logging.info('WindChill - compute')

        # holds data from all the groups
        df_list = []
        try:
            dependencies_list = get_dependencies(
                self.groups,
                self.meta_df,
                'WindChill',
                self.plugin_mandatory_dependencies)
        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f'{WindChill} - No matching dependencies found')
        else:
            for dependencies_df, _ in dependencies_list:
                tt_df = get_from_dataframe(dependencies_df, 'TT')
                uv_df = get_from_dataframe(dependencies_df, 'UV')

                re_df = create_empty_result(
                    tt_df, self.plugin_result_specifications['RE'])

                for i in re_df.index:
                    tt = tt_df.at[i, 'd']
                    uv = uv_df.at[i, 'd']
                    re_df.at[i, 'd'] = wind_chill(tt, uv)

                df_list.append(re_df)
        finally:
            return self.final_results(df_list, WindChillError,
                                      dependency_check = self.dependency_check, 
                                      copy_input = self.copy_input)
