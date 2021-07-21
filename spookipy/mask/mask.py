# -*- coding: utf-8 -*-
from ..utils import initializer
from ..plugin import Plugin
import pandas as pd
import numpy as np
import operator as op
import fstpy.all as fstpy

def eq(v,t):
    if (v >= (t - 0.4) ) and (v <= (t + 0.4)):
        return True
    return False

class MaskError(Exception):
    pass

#[Mask --thresholds 0.0,10.0,15.0,20.0 --values 0.0,10.0,15.0,20.0 --operators GE,GE,GE,GE] >> 
class Mask(Plugin):

    @initializer
    def __init__(self, df:pd.DataFrame, thresholds=None, values=None, operators=None, nomvar_out=''):
        # self.df = df
        # self.thresholds = thresholds
        # self.values = values
        # self.operators = operators
        # self.nomvar_out = nomvar_out
        if self.df.empty:
            raise  MaskError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)
            
        length = len(thresholds)
        if not all(len(lst) == length for lst in [values, operators]):
            raise MaskError('Threshholds, values and operators lists, must have the same lenght')
        ops = {op.lt,op.le,eq,op.ge,op.gt}
        in_ops = set(self.operators)
        
        if not in_ops.issubset(ops):
            raise MaskError('Operators must have values included in %s' % ops)
        self.df = fstpy.load_data(self.df)
        self.lenght = length
        self.thresholds = np.flip(thresholds)
        self.values = np.flip(values)
        self.operators = np.flip(operators)


    def get_etiket(self) -> str:
        return str(__class__).split(__name__,1)[1][1:-2]


    def compute(self) -> pd.DataFrame:
        #holds data from all the groups
        outdf = self.df.copy(deep=True)
        if len(self.nomvar_out):
            # outdf = fstpy.zap(outdf, nomvar=self.nomvar_out, etiket=self.get_etiket())
            outdf['nomvar'] = self.nomvar_out
            outdf['etiket'] = self.get_etiket()
        else:
            outdf['etiket']=self.get_etiket()
        vmask = np.vectorize(self.mask)
        for i in self.df.index:
            pds = self.df.at[i,'d'].flatten()
            outdf.at[i,'d'] = vmask(pds)
            outdf.at[i,'d'] = outdf.at[i,'d'].reshape(outdf.at[i,'shape'])
        return outdf

    def mask(self, value):
        # La valeur par defaut est 0.
        rslt = 0.0
        res=False
        # Verifier toutes les conditions sur 1 point, en partant de la derniere condition.
        # Arreter lorsqu'une condition est trouvee.

        for i in range(len(self.values)):
            if self.operators[i](value, self.thresholds[i]):
                return self.values[i]
        return rslt


        
        