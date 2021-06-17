# -*- coding: utf-8 -*-
import abc
import pandas as pd

class EmptyDataframeError(Exception):
    pass

class Plugin(abc.ABC):
    def __init__(self,df:pd.DataFrame) -> None:
        self.df = df
        self.validate_input()
        print("super __init__")

    def validate_input(self):
        if self.df.empty:
            raise  EmptyDataframeError( "Plugin" + ' - no data to process')
      
    @abc.abstractmethod
    def compute(self) -> pd.DataFrame:
        pass