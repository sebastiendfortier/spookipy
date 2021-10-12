# -*- coding: utf-8 -*-
import copy
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, dataframe_arrays_to_dask, final_results, get_3d_array,
                     initializer, reshape_arrays, to_numpy, validate_nomvar)


class MatchLevelIndexToValueError(Exception):
    pass


class MatchLevelIndexToValue(Plugin):

    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            error_value=-1,
            nomvar_out=None,
            nomvar_index='IND'):
        self.plugin_result_specifications = \
            {
                'ALL': {'etiket': 'MLIVAL', 'ip1': 0}
            }
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise MatchLevelIndexToValueError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        validate_nomvar(
            self.nomvar_out,
            'MatchLevelIndexToValue',
            MatchLevelIndexToValueError)

        validate_nomvar(
            self.nomvar_index,
            'MatchLevelIndexToValue',
            MatchLevelIndexToValueError)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(
            self.df, columns=[
                'forecast_hour', 'ip_info'])

        keep = self.df.loc[~self.df.nomvar.isin(
            ["KBAS", "KTOP"])].reset_index(drop=True)

        self.groups = keep.groupby(by=['grid', 'dateo', 'forecast_hour', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        logging.info('MatchLevelIndexToValue - compute')
        df_list = []
        for (grid, dateo, forecast_hour, ip1_kind), group_df in self.groups:

            ind_df = group_df.loc[group_df.nomvar == self.nomvar_index].reset_index(drop=True)
            ind = np.expand_dims(to_numpy(ind_df.iloc[0]['d']).flatten().astype(dtype=np.int32),axis=0)
            others_df = group_df.loc[group_df.nomvar != self.nomvar_index].reset_index(drop=True)
            nomvars = others_df.nomvar.unique()

            if not(self.nomvar_out is None) and (len(nomvars) > 1):
                raise MatchLevelIndexToValueError(
                    'whenever parameter nomvar_out is specified, only 2 inputs are allowed: IND and another field; got {nomvars} in input')

            for nomvar in nomvars:
                # get current var
                var_df = group_df.loc[group_df.nomvar == nomvar]

                # sort values by level
                var_df = var_df.sort_values(by='level',ascending=var_df.ascending.unique()[0]).reset_index(drop=True)

                res_df = create_empty_result(var_df, self.plugin_result_specifications['ALL'])

                if not(self.nomvar_out is None):
                    res_df.loc[:, 'nomvar'] = self.nomvar_out

                # get the valid index range from our current variable
                num_levels = len(var_df.index)

                levels_range = list(range(0, num_levels))
                # create a mask of valid indexes
                mask = np.isin(ind, levels_range)

                # replace invalid indexes by error_row index
                valid_ind = np.where(mask, ind, num_levels)

                # create 3d array of our variable
                error_row = copy.deepcopy(var_df.iloc[0])
                error_row['d'] = np.full_like(to_numpy(error_row['d']), self.error_value)

                var_df = var_df.append(error_row).reset_index(drop=True)
                # print(var_df[['ascending','level']])
                var_df = fstpy.compute(var_df)
                arr_3d = get_3d_array(var_df, flatten=True)

                res_df.at[0, 'd'] = np.take_along_axis(arr_3d, valid_ind, axis=0)

                res_df = reshape_arrays(res_df)
                res_df = dataframe_arrays_to_dask(res_df)
                df_list.append(res_df)

        return final_results(df_list, MatchLevelIndexToValueError, self.meta_df)
