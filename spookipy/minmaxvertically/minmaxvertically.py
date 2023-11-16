# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..minmaxlevelindex import MinMaxLevelIndex
from ..plugin import Plugin, PluginParser
from ..utils import (get_from_dataframe, initializer, 
                    reshape_arrays, validate_nomvar)
from typing import Final

LABEL   : Final[str] = 'MNMXVY'

class MinMaxVerticallyError(Exception):
    pass

class MinMaxVertically(Plugin):
    """Finds the maximum and/or minimum value in the column or part of it.

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    :param nomvar: Target nomvar for the computation
    :type nomvar: str
    :param min: get the  minimum, defaults to False
    :type min: bool, optional
    :param max: get the maximum, defaults to False
    :type max: bool, optional
    :param bounded: limit search between KBAS and KTOP, defaults to False
    :type bounded: bool, optional
    :param nomvar_min_val: nomvar of the min result value, defaults to 'MIN'
    :type nomvar_min_val: str, optional
    :param nomvar_max_val: nomvar of the max result value, defaults to 'MAX'
    :type nomvar_max_val: str, optional
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional 
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            nomvar          = str,
            min             = False,
            max             = False,
            bounded         = False,
            ascending       = True,
            nomvar_min: str = None,
            nomvar_max: str = None,
            copy_input      = False,
            reduce_df       = True
            ):
        super().__init__(self.df)
        self.validate_params_and_input()

    def validate_params_and_input(self):   

        if not (self.nomvar_min is None):
            validate_nomvar(
                self.nomvar_min,
                'MinMaxVertically',
                MinMaxVerticallyError)

        if not (self.nomvar_max is None):
            validate_nomvar(
                self.nomvar_max,
                'MinMaxVertically',
                MinMaxVerticallyError)

        if (not self.min) and (not self.max):
            self.min = True
            self.max = True

        if self.bounded:
            if (self.no_meta_df.loc[self.no_meta_df.nomvar == "KBAS"]).empty or \
               (self.no_meta_df.loc[self.no_meta_df.nomvar == "KTOP"]).empty:
                raise MinMaxVerticallyError('Missing fields KBAS and/or KTOP with BOUNDED option!')

    def compute(self) -> pd.DataFrame:
        logging.info('MinMaxVertically - compute')

        df_list=[]

        if not (self.nomvar_min is None):
            min_out = self.nomvar_min
        else:
            min_out = "MIN"

        if not (self.nomvar_max is None):
            max_out = self.nomvar_max
        else:
            max_out = "MAX"

        df=MinMaxLevelIndex(self.df,
                            nomvar          = self.nomvar, 
                            min             = self.min, 
                            max             = self.max,
                            bounded         = self.bounded,
                            ascending       = self.ascending,
                            nomvar_min_idx  = "_MIN",
                            nomvar_min_val  = min_out,
                            nomvar_max_idx  = "_MAX",
                            nomvar_max_val  = max_out,
                            value_to_return = True,
                            copy_input      = self.copy_input,
                            reduce_df       = False).compute()

        if self.min:
            min_df = get_from_dataframe(df, min_out)
            min_df['label'] = LABEL
            min_df = reshape_arrays(min_df)
            df_list.append(min_df)
            
        if self.max:
            max_df = get_from_dataframe(df, max_out)
            max_df['label'] = LABEL
            max_df = reshape_arrays(max_df)
            df_list.append(max_df)

        return self.final_results(df_list, MinMaxVerticallyError,
                                  copy_input = self.copy_input,
                                  reduce_df  = self.reduce_df)



    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """

        parser = PluginParser(prog=MinMaxVertically.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--minMax',type=str,choices=["MIN","MAX","BOTH"], help="Finds either the maximum or minimum value index or both")
        parser.add_argument('--bounded',dest='bounded',action='store_true',default=False, help="Searches in part of the column (requires fields KBAS and KTOP as inputs) Default: searches the whole column")
        parser.add_argument('--fieldName',type=str,dest='nomvar', help="Name of the field.")
        parser.add_argument('--outputFieldName1',type=str,default="MIN",dest='nomvar_min',help="Option to change the name of output field MIN")
        parser.add_argument('--outputFieldName2',type=str,default="MAX",dest='nomvar_max',help="Option to change the name of output field MAX")

        parsed_arg = vars(parser.parse_args(args.split()))
        if parsed_arg['nomvar'] is not None:
            validate_nomvar(parsed_arg['nomvar'],"MinMaxVertically",MinMaxVerticallyError)
            
        validate_nomvar(parsed_arg['nomvar_min'],"MinMaxVertically",MinMaxVerticallyError)
        validate_nomvar(parsed_arg['nomvar_max'],"MinMaxVertically",MinMaxVerticallyError)

        if parsed_arg['minMax'] == "MIN":
            parsed_arg['min'] = True
        elif parsed_arg['minMax'] == "MAX":
            parsed_arg['max'] = True
        else:
            parsed_arg['min'] = True
            parsed_arg['max'] = True

        return parsed_arg

