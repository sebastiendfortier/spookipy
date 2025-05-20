# -*- coding: utf-8 -*-                                 # always use utf8 encoding when editing files

# use logging for console output, logging.debug, logging.info,
# logging.warning, logging.critical
import logging

import fstpy
import numpy as np
import pandas as pd


# ex.: logging.info('ExamplePlugin - compute')
# interface class for all plugins
from ..plugin import Plugin, PluginParser
from ..utils import (
    create_empty_result,
    existing_results,  # plugin tools
    get_dependencies,
    get_existing_result,
    get_from_dataframe,
    initializer,
)
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
    return (a**2 + b**2) ** 0.5


# define an exception to use in this plugin
class ExamplePluginError(Exception):
    pass


class ExamplePlugin(Plugin):
    @initializer  # this decorator can be used when you have multiple parameters, it will automatically initialize self. class variable
    # in this case you'll have self.df, self.argument, self.copy_input and self.reduce_df
    def __init__(
        self,
        df: pd.DataFrame,
        argument: str = "something",  # example of a class argument
        flag: bool = False,  # example of a bool class argument
        copy_input=False,  # all plugin should have that, if true, the input dataframe should be added to the result dataframe
        reduce_df=True,
    ):  # all plugin should have that, when true, the output dataframe should only comtain the essential columns,
        self.plugin_mandatory_dependencies = [
            {  # define one or more filed dependencies specifications
                # in this case we want uu and vv in knots from the dataframe
                "UU": {"nomvar": "UU", "unit": "knot"},
                "VV": {"nomvar": "VV", "unit": "knot"},
            }
        ]
        # if the field dependency is computable, the system will try to run the plugin
        # as an example PX can be computed, 'PX':{'nomvar':'PX','unit':'hPa'}
        # if the field is computable you can choose to select it instead of trying to compute
        # with the special key value pair 'select_only':True
        # 'PX':{'nomvar':'PX','unit':'hPa', 'select_only':True}
        # also any column of the dataframe can be included in the specification
        # as an example, if you wanted to select the surface level only, you could add 'surface':True
        # 'UU':{'nomvar':'UU','unit':'knot', 'surface':True}
        # units are stored in fstpy.UNITS, >>> fstpy.UNITS to print the contents
        # see get_plugin_dependencies funtion documentation for computable
        # dependencies

        self.plugin_result_specifications = {  # define the resulting fields specifications
            # in this case, we want the comvar to be UV, the etiket to be
            # WNDMOD
            "UV": {"nomvar": "UV", "label": "WNDMOD", "unit": "knot"}
        }  # and since the result is in knots, we want to set the unit to knots

        # since we used the @initializer decorator, we don't need to set
        # the class variable manually, like:
        # self.df = df

        # delete all the useless metadata from self.df
        # should always be done before "super().__init__(self.df)"
        # to make sure that self.meta_df contains only useful fields
        self.df = fstpy.metadata_cleanup(self.df)

        # call the Plugin class __init__
        # it will check that df is not empty and will create self.meta_df and self.no_meta_df
        # (a df containing only metadata and a df containing everything else)
        super().__init__(self.df)

        # here we validate our parameters ans other things before the
        # calculations
        self.validate_params()

        # here we prepare the groups on which the algorithm is applied
        self.prepare_groups()

    def prepare_groups(self):
        # add some columns if they are not already in the dataframe
        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=["unit", "ip_info"])
        # this helps with sorting and grouping the data
        # ip_info tag includes the decoding (gets the kind and value) of ip1, ip2 ip3
        # the vertical coordinate type, the surface flag, the vertical coordinate type
        # and the ascending value for the type of level

        # check if result already exists
        # this function will look in the dataframe to see if the result isn't
        # already present
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(["grid", "datev", "dateo", "vctype"])

    def validate_params(self):
        # check that our arguments are valide
        supported_argument_options = ["something", "some_option", "something_else"]
        if self.argument not in supported_argument_options:
            raise ExamplePluginError(f"argument {self.argument} not in {supported_argument_options}")

        # add some columns if they are not already in the dataframe
        self.df = fstpy.add_columns(self.df, columns=["unit", "forecast_hour", "ip_info"])
        # this helps with sorting and grouping the data
        # ip_info tag includes the decoding (gets the kind and value) of ip1, ip2 ip3
        # the vertical coordinate type, the surface flag, the vertical coordinate type
        # and the ascending value for the type of level

    def compute(self) -> pd.DataFrame:
        # return the existing results if we found them
        if not self.existing_result_df.empty:
            return existing_results("ExamplePlugin", self.existing_result_df, self.meta_df)

        logging.info("ExamplePlugin - compute")
        df_list = []

        try:
            dependencies_list = get_dependencies(
                self.groups, self.meta_df, "ExamplePlugin", self.plugin_mandatory_dependencies, intersect_levels=True
            )
            # search in every group for the dependencies and create a list of
            # matching dataframes

        except ExamplePluginError:
            raise ExamplePluginError(f"{ExamplePlugin} - No matching dependencies found")

        else:
            for dependencies_df, _ in dependencies_list:
                # get a specific field (as a dataframe) from the dataframe, make
                # sure is sorted and reindexed
                uu_df = get_from_dataframe(dependencies_df, "UU")
                vv_df = get_from_dataframe(dependencies_df, "VV")
                # make a copy (in this case all rows) of the vv dataframe, and
                # apply the column specification changes
                uv_df = create_empty_result(vv_df, self.plugin_result_specifications["UV"], all_rows=True)
                # in this case, according to the plugin_result_specifications,
                # we will change the nomvar to 'UV'
                # change the etiket to 'WNDMOD'
                # and change the unit to 'knot'

                # using a loop for easier reading, number of rows in dataframe is
                # small
                for i in uv_df.index:
                    # get a variable corresponding to uu array
                    uu = uu_df.at[i, "d"]
                    # get a variable corresponding to uu array
                    vv = vv_df.at[i, "d"]
                    # compute in python and store the result in our new dataframe
                    uv_df.at[i, "d"] = python_algorithm(uu, vv)
                    # or
                    # compute in cpp and store the result in our new dataframe
                    # uv_df.at[i, 'd'] = wind_modulus_cpp(uu,vv)
                    # or
                    ni = uv_df.at[i, "d"].shape[0]
                    nj = uv_df.at[i, "d"].shape[1]
                    # compute in fortran and store the result in our new dataframe
                    # uv_df.at[i, 'd'] = fortran_function(uu, vv, ni, nj)

                # keep the results of this group
                df_list.append(uv_df)

        # concatenate all the dataframes together with the original metadata,
        # reduce df columns and copy input if requested
        return self.final_results(df_list, ExamplePluginError)

    # This static method is used to parse the spooki syntax and
    # translate it into a dict of argument to initialize ExamplePlugin
    # ex: [ExamplePlugin --myArgument something --flag]
    # will generate: {'argument': 'something', 'flag': True}
    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=ExamplePlugin.__name__, parents=[Plugin.base_parser], add_help=False)

        # add all the argument you need here, see argparse doc for info
        parser.add_argument(
            "--myArgument",
            choices=["something", "some_option", "something_else"],
            type=str,
            dest="argument",
            help="Does something blablabla",
        )
        parser.add_argument("--flag", action="store_true", default=False, help="This flag ... blablabla")

        parsed_arg = vars(parser.parse_args(args.split()))

        # you can do extra processing
        # you can add new things in the dictionary too
        # (only the key that have a matching name with a param in
        # __init__ will be used, the others will be ignored)
        # here are some example of things you could do:
        # parsed_arg['group_by_nomvar']        = (parsed_arg['group_by'] == 'FIELD_NAME')
        # if parsed_arg['nomvar_out']:
        #     validate_nomvar(parsed_arg['nomvar_out'],"AddElementsByPoint",AddElementsByPointError)
        # if parsed_arg['xyDimensions'] is not None:
        #     parsed_arg['xyDimensions']        = parsed_arg['xyDimensions'].split(",")
        #     parsed_arg['ni']                  = int(parsed_arg['xyDimensions'][0])
        #     parsed_arg['nj']                  = int(parsed_arg['xyDimensions'][1])

        return parsed_arg
