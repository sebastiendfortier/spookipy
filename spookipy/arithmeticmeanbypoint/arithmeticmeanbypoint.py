# -*- coding: utf-8 -*-
import logging

import numpy as np
import pandas as pd

from ..opelementsbycolumn import OpElementsByColumn
from ..plugin import Plugin, PluginParser
from ..utils import initializer, validate_nomvar


class ArithmeticMeanByPointError(Exception):
    pass


class ArithmeticMeanByPoint(Plugin):
    """Arithmetic mean for each point of all the fields received

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param group_by_nomvar: group fields by field name, defaults to False
    :type group_by_nomvar: bool, optional       
    :param nomvar_out: nomvar for output result, defaults to 'MEAN'
    :type nomvar_out: str, optional
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional 
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            group_by_forecast_hour=False,
            group_by_nomvar: bool=False,
            nomvar_out=None,
            copy_input=False):

        self.validate_params()

    def validate_params(self):
        if self.nomvar_out:
            if self.group_by_nomvar:
                raise ArithmeticMeanByPoint(' Cannot use nomvar_out option with group_by_nomvar \n')
        else:
            self.nomvar_out = 'MEAN'


    def compute(self) -> pd.DataFrame:
        logging.info('ArithmeticMeanByPoint - compute')
        return OpElementsByColumn(
            self.df,
            operator=np.mean,
            operation_name='ArithmeticMeanByPoint',
            exception_class=ArithmeticMeanByPointError,
            group_by_forecast_hour=self.group_by_forecast_hour,
            group_by_level=True,
            group_by_nomvar=self.group_by_nomvar,
            nomvar_out=self.nomvar_out,
            etiket='MEANPT',
            copy_input=self.copy_input).compute()

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=ArithmeticMeanByPoint.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--outputFieldName',type=str, dest='nomvar_out', help="Option to change the name of output field 'MEAN'.")
        parser.add_argument('--groupBy',type=str,choices=['FORECAST_HOUR','FIELD_NAME'],dest='group_by', help="Option to group fields by attribute when performing calculation.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['group_by_forecast_hour'] = (parsed_arg['group_by'] == 'FORECAST_HOUR')
        parsed_arg['group_by_nomvar']        = (parsed_arg['group_by'] == 'FIELD_NAME')
        if parsed_arg['nomvar_out']:
            validate_nomvar(parsed_arg['nomvar_out'], "ArithmeticMeanByPoint", ArithmeticMeanByPointError)

        return parsed_arg
