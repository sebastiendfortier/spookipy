# -*- coding: utf-8 -*-
import argparse
import copy
import logging
import warnings

import fstpy
import numpy as np
import pandas as pd
import rpnpy.librmn.all as rmn

from ..plugin import Plugin
from ..utils import (create_empty_result, dataframe_arrays_to_dask, final_results, get_3d_array,
                     initializer, reshape_arrays, to_numpy, validate_nomvar)

class MatchLevelIndexToValueError(Exception):
    pass

class MatchLevelIndexToValue(Plugin):
    """Associates, to each given vertical level index, a value of one or many 3D meteorological fields from the input.

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    :param error_value: value to return if index is not found or not in valid range, defaults to -1
    :type error_value: int, optional
    :param nomvar_out: nomvar for output result, defaults to None
    :type nomvar_out: str, optional
    :param nomvar_index: nomvar of index field, defaults to 'IND'
    :type nomvar_index: str, optional
    :param use_interval: utilisation de l'objet intervalle, defaults to 'FALSE'
    :type use_interval: str, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            error_value=-1,
            nomvar_out=None,
            nomvar_index='IND',
            use_interval=False):

        self.plugin_result_specifications = \
            {
                'ALL': {'etiket': 'MLIVAL', 'ip1': 0}
            }

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)
        self.validate_params_and_input()

    def validate_params_and_input(self):

        if not(self.nomvar_out is None):
            validate_nomvar(
                self.nomvar_out,
                'MatchLevelIndexToValue',
                MatchLevelIndexToValueError)

        validate_nomvar(
            self.nomvar_index,
            'MatchLevelIndexToValue',
            MatchLevelIndexToValueError)
        
        if self.no_meta_df.loc[(self.no_meta_df.nomvar == self.nomvar_index)].empty:
            raise MatchLevelIndexToValueError(
                    f'Missing indices field {self.nomvar_index} !') 

        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=[
                'forecast_hour', 'ip_info'])

        self.groups = self.no_meta_df.groupby(by=['grid', 'datev', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        logging.info('MatchLevelIndexToValue - compute')

        df_list = []
        for (grid, dateo, ip1_kind), group_df in self.groups:

            # print(f'group_df: \n {group_df.ip2.unique()} \n\n')
            ind_df = group_df.loc[group_df.nomvar == self.nomvar_index].reset_index(drop=True)
            if ind_df.empty:
                logging.warning(
                    f'Cannot find {self.nomvar_index} field in this group - skipping the group ')
                continue
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                ind = np.expand_dims(to_numpy(ind_df.iloc[0]['d']).flatten().astype(dtype=np.int32),axis=0)
            others_df = group_df.loc[group_df.nomvar != self.nomvar_index].reset_index(drop=True)
            if others_df.empty:
                logging.warning(
                    f'Cannot find input field in this group to match the {self.nomvar_index} index field  - skipping the group')
                continue
            nomvars   = others_df.nomvar.unique()

            if not(self.nomvar_out is None) and (len(nomvars) > 1):  
                raise MatchLevelIndexToValueError(
                    f'whenever parameter nomvar_out is specified, only 2 inputs are allowed: IND and another field; got {nomvars} in input')

            for nomvar in nomvars:
                # get current var
                var_df = group_df.loc[group_df.nomvar == nomvar]

                # sort values by level
                var_df = var_df.sort_values(by='level',ascending=var_df.ascending.unique()[0]).reset_index(drop=True)
                var_df = fstpy.add_ip_info_columns(var_df)

                # Utilisation de la cle pour l'intervalle ?
                if self.use_interval:
                    # Si le champ d'indice n'a pas d'intervalle, on prend le 1er et le dernier niveau des donnees 
                    # du champ d'entree
                    if ind_df.interval.isnull().bool():
                        levels     = var_df.level.unique()
                        borne_inf  = levels[0]
                        borne_sup  = levels[-1]
                        res_df     = create_result_container(var_df,borne_inf, borne_sup, ip1_kind)
                    else:
                        # Si le champ d'indice a un interval, on prend ses infos
                        res_df = create_empty_result(ind_df, {'etiket':'MLIVAL'})
                else:
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
                error_row      = copy.deepcopy(var_df.iloc[0])
                error_row['d'] = np.full_like(to_numpy(error_row['d']), self.error_value)

                var_df = var_df.append(error_row).reset_index(drop=True)
                var_df = fstpy.compute(var_df)
                arr_3d = get_3d_array(var_df, flatten=True)
                
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    res_df.at[0, 'd'] = np.take_along_axis(arr_3d, valid_ind, axis=0)

                res_df = reshape_arrays(res_df)
                res_df = dataframe_arrays_to_dask(res_df)
                df_list.append(res_df)
                

        if len(df_list):
            return final_results(df_list, MatchLevelIndexToValueError, self.meta_df)
        else:
            raise MatchLevelIndexToValueError('No results produced !')


    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=MatchLevelIndexToValue.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--indexFieldName',type=str,default="IND",dest='nomvar_index', help="Option to use a different field name other than IND for the field of indices.")
        parser.add_argument('--outputFieldName',type=str,dest='nomvar_out',help="Option to give the output field a different name from the input field name applicable only with one input meteorological field.")

        parsed_arg = vars(parser.parse_args(args.split()))
        validate_nomvar(parsed_arg['nomvar_index'],"MatchLevelIndexToValue",MatchLevelIndexToValueError)
        if parsed_arg['nomvar_out'] is not None:
            validate_nomvar(parsed_arg['nomvar_out'],"MatchLevelIndexToValue",MatchLevelIndexToValueError)

        return parsed_arg

def create_result_container(df, b_inf, b_sup, ip1_kind):
    ip1 = float(b_inf)
    ip3 = float(b_sup)
    ip2 = 0
    kind = int(ip1_kind)
    
    ip1_enc = rmn.ip1_val(ip1, kind)
    ip3_enc = rmn.ip1_val(ip3, kind)

    res_df = create_empty_result(df, {'etiket':'MLIVAL', 'ip1': ip1_enc, 'ip3': ip3_enc})
    return res_df
