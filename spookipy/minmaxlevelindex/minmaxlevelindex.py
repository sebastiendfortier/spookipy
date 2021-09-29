# -*- coding: utf-8 -*-
import logging
import sys

import fstpy.all as fstpy
import numpy as np
import pandas as pd
from fstpy.std_reader import to_cmc_xarray

from ..plugin import Plugin
from ..utils import (create_empty_result, final_results, get_3d_array,
                     initializer, to_numpy, validate_nomvar)


class MinMaxLevelIndexError(Exception):
    pass


class MinMaxLevelIndex(Plugin):
    # plugin_requires = '(nomvar in ["TD","TT"]) and (unit == "celsius")'

    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            ascending=True,
            min=False,
            max=False,
            bounded=False,
            nomvar_min='KMIN',
            nomvar_max='KMAX'):
        self.plugin_result_specifications = \
            {
                'ALL': {'etiket': 'MMLVLI', 'unit': 'scalar', 'ip1': 0}
            }
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise MinMaxLevelIndexError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        validate_nomvar(
            self.nomvar_min,
            'MinMaxLevelIndex',
            MinMaxLevelIndexError)

        validate_nomvar(
            self.nomvar_max,
            'MinMaxLevelIndex',
            MinMaxLevelIndexError)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        if (not self.min) and (not self.max):
            self.min = True
            self.max = True

        self.df = fstpy.add_columns(self.df, columns=['forecast_hour', 'ip_info'])

        keep = self.df.loc[~self.df.nomvar.isin(["KBAS", "KTOP"])].reset_index(drop=True)

        self.nomvar_groups = keep.groupby(
            by=['grid', 'dateo', 'forecast_hour', 'ip1_kind', 'nomvar'])

    def compute(self) -> pd.DataFrame:
        logging.info('MinMaxLevelIndex - compute')
        df_list = []
        for _, group in self.nomvar_groups:

            group.sort_values(by='level',ascending=group.ascending.unique()[0],inplace=True)
           
            ds = to_cmc_xarray(group)
                
            # print(list(ds.keys()))   
            first_field = list(ds.keys())[0]
            print('UU',ds[first_field])
            maxpos = ds[first_field].compute().argmax(dim='level') # if no compute xarray and dask dont work atm
            print(ds[first_field].compute())
            print('maxpos',maxpos)
            rds = ds[first_field].reindex(level=list(reversed(ds[first_field].level)))
            print('RUU',rds)
            rmaxpos = rds.compute().argmax(dim='level') # if no compute xarray and dask dont work atm
            print('rmaxpos',rmaxpos)
            print(rds.compute())
            mask = np.ones((ds.dims['level']))
            print('mask',mask)
            sys.exit(-1)

            group.loc[:, 'etiket'] = self.plugin_result_specifications['ALL']['etiket']
            
            kmin_df = create_empty_result(group, self.plugin_result_specifications['ALL'])
            kmin_df['nomvar'] = self.nomvar_min
            

            kmax_df = create_empty_result(group, self.plugin_result_specifications['ALL'])
            kmax_df['nomvar'] = self.nomvar_max
            

            array_3d = get_3d_array(group)

            # if not ascending, reverse array
            if not self.ascending:
                array_3d = np.flip(array_3d, axis=0)

            if self.bounded:
                # get kbas and ktop for this grid
                kbas = self.df.loc[(self.df.nomvar == "KBAS") & (
                    self.df.grid == group.iloc[0]['grid'])].reset_index(drop=True)

                ktop = self.df.loc[(self.df.nomvar == "KTOP") & (
                    self.df.grid == group.iloc[0]['grid'])].reset_index(drop=True)

                kbas_arr = to_numpy(kbas.iloc[0]['d']).ravel(order='F').astype('int32')
                kbas_mask = kbas_arr == -1

                kbas_arr_missing = np.where(kbas_arr == -1, np.nan, kbas_arr)
                ktop_arr = to_numpy(ktop.iloc[0]['d']).ravel(order='F').astype('int32')
                ktop_mask = kbas_arr == -1
                ktop_arr_missing = np.where(ktop_arr == -1, np.nan, ktop_arr)

                array_3d = bound_array(array_3d, kbas_arr_missing, ktop_arr_missing)

            if self.ascending:
                kmin_df.at[0, 'd'] = np.nanargmin(array_3d, axis=0).astype(np.float32)
                kmax_df.at[0, 'd'] = np.nanargmax(array_3d, axis=0).astype(np.float32)

            else:
                kmin_df.at[0, 'd'] = (array_3d.shape[0] - 1 - np.nanargmin(array_3d, axis=0)).astype(np.float32)
                kmax_df.at[0, 'd'] = (array_3d.shape[0] - 1 - np.nanargmax(array_3d, axis=0)).astype(np.float32)

            if self.bounded:
                mask = kbas_mask | ktop_mask
                kmin_df.at[0, 'd'] = np.where(mask, -1.0, kmin_df.at[0, 'd'])
                kmax_df.at[0, 'd'] = np.where(mask, -1.0, kmax_df.at[0, 'd'])

            if self.min:
                df_list.append(kmin_df)
            if self.max:
                df_list.append(kmax_df)
            df_list.append(group)

        return final_results(df_list, MinMaxLevelIndexError, self.meta_df)


def fix_ktop(ktop, array_max_index):
    newktop = (array_max_index - 1) - ktop
    return newktop


def bound_array(a, kbas, ktop):
    arr = a.copy()
    newktop = fix_ktop(ktop, arr.shape[0])
    arr = np.rot90(arr)
    arr[np.flip(kbas[:, None]) > np.arange(arr.shape[1])] = np.nan
    arr = np.rot90(arr, k=2)
    arr[newktop[:, None] > np.arange(arr.shape[1])] = np.nan
    arr = np.rot90(arr, k=-3)
    return arr
