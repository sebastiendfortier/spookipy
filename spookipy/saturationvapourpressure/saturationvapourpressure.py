# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..humidityutils import (get_temp_phase_switch, validate_humidity_parameters, 
                            mandatory_temp_phase_switch_when_using_ice_water_phase_both)
from ..plugin import Plugin, PluginParser
from ..science import TDPACK_OFFSET_FIX, rpn_svp_from_tt, svp_from_tt
from ..utils import (create_empty_result, existing_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer, explicit_params_checker, DependencyError)
from ..configparsingutils import check_and_format_humidity_parsed_arguments, preprocess_negative_args


class SaturationVapourPressureError(Exception):
    pass


class SaturationVapourPressure(Plugin):
    """Calculates the saturation vapour pressure as a function of temperature.

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
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """
    computable_plugin = "SVP"
    @explicit_params_checker
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            ice_water_phase,
            temp_phase_switch      = None,
            temp_phase_switch_unit = 'celsius',
            rpn                    = False,
            dependency_check       = False,
            copy_input             = False,
            reduce_df              = True):

        self.plugin_params = {
            'ice_water_phase'       : self.ice_water_phase,
            'temp_phase_switch'     : self.temp_phase_switch,
            'temp_phase_switch_unit': self.temp_phase_switch_unit,
            'rpn'                   : self.rpn}

        self.plugin_mandatory_dependencies_rpn = [
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'}
            }
        ]

        self.plugin_mandatory_dependencies = [
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'}
            }
        ]
        self.plugin_result_specifications = {
            'SVP': {
                'nomvar': 'SVP',
                'label' : 'SVPRES',
                'unit'  : 'hectoPascal',
                'nbits' : 16,
                'datyp' : 1},
        }

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):

        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=['unit', 'forecast_hour', 'ip_info'])

        mandatory_temp_phase_switch_when_using_ice_water_phase_both(
            SaturationVapourPressureError,
            self.explicit_params,
            self.ice_water_phase,
            self.rpn,
            True)

        validate_humidity_parameters(
            SaturationVapourPressureError,
            self.ice_water_phase,
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            rpn=self.rpn,
            rpn_no_warning=self.dependency_check)

        self.temp_phase_switch, self.temp_phase_switch_unit  = get_temp_phase_switch(
            SaturationVapourPressureError,
            self.ice_water_phase == 'both',
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            self.rpn)

        # check if result already exists
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(['grid', 'datev', 'dateo', 'vctype'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'SaturationVapourPressure',
                self.existing_result_df,
                self.meta_df)
                
        logging.info('SaturationVapourPressure - compute')

        df_list = []
        try:
            if self.rpn:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'SaturationVapourPressure',
                    self.plugin_mandatory_dependencies_rpn,
                    self.plugin_params,
                    dependency_check = self.dependency_check)
            else:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'SaturationVapourPressure',
                    self.plugin_mandatory_dependencies,
                    self.plugin_params,
                    dependency_check = self.dependency_check)
        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f'{SaturationVapourPressure} - No matching dependencies found')
        else:
            for dependencies_df, _ in dependencies_list:

                tt_df = get_from_dataframe(dependencies_df, 'TT')
                svp_df = create_empty_result(
                    tt_df, self.plugin_result_specifications['SVP'], all_rows=True)

                if self.rpn:
                    logging.info('SaturationVapourPressure - rpn option 1')
                    for i in svp_df.index:
                        ttk = tt_df.at[i, 'd']
                        svp_df.at[i,
                                'd'] = rpn_svp_from_tt(ttk,
                                                        tpl=(self.temp_phase_switch if self.ice_water_phase != 'water' else -40),
                                                        swph=self.ice_water_phase == 'both').astype(np.float32)
                else:
                    logging.info('SaturationVapourPressure - option 2')
                    for i in tt_df.index:
                        tt = tt_df.at[i, 'd']
                        svp_df.at[i,
                                'd'] = svp_from_tt(tt - TDPACK_OFFSET_FIX,
                                                    tpl=(self.temp_phase_switch if self.ice_water_phase != 'water' else -40),
                                                    swph=self.ice_water_phase == 'both').astype(np.float32)

                df_list.append(svp_df)
        finally:
            return self.final_results(df_list, SaturationVapourPressureError, 
                                      dependency_check = self.dependency_check, 
                                      copy_input       = self.copy_input,
                                      reduce_df        = self.reduce_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=SaturationVapourPressure.__name__, parents=[Plugin.base_parser],add_help=False)

        parser.add_argument('--iceWaterPhase',type=str,required=True,choices=["WATER","BOTH"],dest='ice_water_phase', help="Switch to determine which phase to consider: ice and water, or, water only.")
        parser.add_argument('--temperaturePhaseSwitch',type=str,help="Temperature at which to change from the ice phase to the water phase.\nMandatory if '--iceWaterPhase BOTH' is used explicitly and without  '--RPN'. \n")
        parser.add_argument('--RPN',action='store_true',default=False,dest="rpn", help="Use of the RPN TdPack functions")

        parsed_arg = vars(parser.parse_args(preprocess_negative_args(args.split(),["--temperaturePhaseSwitch"])))

        check_and_format_humidity_parsed_arguments(parsed_arg, error_class=SaturationVapourPressureError)

        return parsed_arg
