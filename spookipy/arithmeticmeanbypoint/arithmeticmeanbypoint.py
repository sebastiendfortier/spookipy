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
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional  
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            group_by_forecast_hour=False,
            group_by_nomvar: bool=False,
            group_by_ensemble_member: bool=False,
            nomvar_out = None,
            copy_input = False,
            reduce_df  = True):

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
            operator                 = np.mean,
            operation_name           = 'ArithmeticMeanByPoint',
            exception_class          = ArithmeticMeanByPointError,
            group_by_forecast_hour   = self.group_by_forecast_hour,
            group_by_level           = True,
            group_by_nomvar          = self.group_by_nomvar,
            group_by_ensemble_member = self.group_by_ensemble_member,
            nomvar_out               = self.nomvar_out,
            label                    = 'MEANPT',
            copy_input               = self.copy_input,
            reduce_df                = self.reduce_df).compute()

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
        # allows a list of multiple group by
        valid_group_by = ['FORECAST_HOUR','FIELD_NAME','ENSEMBLE_MEMBER']
        parser.add_argument('--groupBy',type=str,dest='group_by', help=f"Options to group fields by attribute when performing calculation. Can have more than one separated by ',' no space allowed, possible values = {valid_group_by}. Ex --groupBy FORECAST_HOUR or --groupBy FORECAST_HOUR,FIELD_NAME,ENSEMBLE_MEMBER")

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg['group_by']:
            group_by_list = parsed_arg['group_by'].split(",")
            # fixed the problem with plugin_parsing_test.py but still causes issues with the parsing in cpp
            for gb in group_by_list:
                if gb not in valid_group_by:
                    raise ArithmeticMeanByPointError(f"{gb} is not a valid option for --group_by, the valid choices are: {valid_group_by}")

            parsed_arg['group_by_forecast_hour']   = 'FORECAST_HOUR' in group_by_list
            parsed_arg['group_by_nomvar']          = 'FIELD_NAME' in group_by_list
            parsed_arg['group_by_ensemble_member'] = 'ENSEMBLE_MEMBER' in group_by_list

        if parsed_arg['nomvar_out']:
            validate_nomvar(parsed_arg['nomvar_out'], "ArithmeticMeanByPoint", ArithmeticMeanByPointError)

        return parsed_arg
