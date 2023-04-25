# -*- coding: utf-8 -*-

import argparse

import fstpy
import pandas as pd

from ..plugin import Plugin, PluginParser
from ..utils import (initializer, print_voir)


class PrintDf(Plugin):
    """Print Dataframe

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param voir: Print dataframe like voir.
    :type voir: bool
    :param columns: Add columns to dataframe before printing.
    :type columns: bool
    :param output: Output file name
    :type output: str
    """

    @initializer
    def __init__(
        self,
        df:pd.DataFrame,
        voir:bool = False,
        columns:bool = False,
        ):
        pass
    
    def compute(self) -> pd.DataFrame:
        """Abstract method that should implement the plugin's algorithm.

        :return: dataframe with the results
        :rtype: pd.DataFrame
        """
        pd.set_option("display.max_rows", 500, "display.max_columns", 500)
        
        if self.voir:
            print_voir(self.df)
        elif self.columns:
            print(fstpy.add_columns(self.df))
        else:
            print(self.df)

        return self.df
    
    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=PrintDf.__name__, parents=[Plugin.base_parser],add_help=False)

        parser.add_argument('--voir',action='store_true',default=False,dest="voir", help="Print dataframe like voir.")
        parser.add_argument('--columns',action='store_true',default=False,dest="columns", help="Add columns to dataframe before printing.")

        return vars(parser.parse_args(args.split()))