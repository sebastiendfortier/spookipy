# -*- coding: utf-8 -*-
import abc
from distutils import dep_util
import argparse
from distutils import dep_util

import pandas as pd

def defines_base_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="Plugin", description=__doc__, add_help=False)
    parser.add_argument('--help-module',type=str,choices=["generic","specific"], help="Produce a help for a given module.")
    parser.add_argument('--optimizationLevel',type=int,choices=[0,1,2], help="Set level of optimization")
    parser.add_argument('--threads','-T',type=int, help="Set the maximum amount of threads to be used.")
    parser.add_argument('--uses',action='store_true', help="Print out the plugins that this module uses - can only be used with full configuration because dependencies need to be created.")
    parser.add_argument('--print_extended','-E',action='store_true', help="Prints the request this plugin generates when called - can only be used with full configuration because dependencies need to be created. This does not stop the request, thus error may arise if used with a fake request to get this information")
    parser.add_argument('--verbose',"-v",action='store_true', help="Increase verbosity level.")
    parser.add_argument('--version',action='store_true', help="Get version number.")

    return parser

class EmptyDataframeError(Exception):
    pass


class Plugin(abc.ABC):
    """Abstract Base Class for plugins

    :param df: input dataframe
    :type df: pd.DataFrame
    """
    base_parser = defines_base_argparser()
    computable_plugin = None
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.validate_input()
        self.get_dataframes()

    def validate_input(self):
        """Checks that the plugin's dataframe is not empty.

        :raises EmptyDataframeError: The plugin's dataframe is empty, no data to process.
        """
        if self.df.empty:
            raise EmptyDataframeError("Plugin" + ' - no data to process')


    def get_dataframes(self):
        """creates self.meta_df and self.no_meta_df"""
        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.no_meta_df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)
        if self.no_meta_df.empty:
            raise EmptyDataframeError("Plugin" + ' - no data to process')    

    @abc.abstractmethod
    def compute(self) -> pd.DataFrame:
        """Abstract method that should implement the plugin's algorithm.

        :return: dataframe with the results
        :rtype: pd.DataFrame
        """
        pass

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters

        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=__class__.__name__, parents=[Plugin.base_parser])
        return vars(parser.parse_args(args.split()))

