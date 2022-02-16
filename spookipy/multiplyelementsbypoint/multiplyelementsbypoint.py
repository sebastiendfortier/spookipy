# -*- coding: utf-8 -*-
import argparse
import logging

import numpy as np
import pandas as pd

from ..opelementsbycolumn import OpElementsByColumn
from ..plugin import Plugin
from ..utils import initializer
from ..configparsingutils import check_length_2_to_4


class MultiplyElementsByPointError(Exception):
    pass


class MultiplyElementsByPoint(Plugin):
    """Multiplication of the values of all the fields received at each point

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param nomvar_out: nomvar for output result, defaults to 'MUEP'
    :type nomvar_out: str, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            group_by_forecast_hour=False,
            nomvar_out='MUEP'):

        pass

    def compute(self) -> pd.DataFrame:
        logging.info('MultiplyElementsByPoint - compute')
        return OpElementsByColumn(
            self.df,
            operator=np.prod,
            operation_name='MultiplyElementsByPoint',
            exception_class=MultiplyElementsByPointError,
            group_by_forecast_hour=self.group_by_forecast_hour,
            group_by_level=True,
            nomvar_out=self.nomvar_out,
            etiket='MULEPT').compute()

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=MultiplyElementsByPoint.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--groupBy',type=str,choices=['FORECAST_HOUR'],dest='group_by_forecast_hour', help="Option to group fields by attribute when performing calculation.")
        parser.add_argument('--outputFieldName',type=str,default="MUEP",dest='nomvar_out',help="Option to change the name of output field 'MUEP'.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['group_by_forecast_hour'] = (parsed_arg['group_by_forecast_hour'] == 'FORECAST_HOUR')
        check_length_2_to_4(parsed_arg['nomvar_out'],False,MultiplyElementsByPointError)

        return parsed_arg
