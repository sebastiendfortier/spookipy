# -*- coding: utf-8 -*-
import logging

import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (final_results, initializer, to_dask, to_numpy,
                     validate_nomvar)
from .f_stenfilt import f_stenfilt


class FilterDigitalError(Exception):
    pass


class FilterDigital(Plugin):

    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            filter: list,
            repetitions: int = 1,
            nomvar_out=None):

        self.plugin_result_specifications = {
            'ALL': {'filtered': True}
            # 'etiket':'FLTRDG',
        }

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise FilterDigitalError('No data to process')

        validate_nomvar(self.nomvar_out, 'FilterDigital', FilterDigitalError)

        if not len(self.filter):
            raise FilterDigitalError('Filter must contain at least 1 value')

        if len(self.filter) % 2 == 0:
            raise FilterDigitalError('Filter lenght must be odd, not even')

        if not (self.repetitions > 0):
            raise FilterDigitalError('Repetitions must be a positive integer')

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

    def compute(self) -> pd.DataFrame:
        logging.info('FilterDigital - compute')

        # if not (self.nomvar_out is None):
        #     self.plugin_result_specifications['ALL']['nomvar'] = self.nomvar_out

        # self.df = fstpy.compute(self.df)

        if not (self.nomvar_out is None):
            self.df['nomvar'] = self.nomvar_out
        self.df['filtered'] = True

        # new_df = create_empty_result(self.df,self.plugin_result_specifications['ALL'],all_rows=True)

        filter_len = len(self.filter)

        filter = np.array(self.filter, dtype=np.int32, order='F')

        df_list = []
        for i in self.df.index:
            ni = self.df.at[i, 'd'].shape[0]
            nj = self.df.at[i, 'd'].shape[1]
            self.df.at[i, 'd'] = to_numpy(self.df.at[i, 'd'])
            f_stenfilt(slab=self.df.at[i,
                                       'd'],
                       ni=ni,
                       nj=nj,
                       npass=self.repetitions,
                       list=filter,
                       l=filter_len)
            self.df.at[i, 'd'] = to_dask(self.df.at[i, 'd'])

        df_list.append(self.df)

        return final_results(df_list, FilterDigitalError, self.meta_df)
