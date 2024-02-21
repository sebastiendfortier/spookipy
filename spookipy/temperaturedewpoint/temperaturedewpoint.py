# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..humidityutils import (get_temp_phase_switch, validate_humidity_parameters, 
                            mandatory_temp_phase_switch_when_using_ice_water_phase_both)
from ..plugin import Plugin, PluginParser
from ..science import TDPACK_OFFSET_FIX, td_from_es, td_from_vppr
from ..utils import (create_empty_result, existing_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer, explicit_params_checker, DependencyError)
from ..configparsingutils import check_and_format_humidity_parsed_arguments, preprocess_negative_args


class TemperatureDewPointError(Exception):
    pass


class TemperatureDewPoint(Plugin):
    """Calculates the thermodynamic temperature of the dew point

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param ice_water_phase: Switch to determine which phase to consider: ice and water ('both'), or, water only ('water')
    :type ice_water_phase: str
    :param temp_phase_switch:  Temperature at which to change from the ice phase to the water phase, defaults to None
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
    computable_plugin = "TD"
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
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'HU': {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'QV': {'nomvar': 'QV', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'HR': {'nomvar': 'HR', 'unit': 'scalar', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
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
                'label' : 'DEWPTT', 
                'unit'  : 'celsius'}
        }

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
       
        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        mandatory_temp_phase_switch_when_using_ice_water_phase_both(
            TemperatureDewPointError,
            self.explicit_params,
            self.ice_water_phase,
            self.rpn)

        validate_humidity_parameters(
            TemperatureDewPointError,
            self.ice_water_phase,
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            rpn=self.rpn,
            rpn_no_warning=self.dependency_check)

        self.temp_phase_switch, self.temp_phase_switch_unit  = get_temp_phase_switch(
            TemperatureDewPointError,
            self.ice_water_phase == 'both',
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            self.rpn)

        self.existing_result_df = get_existing_result(
            self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(['grid', 'datev', 'dateo', 'vctype'])

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
                    intersect_levels=True,
                    dependency_check = self.dependency_check)
            else:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'TemperatureDewPoint',
                    self.plugin_mandatory_dependencies,
                    self.plugin_params,
                    intersect_levels=True,
                    dependency_check = self.dependency_check)
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
            return self.final_results(df_list, TemperatureDewPointError, 
                                      dependency_check = self.dependency_check, 
                                      copy_input       = self.copy_input,
                                      reduce_df        = self.reduce_df)

    def temperaturedewpoint_from_tt_vppr(self, dependencies_df, option):
        logging.info(f'TemperatureDewPoint - option {option+1}')
        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
        vppr_df = self.compute_vppr(dependencies_df)

        tt_df = get_from_dataframe(dependencies_df, 'TT')
        td_df = create_empty_result(
            tt_df,
            self.plugin_result_specifications['TD'],
            all_rows=True)
        for i in td_df.index:
            tt   = tt_df.at[i, 'd']
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
                [ dependencies_df,
                  self.meta_df ],
                ignore_index=True),
            ice_water_phase        = self.ice_water_phase,
            temp_phase_switch      = self.temp_phase_switch,
            temp_phase_switch_unit = self.temp_phase_switch_unit, 
            dependency_check       = True,
            reduce_df              = False).compute()
        # A noter que l'option dependency_check est a True pour l'appel a VapourPressure:
        #       On veut eviter de faire le nettoyage des metadata inutilement puisqu'il a deja ete fait.
        #       Aussi, puisque l'option est a true, on doit verifier si le dataframe est vide suite a 
        #       l'appel (pas de resultats calcules) car si c'est le cas, le plugin ne retournera pas une erreur
        if vppr_df.empty:
            raise TemperatureDewPointError('No results produced by TemperatureDewPoint, unable to calculate VapourPressure!')
        vppr_df = get_from_dataframe(vppr_df, 'VPPR')
        return vppr_df

    def temperaturedewpoint_from_tt_es(self, es_df, dependencies_df, option, rpn=False):
        if rpn:
            logging.info(f'TemperatureDewPoint - rpn option {option+1}')
        else:
            logging.info(f'TemperatureDewPoint - option {option+1}')

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
                [ dependencies_df,
                  self.meta_df ],
                ignore_index=True),
            ice_water_phase  = self.ice_water_phase,
            rpn              = True, 
            dependency_check = True,
            reduce_df        = False).compute()
        # A noter que l'option dependency_check est a True pour l'appel a DewPointDepression, voir 
        # note dans compute_vppr
        if es_df.empty:
            raise TemperatureDewPointError('No results produced by TemperatureDewPoint, unable to calculate DewPointDepression!')
        es_df = get_from_dataframe(es_df, 'ES')
        return es_df

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=TemperatureDewPoint.__name__, parents=[Plugin.base_parser],add_help=False)

        parser.add_argument('--iceWaterPhase',type=str,required=True,choices=["WATER","BOTH"],dest='ice_water_phase', help="Switch to determine which phase to consider: ice and water, or, water only.")
        parser.add_argument('--temperaturePhaseSwitch',type=str,help="Temperature at which to change from the ice phase to the water phase.\nMandatory if '--iceWaterPhase BOTH' is used.\n")
        parser.add_argument('--RPN',action='store_true',default=False,dest="rpn", help="Use of the RPN TdPack functions")


        parsed_arg = vars(parser.parse_args(preprocess_negative_args(args.split(),["--temperaturePhaseSwitch"])))

        check_and_format_humidity_parsed_arguments(parsed_arg, error_class=TemperatureDewPointError)

        return parsed_arg
