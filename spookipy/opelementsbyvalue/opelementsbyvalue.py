# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
from spookipy.utils import create_empty_result, initializer, remove_load_data_info, validate_nomvar
import pandas as pd
import fstpy.all as fstpy

class OpElementsByValueError(Exception):
    pass

class OpElementsByValue(Plugin):
    @initializer
    def __init__(self, df:pd.DataFrame, operator, value, operation_name='OpElementsByValue', exception_class = OpElementsByValueError, nomvar_out='', unit=''):
        self.validate_input()
        
    def validate_input(self):
        if self.df.empty:
            raise self.exception_class(self.operation_name + ' - no data to process')

        self.df = fstpy.metadata_cleanup(self.df)    

        validate_nomvar(self.nomvar_out, self.operation_name, self.exception_class)

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True) 

        self.df = self.df.query('nomvar not in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True) 
        
        self.plugin_result_specifications = {'ALL':{'nomvar':self.nomvar_out,'etiket':self.operation_name,'unit':self.unit}}

    def compute(self) -> pd.DataFrame:
        res_df = create_empty_result(self.df,self.plugin_result_specifications['ALL'],copy=True)
        res_df = fstpy.load_data(res_df)
        res_df['d'] = self.operator(res_df['d'], self.value)

        self.meta_df = fstpy.load_data(self.meta_df)
        # merge all results together
        res_df = pd.concat([res_df,self.meta_df],ignore_index=True)

        res_df = remove_load_data_info(res_df)
        res_df = fstpy.metadata_cleanup(res_df)

        return res_df 