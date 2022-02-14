# -*- coding: utf-8 -*-
import argparse
import logging

import pandas as pd

from ..opelementsbyvalue import OpElementsByValue
from ..plugin import Plugin
from ..utils import initializer
from ..configparsingutils import check_length_2_to_4


def add_value(a, v):
    return a + v

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
    def __init__(self, df: pd.DataFrame, value:float, nomvar_out:str=None):
        pass

    def compute(self) -> pd.DataFrame:
        logging.info('AddToElement - compute')
        return OpElementsByValue(
            df=self.df,
            operator=add_value,
            value=self.value,
            operation_name='AddToElement',
            exception_class=AddToElementError,
            nomvar_out=self.nomvar_out,
            etiket='ADDTOE').compute()

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=AddToElement.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--outputFieldName',type=str,dest='nomvar_out', help="Option to give the output field a different name from the input field name.")
        parser.add_argument('--value',type=float,required=True, help="Value to add to field.")

        parsed_arg = vars(parser.parse_args(args.split()))

        check_length_2_to_4(parsed_arg['nomvar_out'],AddToElementError)

        return parsed_arg
