# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
import pandas as pd
import numpy as np
from spookipy.opelementsbypoint.opelementsbypoint import OpElementsByPoint

class AddElementsByPointError(Exception):
    pass

class AddElementsByPoint(Plugin):
    def __init__(self, df:pd.DataFrame, group_by_forecast_hour=False, nomvar_out='ADEP'):
        self.df = df
        self.group_by_forecast_hour = group_by_forecast_hour
        self.nomvar_out = nomvar_out
        
    def compute(self) -> pd.DataFrame:
        return OpElementsByPoint(self.df, 
        operator = np.sum,
        operation_name='AddElementsByPoint', 
        exception_class = AddElementsByPointError, 
        group_by_forecast_hour=self.group_by_forecast_hour, 
        group_by_level=True, 
        nomvar_out=self.nomvar_out).compute()
