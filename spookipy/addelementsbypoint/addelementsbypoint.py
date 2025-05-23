# -*- coding: utf-8 -*-
import logging

import numpy as np
import pandas as pd

from ..opelementsbycolumn import OpElementsByColumn
from ..plugin import Plugin, PluginParser
from ..utils import initializer, validate_nomvar


class AddElementsByPointError(Exception):
    pass


class AddElementsByPoint(Plugin):
    """Add, for each point, the values of all the fields received

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param group_by_nomvar: group fields by field name, defaults to False
    :type group_by_nomvar: bool, optional
    :param nomvar_out: nomvar for output result, defaults to 'ADEP'
    :type nomvar_out: str, optional
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """

    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        group_by_forecast_hour: bool = False,
        group_by_nomvar: bool = False,
        nomvar_out=None,
        copy_input=False,
        reduce_df=True,
    ):
        pass  # The decorator handles everything!

    def compute(self) -> pd.DataFrame:
        logging.info("AddElementsByPoint - compute")
        return OpElementsByColumn(
            self.df,
            operator=np.sum,
            operation_name="AddElementsByPoint",
            exception_class=AddElementsByPointError,
            group_by_forecast_hour=self.group_by_forecast_hour,
            group_by_level=True,
            group_by_nomvar=self.group_by_nomvar,
            nomvar_out=self.nomvar_out,
            plugin_nomvar_out="ADEP",
            label="ADDEPT",
            copy_input=self.copy_input,
            reduce_df=self.reduce_df,
        ).compute()

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=AddElementsByPoint.__name__, parents=[Plugin.base_parser], add_help=False)
        parser.add_argument(
            "--outputFieldName", type=str, dest="nomvar_out", help="Option to change the name of output field 'ADEP'."
        )
        parser.add_argument(
            "--groupBy",
            type=str,
            choices=["FORECAST_HOUR", "FIELD_NAME"],
            dest="group_by",
            help="Option to group fields by attribute when performing calculation.",
        )

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg["group_by_forecast_hour"] = parsed_arg["group_by"] == "FORECAST_HOUR"
        parsed_arg["group_by_nomvar"] = parsed_arg["group_by"] == "FIELD_NAME"
        if parsed_arg["nomvar_out"]:
            validate_nomvar(parsed_arg["nomvar_out"], "AddElementsByPoint", AddElementsByPointError)

        return parsed_arg
