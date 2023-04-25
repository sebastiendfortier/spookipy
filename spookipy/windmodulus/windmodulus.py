# -*- coding: utf-8 -*-

import logging

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (DependencyError, create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer)


class WindModulusError(Exception):
    pass


def wind_modulus(uu: np.ndarray, vv: np.ndarray) -> np.ndarray:
    """Computes the wind modulus from the wind components

    :param uu: U wind component
    :type uu: np.ndarray
    :param vv: V wind component
    :type vv: np.ndarray
    :return: wind modulus
    :rtype: np.ndarray
    """
    return (uu**2 + vv**2)**.5


class WindModulus(Plugin):
    """Calculation of the wind modulus from its 2 horizontal components

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param dependency_check: Indicates the plugin is being called from another one who checks dependencies , defaults to False
    :type dependency_check: bool, optional
    """
    computable_plugin = "UV"
    @initializer
    def __init__(
        self,
        df:pd.DataFrame,
        dependency_check=False
        ):

        self.plugin_mandatory_dependencies = [
            {
                'UU': {'nomvar': 'UU', 'unit': 'knot'},
                'VV': {'nomvar': 'VV', 'unit': 'knot'},
            }
        ]

        self.plugin_result_specifications = {
            'UV': {'nomvar': 'UV', 'etiket': 'WNDMOD', 'unit': 'knot'}
        }

        #ajouter forecast_hour et unit
        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)    
        self.prepare_groups()

    # might be able to move
    def prepare_groups(self):
        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        # check if result already exists
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(['grid', 'datev', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'WindModulus',
                self.existing_result_df,
                self.meta_df)

        logging.info('WindModulus - compute')

        df_list = []
        try:
            dependencies_list = get_dependencies(
                self.groups,
                self.meta_df,
                'WindModulus',
                self.plugin_mandatory_dependencies,
                intersect_levels=True)
        except DependencyError:
             raise DependencyError(f'{WindModulus} - No matching dependencies found')
        else:
            for dependencies_df, _ in dependencies_list:
                uu_df = get_from_dataframe(dependencies_df, 'UU')
                vv_df = get_from_dataframe(dependencies_df, 'VV')
                uv_df = create_empty_result(
                    vv_df, self.plugin_result_specifications['UV'], all_rows=True)

                for i in uv_df.index:
                    uu = uu_df.at[i,'d']
                    vv = vv_df.at[i,'d']
                    uv_df.at[i,'d'] = wind_modulus(uu,vv)

                df_list.append(uv_df)

        finally:
            return final_results(df_list, WindModulusError, self.meta_df, self.dependency_check)
