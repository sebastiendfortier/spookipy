# -*- coding: utf-8 -*-

import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..minmaxlevelindex import MinMaxLevelIndex
from ..plugin import Plugin
from ..utils import (final_results,get_from_dataframe, initializer, 
                    reshape_arrays, validate_nomvar)

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
            ascending=True,
            nomvar_min: str = None,
            nomvar_max: str = None):
        super().__init__(df)
        self.validate_params_and_input()

    def validate_params_and_input(self):   

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

        if self.bounded:
            if (self.no_meta_df.loc[self.no_meta_df.nomvar == "KBAS"]).empty or \
               (self.no_meta_df.loc[self.no_meta_df.nomvar == "KTOP"]).empty:
                raise MinMaxVerticallyError('Missing fields KBAS and/or KTOP with BOUNDED option!')

    def compute(self) -> pd.DataFrame:
        logging.info('MinMaxVertically - compute')

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
                            min=self.min, 
                            max=self.max,
                            bounded=self.bounded,
                            ascending=self.ascending,
                            nomvar_min_idx= "_MIN",
                            nomvar_min_val= min_out,
                            nomvar_max_idx= "_MAX",
                            nomvar_max_val= max_out,
                            value_to_return=True).compute()

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
