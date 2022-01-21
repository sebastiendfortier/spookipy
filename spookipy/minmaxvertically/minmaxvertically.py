# -*- coding: utf-8 -*-

import logging

from numpy.core.numeric import True_

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe, initializer, reshape_arrays,
                     to_dask, to_numpy, validate_nomvar)


class MinMaxVerticallyError(Exception):
    pass

class MinMaxVertically(Plugin):
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            nomvar=str,
            min=False,
            max=False,
            bounded=False,
            nomvar_min: str = None,
            nomvar_max: str = None):

        self.validate_input()

    def validate_input(self):   
        if self.df.empty:
            raise MinMaxVerticallyError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        if not (self.nomvar_min is None):
            validate_nomvar(
                self.nomvar_min,
                'MinMaxVertically',
                MinMaxVerticallyError)

        if not (self.nomvar_max is None):
            validate_nomvar(
                self.nomvar_max,
                'MinMaxVertically',
                MinMaxVerticallyError)

        if (not self.min) and (not self.max):
            self.min = True
            self.max = True

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        keep = self.df.loc[~self.df.nomvar.isin(["KBAS", "KTOP"])].reset_index(drop=True)

        if self.bounded:
            if (self.df.loc[self.df.nomvar == "KBAS"]).empty or (self.df.loc[self.df.nomvar == "KTOP"]).empty:
                raise MinMaxVerticallyError('Missing fields KBAS and/or KTOP with BOUNDED option!')

    def compute(self) -> pd.DataFrame:
        from ..all import MinMaxLevelIndex

        df_list=[]

        if not (self.nomvar_min is None):
            min_out = self.nomvar_min
        else:
            min_out = "KMIN"

        if not (self.nomvar_max is None):
            max_out = self.nomvar_max
        else:
            max_out = "KMAX"

        df=MinMaxLevelIndex(self.df,
                            nomvar=self.nomvar, 
                            ascending=True, 
                            min=self.min, 
                            max=self.max,
                            bounded=self.bounded,
                            nomvar_min_idx= "_MIN",
                            nomvar_min_val= min_out,
                            nomvar_max_idx= "_MAX",
                            nomvar_max_val= max_out,
                            value_to_return=True).compute()

        logging.warning('MinMaxVertically - compute')

        if self.min:
            min_df = get_from_dataframe(df, min_out)
            min_df['etiket'] = "MNMXVY"
            min_df = reshape_arrays(min_df)
            df_list.append(min_df)
            
        if self.max:
            max_df = get_from_dataframe(df, max_out)
            max_df['etiket'] = "MNMXVY"
            max_df = reshape_arrays(max_df)
            df_list.append(max_df)

        return final_results(df_list, MinMaxVerticallyError, self.meta_df)
