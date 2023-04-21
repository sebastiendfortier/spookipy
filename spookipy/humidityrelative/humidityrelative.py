# -*- coding: utf-8 -*-
import argparse
import logging

import fstpy
import numpy as np
import pandas as pd

from ..humidityutils import (get_temp_phase_switch, validate_humidity_parameters, 
                            mandatory_temp_phase_switch_when_using_ice_water_phase_both)
from ..plugin import Plugin, PluginParser
from ..science import hr_from_svp_vppr, rpn_hr_from_es, rpn_hr_from_hu
from ..utils import (create_empty_result, existing_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer, explicit_params_checker, DependencyError)
from ..configparsingutils import check_and_format_humidity_parsed_arguments


class HumidityRelativeError(Exception):
    pass


class HumidityRelative(Plugin):
    """Calculation of the relative humidity, the ratio between the partial pressure of water vapour content in the air and the saturated vapour pressure at the same temperature.

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    :param ice_water_phase: Switch to determine which phase to consider: ice and water ('both'), or, water only ('water')  
    :type ice_water_phase: str
    :param temp_phase_switch: Temperature at which to change from the ice phase to the water phase, defaults to None
    :type temp_phase_switch: float, optional
    :param temp_phase_switch_unit: Temperature phase switch unit, defaults to 'celsius'
    :type temp_phase_switch_unit: str, optional
    :param rpn: Use rpn library algorithm, defaults to False
    :type rpn: bool, optional
    :param dependency_check: Indicates the plugin is being called from another one who checks dependencies , defaults to False
    :type dependency_check: bool, optional
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional 
    """
    computable_plugin = "HR"
    @explicit_params_checker
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            ice_water_phase,
            temp_phase_switch=None,
            temp_phase_switch_unit='celsius',
            rpn=False,
            dependency_check=False,
            copy_input=False):

        self.plugin_params = {
            'ice_water_phase'       : self.ice_water_phase,
            'temp_phase_switch'     : self.temp_phase_switch,
            'temp_phase_switch_unit': self.temp_phase_switch_unit,
            'rpn'                   : self.rpn}
        self.plugin_mandatory_dependencies_rpn = [
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'HU': {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'QV': {'nomvar': 'QV', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'ES': {'nomvar': 'ES', 'unit': 'kelvin', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'TD': {'nomvar': 'TD', 'unit': 'kelvin', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            }
        ]
        self.plugin_mandatory_dependencies = [
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'HU': {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'QV': {'nomvar': 'QV', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'TD': {'nomvar': 'TD', 'unit': 'celsius', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'ES': {'nomvar': 'ES', 'unit': 'celsius', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'},
            }
        ]

        self.plugin_result_specifications = {
            'HR': {
                'nomvar': 'HR',
                'label': 'HUMREL',
                'unit'  : 'scalar',
                'nbits' : 12,
                'datyp' : 1}}
        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)
        self.prepare_groups()

    def prepare_groups(self):

        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=['unit', 'forecast_hour', 'ip_info'])

        mandatory_temp_phase_switch_when_using_ice_water_phase_both(
            HumidityRelativeError,
            self.explicit_params,
            self.ice_water_phase,
            self.rpn)

        validate_humidity_parameters(
            HumidityRelativeError,
            self.ice_water_phase,
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            rpn=self.rpn)

        self.temp_phase_switch = get_temp_phase_switch(
            HumidityRelativeError,
            self.ice_water_phase == 'both',
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            self.rpn)

        # check if result already exists
        self.existing_result_df = get_existing_result(
            self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(
            ['grid', 'datev', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'HumidityRelative',
                self.existing_result_df,
                self.meta_df)

        logging.info('HumidityRelative - compute')

        df_list = []
        try:
            if self.rpn:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'HumidityRelative',
                    self.plugin_mandatory_dependencies_rpn,
                    self.plugin_params,
                    intersect_levels=True,
                    dependency_check = self.dependency_check)
            else:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'HumidityRelative',
                    self.plugin_mandatory_dependencies,
                    self.plugin_params,
                    intersect_levels=True,
                    dependency_check = self.dependency_check)
        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f'{HumidityRelative} - No matching dependencies found')
        else:
            for dependencies_df, option in dependencies_list:
                if self.rpn:
                    if option == 0:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        hu_df = get_from_dataframe(dependencies_df, 'HU')
                        hr_df = self.rpn_humidityrelative_from_tt_hu_px(dependencies_df, hu_df, option)

                    elif option == 1:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        hu_df = self.compute_hu(dependencies_df)
                        hr_df = self.rpn_humidityrelative_from_tt_hu_px(
                            dependencies_df, hu_df, option)

                    elif option == 2:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        es_df = get_from_dataframe(dependencies_df, 'ES')
                        hr_df = self.rpn_humidityrelative_from_tt_es_px(dependencies_df, es_df, option)
                    else:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        es_df = self.compute_es(dependencies_df)
                        hr_df = self.rpn_humidityrelative_from_tt_es_px(dependencies_df, es_df, option)

                else:  # not rpn
                    hr_df = self.humidityrelative_from_svp_vppr(
                        dependencies_df, option)

                df_list.append(hr_df)
        finally:
            return self.final_results(df_list, HumidityRelative, 
                                      dependency_check = self.dependency_check, 
                                      copy_input = self.copy_input)

    def rpn_humidityrelative_from_tt_hu_px(
            self, dependencies_df, hu_df, option):
        logging.info(f'HumidityRelative - rpn option {option+1}')

        ttk_df  = get_from_dataframe(dependencies_df, 'TT')
        pxpa_df = get_from_dataframe(dependencies_df, 'PX')
        hr_df   = create_empty_result(
                                        ttk_df,
                                        self.plugin_result_specifications['HR'],
                                        all_rows=True)

        for i in hr_df.index:
            ttk = ttk_df.at[i, 'd']
            pxpa = pxpa_df.at[i, 'd']
            hu = hu_df.at[i, 'd']
            hr_df.at[i, 'd'] = rpn_hr_from_hu(tt=ttk, 
                                              hu=hu, 
                                              px=pxpa,
                                              swph=self.ice_water_phase == 'both').astype(np.float32)
        return hr_df

    def compute_hu(self, dependencies_df):
        from ..humidityspecific.humidityspecific import HumiditySpecific
        hu_df = HumiditySpecific(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            rpn=True, 
            dependency_check=self.dependency_check).compute()
        hu_df = get_from_dataframe(hu_df, 'HU')
        return hu_df

    def rpn_humidityrelative_from_tt_es_px(
            self, dependencies_df, es_df, option):
        logging.info(f'HumidityRelative - rpn option {option+1}')

        ttk_df  = get_from_dataframe(dependencies_df, 'TT')
        pxpa_df = get_from_dataframe(dependencies_df, 'PX')
        hr_df   = create_empty_result(
                                        ttk_df,
                                        self.plugin_result_specifications['HR'],
                                        all_rows=True)

        for i in hr_df.index:
            ttk = ttk_df.at[i, 'd']
            pxpa = pxpa_df.at[i, 'd']
            es = es_df.at[i, 'd']
            hr_df.at[i, 'd'] = rpn_hr_from_es(tt=ttk,
                                              es=es,
                                              px=pxpa, 
                                              swph=self.ice_water_phase == 'both').astype(np.float32)
        return hr_df

    def compute_es(self, dependencies_df):
        from ..dewpointdepression.dewpointdepression import DewPointDepression

        es_df = DewPointDepression(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            rpn=True, 
            dependency_check=self.dependency_check).compute()
        es_df = get_from_dataframe(es_df, 'ES')
        return es_df

    def humidityrelative_from_svp_vppr(self, dependencies_df, option):
        from ..saturationvapourpressure.saturationvapourpressure import \
            SaturationVapourPressure
        from ..vapourpressure.vapourpressure import VapourPressure
        logging.info(f'HumidityRelative - option {option+1}')
        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])

        tt_df   = get_from_dataframe(dependencies_df, 'TT')
        hr_df   = create_empty_result(
                                        tt_df,
                                        self.plugin_result_specifications['HR'],
                                        all_rows=True)
        svp_df  = SaturationVapourPressure(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            temp_phase_switch=(
                self.temp_phase_switch if self.ice_water_phase != 'water' else None),
                dependency_check=self.dependency_check).compute()
        svp_df  = get_from_dataframe(svp_df, 'SVP')
        vppr_df = VapourPressure(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            temp_phase_switch=(
                self.temp_phase_switch if self.ice_water_phase != 'water' else None),
                dependency_check=self.dependency_check).compute()
        vppr_df  = get_from_dataframe(vppr_df, 'VPPR')
        for i in hr_df.index:
            svp  = svp_df.at[i, 'd']
            vppr = vppr_df.at[i, 'd']
            hr_df.at[i, 'd'] = hr_from_svp_vppr(svp=svp, 
                                                vppr=vppr).astype(np.float32)
        return hr_df

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=HumidityRelative.__name__, parents=[Plugin.base_parser],add_help=False)

        parser.add_argument('--iceWaterPhase',type=str,required=True,choices=["WATER","BOTH"],dest='ice_water_phase', help="Switch to determine which phase to consider: ice and water, or, water only.")
        parser.add_argument('--temperaturePhaseSwitch',type=str,help="Temperature at which to change from the ice phase to the water phase.\nMandatory if '--iceWaterPhase BOTH' is usedwithout '--RPN'. \nNot accepted if '--RPN is used'.")
        parser.add_argument('--RPN',action='store_true',default=False,dest="rpn", help="Use of the RPN TdPack functions")

        parsed_arg = vars(parser.parse_args(args.split()))

        check_and_format_humidity_parsed_arguments(parsed_arg, error_class=HumidityRelativeError)

        return parsed_arg
