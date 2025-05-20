# -*- coding: utf-8 -*-
import logging

import pandas as pd

from ..opelementsbyvalue import OpElementsByValue
from ..plugin import Plugin, PluginParser
from ..utils import initializer, validate_nomvar


def power_value_by(a, v):
    return v**a


class PowerValueByElementError(Exception):
    pass


class PowerValueByElement(Plugin):
    """For each element, powers a given value by that element.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param value: value to use
    :type value: float
    :param nomvar_out: nomvar for output result, defaults to None
    :type nomvar_out: str, optional
    """

    @initializer
    def __init__(self, df: pd.DataFrame, value, nomvar_out=None):
        self.OpElementsByValue = OpElementsByValue(
            self.df,
            value=self.value,
            operation_name="PowerValueByElement",
            nomvar_out=self.nomvar_out,
            operator=power_value_by,
            exception_class=PowerValueByElementError,
        )

    def compute(self) -> pd.DataFrame:
        logging.info("PowerValueByElement - compute")
        return self.OpElementsByValue.compute()

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=PowerValueByElement.__name__, parents=[Plugin.base_parser], add_help=False)
        parser.add_argument("--value", type=float, required=True, help="Power this value by each element.")
        parser.add_argument(
            "--outputFieldName",
            type=str,
            dest="nomvar_out",
            help="Option to give the output field a different name from the input field name.",
        )

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg["nomvar_out"] is not None:
            validate_nomvar(parsed_arg["nomvar_out"], "PowerValueByElement", PowerValueByElementError)

        return parsed_arg
