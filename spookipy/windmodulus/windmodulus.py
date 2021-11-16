# -*- coding: utf-8 -*-

import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe)



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
    """
    def __init__(self,df:pd.DataFrame):
        self.plugin_mandatory_dependencies = [{
            'UU': {'nomvar': 'UU', 'unit': 'knot'},
            'VV': {'nomvar': 'VV', 'unit': 'knot'},
        }]
        self.plugin_result_specifications = {
            'UV': {'nomvar': 'UV', 'etiket': 'WNDMOD', 'unit': 'knot'}
        }
        self.df = df

        #ajouter forecast_hour et unit
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise WindModulusError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(
            self.df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        # check if result already exists
        self.existing_result_df = get_existing_result(
            self.df, self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)
        # print(self.df[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
        self.groups = self.df.groupby(
            ['grid', 'dateo', 'forecast_hour', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'WindModulus',
                self.existing_result_df,
                self.meta_df)

        logging.info('WindModulus - compute')
        df_list = []
        dependencies_list = get_dependencies(
            self.groups,
            self.meta_df,
            'WindModulus',
            self.plugin_mandatory_dependencies,
            intersect_levels=True)
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

        return final_results(df_list, WindModulusError, self.meta_df)
