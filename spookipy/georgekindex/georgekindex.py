# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
import numpy as np

class GeorgeKIndexError(Exception):
    pass

def george_k_index(tt850:np.ndarray, tt500:np.ndarray, td850:np.ndarray, tt700:np.ndarray, td700:np.ndarray) -> np.ndarray:
    return (tt850 - tt500) + td850 - (tt700 - td700)

class GeorgeKIndex(Plugin):
    plugin_requires = '(nomvar in ["TT","TD"]) and (level in [850,700,500]) and (ip1_pkind =="mb")' 
    plugin_result = {'KI':{'nomvar':'KI','etiket':'GeorgeKIndex','unit':'scalar'}}

    def __init__(self,df:pd.DataFrame):
        self.df = df
        if df.empty:
            raise GeorgeKIndexError(GeorgeKIndex + ' - no data to process') 
        self.df = self.df.query(self.plugin_requires)
        self.df = fstpy.load_data(self.df)
        self.groups= df.groupby(by=['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        kidfs=[]
        for _, group in self.groups:
            tt850df = group.query( '(nomvar=="TT") and (level==850) and (pkind=="mb")')
            tt700df = group.query( '(nomvar=="TT") and (level==700) and (pkind=="mb")')
            tt500df = group.query( '(nomvar=="TT") and (level==500) and (pkind=="mb")')
            td850df = group.query( '(nomvar=="TD") and (level==850) and (pkind=="mb")')
            td700df = group.query( '(nomvar=="TD") and (level==700) and (pkind=="mb")')
            kidf = fstpy.create_1row_df_from_model(tt850df)
            # kidf = fstpy.zap(kidf,**self.plugin_result_specifications)
            for k,v in self.plugin_result_specifications['ES'].items():kidf[k] = v
            kidf.iloc[0]['d'] = george_k_index(tt850df.iloc[0]['d'],tt500df.iloc[0]['d'],td850df.iloc[0]['d'],tt700df.iloc[0]['d'],td700df.iloc[0]['d'])
            kidfs.append(kidf)
        res = pd.concat(kidfs,ignore_index=True)
        return res