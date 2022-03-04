# -*- coding: utf-8 -*-
import argparse
import logging

import numpy as np
import pandas as pd

from ..opelementsbycolumn import OpElementsByColumn
from ..plugin import Plugin
from ..utils import initializer, validate_nomvar

class AddElementsByPointError(Exception):
    pass


class AddElementsByPoint(Plugin):
    """Add, for each point, the values of all the fields received

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param nomvar_out: nomvar for output result, defaults to 'ADEP'
    :type nomvar_out: str, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            group_by_forecast_hour: bool=False,
            nomvar_out: str='ADEP'):

        pass

    def compute(self) -> pd.DataFrame:
        logging.info('AddElementsByPoint - compute')
        return OpElementsByColumn(
            self.df,
            operator=np.sum,
            operation_name='AddElementsByPoint',
            exception_class=AddElementsByPointError,
            group_by_forecast_hour=self.group_by_forecast_hour,
            group_by_level=True,
            nomvar_out=self.nomvar_out,
            etiket='ADDEPT').compute()


    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=AddElementsByPoint.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--outputFieldName',type=str,default="ADEP",dest='nomvar_out', help="Option to change the name of output field 'ADEP'.")
        parser.add_argument('--groupBy',type=str,choices=['FORECAST_HOUR'],dest='group_by_forecast_hour', help="Option to group fields by attribute when performing calculation.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['group_by_forecast_hour'] = (parsed_arg['group_by_forecast_hour'] == 'FORECAST_HOUR')

        validate_nomvar(parsed_arg['nomvar_out'],"AddElementsByPoint",AddElementsByPointError)

        return parsed_arg

