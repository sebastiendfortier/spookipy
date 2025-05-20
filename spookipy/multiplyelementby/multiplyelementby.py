# -*- coding: utf-8 -*-
import logging

import pandas as pd
import numpy as np

from ..opelementsbyvalue import OpElementsByValue
from ..plugin import Plugin, PluginParser
from ..utils import initializer, validate_nomvar


class MultiplyElementByError(Exception):
    pass


class MultiplyElementBy(Plugin):
    """Multiplies each element of a field by a given value

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
            operation_name="MultiplyElementBy",
            nomvar_out=self.nomvar_out,
            operator=np.multiply,
            exception_class=MultiplyElementByError,
            label="MULEBY",
        )

    def compute(self) -> pd.DataFrame:
        logging.info("MultiplyElementBy - compute")
        return self.OpElementsByValue.compute()

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=MultiplyElementBy.__name__, parents=[Plugin.base_parser], add_help=False)
        parser.add_argument("--value", type=float, required=True, help="Value to multiply to field.")
        parser.add_argument(
            "--outputFieldName",
            type=str,
            dest="nomvar_out",
            help="Option to give the output field a different name from the input field name.",
        )

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg["nomvar_out"] is not None:
            validate_nomvar(parsed_arg["nomvar_out"], "MultiplyElementBy", MultiplyElementByError)

        return parsed_arg
