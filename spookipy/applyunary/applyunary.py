# -*- coding: utf-8 -*-
from ..plugin import Plugin
from ..utils import initializer, remove_load_data_info, validate_nomvar
import pandas as pd
import fstpy.all as fstpy
import sys

#see functions without arguments from numpy lib
#https://numpy.org/doc/stable/reference/routines.math.html
class ApplyUnaryError(Exception):
    pass     
class ApplyUnary(Plugin):
    @initializer
    def __init__(self, df:pd.DataFrame, function=None, nomvar_in=None, nomvar_out=None, etiket=None):
        self.validate_input()

    def validate_input(self):
        validate_nomvar(self.nomvar_out, 'ApplyUnary', ApplyUnaryError)
        if self.df.empty:
            raise  ApplyUnaryError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)
        
        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True) 

        self.df = self.df.query('nomvar not in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)         


    def compute(self) -> pd.DataFrame:
        sys.stdout.write('ApplyUnary - compute')
        in_df = self.df.query( 'nomvar=="%s"'%self.nomvar_in).reset_index(drop=True)
        
        if in_df.empty:
            raise ApplyUnaryError(f'No data to process with nomvar {self.nomvar_in}')

        in_df = fstpy.load_data(in_df)
        res_df = in_df.copy(deep=True)
        res_df['nomvar']=self.nomvar_out
        res_df['etiket']=self.etiket
        for i in res_df.index:
            res_df.at[i,'d'] = self.function(in_df.at[i,'d'])
        
        self.meta_df = fstpy.load_data(self.meta_df)
        # merge all results together
        res_df = pd.concat([res_df,self.meta_df],ignore_index=True)

        res_df = remove_load_data_info(res_df)
        res_df = fstpy.metadata_cleanup(res_df)

        return res_df