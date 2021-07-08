# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
from spookipy.utils import validate_nomvar
import pandas as pd
import fstpy.all as fstpy

#see functions without arguments from numpy lib
#https://numpy.org/doc/stable/reference/routines.math.html
class ApplyUnaryError(Exception):
    pass     
class ApplyUnary(Plugin):
    
    def __init__(self, df:pd.DataFrame, function=None, nomvar_in=None, nomvar_out=None, etiket=None):
        self.df = df
        self.function = function
        self.nomvar_in = nomvar_in
        self.nomvar_out = nomvar_out
        self.etiket = etiket
        validate_nomvar(nomvar_out, 'ApplyUnary', ApplyUnaryError)
        if self.df.empty:
            raise  ApplyUnaryError( 'ApplyUnary' + ' - no data to process')


    def compute(self) -> pd.DataFrame:
        indf = self.df.query( 'nomvar=="%s"'%self.nomvar_in).reset_index(drop=True)
        indf.sort_values('level')
        indf = fstpy.load_data(indf)
        outdf = indf.copy(deep=True)
        outdf['nomvar']=self.nomvar_out
        outdf['etiket']=self.etiket
        for i in outdf.index:
            outdf.at[i,'d'] = self.function(indf.at[i,'d'])
           
        return outdf

   