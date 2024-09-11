# -*- coding: utf-8 -*-
import logging

import dask.array as da
import fstpy
import numpy as np
import pandas as pd
import warnings
from ..plugin import Plugin, PluginParser
from ..utils import create_empty_result, initializer, validate_nomvar
from ..configparsingutils import preprocess_negative_args


def set_value(a, v):
    a[:] = v
    return a


def set_series_value(a: pd.Series, v):
    return a.apply(set_value, args=(v,))


class SetConstantValueError(Exception):
    pass


class SetConstantValue(Plugin):
    """Copies the input field and replace all its values by a given constant

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param value: replacement value used to replace contents of the input field, defaults to 0 (min index)
    :type value: float, optional
    :param nomvar_out: nomvar of the results field, defaults to None
    :type nomvar_out: str, optional
    :param min_index: will fill the field with the min index value, defaults to False
    :type min_index: bool, optional
    :param max_index: will fill the field with the max index value, defaults to False
    :type max_index: bool, optional
    :param nb_levels: will fill the field with the number of levels value of the provided field, defaults to False
    :type nb_levels: bool, optional
    :param bi_dimensionnal: forces 2D field output even if the input is a 3D field, defaults to False
    :type bi_dimensionnal: bool, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            value:float=0.,
            nomvar_out=None,
            min_index=False,
            max_index=False,
            nb_levels=False,
            bi_dimensionnal=False,
            reduce_df = False):

        self.plugin_result_specifications = {
            'ALL': {'label': 'SETVAL', 'unit': 'scalar'}
        }     
        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
    
        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        self.groups = self.no_meta_df.groupby(by=['grid', 'nomvar', 'datev', 'dateo'])

        l = [self.min_index, self.max_index, self.nb_levels]

        lcount = l.count(True)

        if lcount > 1:
            raise SetConstantValueError(
                'Too many options selected, you can only choose one option at a time in %s' % [
                    'min_index',
                    'max_index',
                    'nb_levels'])
        if self.min_index:
            self.value = 0

    def compute(self) -> pd.DataFrame:
        logging.info('SetConstantValue - compute')
        df_list = []
        for _, df in self.groups:
            if self.max_index:
                self.value = len(df.index) - 1
            if self.nb_levels:
                self.value = len(df.index)

            res_df = create_empty_result(
                df, self.plugin_result_specifications['ALL'], all_rows=True)

            if not (self.nomvar_out is None):
                res_df['nomvar'] = self.nomvar_out

            for i in res_df.index:
                res_df.at[i, 'd'] = da.full_like(
                    res_df.at[i, 'd'], self.value, order='F', dtype=np.float32)

            if self.bi_dimensionnal:
                res_df.drop(res_df.index[1:], inplace=True)
                # Suppression d'un future warning de pandas; dans notre cas, on veut conserver le meme comportement
                # meme avec le nouveau comportement a venir. On encapsule la suppression du warning pour ce cas seulement.
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore', category=FutureWarning)
                    res_df.loc[:, 'ip1']      = 0
                    res_df.loc[:, 'level']    = 0
                    res_df.loc[:, 'ip1_kind'] = 3   # Arbitrary code
            df_list.append(res_df)

        return self.final_results(df_list, 
                                  SetConstantValueError,                                  
                                  copy_input = False,
                                  reduce_df = self.reduce_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=SetConstantValue.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--value',type=str,required=True, help="Replacement constant value.")
        parser.add_argument('--outputFieldName',type=str,dest='nomvar_out',help="Option to give the output field a different name from the input field name.")
        parser.add_argument('--bidimensional',action='store_true',dest='bi_dimensionnal',help="2D field output even if the input is a 3D field")

        parsed_arg = vars(parser.parse_args(preprocess_negative_args(args.split(),['value'])))

        if parsed_arg['value'] in ["MAXINDEX","MININDEX","NBLEVELS"]:
            if parsed_arg['value'] == "MAXINDEX":
                parsed_arg['max_index'] = True
            elif parsed_arg['value'] == "MININDEX":
                parsed_arg['min_index'] = True
            elif parsed_arg['value'] == "NBLEVELS":
                parsed_arg['nb_levels'] = True
        else:
            parsed_arg['value'] = float(parsed_arg['value'])

        if parsed_arg['nomvar_out'] is not None:
            validate_nomvar(parsed_arg['nomvar_out'],"SetConstantValue",SetConstantValueError)

        return parsed_arg

