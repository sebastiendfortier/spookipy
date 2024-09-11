# -*- coding: utf-8 -*-
import abc
import argparse

import pandas as pd
from ..utils import (dataframe_arrays_to_dask, reshape_arrays)
import fstpy
from   fstpy.dataframe_utils import convert_cols_to_boolean_dtype

class PluginParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        parsed_arg = super().parse_args(args,namespace)

        parsed_arg_dict = vars(parsed_arg)
        if "help-module" in parsed_arg_dict:
            self.print_help()

        return parsed_arg

def defines_base_argparser() -> PluginParser:
    parser = PluginParser(prog="Plugin", description=__doc__, add_help=True)

    generic_group = parser.add_argument_group('Generic Options')
    generic_group.add_argument('--help-module',type=str,choices=["generic","specific"], help="Produces a help for a given module.")
    generic_group.add_argument('--optimizationLevel',type=int,choices=[0,1,2], help="Sets level of optimization")
    generic_group.add_argument('--threads','-T',type=int, help="Sets the maximum amount of threads to be used.")
    generic_group.add_argument('--print_extended','-E',action='store_true', help="Prints the request this plugin generates when called - can only be used with full configuration because dependencies need to be created. This does not stop the request, thus error may arise if used with a fake request to get this information")
    generic_group.add_argument('--copy_input','-C',action='store_true', help="Copies the input fields to the output.")
    generic_group.add_argument('--uses',action='store_true', help="Prints out the plugins that this module uses - can only be used with full configuration because the dependencies need to be created.")
    generic_group.add_argument('--verbose',"-v",action='store_true', help="Increases verbosity level.")
    generic_group.add_argument('--version',action='store_true', help="Gets version number.")
    generic_group.add_argument('--plugin_language',type=str,choices=["PYTHON","CPP"], help="Force spooki_run to use the plugin in this language despite the --plugin_language_option.")

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
        self.df = fstpy.add_columns(df,'unit')
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
        
        # Ajout des colonnes reliees a l'etiket aux meta donnees.
        # Cet ajout est fait automatiquement pour les donnees dans create_empty_result.
        if ~self.meta_df.empty:
            self.meta_df = fstpy.add_columns(self.meta_df, columns=['etiket'])  

    def final_results(
        self,
        df_list: "list[pd.DataFrame]",
        error_class: 'type',
        dependency_check = False,
        copy_input = False,
        reduce_df = False) -> pd.DataFrame:
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
                if reduce_df:
                    df = fstpy.reduce_columns(df)
                new_list.append(df)

        if not len(new_list):
            if dependency_check:
                return pd.DataFrame(dtype=object)
            else:
                raise error_class('No results were produced')

        if reduce_df:
            self.meta_df = fstpy.reduce_parsed_etiket_columns(self.meta_df)
            # Suppression des colonnes des meta-data sans appliquer la reduction de colonnes
            self.meta_df = fstpy.remove_all_expanded_columns(self.meta_df)

        new_list.append(self.meta_df)

        # Ajout des données recues en input
        if copy_input:
            if reduce_df:
                self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=['etiket'])
                self.no_meta_df = fstpy.reduce_columns(self.no_meta_df)
            new_list.append(self.no_meta_df)

        # merge all results together
        boolean_cols = ['surface', 'ascending', 'follow_topography', 'multiple_modifications', 'zapped', 
                        'filtered', 'interpolated', 'unit_converted', 'bounded', 'missing_data', 
                        'ensemble_extra_info', 'masks', 'masked']

        # Conversion des colonnes a boolean pour eviter warning "object-dtype columns with all-bool values ..."
        for tmp_df in new_list:
            tmp_df = convert_cols_to_boolean_dtype(tmp_df, boolean_cols)

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
        parser = PluginParser(prog=__class__.__name__, parents=[Plugin.base_parser],add_help=False)
        return vars(parser.parse_args(args.split()))

