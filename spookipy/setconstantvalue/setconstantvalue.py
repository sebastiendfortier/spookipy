# -*- coding: utf-8 -*-
import logging

import dask.array as da
import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import create_empty_result, final_results, initializer


def set_value(a, v):
    a[:] = v
    return a


def set_series_value(a: pd.Series, v):
    return a.apply(set_value, args=(v,))


class SetConstantValueError(Exception):
    pass


class SetConstantValue(Plugin):
    """Copies the input field and replace all its values by a given constant

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param value: replacement value used to replace contents of the input field, defaults to 0 (min index)
    :type value: float, optional
    :param nomvar_out: nomvar of the results field, defaults to None
    :type nomvar_out: str, optional
    :param min_index: will fill the field with the min index value, defaults to False
    :type min_index: bool, optional
    :param max_index: will fill the field with the max index value, defaults to False
    :type max_index: bool, optional
    :param nb_levels: will fill the field with the number of levels value of the provided field, defaults to False
    :type nb_levels: bool, optional
    :param bi_dimensionnal: forces 2D field output even if the input is a 3D field, defaults to False
    :type bi_dimensionnal: bool, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            value:float=0.,
            nomvar_out=None,
            min_index=False,
            max_index=False,
            nb_levels=False,
            bi_dimensionnal=False):

        self.plugin_result_specifications = {
            'ALL': {'etiket': 'SETVAL', 'unit': 'scalar'}
        }
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise SetConstantValueError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(
            self.df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.groups = self.df.groupby(
            by=['grid', 'nomvar', 'dateo', 'forecast_hour'])

        l = [self.min_index, self.max_index, self.nb_levels]

        lcount = l.count(True)

        if lcount > 1:
            raise SetConstantValueError(
                'Too many options selected, you can only choose one option at a time in %s' % [
                    'min_index',
                    'max_index',
                    'nb_levels'])
        if self.min_index:
            self.value = 0

    def compute(self) -> pd.DataFrame:
        logging.info('SetConstantValue - compute')
        df_list = []
        for _, df in self.groups:
            if self.max_index:
                self.value = len(df.index) - 1
            if self.nb_levels:
                self.value = len(df.index)

            res_df = create_empty_result(
                self.df, self.plugin_result_specifications['ALL'], all_rows=True)

            if not (self.nomvar_out is None):
                res_df['nomvar'] = self.nomvar_out

            for i in res_df.index:
                res_df.at[i, 'd'] = da.full_like(
                    res_df.at[i, 'd'], self.value, order='F', dtype=np.float32)

            if self.bi_dimensionnal:
                res_df.drop(res_df.index[1:], inplace=True)
                res_df.loc[:, 'ip1'] = 0
            df_list.append(res_df)

        return final_results(df_list, SetConstantValueError, self.meta_df)
