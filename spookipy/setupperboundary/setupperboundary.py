# -*- coding: utf-8 -*-

import argparse
import logging
from typing import Final
import warnings

import numpy as np
import pandas as pd

from ..plugin import Plugin, PluginParser
from ..utils import (create_empty_result, final_results, initializer, validate_nomvar)

ETIKET: Final[str] = 'SETUPR'

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
    def __init__(self, df: pd.DataFrame, value: float = None, nomvar_out: str = None):
        self.plugin_result_specifications = {'etiket': ETIKET}
        super().__init__(df)
        self.validate_params()

    def validate_params(self):
        if (self.no_meta_df.nomvar.unique().size > 1) and (not (self.nomvar_out is None)):
            raise SetUpperBoundaryError('nomvar_out can only be used when only 1 field is present')

        if (self.no_meta_df.nomvar.unique().size == 1) and (not (self.nomvar_out is None)):
            validate_nomvar(self.nomvar_out, 'SetUpperBoundary', SetUpperBoundaryError)

    def compute(self) -> pd.DataFrame:    
        logging.info('SetUpperBoundary - compute')
        df_list=[]
        res_df = create_empty_result(self.no_meta_df, self.plugin_result_specifications, all_rows=True)
        if  (self.no_meta_df.nomvar.unique().size == 1) and (not (self.nomvar_out is None)):
            res_df['nomvar'] = self.nomvar_out
        data = np.stack(res_df.d)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res_df['d'] = np.split(np.where(data > self.value, self.value, data),data.shape[0])

        df_list.append(res_df)

        df_final = final_results(df_list, SetUpperBoundaryError, self.meta_df)
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
