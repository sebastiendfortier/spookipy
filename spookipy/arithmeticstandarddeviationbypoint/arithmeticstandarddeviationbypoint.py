# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd
import dask.array as da

from spookipy.configparsingutils.configparsingutils import apply_lambda_to_list

from ..plugin import Plugin, PluginParser
from ..science import hmx_from_svp
from ..utils import (create_empty_result, existing_results, 
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer, find_common_levels)


class ArithmeticStandardDeviationByPointError(Exception):
    pass


class ArithmeticStandardDeviationByPoint(Plugin):
    """ArithmeticStandardDeviationByPoint calculation. 

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param deltaDegreesOfFreedom: 1 (echantillon, default) or 0 (population)
    :type deltaDegreesOfFreedom: list[float]
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """

    @initializer
    def __init__(
            self, 
            df: pd.DataFrame,
            delta_degrees_of_freedom: int = 1,
            ignore_mask = False,
            copy_input  = False,
            reduce_df   = True,
            ):
        
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
        # group by grid, dateo-v
        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=['etiket','ip_info','flags'])

        self.groups = self.no_meta_df.groupby(
            ['grid', 'datev', 'dateo', 'nomvar'])

    def compute(self) -> pd.DataFrame:

        df_list = []
        for _, df_group in self.groups:
            # create empty container here?
            common_level_df = find_common_levels(df_group,list_nomvar=df_group.ensemble_member.unique(),column_to_match='ensemble_member')
            level_groups = common_level_df.groupby('level')# ensemble_groups = self.no_meta_df.groupby(['ensemble_member'])
            for l,level_df in level_groups:
                data = level_df['d']
                all_ensemble_data = np.stack(data, axis=0)
                if type(all_ensemble_data) == da.core.Array:
                    all_ensemble_data = all_ensemble_data.compute()
                all_ensemble_data_result = np.std(all_ensemble_data, ddof=self.delta_degrees_of_freedom, axis=0)


                percentile_res_df = create_empty_result(
                    level_df,
                    {"label": "SSTD__", "ensemble_member":"ALL",
                        "ensemble_extra_info": True, # add ! to typvar
                        "d": [all_ensemble_data_result],
                        "unit": "scalar"
                    })
                # percentile_res_df['d'] = all_ensemble_data_result
                df_list.append(percentile_res_df)
                
        
        r = self.final_results(df_list, ArithmeticStandardDeviationByPointError,
                                      copy_input       = self.copy_input,
                                      reduce_df        = self.reduce_df)

        return r


    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=ArithmeticStandardDeviationByPoint.__name__, parents=[Plugin.base_parser],add_help=False)
        # should we add the option to chose what to group by??? like the others
        # # add option to group on member and allow a list of multiple group by
        # parser.add_argument('--groupBy',type=str,choices=['FORECAST_HOUR','FIELD_NAME'],dest='group_by', help="Option to group fields by attribute when performing calculation.")
        parser.add_argument('--deltaDegreesOfFreedom', choices=[0,1], type=int,help='Par défaut 1 (pour écart-type échantillion). Pour calculer l\'écart-type de la population, il faut ajuster cette variable à 0. Une seule valeur entière 0 ou 1.')
        parser.add_argument('--ignore_mask', action='store_true', default=False, help="Par défaut , on vérifie s'il y a un masque à tenir compte dans les calcul. Cette option ignore les masques.")
        
        parsed_arg = vars(parser.parse_args(args.split()))

        return parsed_arg

