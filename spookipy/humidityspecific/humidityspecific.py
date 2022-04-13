# -*- coding: utf-8 -*-
import argparse
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils import get_temp_phase_switch, validate_humidity_parameters
from ..plugin import Plugin
from ..science import hu_from_qv, hu_from_vppr, rpn_hu_from_es, rpn_hu_from_hr
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer, DependencyError)
from ..configparsingutils import add_argument_for_humidity_plugin, check_and_format_humidity_parsed_arguments


class HumiditySpecificError(Exception):
    pass


class HumiditySpecific(Plugin):
    """Calculation of the specific humidity, the ratio of the mass of water vapour in the air to the total mass of moist air.

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    :param ice_water_phase: Switch to determine which phase to consider: ice and water ('both'), or, water only ('water'), defaults to None   
    :type ice_water_phase: str, optional
    :param temp_phase_switch: Temperature at which to change from the ice phase to the water phase, defaults to None
    :type temp_phase_switch: float, optional
    :param temp_phase_switch_unit: temp_phase_switch unit, can be kelvin or celcius, defaults to 'celsius'
    :type temp_phase_switch_unit: str, optional
    :param rpn: Use the RPN TdPack functions, defaults to False
    :type rpn: bool, optional
    :param dependency_check: Indicates the plugin is being called from another one who checks dependencies , defaults to False
    :type dependency_check: bool, optional   
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            ice_water_phase=None,
            temp_phase_switch=None,
            temp_phase_switch_unit='celsius',
            rpn=False,
            dependency_check=False):

        self.plugin_params = {
            'ice_water_phase': self.ice_water_phase,
            'temp_phase_switch': self.temp_phase_switch,
            'temp_phase_switch_unit': self.temp_phase_switch_unit,
            'rpn': self.rpn}

        self.plugin_mandatory_dependencies_rpn = [
            {
                'QV': {'nomvar': 'QV', 'unit': 'kilogram_per_kilogram', 'select_only': True},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'HR': {'nomvar': 'HR', 'unit': 'scalar', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'ES': {'nomvar': 'ES', 'unit': 'celsius', 'select_only': True},
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
                'QV': {'nomvar': 'QV', 'unit': 'kilogram_per_kilogram', 'select_only': True},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'HR': {'nomvar': 'HR', 'unit': 'scalar', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'ES': {'nomvar': 'ES', 'unit': 'celsius', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'TD': {'nomvar': 'TD', 'unit': 'celsius', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            }
        ]

        self.plugin_result_specifications = {
            'HU': {
                'nomvar': 'HU',
                'etiket': 'HUMSPF',
                'unit': 'kilogram_per_kilogram',
                'nbits': 16,
                'datyp': 1}}

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)
        self.prepare_groups()

    # might be able to move
    def prepare_groups(self):

        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=['unit', 'forecast_hour', 'ip_info'])

        validate_humidity_parameters(
            HumiditySpecificError,
            self.ice_water_phase,
            self.temp_phase_switch,
            self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(
            HumiditySpecificError,
            self.ice_water_phase == 'both',
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            self.rpn)

        # check if result already exists
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(['grid', 'datev', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'HumiditySpecific',
                self.existing_result_df,
                self.meta_df)

        logging.info('HumiditySpecific - compute')
        df_list = []

        try:
            if self.rpn:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'HumiditySpecific',
                    self.plugin_mandatory_dependencies_rpn,
                    self.plugin_params,
                    intersect_levels=True)
            else:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'HumiditySpecific',
                    self.plugin_mandatory_dependencies,
                    self.plugin_params,
                    intersect_levels=True)
        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f'{HumiditySpecific} - No matching dependencies found')
        else:

            for dependencies_df, option in dependencies_list:
                if self.rpn:
                    if option == 0:
                        hu_df = self.humidityspecific_from_qv(
                            dependencies_df, 0, True)

                    elif option == 1:
                        hu_df = self.rpn_humnidityspecific_from_tt_hr_px(
                            dependencies_df, option)

                    elif option == 2:  # test 11
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        es_df = get_from_dataframe(dependencies_df, 'ES')
                        hu_df = self.rpn_humidity_specific_from_tt_es_px(
                            es_df, dependencies_df, option)

                    else:  # test 13
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        es_df = self.compute_es(dependencies_df)
                        hu_df = self.rpn_humidity_specific_from_tt_es_px(
                            es_df, dependencies_df, option)

                else:
                    if option == 0:
                        hu_df = self.humidityspecific_from_qv(dependencies_df, 0)

                    else:
                        hu_df = self.humidityspecific_from_vppr_px(
                            dependencies_df, option)

                df_list.append(hu_df)
        finally:
            return final_results(df_list, HumiditySpecificError, self.meta_df, self.dependency_check)

    def rpn_humnidityspecific_from_tt_hr_px(self, dependencies_df, option):
        logging.info(f'rpn option {option+1}')
        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])

        ttk_df = get_from_dataframe(dependencies_df, 'TT')
        hr_df = get_from_dataframe(dependencies_df, 'HR')
        pxpa_df = get_from_dataframe(dependencies_df, 'PX')
        hu_df = create_empty_result(
            ttk_df,
            self.plugin_result_specifications['HU'],
            all_rows=True)
        for i in hu_df.index:
            ttk = ttk_df.at[i, 'd']
            pxpa = pxpa_df.at[i, 'd']
            hr = hr_df.at[i, 'd']
            hu_df.at[i, 'd'] = rpn_hu_from_hr(
                tt=ttk, hr=hr, px=pxpa, swph=self.ice_water_phase == 'both').astype(np.float32)
        return hu_df

    def rpn_humidity_specific_from_tt_es_px(self, es_df, dependencies_df, option):
        logging.info(f'rpn option {option+1}')

        ttk_df = get_from_dataframe(dependencies_df, 'TT')
        pxpa_df = get_from_dataframe(dependencies_df, 'PX')
        hu_df = create_empty_result(
            ttk_df,
            self.plugin_result_specifications['HU'],
            all_rows=True)

        for i in hu_df.index:
            ttk = ttk_df.at[i, 'd']
            es = es_df.at[i, 'd']
            pxpa = pxpa_df.at[i, 'd']
            hu_df.at[i, 'd'] = rpn_hu_from_es(
                tt=ttk, es=es, px=pxpa, swph=self.ice_water_phase == 'both').astype(np.float32)
        return hu_df

    def compute_es(self, dependencies_df):
        from spookipy.dewpointdepression.dewpointdepression import \
            DewPointDepression
        es_df = DewPointDepression(pd.concat(
            [dependencies_df, self.meta_df], ignore_index=True), 
            ice_water_phase='water', 
            dependency_check=self.dependency_check).compute()
        es_df = get_from_dataframe(es_df, 'ES')
        return es_df

    def humidityspecific_from_qv(self, dependencies_df, option, rpn=False):
        if rpn:
            logging.info(f'rpn option {option+1}')
        else:
            logging.info(f'option {option+1}')

        qvkgkg_df = get_from_dataframe(dependencies_df, 'QV')
        hu_df = create_empty_result(
            qvkgkg_df,
            self.plugin_result_specifications['HU'],
            all_rows=True)

        for i in hu_df.index:
            qvkgkg = qvkgkg_df.at[i, 'd']
            hu_df.at[i, 'd'] = hu_from_qv(qv=qvkgkg).astype(np.float32)
        return hu_df

    def humidityspecific_from_vppr_px(self, dependencies_df, option):
        from ..vapourpressure.vapourpressure import VapourPressure
        logging.info(f'option {option+1}')
        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])

        px_df = get_from_dataframe(dependencies_df, 'PX')
        hu_df = create_empty_result(
            px_df,
            self.plugin_result_specifications['HU'],
            all_rows=True)
        vppr_df = VapourPressure(
            pd.concat(
                [dependencies_df,
                self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            temp_phase_switch=self.temp_phase_switch,
            temp_phase_switch_unit=self.temp_phase_switch_unit, 
            dependency_check=self.dependency_check).compute()
        vppr_df = get_from_dataframe(vppr_df, 'VPPR')
        vpprpa_df = fstpy.unit_convert(vppr_df, 'pascal')
        for i in hu_df.index:
            px = px_df.at[i, 'd']
            vppr = vpprpa_df.at[i, 'd']
            hu_df.at[i, 'd'] = hu_from_vppr(
                vppr=vppr, px=px).astype(np.float32)
        return hu_df

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=HumiditySpecific.__name__, parents=[Plugin.base_parser])
        add_argument_for_humidity_plugin(parser)

        parsed_arg = vars(parser.parse_args(args.split()))

        check_and_format_humidity_parsed_arguments(parsed_arg, HumiditySpecificError)

        return parsed_arg
