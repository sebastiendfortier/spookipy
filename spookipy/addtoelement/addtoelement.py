# -*- coding: utf-8 -*-
import logging

import pandas as pd
import numpy as np

from ..opelementsbyvalue import OpElementsByValue
from ..plugin import Plugin, PluginParser
from ..utils import initializer, validate_nomvar


class AddToElementError(Exception):
    pass


class AddToElement(Plugin):
    """Add a given number to each element of a field

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param value: value to add to field
    :type value: float
    :param nomvar_out: nomvar for output result, defaults to None
    :type nomvar_out: str, optional
    """

    @initializer
    def __init__(self, df: pd.DataFrame, value: float, nomvar_out: str = None):
        pass

    def compute(self) -> pd.DataFrame:
        logging.info("AddToElement - compute")
        return OpElementsByValue(
            df=self.df,
            operator=np.add,
            value=self.value,
            operation_name="AddToElement",
            exception_class=AddToElementError,
            nomvar_out=self.nomvar_out,
            label="ADDTOE",
        ).compute()

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=AddToElement.__name__, parents=[Plugin.base_parser], add_help=False)
        parser.add_argument(
            "--outputFieldName",
            type=str,
            dest="nomvar_out",
            help="Option to give the output field a different name from the input field name.",
        )
        parser.add_argument("--value", type=float, required=True, help="Value to add to field.")

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg["nomvar_out"] is not None:
            validate_nomvar(parsed_arg["nomvar_out"], "AddToElement", AddToElementError)

        return parsed_arg
