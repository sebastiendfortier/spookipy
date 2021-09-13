# -*- coding: utf-8 -*-
from ..plugin import Plugin
from ..utils import create_empty_result, initializer, final_results, validate_nomvar
import pandas as pd
import fstpy.all as fstpy
import logging

class OpElementsByValueError(Exception):
    pass

class OpElementsByValue(Plugin):
    @initializer
    def __init__(self, df:pd.DataFrame, operator, value, operation_name='OpElementsByValue', exception_class = OpElementsByValueError, nomvar_out=None, unit='',etiket=None):
        if self.etiket is None:
            self.etiket=self.operation_name
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise self.exception_class(self.operation_name + ' - no data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        validate_nomvar(self.nomvar_out, self.operation_name, self.exception_class)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        if not (self.nomvar_out is None):
            self.plugin_result_specifications = {'ALL':{'nomvar':self.nomvar_out,'etiket':self.etiket,'unit':self.unit}}
        else:
            self.plugin_result_specifications = {'ALL':{'etiket':self.etiket,'unit':self.unit}}

    def compute(self) -> pd.DataFrame:
        logging.info('OpElementsByValue - compute\n')
        df_list = []
        res_df = create_empty_result(self.df,self.plugin_result_specifications['ALL'],all_rows=True)
        res_df = fstpy.load_data(res_df)
        res_df['d'] = self.operator(res_df['d'], self.value)
        df_list.append(res_df)

        return final_results(df_list, self.exception_class, self.meta_df)
