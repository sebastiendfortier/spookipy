# -*- coding: utf-8 -*-                                 # always use utf8 encoding when editing files

# use logging for console output, logging.debug, logging.info,
# logging.warning, logging.critical
import logging

import fstpy
import numpy as np
import pandas as pd


# ex.: logging.info('ExamplePlugin - compute')
# interface class for all plugins
from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results,  # plugin tools
                     final_results, get_dependencies, get_existing_result,
                     get_from_dataframe)
# from .fortran.fortran_function import fortran_function
# from .ccp.windmoduluscpp import wind_modulus_cpp


def python_algorithm(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Comment the function

    :param a: a  - dataframe data field
    :type a: np.ndarray
    :param b: b - dataframe data field
    :type b: np.ndarray
    :return: python_algorithm
    :rtype: np.ndarray
    """
    return (a**2 + b**2)**.5


# define an exception to use in this plugin
class ExamplePluginError(Exception):
    pass


class ExamplePlugin(Plugin):
    # @initializer                                                                this decorator can be used when you have multiple parameters, it will automatically initialize self. class variable
    def __init__(self, df: pd.DataFrame, language='python'):
        supported_languages = ['python','cpp','fortran']
        if language not in supported_languages:
            raise ExamplePluginError(f'language {language} not in {supported_languages}')
        self.language = language
        self.plugin_mandatory_dependencies = [{                                  # define one or more filed dependencies specifications
            # in this case we want uu and vv in knots from the dataframe
            'UU': {'nomvar': 'UU', 'unit': 'knot'},
            # if the field dependency is computable, the system will try to run
            # the plugin
            'VV': {'nomvar': 'VV', 'unit': 'knot'},
        }]                                                                       # as an example PX can be conputed, 'PX':{'nomvar':'PX','unit':'hectoPascal'}
        # if the field is computable you can choose to select it instead of trying to compute
        # with the special key value pair 'select_only':True
        # 'PX':{'nomvar':'PX','unit':'hectoPascal', 'select_only':True}
        # also any column of the dataframe can be included in the specification
        # as an example, if you wanted to select the surface level only, you could add 'surface':True
        # 'UU':{'nomvar':'UU','unit':'knot', 'surface':True}
        # units are stored in fstpy.UNITS, >>> fstpy.UNITS to print the contents
        # see get_plugin_dependencies funtion documentation for computable
        # dependencies

        self.plugin_result_specifications = {                                    # define the resulting fields specifications
            # in this case, we want the comvar to be UV, the etiket to be
            # WNDMOD
            'UV': {'nomvar': 'UV', 'etiket': 'WNDMOD', 'unit': 'knot'}
        }                                                                        # and since the result is in knots, we want to set the unit to knots

        # here, since we didn't use the @initializer decorator, we have to set
        # the class variable manually
        self.df = df

        # here we validate our paramters ans other things befor the
        # calculations
        self.validate_input()

    def validate_input(self):
        # always check our dataframe is not empty
        if self.df.empty:
            raise ExamplePluginError('No data to process')

        # cleaup the metadata fields that we received with the dataframe
        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(
            drop=True)   # keep the metadata to be added at the end

        # add some columns if they are not already in the dataframe
        self.df = fstpy.add_columns(
            self.df, columns=[
                'unit', 'forecast_hour', 'ip_info'])
        # this helps with sorting and grouping the data
        # ip_info tag includes the decoding (gets the kind and value) of ip1, ip2 ip3
        # the virtical coordinate type, the surface flag, the virtical coordinate type
        # and the ascending value for the type of level

        # check if result already exists
        # this function will look in the dataframe to see if the result isn't
        # already present
        self.existing_result_df = get_existing_result(
            self.df, self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(
            drop=True)  # get dataframe without metadata

        self.groups = self.df.groupby(
            ['grid', 'dateo', 'forecast_hour', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        # return the existing results if we found them
        if not self.existing_result_df.empty:
            return existing_results(
                'ExamplePlugin',
                self.existing_result_df,
                self.meta_df)

        logging.info('ExamplePlugin - compute')
        df_list = []
        dependencies_list = get_dependencies(
            self.groups,
            self.meta_df,
            'ExamplePlugin',
            self.plugin_mandatory_dependencies,
            intersect_levels=True)
        # search in every group for the dependencies and create a list of
        # matching dataframes
        for dependencies_df, _ in dependencies_list:

            # get a specific field (as a dataframe) from the dataframe, make
            # sure is sorted and reindexed
            uu_df = get_from_dataframe(dependencies_df, 'UU')
            vv_df = get_from_dataframe(dependencies_df, 'VV')
            # make a copy (in this case all rows) of the vv dataframe, and
            # apply the column specification changes
            uv_df = create_empty_result(
                vv_df, self.plugin_result_specifications['UV'], all_rows=True)
            # in this case, according to the plugin_result_specifications,
            # we will change the nomvar to 'UV'
            # change the etiket to 'WNDMOD'
            # and change the unit to 'knot'

            # using a loop for easier reading, number of rows in dataframe is
            # small
            for i in uv_df.index:
                # get a variable corresponding to uu array
                uu = uu_df.at[i, 'd']
                # get a variable corresponding to uu array
                vv = vv_df.at[i, 'd']
                # compute in python and store the result in our new dataframe
                uv_df.at[i, 'd'] = python_algorithm(uu, vv)
                #or
                # compute in cpp and store the result in our new dataframe
                # uv_df.at[i, 'd'] = wind_modulus_cpp(uu,vv)
                # or
                ni = uv_df.at[i, 'd'].shape[0]
                nj = uv_df.at[i, 'd'].shape[1]
                # compute in fortran and store the result in our new dataframe
                # uv_df.at[i, 'd'] = fortran_function(uu, vv, ni, nj) 

            # keep the results of this group
            df_list.append(uv_df)

        # concatenate all the dataframes together with the original metadata
        return final_results(df_list, ExamplePluginError, self.meta_df)
