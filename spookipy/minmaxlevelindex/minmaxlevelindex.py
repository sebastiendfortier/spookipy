# -*- coding: utf-8 -*-
import argparse
import logging
import warnings

import fstpy
import numpy as np
import pandas as pd
import rpnpy.librmn.all as rmn

from ..plugin import Plugin, PluginParser
from ..utils import (create_empty_result, dataframe_arrays_to_dask,
                    get_3d_array,get_dependencies, get_from_dataframe, initializer, 
                    reshape_arrays, validate_nomvar)

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
    :param nomvar_min_idx: nomvar of the min result index, defaults to 'KMIN'
    :type nomvar_min_idx: str, optional
    :param nomvar_max_idx: nomvar of the max result index, defaults to 'KMAX'
    :type nomvar_max_idx: str, optional
    :param value_to_return: return also the maximum and/or the minimum values corresponding to the indices, defaults to False
    :type value_to_return: bool, optional
    :param nomvar_min_val: nomvar of the min result value, defaults to 'MIN'
    :type nomvar_min_val: str, optional
    :param nomvar_max_val: nomvar of the max result value, defaults to 'MAX'
    :type nomvar_max_val: str, optional
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional 
    """

    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            nomvar : str=None,
            ascending=True,
            min=False,
            max=False,
            bounded=False,
            value_to_return=False,
            nomvar_min_idx='KMIN',
            nomvar_max_idx='KMAX',
            nomvar_min_val='MIN',
            nomvar_max_val='MAX',
            copy_input=False
            ):

        self.df = fstpy.metadata_cleanup(self.df)

        super().__init__(df)

        if self.nomvar is None:
            nomvar_list = self.no_meta_df[~self.no_meta_df.nomvar.isin(["KBAS","KTOP"])].nomvar.unique()
            if len(nomvar_list) == 1:
                self.nomvar = nomvar_list[0]
            else:
                raise MinMaxLevelIndexError("Too many input fields, provide one field or set nomvar : {}".format(nomvar_list))

        self.plugin_mandatory_dependencies=[{}]
        input_field = {self.nomvar : {'nomvar': self.nomvar}}
        self.plugin_mandatory_dependencies[0]= input_field

        if self.bounded:
            dict_Kbas = {'nomvar': 'KBAS'}
            dict_Ktop = {'nomvar': 'KTOP'}
            self.plugin_mandatory_dependencies[0]['KBAS'] = dict_Kbas
            self.plugin_mandatory_dependencies[0]['KTOP'] = dict_Ktop

        self.plugin_result_specifications = \
            {
                'ALL': {'etiket': 'MMLVLI', 'unit': 'scalar'}
            }

        self.validate_params_and_input()

    def validate_params_and_input(self):

        validate_nomvar(
            self.nomvar,
            'MinMaxLevelIndex',
            MinMaxLevelIndexError)

        validate_nomvar(
            self.nomvar_min_idx,
            'MinMaxLevelIndex',
            MinMaxLevelIndexError)

        validate_nomvar(
            self.nomvar_max_idx,
            'MinMaxLevelIndex',
            MinMaxLevelIndexError)

        validate_nomvar(
            self.nomvar_min_val,
            'MinMaxLevelIndex',
            MinMaxLevelIndexError)

        validate_nomvar(
            self.nomvar_max_val,
            'MinMaxLevelIndex',
            MinMaxLevelIndexError)

        if (not self.min) and (not self.max):
            self.min = True
            self.max = True

        if self.bounded:
            if (self.no_meta_df.loc[self.no_meta_df.nomvar == "KBAS"]).empty or \
               (self.no_meta_df.loc[self.no_meta_df.nomvar == "KTOP"]).empty:
                raise MinMaxLevelIndexError('Missing fields KBAS and/or KTOP with BOUNDED option!')

        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=['forecast_hour', 'ip_info', 'unit'])

        keep = self.no_meta_df.loc[self.no_meta_df.nomvar.isin([self.nomvar, "KBAS","KTOP"])].reset_index(drop=True)

        if (keep.loc[keep.nomvar == self.nomvar]).empty:
                raise MinMaxLevelIndexError(f'INVALID INPUT - MISSING {self.nomvar} !')    

        self.nomvar_groups = keep.groupby(by=['grid', 'datev','ip1_kind'])

        self.dependencies_list = get_dependencies(
            self.nomvar_groups,
            self.meta_df,
            'MinMaxLevelIndex',
            self.plugin_mandatory_dependencies,
            intersect_levels=False)

    def compute(self) -> pd.DataFrame:
        logging.info('MinMaxLevelIndex - compute')

        df_list=[]
        for dependencies_df, option in self.dependencies_list:
            var_df = get_from_dataframe(dependencies_df, self.nomvar)

            borne_inf  = var_df.iloc[0].level
            borne_sup  = var_df.iloc[-1].level

            min_idx_df = create_result_container(var_df,borne_inf, borne_sup, self.nomvar_min_idx, 
                                                self.bounded, self.plugin_result_specifications)
            max_idx_df = create_result_container(var_df,borne_inf, borne_sup, self.nomvar_max_idx, 
                                                self.bounded, self.plugin_result_specifications)
            min_val_df = create_result_container(var_df,borne_inf, borne_sup, self.nomvar_min_val, 
                                                self.bounded, self.plugin_result_specifications)
            max_val_df = create_result_container(var_df,borne_inf, borne_sup, self.nomvar_max_val, 
                                                self.bounded, self.plugin_result_specifications)

            array_3d   = get_3d_array(var_df,flatten=True)

            # if not ascending, reverse array
            if not self.ascending:
                array_3d = np.flip(array_3d,axis=0)

            if self.bounded:
                # get kbas and ktop for this grid
                kbas = get_from_dataframe(dependencies_df, 'KBAS')
                ktop = get_from_dataframe(dependencies_df, 'KTOP')
                kbas_arr  = kbas.iloc[0]['d'].flatten().astype('int32')
                kbas_mask = kbas_arr == -1

                kbas_arr_missing = np.where(kbas_arr == -1 , np.nan, kbas_arr)
                ktop_arr  = ktop.iloc[0]['d'].flatten().astype('int32') 
                ktop_mask = kbas_arr == -1
                ktop_arr_missing = np.where(ktop_arr == -1, np.nan, ktop_arr)
                
                # Ajustement du kbas lorsque la direction est descending
                if not self.ascending:
                    newkbas = (array_3d.shape[0]-1)-ktop_arr_missing
                    newktop = (array_3d.shape[0]-1)-kbas_arr_missing
                else:
                    newkbas = kbas_arr_missing
                    newktop = ktop_arr_missing

                array_3d = bound_array(array_3d, newkbas, newktop)

            if self.ascending:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    min_idx = np.nanargmin(array_3d, axis=0).astype('int32')
                    min_idx = np.expand_dims(min_idx,axis=0)
                    max_idx = np.nanargmax(array_3d, axis=0).astype('int32')
                    max_idx = np.expand_dims(max_idx,axis=0)

                    min_idx_df.at[0,'d'] = np.nanargmin(array_3d, axis=0).astype('float32')
                    max_idx_df.at[0,'d'] = np.nanargmax(array_3d, axis=0).astype('float32')
            else:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    min_idx = (array_3d.shape[0]-1 - np.nanargmin(array_3d, axis=0)).astype('int32')
                    min_idx = np.expand_dims(min_idx,axis=0)
                    max_idx = (array_3d.shape[0]-1 - np.nanargmax(array_3d, axis=0)).astype('int32')
                    max_idx = np.expand_dims(max_idx,axis=0)

                    min_idx_df.at[0,'d'] = (array_3d.shape[0]-1 - np.nanargmin(array_3d, axis=0)).astype('float32')
                    max_idx_df.at[0,'d'] = (array_3d.shape[0]-1 - np.nanargmax(array_3d, axis=0)).astype('float32')

            # Prendre les valeurs associees aux indices
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                min_val_df.at[0,'d'] = np.take_along_axis(array_3d, min_idx, axis=0).astype('float32')
                max_val_df.at[0,'d'] = np.take_along_axis(array_3d, max_idx, axis=0).astype('float32')

            if self.bounded:
                mask = kbas_mask | ktop_mask
                min_idx_df.at[0,'d'] = np.where(mask,-1.0,min_idx_df.at[0,'d'])
                max_idx_df.at[0,'d'] = np.where(mask,-1.0,max_idx_df.at[0,'d'])

            if self.min:
                min_idx_df = reshape_arrays(min_idx_df)
                min_idx_df = dataframe_arrays_to_dask(min_idx_df)
                df_list.append(min_idx_df)
                
            if self.max:
                max_idx_df = reshape_arrays(max_idx_df)
                max_idx_df = dataframe_arrays_to_dask(max_idx_df)
                df_list.append(max_idx_df)

            if self.value_to_return:
                if self.min:
                    min_val_df =  reshape_arrays(min_val_df)
                    min_val_df = dataframe_arrays_to_dask(min_val_df)
                    df_list.append(min_val_df)
                if self.max:
                    max_val_df =  reshape_arrays(max_val_df)
                    max_val_df = dataframe_arrays_to_dask(max_val_df)
                    df_list.append(max_val_df)

            # Lorsque l'option copy_input n'est pas a True, on garde le comportement original du plugin
            # i.e. qu'on sort seulement le champ pour lequel on cherche le min/max et non tous les champs d'input
            if not self.copy_input:
                var_df = reshape_arrays(var_df)  
                var_df = dataframe_arrays_to_dask(var_df)
                df_list.append(var_df)

        return self.final_results(df_list, MinMaxLevelIndexError,
                                  copy_input = self.copy_input)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=MinMaxLevelIndex.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--minMax',type=str,choices=["MIN","MAX","BOTH"], help="Finds either the maximum or minimum value index or both")
        parser.add_argument('--direction',type=str,default="ASCENDING",choices=["ASCENDING","DESCENDING"], help="The level iteration direction (upward or downward)")
        parser.add_argument('--bounded',dest='bounded',action='store_true',default=False, help="Searches in part of the column (requires fields KBAS and KTOP as inputs) Default: searches the whole column")
        parser.add_argument('--fieldName',type=str,dest='nomvar', help="Name of the field.")
        parser.add_argument('--outputFieldName1',type=str,default="KMIN",dest='nomvar_min',help="Option to change the name of output field KMIN")
        parser.add_argument('--outputFieldName2',type=str,default="KMAX",dest='nomvar_max',help="Option to change the name of output field KMAX")

        parsed_arg = vars(parser.parse_args(args.split()))
        if parsed_arg['nomvar'] is not None:
            validate_nomvar(parsed_arg['nomvar'],"MinMaxLevelIndex",MinMaxLevelIndexError)
            
        validate_nomvar(parsed_arg['nomvar_min'],"MinMaxLevelIndex",MinMaxLevelIndexError)
        validate_nomvar(parsed_arg['nomvar_max'],"MinMaxLevelIndex",MinMaxLevelIndexError)

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

def create_result_container(df, b_inf, b_sup, nomvar, bounded, result_specifications):
    ip1 = b_inf
    ip3 = b_sup
    kind = int(df.iloc[0].ip1_kind)
    
    inter = fstpy.Interval('ip1', ip1, ip3, kind)
  
    result_specifications["ALL"]["nomvar"]   = nomvar
    result_specifications["ALL"]["interval"] = inter

    res_df = create_empty_result(df, result_specifications['ALL'])
    if bounded:
        res_df = fstpy.add_flag_values(res_df)
        res_df.bounded = True 

    return res_df
