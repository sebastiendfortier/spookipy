# -*- coding: utf-8 -*-
import abc
import pandas as pd

class EmptyDataframeError(Exception):
    pass

class Plugin(abc.ABC):
    """Abstract Base Class for plugins

    :param df: input dataframe
    :type df: pd.DataFrame
    """
    def __init__(self,df:pd.DataFrame) -> None:
        self.df = df
        self.validate_input()
        print("super __init__")

    def validate_input(self):
        """Checks that the plugin's dataframe is not empty.

        :raises EmptyDataframeError: The plugin's dataframe is empty, no data to process.
        """
        if self.df.empty:
            raise  EmptyDataframeError( "Plugin" + ' - no data to process')
      
    @abc.abstractmethod
    def compute(self) -> pd.DataFrame:
        """Abstract method that should implement the plugin's algorithm.

        :return: dataframe with the results
        :rtype: pd.DataFrame
        """
        pass