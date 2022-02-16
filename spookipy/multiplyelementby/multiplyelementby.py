# -*- coding: utf-8 -*-
import argparse
import logging

import pandas as pd

from ..opelementsbyvalue import OpElementsByValue
from ..plugin import Plugin
from ..utils import initializer
from ..configparsingutils import check_length_2_to_4


def mult_value(a, v):
    return a * v


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
        pass

    def compute(self) -> pd.DataFrame:
        logging.info('MultiplyElementsBy - compute')
        return OpElementsByValue(self.df,
                                 value=self.value,
                                 operation_name='MultiplyElementsBy',
                                 nomvar_out=self.nomvar_out,
                                 operator=mult_value,
                                 exception_class=MultiplyElementByError,
                                 etiket='MULEBY').compute()

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=MultiplyElementBy.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--value',type=float,required=True, help="Value to multiply to field.")
        parser.add_argument('--outputFieldName',type=str,dest='nomvar_out',help="Option to give the output field a different name from the input field name.")

        parsed_arg = vars(parser.parse_args(args.split()))

        check_length_2_to_4(parsed_arg['nomvar_out'],True,MultiplyElementByError)

        return parsed_arg
