# -*- coding: utf-8 -*-
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils import get_temp_phase_switch, validate_humidity_parameters
from ..plugin import Plugin
from ..science import TDPACK_OFFSET_FIX, rpn_svp_from_tt, svp_from_tt
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer)


class SaturationVapourPressureError(Exception):
    pass


class SaturationVapourPressure(Plugin):
    """Calculates the saturation vapour pressure as a function of temperature.

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
        self.plugin_mandatory_dependencies = [
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'}
            }
        ]
        self.plugin_result_specifications = {
            'SVP': {
                'nomvar': 'SVP',
                'etiket': 'SVPRES',
                'unit': 'hectoPascal',
                'nbits': 16,
                'datyp': 1},
        }
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise SaturationVapourPressureError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(
            self.df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        validate_humidity_parameters(
            SaturationVapourPressureError,
            self.ice_water_phase,
            self.temp_phase_switch,
            self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(
            SaturationVapourPressureError,
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

        self.groups = self.df.groupby(
            ['grid', 'dateo', 'forecast_hour', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'SaturationVapourPressure',
                self.existing_result_df,
                self.meta_df)

        logging.info('SaturationVapourPressure - compute')
        df_list = []

        dependencies_list = get_dependencies(
            self.groups,
            self.meta_df,
            'SaturationVapourPressure',
            self.plugin_mandatory_dependencies,
            self.plugin_params)

        for dependencies_df, _ in dependencies_list:

            tt_df = get_from_dataframe(dependencies_df, 'TT')
            svp_df = create_empty_result(
                tt_df, self.plugin_result_specifications['SVP'], all_rows=True)

            if self.rpn:
                logging.info('rpn option 1')
                ttk_df = fstpy.unit_convert(tt_df, 'kelvin')
                for i in svp_df.index:
                    ttk = ttk_df.at[i, 'd']
                    svp_df.at[i,
                              'd'] = rpn_svp_from_tt(ttk,
                                                     tpl=(self.temp_phase_switch if self.ice_water_phase != 'water' else -40),
                                                     swph=self.ice_water_phase == 'both').astype(np.float32)
            else:
                logging.info('option 2')
                for i in tt_df.index:
                    tt = tt_df.at[i, 'd']
                    svp_df.at[i,
                              'd'] = svp_from_tt(tt - TDPACK_OFFSET_FIX,
                                                 tpl=(self.temp_phase_switch if self.ice_water_phase != 'water' else -40),
                                                 swph=self.ice_water_phase == 'both').astype(np.float32)

            df_list.append(svp_df)

        return final_results(
            df_list,
            SaturationVapourPressureError,
            self.meta_df)
