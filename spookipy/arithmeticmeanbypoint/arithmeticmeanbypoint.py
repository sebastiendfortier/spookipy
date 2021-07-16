# -*- coding: utf-8 -*-
from spookipy.utils import initializer
from spookipy.plugin import Plugin
import pandas as pd
import numpy as np
from spookipy.opelementsbypoint.opelementsbypoint import OpElementsByPoint

class ArithmeticMeanByPointError(Exception):
    pass

class ArithmeticMeanByPoint(Plugin):
    @initializer
    def __init__(self, df:pd.DataFrame, group_by_forecast_hour=False, nomvar_out='MEAN'):
        pass

    def compute(self) -> pd.DataFrame:
        return OpElementsByPoint(self.df, 
        operator = np.mean,
        operation_name='ArithmeticMeanByPoint', 
        exception_class = ArithmeticMeanByPointError, 
        group_by_forecast_hour=self.group_by_forecast_hour, 
        group_by_level=True, 
        nomvar_out=self.nomvar_out).compute()

