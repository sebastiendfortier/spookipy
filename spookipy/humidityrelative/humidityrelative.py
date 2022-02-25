# -*- coding: utf-8 -*-
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils import get_temp_phase_switch, validate_humidity_parameters
from ..plugin import Plugin
from ..science import hr_from_svp_vppr, rpn_hr_from_es, rpn_hr_from_hu
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer)


class HumidityRelativeError(Exception):
    pass


class HumidityRelative(Plugin):
    """Calculation of the relative humidity, the ratio between the partial pressure of water vapour content in the air and the saturated vapour pressure at the same temperature.

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
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            ice_water_phase=None,
            temp_phase_switch=None,
            temp_phase_switch_unit='celsius',
            rpn=False):

        self.plugin_params = {
            'ice_water_phase': self.ice_water_phase,
            'temp_phase_switch': self.temp_phase_switch,
            'temp_phase_switch_unit': self.temp_phase_switch_unit,
            'rpn': self.rpn}
        self.plugin_mandatory_dependencies_rpn = [
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'HU': {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'QV': {'nomvar': 'QV', 'unit': 'gram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'ES': {'nomvar': 'ES', 'unit': 'celsius', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'pascal'},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'TD': {'nomvar': 'TD', 'unit': 'celsius', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'},
            }
        ]
        self.plugin_mandatory_dependencies = [
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'},
                'HU': {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram', 'select_only': True},
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'QV': {'nomvar': 'QV', 'unit': 'gram_per_kilogram', 'select_only': True},
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
                'etiket': 'HUMREL',
                'unit': 'scalar',
                'nbits': 12,
                'datyp': 1}}
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise HumidityRelativeError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(
            self.df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        validate_humidity_parameters(
            HumidityRelativeError,
            self.ice_water_phase,
            self.temp_phase_switch,
            self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(
            HumidityRelativeError,
            self.ice_water_phase == 'both',
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            self.rpn)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        # check if result already exists
        self.existing_result_df = get_existing_result(
            self.df, self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)
        # print(self.df[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
        self.groups = self.df.groupby(
            ['grid', 'dateo', 'forecast_hour', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'HumidityRelative',
                self.existing_result_df,
                self.meta_df)

        logging.info('HumidityRelative - compute')
        df_list = []

        if self.rpn:
            dependencies_list = get_dependencies(
                self.groups,
                self.meta_df,
                'HumidityRelative',
                self.plugin_mandatory_dependencies_rpn,
                self.plugin_params,
                intersect_levels=True)
        else:
            dependencies_list = get_dependencies(
                self.groups,
                self.meta_df,
                'HumidityRelative',
                self.plugin_mandatory_dependencies,
                self.plugin_params,
                intersect_levels=True)

        for dependencies_df, option in dependencies_list:
            if self.rpn:
                if option == 0:
                    # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    hu_df = get_from_dataframe(dependencies_df, 'HU')
                    self.rpn_humidityrelative_from_tt_hu_px(
                        dependencies_df, hu_df, option)

                elif option == 1:
                    # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    hu_df = self.compute_hu(dependencies_df)
                    self.rpn_humidityrelative_from_tt_hu_px(
                        dependencies_df, hu_df, option)

                elif option == 2:
                    # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    es_df = get_from_dataframe(dependencies_df, 'ES')
                    self.rpn_humidityrelative_from_tt_es_px(
                        dependencies_df, es_df, option)
                else:
                    # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies_rpn[option])
                    es_df = self.compute_es(dependencies_df)
                    self.rpn_humidityrelative_from_tt_es_px(
                        dependencies_df, es_df, option)

            else:  # not rpn
                hr_df = self.humidityrelative_from_svp_vppr(
                    dependencies_df, option)

            df_list.append(hr_df)

        return final_results(df_list, HumidityRelativeError, self.meta_df)

    def rpn_humidityrelative_from_tt_hu_px(
            self, dependencies_df, hu_df, option):
        logging.info(f'rpn option {option+1}')

        ttk_df = get_from_dataframe(dependencies_df, 'TT')
        pxpa_df = get_from_dataframe(dependencies_df, 'PX')
        hr_df = create_empty_result(
            ttk_df,
            self.plugin_result_specifications['HR'],
            all_rows=True)
        # ttk_df = fstpy.unit_convert(tt_df, 'kelvin')
        # pxpa_df = fstpy.unit_convert(px_df, 'pascal')
        for i in hr_df.index:
            ttk = ttk_df.at[i, 'd']
            pxpa = pxpa_df.at[i, 'd']
            hu = hu_df.at[i, 'd']
            hr_df.at[i, 'd'] = rpn_hr_from_hu(
                tt=ttk, hu=hu, px=pxpa, swph=self.ice_water_phase == 'both').astype(np.float32)

    def compute_hu(self, dependencies_df):
        from ..humidityspecific.humidityspecific import HumiditySpecific
        hu_df = HumiditySpecific(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            temp_phase_switch=self.temp_phase_switch,
            rpn=True).compute()
        hu_df = get_from_dataframe(hu_df, 'HU')
        return hu_df

    def rpn_humidityrelative_from_tt_es_px(
            self, dependencies_df, es_df, option):
        logging.info(f'rpn option {option+1}')

        ttk_df = get_from_dataframe(dependencies_df, 'TT')
        pxpa_df = get_from_dataframe(dependencies_df, 'PX')
        hr_df = create_empty_result(
            ttk_df,
            self.plugin_result_specifications['HR'],
            all_rows=True)
        # ttk_df = fstpy.unit_convert(tt_df, 'kelvin')
        # pxpa_df = fstpy.unit_convert(px_df, 'pascal')
        for i in hr_df.index:
            ttk = ttk_df.at[i, 'd']
            pxpa = pxpa_df.at[i, 'd']
            es = es_df.at[i, 'd']
            hr_df.at[i, 'd'] = rpn_hr_from_es(
                tt=ttk, es=es, px=pxpa, swph=self.ice_water_phase == 'both').astype(np.float32)

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
            rpn=True).compute()
        es_df = get_from_dataframe(es_df, 'ES')
        return es_df

    def humidityrelative_from_svp_vppr(self, dependencies_df, option):
        from ..saturationvapourpressure.saturationvapourpressure import \
            SaturationVapourPressure
        from ..vapourpressure.vapourpressure import VapourPressure
        logging.info(f'option {option+1}')
        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])

        tt_df = get_from_dataframe(dependencies_df, 'TT')
        hr_df = create_empty_result(
            tt_df,
            self.plugin_result_specifications['HR'],
            all_rows=True)
        svp_df = SaturationVapourPressure(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            temp_phase_switch=(
                self.temp_phase_switch if self.ice_water_phase != 'water' else None)).compute()
        svp_df = get_from_dataframe(svp_df, 'SVP')
        vppr_df = VapourPressure(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            temp_phase_switch=(
                self.temp_phase_switch if self.ice_water_phase != 'water' else None)).compute()
        vppr_df = get_from_dataframe(vppr_df, 'VPPR')
        for i in hr_df.index:
            svp = svp_df.at[i, 'd']
            vppr = vppr_df.at[i, 'd']
            hr_df.at[i, 'd'] = hr_from_svp_vppr(
                svp=svp, vppr=vppr).astype(np.float32)
        return hr_df
