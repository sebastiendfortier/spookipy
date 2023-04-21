# -*- coding: utf-8 -*-
import argparse
import logging
import warnings

import fstpy
import numpy as np
import pandas as pd
import rpnpy.librmn.all as rmn

from ..plugin import Plugin, PluginParser
from ..utils import (create_empty_result, dataframe_arrays_to_dask,
                     get_dependencies, get_from_dataframe,initializer, reshape_arrays,
                     explicit_params_checker, DependencyError)

class HumidityRelativeWeightedMeanError(Exception):
    pass


def hum_relative_weighted_mean(hu_val1, hu_val2, hu_val3, hus_val1, hus_val2, hus_val3):
    return (hu_val1 + 2*hu_val2 + hu_val3) /  (hus_val1 + 2*hus_val2 + hus_val3)

class HumidityRelativeWeightedMean(Plugin):
    """Calculates the weighted mean of relative humidity in the lower troposphere and separately in the middle troposphere.

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    :type capped_value: float, optional
    :param capped_value: Highest value that the HR field can have
    :param dependency_check: Indicates the plugin is being called from another one who checks dependencies , defaults to False
    :type dependency_check: bool, optional
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional  
    """

    @explicit_params_checker
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            capped_value: float = None,
            dependency_check=False,
            copy_input=False):

        self.plugin_mandatory_dependencies = [
            {
                'TT1' : {'nomvar': 'TT', 'unit': 'celsius','level': 1000, 'ip1_pkind': 'mb'},
                'TT2' : {'nomvar': 'TT', 'unit': 'celsius','level': 925,  'ip1_pkind': 'mb'},
                'TT3' : {'nomvar': 'TT', 'unit': 'celsius','level': 850,  'ip1_pkind': 'mb'},
                'TT4' : {'nomvar': 'TT', 'unit': 'celsius','level': 700,  'ip1_pkind': 'mb'},
                'TT5' : {'nomvar': 'TT', 'unit': 'celsius','level': 500,  'ip1_pkind': 'mb'},
                'HU1' : {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram','level': 1000, 'ip1_pkind': 'mb','select_only': True },
                'HU2' : {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram','level': 925,  'ip1_pkind': 'mb','select_only': True },
                'HU3' : {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram','level': 850,  'ip1_pkind': 'mb','select_only': True },
                'HU4' : {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram','level': 700,  'ip1_pkind': 'mb','select_only': True },             
                'HU5' : {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram','level': 500,  'ip1_pkind': 'mb','select_only': True }
            }
        ]

        self.plugin_result_specifications = \
            {
                'HR'  : {'label': 'HRWAVG','unit': 'percent'}
            }

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)
        self.validate_params_and_input()

    def validate_params_and_input(self):

        if self.capped_value is not None:
            if (self.capped_value <= 0):
                raise HumidityRelativeWeightedMeanError(
                        f'The capped_value is negative =  {self.capped_value} !') 

        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=['forecast_hour', 'ip_info'])

        keep = self.no_meta_df.loc[self.no_meta_df.nomvar.isin(["TT","HU"])].reset_index(drop=True) 

        self.nomvar_groups = keep.groupby(by=['grid', 'datev','ip1_kind'])


    def compute(self) -> pd.DataFrame:
        logging.info('HumidityRelativeWeightedMean - compute')

        df_list=[]
        try:
           dependencies_list = get_dependencies(
                    self.nomvar_groups,
                    self.meta_df,
                    'HumidityRelativeWeightedMean',
                    self.plugin_mandatory_dependencies,
                    intersect_levels=False)

        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f'{HumidityRelativeWeightedMean} - No matching dependencies found')
        else:
             for dependencies_df, option in dependencies_list:

                tt_df = get_from_dataframe(dependencies_df, 'TT')
                hu_df = get_from_dataframe(dependencies_df, 'HU')

                tt1000_df = tt_df.loc[(tt_df.level == 1000)].reset_index(drop=True)
                tt925_df  = tt_df.loc[(tt_df.level == 925)].reset_index(drop=True)
                tt850_df  = tt_df.loc[(tt_df.level == 850)].reset_index(drop=True)
                tt700_df  = tt_df.loc[(tt_df.level == 700)].reset_index(drop=True)
                tt500_df  = tt_df.loc[(tt_df.level == 500)].reset_index(drop=True)

                hu1000_df = hu_df.loc[(hu_df.level == 1000)].reset_index(drop=True)
                hu925_df  = hu_df.loc[(hu_df.level == 925)].reset_index(drop=True)
                hu850_df  = hu_df.loc[(hu_df.level == 850)].reset_index(drop=True)
                hu700_df  = hu_df.loc[(hu_df.level == 700)].reset_index(drop=True)
                hu500_df  = hu_df.loc[(hu_df.level == 500)].reset_index(drop=True)

                tt_reduit_df = pd.concat(
                [   tt1000_df,tt925_df,
                    tt850_df, tt700_df, 
                    tt500_df],ignore_index=True)

                # Pour calculer HUs (saturation specific humidity),  on remplace les valeurs de TD 
                # par les valeurs de TT lors de l'appel a HumiditySpecific.
                td_df = tt_reduit_df.copy(deep=True)
                td_df.loc[:,'nomvar'] = "TD"

                hus_df = self.compute_hus(tt_reduit_df, td_df)

                hus1000_df = hus_df.loc[(hus_df.level == 1000)].reset_index(drop=True)
                hus925_df  = hus_df.loc[(hus_df.level == 925)].reset_index(drop=True)
                hus850_df  = hus_df.loc[(hus_df.level == 850)].reset_index(drop=True)
                hus700_df  = hus_df.loc[(hus_df.level == 700)].reset_index(drop=True)
                hus500_df  = hus_df.loc[(hus_df.level == 500)].reset_index(drop=True)

                hrl_df = create_result_container(tt1000_df,'HR', 1000, 850, self.plugin_result_specifications)
                hrm_df = create_result_container(tt1000_df,'HR', 850,  500, self.plugin_result_specifications)

                hrl_df.at[0,'d'] = hum_relative_weighted_mean(
                                                hu1000_df.at [0,'d'],
                                                hu925_df.at  [0,'d'],
                                                hu850_df.at  [0,'d'],
                                                hus1000_df.at[0,'d'],
                                                hus925_df.at [0,'d'],
                                                hus850_df.at [0,'d'])

                hrm_df.at[0,'d'] = hum_relative_weighted_mean(
                                                hu850_df.at  [0,'d'],
                                                hu700_df.at  [0,'d'],
                                                hu500_df.at  [0,'d'],
                                                hus850_df.at [0,'d'],
                                                hus700_df.at [0,'d'],
                                                hus500_df.at [0,'d'])

                if not(self.capped_value is None):
                    hrl_df.at[0,'d'] = np.where(hrl_df.at[0,'d'] > self.capped_value , self.capped_value, hrl_df.at[0,'d'])
                    hrl_df = reshape_arrays(hrl_df)
                    hrl_df = dataframe_arrays_to_dask(hrl_df)

                    hrm_df.at[0,'d'] = np.where(hrm_df.at[0,'d'] > self.capped_value , self.capped_value, hrm_df.at[0,'d'])
                    hrm_df = reshape_arrays(hrm_df)
                    hrm_df = dataframe_arrays_to_dask(hrm_df)

                df_list.append(hrl_df)
                df_list.append(hrm_df)
        finally:     
            return self.final_results(df_list, HumidityRelativeWeightedMeanError,
                                      dependency_check = self.dependency_check, 
                                      copy_input = self.copy_input)

    def compute_hus(self, tt_df, td_df):
        from ..humidityspecific.humidityspecific import HumiditySpecific
        hus_df = HumiditySpecific(
            pd.concat(
                [   tt_df,
                    td_df],
            ignore_index=True), 
            dependency_check=self.dependency_check).compute()
        hus_df = get_from_dataframe(hus_df, 'HU')
        hus_df.loc[:,'nomvar'] = "HUS"

        return hus_df


    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=HumidityRelativeWeightedMean.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--capped',type=float, help="The highest value that the HR field can have")

        parsed_arg = vars(parser.parse_args(args.split()))
        return parsed_arg

def create_result_container(df, nomvar, b_inf, b_sup, result_specification):
  
    ip1 = b_inf
    ip3 = b_sup
    kind = int(df.iloc[0].ip1_kind)

    inter = fstpy.Interval('ip1', ip1, ip3, kind)

    result_specification["HR"]["nomvar"]   = nomvar
    result_specification["HR"]["interval"] = inter
    res_df = create_empty_result(df, result_specification['HR'])

    return res_df

