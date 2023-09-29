# -*- coding: utf-8 -*-
import logging
from typing import Final

import numpy as np
import pandas as pd
import warnings 
import fstpy

from ..plugin import Plugin, PluginParser
from ..utils import (create_empty_result, initializer, validate_nomvar)

ETIKET: Final[str] = 'SETLWR'

class SetLowerBoundaryError(Exception):
    pass

class SetLowerBoundary(Plugin):
    """Limit the minimum value of a field to the specified value

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
        
        self.plugin_result_specifications = {'label': ETIKET}
        
        super().__init__(self.df)
        self.validate_params()

    def validate_params(self):
        if (self.no_meta_df.nomvar.unique().size > 1) and (not (self.nomvar_out is None)):
            raise SetLowerBoundaryError('nomvar_out can only be used when only 1 field is present')

        if (self.no_meta_df.nomvar.unique().size == 1) and (not (self.nomvar_out is None)):
            validate_nomvar(self.nomvar_out, 'SetLowerBoundary', SetLowerBoundaryError)

    def compute(self) -> pd.DataFrame:    
        logging.info('SetLowerBoundary - compute')
        df_list=[]
        res_df = create_empty_result(self.no_meta_df, self.plugin_result_specifications, all_rows=True)

        if  (self.no_meta_df.nomvar.unique().size == 1) and (not (self.nomvar_out is None)):
            res_df['nomvar'] = self.nomvar_out
            
        groups_grid = res_df.groupby(['grid'])
        for _, grid_df in groups_grid:
            data = np.stack(grid_df.d)
            
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                grid_df['d'] = np.split(np.where(data < self.value, self.value, data),data.shape[0])
                
            df_list.append(grid_df)

        # Conversion du dask array en numpy array, pour que le squeeze fonctionne bien 
        for i in self.meta_df.index:
            self.meta_df.at[i,'d'] = fstpy.to_numpy(self.meta_df.at[i,'d'])

        df_final = self.final_results(df_list, 
                                      SetLowerBoundaryError, 
                                      copy_input=False)
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
        parser = PluginParser(prog=SetLowerBoundary.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--value',type=float,required=True, help="Value of lower boundary.")
        parser.add_argument('--outputFieldName',type=str,dest='nomvar_out',help="Option to give the output field a different name from the input field name.")

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg['nomvar_out'] is not None:
            validate_nomvar(parsed_arg['nomvar_out'],"SetLowerBoundary",SetLowerBoundaryError)

        return parsed_arg
