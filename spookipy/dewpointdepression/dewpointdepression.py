# -*- coding: utf-8 -*-
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils import (get_temp_phase_switch,
                             validate_humidity_parameters)
from ..plugin import Plugin

from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result,
                     get_from_dataframe, initializer)

from ..science import es_from_td, rpn_es_from_hr, rpn_es_from_hu, TDPACK_OFFSET_FIX


class DewPointDepressionError(Exception):
    pass


class DewPointDepression(Plugin):

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
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'HU': {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'}
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'QV': {'nomvar': 'QV', 'unit': 'gram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'}
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'HR': {'nomvar': 'HR', 'unit': 'scalar', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'}
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'TD': {'nomvar': 'TD', 'unit': 'celsius', 'select_only': True},
            }
        ]
        self.plugin_mandatory_dependencies = [
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'HU': {'nomvar': 'HU', 'unit': 'kilogram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'}
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'QV': {'nomvar': 'QV', 'unit': 'gram_per_kilogram', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'}
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'HR': {'nomvar': 'HR', 'unit': 'scalar', 'select_only': True},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'}
            },
            {
                'TT': {'nomvar': 'TT', 'unit': 'celsius'},
                'TD': {'nomvar': 'TD', 'unit': 'celsius', 'select_only': True},
            }
        ]

        self.plugin_result_specifications = {
            'ES': {
                'nomvar': 'ES',
                'etiket': 'DEWPTD',
                'unit': 'celsius',
                'nbits': 16,
                'datyp': 1}}
        self.validate_input()

    # might be able to move

    def validate_input(self):
        if self.df.empty:
            raise DewPointDepressionError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(
            self.df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        validate_humidity_parameters(
            DewPointDepressionError,
            self.ice_water_phase,
            self.temp_phase_switch,
            self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(
            DewPointDepressionError,
            self.ice_water_phase == 'both',
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            self.rpn)

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
                'DewPointDepression',
                self.existing_result_df,
                self.meta_df)

        logging.info('DewPointDepression - compute')
        df_list = []
        if self.rpn:
            dependencies_list = get_dependencies(
                self.groups,
                self.meta_df,
                'DewPointDepression',
                self.plugin_mandatory_dependencies_rpn,
                self.plugin_params,
                intersect_levels=True)
        else:
            dependencies_list = get_dependencies(
                self.groups,
                self.meta_df,
                'DewPointDepression',
                self.plugin_mandatory_dependencies,
                self.plugin_params,
                intersect_levels=True)

        for dependencies_df, option in dependencies_list:

            if self.rpn:
                if option == 0:
                    hu_df = get_from_dataframe(dependencies_df, 'HU')
                    es_df = self.rpn_dewpointdepression_from_tt_hu_px(
                        hu_df, dependencies_df, option)

                elif option == 1:
                    hu_df = self.compute_hu(dependencies_df)
                    es_df = self.rpn_dewpointdepression_from_tt_hu_px(
                        hu_df, dependencies_df, option)

                elif option == 2:
                    es_df = self.rpn_dewpointdepression_from_tt_hr_px(
                        dependencies_df, option)

                else:
                    td_df = get_from_dataframe(dependencies_df, 'TD')
                    es_df = self.dewpointdepression_from_tt_td(
                        td_df, dependencies_df, option, True)

            else:
                if option in range(0, 3):
                    td_df = self.compute_td(dependencies_df)
                    es_df = self.dewpointdepression_from_tt_td(
                        td_df, dependencies_df, option)

                else:
                    td_df = get_from_dataframe(dependencies_df, 'TD')
                    es_df = self.dewpointdepression_from_tt_td(
                        td_df, dependencies_df, option)

            df_list.append(es_df)

        return final_results(df_list, DewPointDepression, self.meta_df)

    def rpn_dewpointdepression_from_tt_hr_px(self, dependencies_df, option):
        logging.info(f'rpn option {option+1}')

        tt_df = get_from_dataframe(dependencies_df, 'TT')
        hr_df = get_from_dataframe(dependencies_df, 'HR')
        px_df = get_from_dataframe(dependencies_df, 'PX')
        es_df = create_empty_result(
            tt_df,
            self.plugin_result_specifications['ES'],
            all_rows=True)
        ttk_df = fstpy.unit_convert(tt_df, 'kelvin')
        pxpa_df = fstpy.unit_convert(px_df, 'pascal')
        for i in es_df.index:
            ttk = ttk_df.at[i, 'd']
            pxpa = pxpa_df.at[i, 'd']
            hr = hr_df.at[i, 'd']
            es_df.at[i, 'd'] = rpn_es_from_hr(
                tt=ttk, hr=hr, px=pxpa, swph=self.ice_water_phase == 'both').astype(np.float32)
        return es_df

    def rpn_dewpointdepression_from_tt_hu_px(
            self, hu_df, dependencies_df, option):
        logging.info(f'rpn option {option+1}')

        tt_df = get_from_dataframe(dependencies_df, 'TT')
        px_df = get_from_dataframe(dependencies_df, 'PX')
        es_df = create_empty_result(
            tt_df,
            self.plugin_result_specifications['ES'],
            all_rows=True)
        ttk_df = fstpy.unit_convert(tt_df, 'kelvin')
        pxpa_df = fstpy.unit_convert(px_df, 'pascal')
        for i in es_df.index:
            ttk = ttk_df.at[i, 'd']
            pxpa = pxpa_df.at[i, 'd']
            hu = hu_df.at[i, 'd']
            es_df.at[i, 'd'] = rpn_es_from_hu(
                tt=ttk, hu=hu, px=pxpa, swph=self.ice_water_phase == 'both').astype(np.float32)
        return es_df

    def compute_hu(self, dependencies_df):
        from ..humidityspecific.humidityspecific import HumiditySpecific
        hu_df = HumiditySpecific(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            rpn=True).compute()
        hu_df = get_from_dataframe(hu_df, 'HU')
        return hu_df

    def dewpointdepression_from_tt_td(
            self,
            td_df,
            dependencies_df,
            option,
            rpn=False):
        if rpn:
            logging.info(f'rpn option {option+1}')
        else:
            logging.info(f'option {option+1}')

        tt_df = get_from_dataframe(dependencies_df, 'TT')
        es_df = create_empty_result(
            tt_df,
            self.plugin_result_specifications['ES'],
            all_rows=True)
        for i in es_df.index:
            tt = tt_df.at[i, 'd']
            td = td_df.at[i, 'd']
            es_df.at[i, 'd'] = es_from_td(tt=tt -
                                          TDPACK_OFFSET_FIX, td=td -
                                          TDPACK_OFFSET_FIX).astype(np.float32)
        return es_df

    def compute_td(self, dependencies_df):
        from ..temperaturedewpoint.temperaturedewpoint import TemperatureDewPoint
        td_df = TemperatureDewPoint(
            pd.concat(
                [
                    dependencies_df,
                    self.meta_df],
                ignore_index=True),
            ice_water_phase=self.ice_water_phase,
            temp_phase_switch=self.temp_phase_switch,
            temp_phase_switch_unit=self.temp_phase_switch_unit).compute()
        td_df = get_from_dataframe(td_df, 'TD')
        return td_df
