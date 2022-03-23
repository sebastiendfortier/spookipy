from mimetypes import init
from turtle import pd
from spookipy.utils import initializer
from ..plugin.plugin import Plugin
import pandas as pd


class Thickness(Plugin):
    @initializer
    def __init__(self, df: pd.DataFrame, base: float, top: float, coordinateType: str):
        self.df = df
        self.base = base
        self.top = top
        self.coordinateType = coordinateType
        
        pass



