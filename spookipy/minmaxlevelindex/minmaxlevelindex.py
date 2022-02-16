# -*- coding: utf-8 -*-
import argparse
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, dataframe_arrays_to_dask, final_results, get_3d_array,
                     initializer, reshape_arrays, validate_nomvar)
from ..configparsingutils import check_length_2_to_4


class MinMaxLevelIndexError(Exception):
    pass


class MinMaxLevelIndex(Plugin):
    """Finds the index of the maximum and/or minimum value in the column or part of it.

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    :param nomvar: Target nomvar for the computation
    :type nomvar: str
    :param ascending: search order, defaults to True
    :type ascending: bool, optional
    :param min: get the  minimum, defaults to False
    :type min: bool, optional
    :param max: get the maximum, defaults to False
    :type max: bool, optional
    :param bounded: limit search between KBAS and KTOP, defaults to False
    :type bounded: bool, optional
    :param nomvar_min: nomvar of the min result, defaults to 'KMIN'
    :type nomvar_min: str, optional
    :param nomvar_max: nomvar of the max result, defaults to 'KMAX'
    :type nomvar_max: str, optional
    """

    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            nomvar : str,
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

        if self.bounded:
            if (self.df.loc[self.df.nomvar == "KBAS"]).empty or (self.df.loc[self.df.nomvar == "KTOP"]).empty:
                raise MinMaxLevelIndexError('Missing fields KBAS and/or KTOP with BOUNDED option!')

        self.df = fstpy.add_columns(self.df, columns=['forecast_hour', 'ip_info'])

        keep = self.df.loc[~self.df.nomvar.isin(["KBAS", "KTOP"])].reset_index(drop=True)

        self.nomvar_groups = keep.groupby(
            by=['grid', 'dateo', 'forecast_hour', 'ip1_kind', 'nomvar'])

    def compute(self) -> pd.DataFrame:
        logging.info('MinMaxLevelIndex - compute')
        df_list=[]
        for (grid, _, _, _, _),group_df in self.nomvar_groups:
            group_df = fstpy.compute(group_df)

            group_df = group_df.sort_values(by='level',ascending=group_df.ascending.unique()[0])
            group_df.loc[:,'etiket'] = self.plugin_result_specifications['ALL']['etiket']

            kmin_df = create_empty_result(group_df,self.plugin_result_specifications['ALL'])
            kmin_df['nomvar']=self.nomvar_min

            kmax_df = create_empty_result(group_df,self.plugin_result_specifications['ALL'])
            kmax_df['nomvar']=self.nomvar_max

            array_3d = get_3d_array(group_df,flatten=True)

            # if not ascending, reverse array
            if not self.ascending:
                array_3d = np.flip(array_3d,axis=0)


            if self.bounded:
                # get kbas and ktop for this grid
                kbas = self.df.loc[(self.df.nomvar=="KBAS") & (self.df.grid==grid)].reset_index(drop=True)
                kbas = fstpy.compute(kbas)
                ktop = self.df.loc[(self.df.nomvar=="KTOP") & (self.df.grid==grid)].reset_index(drop=True)
                ktop = fstpy.compute(ktop)
                kbas_arr = kbas.iloc[0]['d'].flatten().astype('int64')
                kbas_mask = kbas_arr == -1

                kbas_arr_missing = np.where(kbas_arr == -1 , np.nan, kbas_arr)
                ktop_arr = ktop.iloc[0]['d'].flatten().astype('int64')
                ktop_mask = kbas_arr == -1
                ktop_arr_missing = np.where(ktop_arr == -1, np.nan, ktop_arr)

                array_3d = bound_array(array_3d, kbas_arr_missing, ktop_arr_missing)

            if self.ascending:
                kmin_df.at[0,'d'] = np.nanargmin(array_3d, axis=0).astype('float32')
                kmax_df.at[0,'d'] = np.nanargmax(array_3d, axis=0).astype('float32')

            else:
                kmin_df.at[0,'d'] = (array_3d.shape[0]-1 - np.nanargmin(array_3d, axis=0)).astype('float32')
                kmax_df.at[0,'d'] = (array_3d.shape[0]-1 - np.nanargmax(array_3d, axis=0)).astype('float32')

            if self.bounded:
                mask = kbas_mask | ktop_mask
                kmin_df.at[0,'d'] = np.where(mask,-1.0,kmin_df.at[0,'d'])
                kmax_df.at[0,'d'] = np.where(mask,-1.0,kmax_df.at[0,'d'])

            if self.min:
                kmin_df = reshape_arrays(kmin_df)
                kmin_df = dataframe_arrays_to_dask(kmin_df)
                df_list.append(kmin_df)
            if self.max:
                kmax_df = reshape_arrays(kmax_df)
                kmax_df = dataframe_arrays_to_dask(kmax_df)
                df_list.append(kmax_df)
                kmax_df = reshape_arrays(kmax_df)
 
            group_df = reshape_arrays(group_df)
            group_df = dataframe_arrays_to_dask(group_df)
            df_list.append(group_df)

        return final_results(df_list, MinMaxLevelIndexError, self.meta_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=MinMaxLevelIndex.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--minMax',type=str,choices=["MIN","MAX","BOTH"], help="Finds either the maximum or minimum value index or both")
        parser.add_argument('--direction',type=str,default="ASCENDING",choices=["ASCENDING","DESCENDING"], help="The level iteration direction (upward or downward)")
        parser.add_argument('--bounded',dest='bounded',action='store_true',default=False, help="Searches in part of the column (requires fields KBAS and KTOP as inputs) Default: searches the whole column")
        parser.add_argument('--fieldName',type=str,dest='nomvar', help="Name of the field.")
        parser.add_argument('--outputFieldName1',type=str,default="KMIN",dest='nomvar_min',help="Option to change the name of output field KMIN")
        parser.add_argument('--outputFieldName2',type=str,default="KMAX",dest='nomvar_max',help="Option to change the name of output field KMAX")

        parsed_arg = vars(parser.parse_args(args.split()))
        check_length_2_to_4(parsed_arg['nomvar'],True,MinMaxLevelIndexError)
        check_length_2_to_4(parsed_arg['nomvar_min'],False,MinMaxLevelIndexError)
        check_length_2_to_4(parsed_arg['nomvar_max'],False,MinMaxLevelIndexError)

        if parsed_arg['minMax'] == "MIN":
            parsed_arg['min'] = True
        elif parsed_arg['minMax'] == "MAX":
            parsed_arg['max'] = True
        else:
            parsed_arg['min'] = True
            parsed_arg['max'] = True

        parsed_arg['ascending'] = parsed_arg['direction'] == "ASCENDING"

        return parsed_arg


def fix_ktop(ktop, array_max_index):
    newktop = (array_max_index-1)-ktop
    return newktop

def bound_array(a, kbas, ktop):
    arr=a.copy()
    newktop = fix_ktop(ktop, arr.shape[0])
    arr = np.rot90(arr)
    arr[np.flip(kbas[:,None]) > np.arange(arr.shape[1])] = np.nan
    arr = np.rot90(arr,k=2)
    arr[newktop[:,None] > np.arange(arr.shape[1])] = np.nan
    arr = np.rot90(arr,k=-3)
    return arr