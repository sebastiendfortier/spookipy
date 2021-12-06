# -*- coding: utf-8 -*-
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd
import rpnpy.librmn.all as rmn

from ..plugin import Plugin
from ..utils import (convip, create_empty_result, dataframe_arrays_to_dask, encode_ip1_and_ip3, final_results, get_3d_array,
                     initializer, reshape_arrays, validate_nomvar)


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
            self.nomvar,
            'MinMaxLevelIndex',
            MinMaxLevelIndexError)

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

        keep = self.df.loc[self.df.nomvar.isin([self.nomvar, "KBAS","KTOP"])].reset_index(drop=True)
        
        cols = ['nomvar','dateo', 'datev','ip2','forecast_hour']
        # print(f'Keep : \n {keep[cols]} \n\n')

        self.nomvar_groups = keep.groupby(
            by=['grid', 'datev','ip1_kind'])

        for (grid, _, _),group_df in self.nomvar_groups:
            if (group_df.loc[group_df.nomvar == self.nomvar]).empty:
                raise MinMaxLevelIndexError('INVALID INPUT - MISSING ', self.nomvar, ' !')        

            if self.bounded:
                if (group_df.loc[group_df.nomvar == "KBAS"]).empty or (group_df.loc[group_df.nomvar == "KTOP"]).empty:
                    raise MinMaxLevelIndexError('Missing fields KBAS and/or KTOP with BOUNDED option!') 

    def compute(self) -> pd.DataFrame:
        logging.info('MinMaxLevelIndex - compute')
        cols = ['nomvar','dateo', 'datev','ip2','forecast_hour']  # A ENLEVER

        df_list=[]
        for (grid, _, _),group_df in self.nomvar_groups:

            var_df = fstpy.compute(group_df.loc[group_df.nomvar == self.nomvar])

            # cols = ['nomvar', 'ip1','ip2','ip3','level']
            # print(f'\n\nVar_df : \n {var_df[cols]} \n\n')

            var_df = var_df.sort_values(by='level',ascending=var_df.ascending.unique()[0])

            # group_df.loc[:,'etiket'] = self.plugin_result_specifications['ALL']['etiket']

            # kmin_df = create_empty_result(group_df[(group_df.nomvar == self.nomvar)],self.plugin_result_specifications['ALL'])
            # kmin_df['nomvar']=self.nomvar_min
            levels=var_df.level.unique()
            num_levels = len(levels)
            print(f'\n\nLevels : \n {levels} \n\n')
        
            borne_inf=levels[0]
            borne_sup=levels[-1]
            kind     =var_df.ip1_kind[0]
            print(f'\nBorne inf : \n {borne_inf}  Borne sup : {borne_sup} Kind : {kind} \n\n')


            # if self.bounded:
            #     kmin_df = create_empty_result(group_df[(group_df.nomvar == self.nomvar)],self.plugin_result_specifications['ALL'])
            #     kmax_df = create_empty_result(group_df[(group_df.nomvar == self.nomvar)],self.plugin_result_specifications['ALL'])
            # else:
            kmin_df = create_result_container(var_df,borne_inf, borne_sup, kind, self.nomvar_min)
            kmax_df = create_result_container(var_df,borne_inf, borne_sup, kind, self.nomvar_max)


            cols = ['nomvar', 'ip1','ip2','ip3','level', 'ip1_kind', 'ip1_pkind']
            print(f'\n\nkmax_df : \n {kmax_df[cols]} \n\n')

            array_3d = get_3d_array(var_df,flatten=True)

            # if not ascending, reverse array
            if not self.ascending:
                array_3d = np.flip(array_3d,axis=0)

            if self.bounded:
                # get kbas and ktop for this grid
                kbas = group_df.loc[(group_df.nomvar=="KBAS")].reset_index(drop=True)
                kbas = fstpy.compute(kbas)
                ktop = group_df.loc[(group_df.nomvar=="KTOP")].reset_index(drop=True)
                ktop = fstpy.compute(ktop)
                kbas_arr = kbas.iloc[0]['d'].flatten().astype('int64')
                kbas_mask = kbas_arr == -1

                kbas_arr_missing = np.where(kbas_arr == -1 , np.nan, kbas_arr)
                ktop_arr = ktop.iloc[0]['d'].flatten().astype('int64')  #int32 ???
                ktop_mask = kbas_arr == -1
                ktop_arr_missing = np.where(ktop_arr == -1, np.nan, ktop_arr)
                
                # Test Guylaine
                # Ajustement du kbas lorsqu'on est descending
                if not self.ascending:
                    newkbas = (array_3d.shape[0]-1)-ktop_arr_missing
                    newktop = (array_3d.shape[0]-1)-kbas_arr_missing
                else:
                    newkbas = kbas_arr_missing
                    newktop = ktop_arr_missing

                # print(f'Array_3d = {array_3d.shape} newkbas = {newkbas.shape} newktop = {newktop.shape} \n')
                array_3d = bound_array(array_3d, newkbas, newktop)

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
                # print(f'kmin_df - Avant append : \n {kmin_df[cols]} \n\n')
                df_list.append(kmin_df)
                
            if self.max:
                kmax_df = reshape_arrays(kmax_df)
                kmax_df = dataframe_arrays_to_dask(kmax_df)
                df_list.append(kmax_df)
                kmax_df = reshape_arrays(kmax_df)
 
            # print(f'group_df - Avant drop : \n {group_df[cols]} \n\n')
            # indexNames = group_df[group_df.nomvar.isin(["KBAS","KTOP"])].index
            # group_df.drop(indexNames, inplace=True)
            # print(f'group_df - Apres drop : \n {group_df[cols]} \n\n')

            var_df = reshape_arrays(var_df)
            var_df = dataframe_arrays_to_dask(var_df)
            df_list.append(var_df)

            # group_df = reshape_arrays(group_df)
            # group_df = dataframe_arrays_to_dask(group_df)
            # df_list.append(group_df.loc[~group_df.nomvar.isin(["KBAS", "KTOP"])])

        return final_results(df_list, MinMaxLevelIndexError, self.meta_df)


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

def create_result_container(df, b_inf, b_sup, ip1_kind, nomvar):
    ip1 = float(b_inf)
    ip3 = float(b_sup)
    ip2 = 0
    kind = int(ip1_kind)
    
    print(f'RECU -- ip1 = {ip1} ip2 = {ip2} ip3 = {ip3} Kind = {kind}')
    ip1_enc = rmn.ip1_val(ip1, kind)
    ip3_enc = rmn.ip1_val(ip3, kind)
     
    print(f'ip1 = {ip1_enc} ip2 = {ip2} ip3 = {ip3_enc}')
    # ip1 = 1000
    # ip3 = 100

    res_df = create_empty_result(df, {'nomvar':nomvar, 'etiket':'MMLVLI', 'ip1': ip1_enc, 'ip3': ip3_enc})
    # kmax_df = create_empty_result(group_df[(group_df.nomvar == self.nomvar)],self.plugin_result_specifications['ALL'])
    return res_df
