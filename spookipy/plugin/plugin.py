# -*- coding: utf-8 -*-
import abc
import argparse

import pandas as pd
from ..utils import (dataframe_arrays_to_dask, reshape_arrays)
import fstpy

class PluginParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        parsed_arg = super().parse_args(args,namespace)

        parsed_arg_dict = vars(parsed_arg)
        if "help" in parsed_arg_dict and parsed_arg_dict['help'] or "help-module" in parsed_arg_dict:
            self.print_help()

        return parsed_arg

def defines_base_argparser() -> PluginParser:
    parser = PluginParser(prog="Plugin", description=__doc__, add_help=False)
    parser.add_argument('--help','-h',action='store_true', help="Produces this help message.")
    parser.add_argument('--help-module',type=str,choices=["generic","specific"], help="Produces a help for a given module.")
    parser.add_argument('--optimizationLevel',type=int,choices=[0,1,2], help="Sets level of optimization")
    parser.add_argument('--threads','-T',type=int, help="Sets the maximum amount of threads to be used.")
    parser.add_argument('--print_extended','-E',action='store_true', help="Prints the request this plugin generates when called - can only be used with full configuration because dependencies need to be created. This does not stop the request, thus error may arise if used with a fake request to get this information")
    parser.add_argument('--copy_input','-C',action='store_true', help="Copies the input fields to the output.")
    parser.add_argument('--uses',action='store_true', help="Prints out the plugins that this module uses - can only be used with full configuration because the dependencies need to be created.")
    parser.add_argument('--verbose',"-v",action='store_true', help="Increases verbosity level.")
    parser.add_argument('--version',action='store_true', help="Gets version number.")
    parser.add_argument('--plugin_language',type=str,choices=["PYTHON","CPP"], help="Force spooki_run to use the plugin in this language despite the --plugin_language_option.")

    return parser

class EmptyDataframeError(Exception):
    pass


class Plugin(abc.ABC):
    """Abstract Base Class for plugins

    :param df: input dataframe
    :type df: pd.DataFrame
    :param: copy_input
    :type copy_input: bool, optional 
    """
    base_parser = defines_base_argparser()

    computable_plugin = None
    def __init__(self, df: pd.DataFrame, copy_input=False) -> None:
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

    def final_results(
        self,
        df_list: "list[pd.DataFrame]",
        error_class: 'type',
        dependency_check = False,
        copy_input = False) -> pd.DataFrame:
        """Returns the final results dataframe, created from the list of dataframes and the meta data

        :param df_list: list of dataframes, one per grouping method in the plugin
        :type df_list: list[pd.DataFrame]
        :param error_class: Exception to raise if list is empty
        :type error_class: Exception
        :raises error_class: error class to raise
        :param dependency_check: Indicates the plugin is being called from another one who checks dependencies , defaults to False
        :type dependency_check: bool, optional
        :return: clean and sorted resulting dataframe
        :rtype: pd.DataFrame
        """
        new_list = []
        for df in df_list:
            if not df.empty:
                new_list.append(df)

        if not len(new_list):
            if dependency_check:
                return pd.DataFrame(dtype=object)
            else:
                raise error_class('No results were produced')

        new_list.append(self.meta_df)

        # Ajout des données recues en input
        if copy_input:
            new_list.append(self.no_meta_df)

        # merge all results together
        res_df = pd.concat(new_list, ignore_index=True)
        res_df = fstpy.metadata_cleanup(res_df)

        return res_df

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
        parser = PluginParser(prog=__class__.__name__, parents=[Plugin.base_parser])
        return vars(parser.parse_args(args.split()))

