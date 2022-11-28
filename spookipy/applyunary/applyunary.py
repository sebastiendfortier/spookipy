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

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise ApplyUnaryError('No data to process')

        validate_nomvar(self.nomvar_out, 'ApplyUnary', ApplyUnaryError)

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

    def compute(self) -> pd.DataFrame:
        logging.info('ApplyUnary - compute')

        in_df = self.df.loc[self.df.nomvar == self.nomvar_in].reset_index(drop=True)
        in_df = fstpy.add_columns(in_df, columns=['npak'])

        if in_df.empty:
            raise ApplyUnaryError(f'No data to process with nomvar {self.nomvar_in}')

        res_df = create_empty_result(in_df,
                                     {'nomvar': self.nomvar_out,
                                      'etiket': self.etiket,
                                      'datyp': 5,
                                      'nbits': 32},
                                     all_rows=True)

        for i in res_df.index:
            res_df.at[i, 'd'] = self.function(in_df.at[i, 'd'])

        return final_results([res_df], ApplyUnaryError, self.meta_df)
