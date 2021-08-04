# -*- coding: utf-8 -*-
from ..plugin import Plugin
from ..utils import initializer
import pandas as pd
import numpy as np
import sys
from ..opelementsbypoint import OpElementsByPoint

class AddElementsByPointError(Exception):
    pass

class AddElementsByPoint(Plugin):
    @initializer
    def __init__(self, df:pd.DataFrame, group_by_forecast_hour=False, nomvar_out='ADEP'):
        pass
        
    def compute(self) -> pd.DataFrame:
        sys.stdout.write('AddElementsByPoint - compute\n')
        return OpElementsByPoint(self.df, 
        operator = np.sum,
        operation_name='AddElementsByPoint', 
        exception_class = AddElementsByPointError, 
        group_by_forecast_hour=self.group_by_forecast_hour, 
        group_by_level=True, 
        nomvar_out=self.nomvar_out).compute()
