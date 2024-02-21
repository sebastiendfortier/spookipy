# -*- coding: utf-8 -*-
import logging
from typing import Final
import fstpy
import numpy as np
import pandas as pd
from ..plugin import Plugin, PluginParser
from ..utils import create_empty_result, initializer, validate_nomvar
import rpnpy.librmn.all as rmn

LABEL: Final[str] =  'SUBEVY'

class SubtractElementsVerticallyError(Exception):
    pass


class SubtractElementsVertically(Plugin):
    """From a field value for a chosen level (either the lowest or the highest), subtract the values from all the other levels of the same field.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param nomvar_out: nomvar for output result
    :type nomvar_out: str, optional
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """
    @initializer
    def __init__(self, 
                 df: pd.DataFrame, 
                 direction: str  ='ascending', 
                 nomvar_out: str = None,
                 reduce_df       = True):
        
        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)

        self.plugin_result_specifications = {'label': LABEL}
        
        self.validate_params_and_input()

    def validate_params_and_input(self):

        if self.direction not in ['ascending', 'descending']:
            raise SubtractElementsVerticallyError("Invalid value '{self.direction}' for direction, valid values are {['ascending', 'descending']}")
        
        if (self.no_meta_df.nomvar.unique().size > 1) and (not (self.nomvar_out is None)):
            raise SubtractElementsVerticallyError('nomvar_out can only be used when only 1 field is present')

        if (self.no_meta_df.nomvar.unique().size == 1) and (not (self.nomvar_out is None)):
            validate_nomvar(self.nomvar_out, 'SubtractElementsVertically', SubtractElementsVerticallyError)

        if len(self.no_meta_df.loc[~self.no_meta_df.interval.isna()].index) > 0:
            raise SubtractElementsVerticallyError('Dataframe cannot contain rows with intervals!')
        
        self.no_meta_df = fstpy.add_columns(self.no_meta_df,'ip_info')

    def compute(self) -> pd.DataFrame:    
        logging.info('SubtractElementsVertically - compute')

        df_list=[]
        groups = self.no_meta_df.groupby(['grid','datev','dateo','nomvar','vctype'])
        for _, nomvar_df in groups:

            if self.direction == 'descending':
                nomvar_df = nomvar_df.sort_values(by='level',ascending=nomvar_df.ascending.unique()[0])
            else:
                nomvar_df = nomvar_df.sort_values(by='level',ascending=(not nomvar_df.ascending.unique()[0]))

            first_level   = nomvar_df.level.min()
            last_level    = nomvar_df.level.max()

            res_df        = create_result_container(nomvar_df, 
                                                    last_level, 
                                                    first_level,  
                                                    self.plugin_result_specifications)
            
            if  (self.no_meta_df.nomvar.unique().size == 1) and (not (self.nomvar_out is None)):
                res_df['nomvar'] = self.nomvar_out

            data  = np.stack(nomvar_df.d)
            data0 = data[-1]
            data  = -1*data
            data  = np.vstack([data0[np.newaxis],data[:-1]])
            # print(nomvar,data, data.shape)
            if data.shape[0]>1:
                res_df['d'] = [np.sum(data, axis=0)]

            df_list.append(res_df)

        return self.final_results(df_list, 
                                  SubtractElementsVerticallyError, 
                                  copy_input=False,
                                  reduce_df = self.reduce_df)
    

    
    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=SubtractElementsVertically.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--outputFieldName',type=str,dest='nomvar_out',help="Option to give the output field a different name from the input field name.")
        parser.add_argument('--direction',required=True,type=str,default="ASCENDING",choices=["ASCENDING","DESCENDING"], help="Direction of vertical iteration.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['direction'] = parsed_arg['direction'].lower()

        if parsed_arg['nomvar_out'] is not None:
            validate_nomvar(parsed_arg['nomvar_out'],"SubtractElementsVertically",SubtractElementsVerticallyError)

        return parsed_arg

def create_result_container(df, b_inf, b_sup, result_specifications):
    ip1 = b_inf
    ip3 = b_sup
    kind = int(df.iloc[0].ip1_kind)
    
    inter = fstpy.Interval('ip1', ip1, ip3, kind)

    result_specifications["interval"] = inter

    res_df = create_empty_result(df, result_specifications)

    return res_df
