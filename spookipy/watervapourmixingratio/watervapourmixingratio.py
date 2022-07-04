# -*- coding: utf-8 -*-
import argparse
import logging

import fstpy
import numpy as np
import pandas as pd

from ..humidityutils import (get_temp_phase_switch, validate_humidity_parameters, 
                            mandatory_ice_water_phase_when_using_temp_phase_switch, 
                            mandatory_temp_phase_switch_when_using_ice_water_phase_both)
from ..plugin import Plugin
from ..science import qv_from_hu, qv_from_vppr
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer, explicit_params_checker, DependencyError)
from ..configparsingutils import check_and_format_humidity_parsed_arguments


class WaterVapourMixingRatioError(Exception):
    pass

class WaterVapourMixingRatio(Plugin):
    """Calculates the water vapour mixing ratio, which is the ratio of the mass of water vapour to the mass of dry air

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
    computable_plugin = "QV"
    @explicit_params_checker
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            ice_water_phase='both',
            temp_phase_switch=-40,
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
                    'HU': {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram'},
                }
            ]
        self.plugin_mandatory_dependencies = [
                {
                    'HU': {'nomvar': 'HU','unit': 'kilogram_per_kilogram', 'select_only': True}, 
                },
                {
                    'VPPR': {'nomvar': 'VPPR', 'unit': 'pascal'},
                    'PX':   {'nomvar': 'PX',   'unit': 'pascal'}, 
                }
            ]

        self.plugin_result_specifications = {
            'QV': {
                'nomvar': 'QV',
                'etiket': 'WVMXRT',
                'unit': 'gram_per_kilogram'}}

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)
        self.prepare_groups()

    def prepare_groups(self):

        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        mandatory_ice_water_phase_when_using_temp_phase_switch(
            WaterVapourMixingRatioError,
            self.explicit_params)

        mandatory_temp_phase_switch_when_using_ice_water_phase_both(
            WaterVapourMixingRatioError,
            self.explicit_params,
            self.ice_water_phase,
            self.rpn)

        validate_humidity_parameters(
            WaterVapourMixingRatioError,
            self.ice_water_phase,
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            explicit_temp_phase_switch = ("temp_phase_switch" in self.explicit_params),
            rpn=self.rpn)

        self.temp_phase_switch = get_temp_phase_switch(
            WaterVapourMixingRatioError,
            self.ice_water_phase == 'both',
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            self.rpn)

        # check if result already exists
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(
            ['grid', 'datev', 'ip1_kind'])

    def compute(self, test_dependency=False) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'WaterVapourMixingRatio',
                self.existing_result_df,
                self.meta_df)

        logging.info('WaterVapourMixingRatio - compute')
        df_list = []

        try:
            if self.rpn:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'WaterVapourMixingRatio',
                    self.plugin_mandatory_dependencies_rpn,
                    self.plugin_params,
                    intersect_levels=True)
           
            else:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'WaterVapourMixingRatio',
                    self.plugin_mandatory_dependencies,
                    self.plugin_params,
                    intersect_levels=True)

        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f'{WaterVapourMixingRatio} - No matching dependencies found')
        else:
            for dependencies_df, option in dependencies_list:
                if option == 0:
                    qv_df = self.watervapourmixingratio_from_hu(dependencies_df, option)
                else:
                    qv_df = self.watervapourmixingratio_from_vppr(dependencies_df, option)

                df_list.append(qv_df)
        finally:
            return final_results(df_list, WaterVapourMixingRatioError, self.meta_df, self.dependency_check)

    def watervapourmixingratio_from_vppr(self, dependencies_df, option):
        logging.info(f'WaterVapourMixingRatio - option {option+1}')
        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])

        vpprpa_df = get_from_dataframe(dependencies_df, 'VPPR')
        pxpa_df   = get_from_dataframe(dependencies_df, 'PX')
        qv_df     = create_empty_result(
            vpprpa_df,
            self.plugin_result_specifications['QV'],
            all_rows=True)

        for i in qv_df.index:
            vpprpa = vpprpa_df.at[i, 'd']
            pxpa = pxpa_df.at[i, 'd']
            qv_df.at[i, 'd'] = qv_from_vppr(
                px=pxpa, vppr=vpprpa).astype(np.float32)
                
        return qv_df

    def watervapourmixingratio_from_hu(self, dependencies_df, option):
        logging.info(f'WaterVapourMixingRatio - option {option+1}')

        hu_df = get_from_dataframe(dependencies_df, 'HU')
        qv_df = create_empty_result(
            hu_df,
            self.plugin_result_specifications['QV'],
            all_rows=True)
        for i in qv_df.index:
            hu = hu_df.at[i, 'd']
            qv_df.at[i, 'd'] = qv_from_hu(hu=hu).astype(np.float32)

        return qv_df

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=WaterVapourMixingRatio.__name__, parents=[Plugin.base_parser])

        parser.add_argument('--iceWaterPhase',type=str,required=False,choices=["WATER","BOTH"],dest='ice_water_phase', help="Switch to determine which phase to consider: ice and water, or, water only.\nMandatory when using --temperaturePhaseSwitch (Default: BOTH)")
        parser.add_argument('--temperaturePhaseSwitch',type=str,help="Temperature at which to change from the ice phase to the water phase.\nMandatory if '--iceWaterPhase BOTH' is used explicitly and without '--RPN'.\nNot accepted if '--RPN is used'. (Default: -40C)")
        parser.add_argument('--RPN',action='store_true',default=False,dest="rpn", help="Use of the RPN TdPack functions")

        parsed_arg = vars(parser.parse_args(args.split()))

        check_and_format_humidity_parsed_arguments(parsed_arg, error_class=WaterVapourMixingRatioError)

        return parsed_arg
