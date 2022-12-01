# -*- coding: utf-8 -*-
import logging

import fstpy
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, final_results, initializer,
                     validate_nomvar)

# see functions without arguments from numpy lib
# https://numpy.org/doc/stable/reference/routines.math.html


class ApplyUnaryError(Exception):
    pass


class ApplyUnary(Plugin):
    """Apply a unary function the data, point by point

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param function: unary function to apply, defaults to None
    :type function: function, optional
    :param nomvar_in: nomvar of field to apply function to, defaults to None
    :type nomvar_in: str, optional
    :param nomvar_out: nomvar of the results field, defaults to None
    :type nomvar_out: str, optional
    :param etiket: etiket to apply to results, defaults to None
    :type etiket: str, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            function=None,
            nomvar_in=None,
            nomvar_out=None,
            etiket=None):

        self.plugin_result_specifications = \
        {
            'ALL': {'etiket': self.etiket,
                    'datyp': 5,
                    'nbits': 32}
        }
        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)
        self.validate_params_and_input()

    def validate_params_and_input(self):

        if self.nomvar_in is None:
            nomvar_list = self.no_meta_df.nomvar.unique()
            if len(nomvar_list) == 1:
                self.nomvar_in = nomvar_list[0]
            elif not(self.nomvar_out is None):
                raise ApplyUnaryError(
                  f'whenever parameter nomvar_out is specified, only 1 input is allowed: got {nomvar_list} in input')
        else:
            validate_nomvar(self.nomvar_in, 'ApplyUnary', ApplyUnaryError)

        if not(self.nomvar_out is None):
            validate_nomvar(self.nomvar_out, 'ApplyUnary', ApplyUnaryError)


    def compute(self) -> pd.DataFrame:
        logging.info('ApplyUnary - compute')

        if self.nomvar_in != None:
            in_df = self.no_meta_df.loc[self.no_meta_df.nomvar == self.nomvar_in].reset_index(drop=True)
        else:
            in_df=self.no_meta_df

        if in_df.empty:
            raise ApplyUnaryError(f'No data to process with nomvar {self.nomvar_in}')

        if not(self.nomvar_out is None):
            self.plugin_result_specifications["ALL"]["nomvar"]   = self.nomvar_out

        res_df = create_empty_result(in_df,
                                     self.plugin_result_specifications['ALL'],       
                                     all_rows=True)
        for i in res_df.index:
            res_df.at[i, 'd'] = self.function(in_df.at[i, 'd'])

        return final_results([res_df], ApplyUnaryError, self.meta_df)
