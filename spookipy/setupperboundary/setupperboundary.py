# -*- coding: utf-8 -*-
import logging
from typing import Final
import warnings

import numpy as np
import pandas as pd
import fstpy

from ..plugin import Plugin, PluginParser
from ..utils import (create_empty_result, initializer, validate_nomvar)

class SetUpperBoundaryError(Exception):
    pass

class SetUpperBoundary(Plugin):
    """Limit the maximum value of a field to the specified value.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param value: value to add to field
    :type value: float
    :param nomvar_out: nomvar for output result, defaults to None
    :type nomvar_out: str, optional
    """
    @initializer
    def __init__(self, 
                 df: pd.DataFrame, 
                 value: float = None, 
                 nomvar_out: str = None):
        
        self.plugin_result_specifications = {}
        
        super().__init__(self.df)
        self.validate_params()

    def validate_params(self):
        if (self.no_meta_df.nomvar.unique().size > 1) and (not (self.nomvar_out is None)):
            raise SetUpperBoundaryError('nomvar_out can only be used when only 1 field is present')

        if (self.no_meta_df.nomvar.unique().size == 1) and (not (self.nomvar_out is None)):
            validate_nomvar(self.nomvar_out, 'SetUpperBoundary', SetUpperBoundaryError)

    def compute(self) -> pd.DataFrame:    
        logging.info('SetUpperBoundary - compute')
        df_list=[]

        res_df = create_empty_result(self.no_meta_df, 
                                     self.plugin_result_specifications, 
                                     all_rows=True)
        res_df = fstpy.add_flag_values(res_df)
        res_df.bounded = True 

        if  (self.no_meta_df.nomvar.unique().size == 1) and (not (self.nomvar_out is None)):
            res_df['nomvar'] = self.nomvar_out

        groups_grid = res_df.groupby(['grid'])
        for _, grid_df in groups_grid:
            data = np.stack(grid_df.d)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                grid_df['d'] = np.split(np.where(data > self.value, self.value, data),data.shape[0])

            df_list.append(grid_df)

        # Conversion du dask array en numpy array, pour que le squeeze fonctionne bien 
        for i in self.meta_df.index:
            self.meta_df.at[i,'d'] = fstpy.to_numpy(self.meta_df.at[i,'d'])

        # # Suppression des colonnes reliees aux ip, on sait qu'elles n'ont pas ete modifiees
        # new_list = []
        # ip_columns = ['level', 'ip1_kind', 'ip1_pkind', 'ip2_dec', 'ip2_kind', 'ip2_pkind', 'ip3_dec',
        #               'ip3_kind', 'ip3_pkind', 'interval', 'surface', 'follow_topography', 'ascending']
        # for df in df_list:
        #     df = fstpy.remove_list_of_columns(df, ip_columns)
        #     new_list.append(df)

        df_final = self.final_results(df_list, 
                                      SetUpperBoundaryError, 
                                      copy_input=False,
                                      reduce_df = True)

        df_final['d'] = df_final.apply(lambda row: np.squeeze(row['d']), axis=1)

        return df_final

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=SetUpperBoundary.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--value',type=float,required=True, help="Value of upper boundary.")
        parser.add_argument('--outputFieldName',type=str,dest='nomvar_out',help="Option to give the output field a different name from the input field name.")

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg['nomvar_out'] is not None:
            validate_nomvar(parsed_arg['nomvar_out'],"SetUpperBoundary",SetUpperBoundaryError)

        return parsed_arg
