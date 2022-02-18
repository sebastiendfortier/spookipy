# -*- coding: utf-8 -*-

import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils import get_temp_phase_switch, validate_humidity_parameters
from ..plugin import Plugin
from ..science import TDPACK_OFFSET_FIX, td_from_es, td_from_vppr
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer, DependencyError)


class TemperatureDewPointError(Exception):
    pass


class TemperatureDewPoint(Plugin):
    """Calculates the thermodynamic temperature of the dew point

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param ice_water_phase: ice water phase, defaults to None
    :type ice_water_phase: str, optional
    :param temp_phase_switch: temperature phase switch , defaults to None
    :type temp_phase_switch: float, optional
    :param temp_phase_switch_unit: temperature phase switch unit, defaults to 'celsius'
    :type temp_phase_switch_unit: str, optional
    :param rpn: use rpn library algorithm, defaults to False
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
                'HR': {'nomvar': 'HR', 'unit': 'scalar', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'ES': {'nomvar': 'ES', 'unit': 'celsius', 'select_only': True}
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
                'HR': {'nomvar': 'HR', 'unit': 'scalar', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'ES': {'nomvar': 'ES', 'unit': 'celsius', 'select_only': True}
            }
        ]

        self.plugin_result_specifications = {
            'TD': {
                'nomvar': 'TD', 
                'etiket': 'DEWPTT', 
                'unit': 'celsius'}
        }

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)
        self.prepare_groups()

    def prepare_groups(self):
       
        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        validate_humidity_parameters(
            TemperatureDewPointError,
            self.ice_water_phase,
            self.temp_phase_switch,
            self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(
            TemperatureDewPointError,
            self.ice_water_phase == 'both',
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            self.rpn)

        self.existing_result_df = get_existing_result(
            self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(
            ['grid', 'datev', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'TemperatureDewPoint',
                self.existing_result_df,
                self.meta_df)

        logging.info('TemperatureDewPoint - compute')

        df_list = []
        try:
            if self.rpn:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'TemperatureDewPoint',
                    self.plugin_mandatory_dependencies_rpn,
                    self.plugin_params,
                    intersect_levels=True)
            else:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'TemperatureDewPoint',
                    self.plugin_mandatory_dependencies,
                    self.plugin_params,
                    intersect_levels=True)
        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f'{TemperatureDewPoint} - No matching dependencies found')
        else:
            for dependencies_df, option in dependencies_list:
                if self.rpn:
                    if option in range(0, 3):
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        es_df = self.compute_es(dependencies_df)
                        td_df = self.temperaturedewpoint_from_tt_es(
                            es_df, dependencies_df, option, True)

                    else:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        es_df = get_from_dataframe(dependencies_df, 'ES')
                        td_df = self.temperaturedewpoint_from_tt_es(
                            es_df, dependencies_df, option)

                else:
                    if option in range(0, 3):
                        td_df = self.temperaturedewpoint_from_tt_vppr(
                            dependencies_df, option)

                    else:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                        es_df = get_from_dataframe(dependencies_df, 'ES')
                        td_df = self.temperaturedewpoint_from_tt_es(
                            es_df, dependencies_df, option)

                df_list.append(td_df)
        finally:
            return final_results(df_list, TemperatureDewPointError, self.meta_df, self.dependency_check)

    def temperaturedewpoint_from_tt_vppr(self, dependencies_df, option):
        logging.info(f'option {option+1}')
        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
        vppr_df = self.compute_vppr(dependencies_df)

        tt_df = get_from_dataframe(dependencies_df, 'TT')
        td_df = create_empty_result(
            tt_df,
            self.plugin_result_specifications['TD'],
            all_rows=True)
        for i in td_df.index:
            tt = tt_df.at[i, 'd']
            vppr = vppr_df.at[i, 'd']
            td_df.at[i,
                     'd'] = td_from_vppr(tt=tt - TDPACK_OFFSET_FIX,
                                         vppr=vppr,
                                         tpl=(self.temp_phase_switch if self.ice_water_phase != 'water' else -40),
                                         swph=self.ice_water_phase == 'both').astype(np.float32)
        return td_df

    def compute_vppr(self, dependencies_df):
        from ..vapourpressure.vapourpressure import VapourPressure
        vppr_df = VapourPressure(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            temp_phase_switch=self.temp_phase_switch,
            temp_phase_switch_unit=self.temp_phase_switch_unit, 
            dependency_check=self.dependency_check).compute()
        vppr_df = get_from_dataframe(vppr_df, 'VPPR')
        return vppr_df

    def temperaturedewpoint_from_tt_es(
            self, es_df, dependencies_df, option, rpn=False):
        if rpn:
            logging.info(f'rpn option {option+1}')
        else:
            logging.info(f'option {option+1}')

        tt_df = get_from_dataframe(dependencies_df, 'TT')
        td_df = create_empty_result(
            tt_df,
            self.plugin_result_specifications['TD'],
            all_rows=True)
        for i in td_df.index:
            tt = tt_df.at[i, 'd']
            es = es_df.at[i, 'd']
            td_df.at[i, 'd'] = td_from_es(
                tt=tt - TDPACK_OFFSET_FIX, es=es).astype(np.float32)
        return td_df

    def compute_es(self, dependencies_df):
        from ..dewpointdepression.dewpointdepression import DewPointDepression
        es_df = DewPointDepression(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            temp_phase_switch=self.temp_phase_switch,
            temp_phase_switch_unit=self.temp_phase_switch_unit,
            rpn=True, 
            dependency_check=self.dependency_check).compute()
        es_df = get_from_dataframe(es_df, 'ES')
        return es_df
