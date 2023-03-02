# -*- coding: utf-8 -*-
import argparse
import logging

import fstpy
import numpy as np
import pandas as pd

from ..humidityutils.humidityutils import (get_temp_phase_switch,
                                           validate_humidity_parameters, 
                                           mandatory_ice_water_phase_when_using_temp_phase_switch)
from ..plugin.plugin import Plugin
from ..science import (TDPACK_OFFSET_FIX, rpn_vppr_from_hu, rpn_vppr_from_td,
                       vppr_from_hr, vppr_from_hu, vppr_from_qv, vppr_from_td)
from ..utils import (create_empty_result, existing_results, 
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer, explicit_params_checker, DependencyError)
from ..configparsingutils import check_and_format_humidity_parsed_arguments


class VapourPressureError(Exception):
    pass


class VapourPressure(Plugin):
    """Calculates the vapour pressure of water

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param ice_water_phase: Switch to determine which phase to consider: ice and water ('both'), or, water only ('water'), defaults to 'both'
    :type ice_water_phase: str, optional
    :param temp_phase_switch: Temperature at which to change from the ice phase to the water phase, defaults to '-40'
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
    computable_plugin = "VPPR"
    @explicit_params_checker
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            ice_water_phase='both',
            temp_phase_switch=-40,
            temp_phase_switch_unit='celsius',
            rpn=False,
            dependency_check=False,
            copy_input=False):

        self.plugin_params = {
            'ice_water_phase': self.ice_water_phase,
            'temp_phase_switch': self.temp_phase_switch,
            'temp_phase_switch_unit': self.temp_phase_switch_unit,
            'rpn': self.rpn}

        self.plugin_mandatory_dependencies_rpn = [
            # HU + PXpa
            {
                'HU': {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'}
            },
            # QVkg + PX
            {
                'QV': {'nomvar': 'QV', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'}
            },
            #TT + HR + PX > HUrpn + PXpa
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'HR': {'nomvar': 'HR', 'unit': 'scalar', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'}
            },
            # ES + TTk
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'ES': {'nomvar': 'ES', 'unit': 'kelvin', 'select_only': True},
            },
            # TDk + TTk
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'TD': {'nomvar': 'TD', 'unit': 'kelvin', 'select_only': True},
            }
        ]
        self.plugin_mandatory_dependencies = [
            # HU + PX
            {
                'HU': {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'}
            },
            # QVkg/kg + PX
            {
                'QV': {'nomvar': 'QV', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'}
            },
            # HR + SVP
            {
                'HR': {'nomvar': 'HR', 'unit': 'scalar', 'select_only': True},
                'SVP': {'nomvar': 'SVP', 'unit': 'hectoPascal'},
            },
            # ES + TT
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'ES': {'nomvar': 'ES', 'unit': 'celsius', 'select_only': True},
            },
            # TD + TT
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'TD': {'nomvar': 'TD', 'unit': 'celsius', 'select_only': True},
            }
        ]

        self.plugin_result_specifications = {
            'VPPR': {
                'nomvar': 'VPPR',
                'etiket': 'VAPRES',
                'unit'  : 'hectoPascal',
                'nbits' : 16,
                'datyp' : 1}}


        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)
        self.prepare_groups()

    def prepare_groups(self):
        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=['unit', 'forecast_hour', 'ip_info'])

        mandatory_ice_water_phase_when_using_temp_phase_switch(
            VapourPressureError,
            self.explicit_params)

        validate_humidity_parameters(
            VapourPressureError,
            self.ice_water_phase,
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            explicit_temp_phase_switch = ("temp_phase_switch" in self.explicit_params),
            rpn=self.rpn)

        self.temp_phase_switch = get_temp_phase_switch(
            VapourPressureError,
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
                'VapourPressure',
                self.existing_result_df,
                self.meta_df)

        logging.info('VapourPressure - compute')
        df_list = []
        try:
            if self.rpn:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'VapourPressure',
                    self.plugin_mandatory_dependencies_rpn,
                    self.plugin_params,
                    intersect_levels=True,
                    dependency_check = self.dependency_check)
            else:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    'VapourPressure',
                    self.plugin_mandatory_dependencies,
                    self.plugin_params,
                    intersect_levels=True,
                    dependency_check = self.dependency_check)
        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f'{VapourPressure} - No matching dependencies found')
        else:
            for dependencies_df, option in dependencies_list:
                if self.rpn:
                    if option == 0:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        hu_df = get_from_dataframe(dependencies_df, 'HU')
                        vppr_df = self.rpn_vapourpressure_from_hu_px(
                            hu_df, dependencies_df, option)

                    elif option == 1:
                        vppr_df = self.vapourpressure_from_qv_px(
                            dependencies_df, option, True)

                    elif option == 2:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        hu_df = self.compute_hu(dependencies_df)
                        vppr_df = self.rpn_vapourpressure_from_hu_px(
                            hu_df, dependencies_df, option)

                    elif option == 3:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        td_df = self.compute_td(dependencies_df)
                        vppr_df = self.rpn_vapourpressure_from_tt_td(
                            td_df, dependencies_df, option)

                    else:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                        td_df = get_from_dataframe(dependencies_df, 'TD')
                        vppr_df = self.rpn_vapourpressure_from_tt_td(
                            td_df, dependencies_df, option)

                else:
                    if option == 0:
                        vppr_df = self.vapourpressure_from_hu_px(
                            dependencies_df, option)

                    elif option == 1:
                        vppr_df = self.vapourpressure_from_qv_px(
                            dependencies_df, option)

                    elif option == 2:
                        vppr_df = self.vapourpressure_from_hr_svp(
                            dependencies_df, option)

                    elif option == 3:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                        td_df = self.compute_td(dependencies_df)
                        vppr_df = self.vapourpressure_from_tt_td(
                            td_df, dependencies_df, option)

                    else:
                        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                        td_df = get_from_dataframe(dependencies_df, 'TD')
                        vppr_df = self.vapourpressure_from_tt_td(
                            td_df, dependencies_df, option)

                df_list.append(vppr_df)
        finally:
            return self.final_results(df_list, VapourPressureError,           
                                      dependency_check = self.dependency_check, 
                                      copy_input = self.copy_input)

    def vapourpressure_from_hu_px(self, dependencies_df, option):
        logging.info(f'VapourPressure - option {option+1}')
        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
        hu_df = get_from_dataframe(dependencies_df, 'HU')

        px_df = get_from_dataframe(dependencies_df, 'PX')
        vppr_df = create_empty_result(
            hu_df, self.plugin_result_specifications['VPPR'], all_rows=True)
        for i in vppr_df.index:
            hu = hu_df.at[i, 'd']
            px = px_df.at[i, 'd']
            vppr_df.at[i, 'd'] = vppr_from_hu(hu=hu, px=px).astype(np.float32)
        return vppr_df

    def vapourpressure_from_hr_svp(self, dependencies_df, option):
        logging.info(f'VapourPressure - option {option+1}')
        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])

        svp_df = get_from_dataframe(dependencies_df, 'SVP')
        hr_df = get_from_dataframe(dependencies_df, 'HR')
        vppr_df = create_empty_result(
            svp_df,
            self.plugin_result_specifications['VPPR'],
            all_rows=True)
        for i in vppr_df.index:
            hr = hr_df.at[i, 'd']
            svp = svp_df.at[i, 'd']
            vppr_df.at[i, 'd'] = vppr_from_hr(
                hr=hr, svp=svp).astype(np.float32)
        return vppr_df

    def rpn_vapourpressure_from_tt_td(self, td_df, dependencies_df, option):
        logging.info(f'VapourPressure - rpn option {option+1}')

        ttk_df = get_from_dataframe(dependencies_df, 'TT')
        vppr_df = create_empty_result(
            ttk_df, self.plugin_result_specifications['VPPR'], all_rows=True)
        tdk_df = fstpy.unit_convert(td_df, 'kelvin')
        for i in vppr_df.index:
            ttk = ttk_df.at[i, 'd']
            tdk = tdk_df.at[i, 'd']
            vppr_df.at[i,
                       'd'] = rpn_vppr_from_td(td=tdk,
                                               tt=ttk,
                                               tpl=(self.temp_phase_switch if self.ice_water_phase != 'water' else -40),
                                               swph=self.ice_water_phase == 'both').astype(np.float32)
        return vppr_df

    def vapourpressure_from_qv_px(self, dependencies_df, option, rpn=False):
        if rpn:
            logging.info(f'VapourPressure - rpn option {option+1}')
        else:
            logging.info(f'VapourPressure - option {option+1}')
        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])

        qvkgkg_df = get_from_dataframe(dependencies_df, 'QV')
        px_df     = get_from_dataframe(dependencies_df, 'PX')
        vppr_df   = create_empty_result(
            qvkgkg_df, self.plugin_result_specifications['VPPR'], all_rows=True)

        for i in vppr_df.index:
            qv = qvkgkg_df.at[i, 'd']
            px = px_df.at[i, 'd']
            vppr_df.at[i, 'd'] = vppr_from_qv(qv=qv, px=px).astype(np.float32)
        return vppr_df

    def vapourpressure_from_tt_td(self, td_df, dependencies_df, option):
        logging.info(f'VapourPressure - option {option+1}')

        tt_df = get_from_dataframe(dependencies_df, 'TT')
        vppr_df = create_empty_result(
            tt_df, self.plugin_result_specifications['VPPR'], all_rows=True)
        for i in vppr_df.index:
            tt = tt_df.at[i, 'd']
            td = td_df.at[i, 'd']
            vppr_df.at[i,
                       'd'] = vppr_from_td(td=td - TDPACK_OFFSET_FIX,
                                           tt=tt - TDPACK_OFFSET_FIX,
                                           tpl=(self.temp_phase_switch if self.ice_water_phase != 'water' else -40),
                                           swph=self.ice_water_phase == 'both').astype(np.float32)
        return vppr_df

    def rpn_vapourpressure_from_hu_px(self, hu_df, dependencies_df, option):
        logging.info(f'VapourPressure - rpn option {option+1}')

        pxpa_df = get_from_dataframe(dependencies_df, 'PX')
        vppr_df = create_empty_result(
            pxpa_df, self.plugin_result_specifications['VPPR'], all_rows=True)
        # pxpa_df = fstpy.unit_convert(px_df, 'pascal')
        for i in vppr_df.index:
            pxpa = pxpa_df.at[i, 'd']
            hu = hu_df.at[i, 'd']
            vppr_df.at[i, 'd'] = rpn_vppr_from_hu(
                hu=hu, px=pxpa).astype(np.float32)
        return vppr_df

    def compute_hu(self, dependencies_df):
        from ..humidityspecific import HumiditySpecific
        hu_df = HumiditySpecific(
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
        hu_df = get_from_dataframe(hu_df, 'HU')
        return hu_df

    def compute_td(self, dependencies_df):
        from ..temperaturedewpoint import TemperatureDewPoint
        td_df = TemperatureDewPoint(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            temp_phase_switch=self.temp_phase_switch,
            temp_phase_switch_unit=self.temp_phase_switch_unit, 
            dependency_check=self.dependency_check).compute()
        td_df = get_from_dataframe(td_df, 'TD')
        return td_df

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=VapourPressure.__name__, parents=[Plugin.base_parser])

        parser.add_argument('--iceWaterPhase',type=str,required=False,choices=["WATER","BOTH"],dest='ice_water_phase', help="Switch to determine which phase to consider: ice and water, or, water only.\nMandatory when using --temperaturePhaseSwitch (Default: BOTH)")
        parser.add_argument('--temperaturePhaseSwitch',type=str,help="Temperature at which to change from the ice phase to the water phase. (Default: -40C)")
        parser.add_argument('--RPN',action='store_true',default=False,dest="rpn", help="Use of the RPN TdPack functions")

        parsed_arg = vars(parser.parse_args(args.split()))

        check_and_format_humidity_parsed_arguments(parsed_arg, error_class=VapourPressureError)

        return parsed_arg
