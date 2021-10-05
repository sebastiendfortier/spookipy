# -*- coding: utf-8 -*-
import copy
import logging
import math

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, initializer)


def diagnostic_cloud_fraction_threshold(level: float) -> float:
    """calcultes thresholds for a given level

    :param level: level to calculate with
    :type level: float
    :return: array of thresholds
    :rtype: np.ndarray
    """
    return 1 - 2 * level + math.pow(level, 2) + math.pow(level, 3) + math.sqrt(
        3.0) * level * (1 - 3 * level + 2 * math.pow(level, 2))


def diagnostic_cloud_fraction(hr: np.ndarray, threshold: float) -> np.ndarray:
    """Diagnostic cloud fraction calculation

    :param hr: ndarray of hr values
    :type hr: np.ndarray
    :param threshold: threshold calculated from level
    :type threshold: float
    :return: Diagnostic cloud fraction
    :rtype: np.ndarray
    """
    cld = np.full_like(hr, -1, dtype=np.float32)
    cld = np.where(hr <= threshold, 0, cld)
    cld = np.where((threshold < hr) & (hr < 1),
                   ((hr - threshold) / (1 - threshold))**2, cld)
    cld = np.where(hr >= 1, 1, cld)
    return cld.astype(np.float32)


class CloudFractionDiagnosticError(Exception):
    pass


class CloudFractionDiagnostic(Plugin):

    @initializer
    def __init__(self, df: pd.DataFrame, use_constant=None):
        self.plugin_mandatory_dependencies = [
            {
                'HR': {'nomvar': 'HR', 'unit': 'scalar', 'select_only': True},
            }
        ]

        self.plugin_result_specifications = {
            'CLD': {
                'nomvar': 'CLD',
                'etiket': 'CloudFractionDiagnostic',
                'unit': 'scalar'}}

        self.constant = 0.8
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise CloudFractionDiagnosticError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(
            self.df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        # check if result already exists
        self.existing_result_df = get_existing_result(
            self.df, self.plugin_result_specifications)

        self.groups = self.df.groupby(
            ['grid', 'dateo', 'forecast_hour', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'CloudFractionDiagnostic',
                self.existing_result_df,
                self.meta_df)

        logging.info('CloudFractionDiagnostic - compute')
        df_list = []
        dependencies_list = get_dependencies(
            self.groups,
            self.meta_df,
            'CloudFractionDiagnostic',
            self.plugin_mandatory_dependencies)

        for dependencies_df, _ in dependencies_list:

            cld_df = create_empty_result(
                dependencies_df,
                self.plugin_result_specifications['CLD'],
                all_rows=True)

            if not (self.use_constant is None):
                for i in cld_df.index:
                    cld_df.at[i, 'd'] = np.full_like(
                        cld_df.at[i, 'd'], self.constant, dtype=np.float32)
            else:
                for i in cld_df.index:
                    level = cld_df.at[i, 'level']
                    hr = copy.deepcopy(cld_df.at[i, 'd'])
                    threshold = diagnostic_cloud_fraction_threshold(level)
                    cld_df.at[i, 'd'] = diagnostic_cloud_fraction(
                        hr, threshold)

            df_list.append(cld_df)

        return final_results(
            df_list,
            CloudFractionDiagnosticError,
            self.meta_df)
