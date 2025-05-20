# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..humidityutils import (
    get_temp_phase_switch,
    validate_humidity_parameters,
    mandatory_temp_phase_switch_when_using_ice_water_phase_both,
)
from ..plugin import Plugin, PluginParser
from ..science import TDPACK_OFFSET_FIX, es_from_td, rpn_es_from_hr, rpn_es_from_hu
from ..utils import (
    create_empty_result,
    existing_results,
    get_dependencies,
    get_existing_result,
    get_from_dataframe,
    initializer,
    explicit_params_checker,
    DependencyError,
)
from ..configparsingutils import check_and_format_humidity_parsed_arguments, preprocess_negative_args


class DewPointDepressionError(Exception):
    pass


class DewPointDepression(Plugin):
    """Calculation of the dew point depression

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

    computable_plugin = "ES"

    @explicit_params_checker
    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        ice_water_phase,
        temp_phase_switch=None,
        temp_phase_switch_unit="celsius",
        rpn=False,
        dependency_check=False,
        copy_input=False,
        reduce_df=True,
    ):
        self.plugin_params = {
            "ice_water_phase": self.ice_water_phase,
            "temp_phase_switch": self.temp_phase_switch,
            "temp_phase_switch_unit": self.temp_phase_switch_unit,
            "rpn": self.rpn,
        }

        self.plugin_mandatory_dependencies_rpn = [
            {
                "TT": {"nomvar": "TT", "unit": "kelvin"},
                "HU": {"nomvar": "HU", "unit": "kg/kg", "select_only": True},
                "PX": {"nomvar": "PX", "unit": "pascal"},
            },
            {
                "TT": {"nomvar": "TT", "unit": "kelvin"},
                "QV": {"nomvar": "QV", "unit": "kg/kg", "select_only": True},
                "PX": {"nomvar": "PX", "unit": "pascal"},
            },
            {
                "TT": {"nomvar": "TT", "unit": "kelvin"},
                "HR": {"nomvar": "HR", "unit": "scalar", "select_only": True},
                "PX": {"nomvar": "PX", "unit": "pascal"},
            },
            {
                "TT": {"nomvar": "TT", "unit": "celsius"},
                "TD": {"nomvar": "TD", "unit": "celsius", "select_only": True},
            },
        ]
        self.plugin_mandatory_dependencies = [
            {
                "TT": {"nomvar": "TT", "unit": "celsius"},
                "HU": {"nomvar": "HU", "unit": "kg/kg", "select_only": True},
                "PX": {"nomvar": "PX", "unit": "hPa"},
            },
            {
                "TT": {"nomvar": "TT", "unit": "celsius"},
                "QV": {"nomvar": "QV", "unit": "kg/kg", "select_only": True},
                "PX": {"nomvar": "PX", "unit": "hPa"},
            },
            {
                "TT": {"nomvar": "TT", "unit": "celsius"},
                "HR": {"nomvar": "HR", "unit": "scalar", "select_only": True},
                "PX": {"nomvar": "PX", "unit": "hPa"},
            },
            {
                "TT": {"nomvar": "TT", "unit": "celsius"},
                "TD": {"nomvar": "TD", "unit": "celsius", "select_only": True},
            },
        ]

        self.plugin_result_specifications = {
            "ES": {"nomvar": "ES", "label": "DEWPTD", "unit": "celsius", "nbits": 16, "datyp": 1}
        }

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=["unit", "forecast_hour", "ip_info"])

        mandatory_temp_phase_switch_when_using_ice_water_phase_both(
            DewPointDepressionError, self.explicit_params, self.ice_water_phase, self.rpn
        )

        validate_humidity_parameters(
            DewPointDepressionError,
            self.ice_water_phase,
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            rpn=self.rpn,
            rpn_no_warning=self.dependency_check,
        )

        self.temp_phase_switch, self.temp_phase_switch_unit = get_temp_phase_switch(
            DewPointDepressionError,
            self.ice_water_phase == "both",
            self.temp_phase_switch,
            self.temp_phase_switch_unit,
            self.rpn,
        )

        # check if result already exists
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)

        # Necessaire d'avoir les 2 dates dans le groupby
        self.groups = self.no_meta_df.groupby(["grid", "datev", "dateo", "vctype"])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results("DewPointDepression", self.existing_result_df, self.meta_df)

        logging.info("DewPointDepression - compute")

        df_list = []
        try:
            if self.rpn:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    "DewPointDepression",
                    self.plugin_mandatory_dependencies_rpn,
                    self.plugin_params,
                    intersect_levels=True,
                    dependency_check=self.dependency_check,
                )
            else:
                dependencies_list = get_dependencies(
                    self.groups,
                    self.meta_df,
                    "DewPointDepression",
                    self.plugin_mandatory_dependencies,
                    self.plugin_params,
                    intersect_levels=True,
                    dependency_check=self.dependency_check,
                )

        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f"{DewPointDepression} - No matching dependencies found")
        else:
            for dependencies_df, option in dependencies_list:
                if self.rpn:
                    if option == 0:
                        hu_df = get_from_dataframe(dependencies_df, "HU")
                        es_df = self.rpn_dewpointdepression_from_tt_hu_px(hu_df, dependencies_df, option)

                    elif option == 1:
                        hu_df = self.compute_hu(dependencies_df)
                        es_df = self.rpn_dewpointdepression_from_tt_hu_px(hu_df, dependencies_df, option)

                    elif option == 2:
                        es_df = self.rpn_dewpointdepression_from_tt_hr_px(dependencies_df, option)

                    else:
                        td_df = get_from_dataframe(dependencies_df, "TD")
                        es_df = self.dewpointdepression_from_tt_td(td_df, dependencies_df, option, True)

                else:
                    if option in range(0, 3):
                        td_df = self.compute_td(dependencies_df)
                        es_df = self.dewpointdepression_from_tt_td(td_df, dependencies_df, option)

                    else:
                        td_df = get_from_dataframe(dependencies_df, "TD")
                        es_df = self.dewpointdepression_from_tt_td(td_df, dependencies_df, option)

                df_list.append(es_df)
        finally:
            return self.final_results(
                df_list,
                DewPointDepressionError,
                dependency_check=self.dependency_check,
                copy_input=self.copy_input,
                reduce_df=self.reduce_df,
            )

    def rpn_dewpointdepression_from_tt_hr_px(self, dependencies_df, option):
        logging.info(f"rpn option {option + 1}")

        ttk_df = get_from_dataframe(dependencies_df, "TT")
        hr_df = get_from_dataframe(dependencies_df, "HR")
        pxpa_df = get_from_dataframe(dependencies_df, "PX")
        es_df = create_empty_result(ttk_df, self.plugin_result_specifications["ES"], all_rows=True)
        for i in es_df.index:
            ttk = ttk_df.at[i, "d"]
            pxpa = pxpa_df.at[i, "d"]
            hr = hr_df.at[i, "d"]
            es_df.at[i, "d"] = rpn_es_from_hr(tt=ttk, hr=hr, px=pxpa, swph=self.ice_water_phase == "both").astype(
                np.float32
            )
        return es_df

    def rpn_dewpointdepression_from_tt_hu_px(self, hu_df, dependencies_df, option):
        logging.info(f"rpn option {option + 1}")

        ttk_df = get_from_dataframe(dependencies_df, "TT")
        pxpa_df = get_from_dataframe(dependencies_df, "PX")
        es_df = create_empty_result(ttk_df, self.plugin_result_specifications["ES"], all_rows=True)
        for i in es_df.index:
            ttk = ttk_df.at[i, "d"]
            pxpa = pxpa_df.at[i, "d"]
            hu = hu_df.at[i, "d"]
            es_df.at[i, "d"] = rpn_es_from_hu(tt=ttk, hu=hu, px=pxpa, swph=self.ice_water_phase == "both").astype(
                np.float32
            )
        return es_df

    def compute_hu(self, dependencies_df):
        from ..humidityspecific.humidityspecific import HumiditySpecific

        hu_df = HumiditySpecific(
            pd.safe_concat([dependencies_df, self.meta_df]),
            ice_water_phase=self.ice_water_phase,
            rpn=True,
            dependency_check=True,
            reduce_df=False,
        ).compute()
        # A noter que l'option dependency_check est a True pour l'appel a HumiditySpecific:
        #       On veut eviter de faire le nettoyage des metadata inutilement puisqu'il a deja ete fait.
        #       Aussi, puisque l'option est a true, on doit verifier si le dataframe est vide suite a
        #       l'appel (pas de resultats calcules) car si c'est le cas, le plugin ne retournera pas une erreur
        if hu_df.empty:
            raise DewPointDepressionError(
                "No results produced by DewPointDepression, unable to calculate HumiditySpecific!"
            )
        hu_df = get_from_dataframe(hu_df, "HU")
        return hu_df

    def dewpointdepression_from_tt_td(self, td_df, dependencies_df, option, rpn=False):
        if rpn:
            logging.info(f"rpn option {option + 1}")
        else:
            logging.info(f"option {option + 1}")

        tt_df = get_from_dataframe(dependencies_df, "TT")
        es_df = create_empty_result(tt_df, self.plugin_result_specifications["ES"], all_rows=True)
        for i in es_df.index:
            tt = tt_df.at[i, "d"]
            td = td_df.at[i, "d"]
            es_df.at[i, "d"] = es_from_td(tt=tt - TDPACK_OFFSET_FIX, td=td - TDPACK_OFFSET_FIX).astype(np.float32)
        return es_df

    def compute_td(self, dependencies_df):
        from ..temperaturedewpoint.temperaturedewpoint import TemperatureDewPoint

        td_df = TemperatureDewPoint(
            pd.safe_concat([dependencies_df, self.meta_df]),
            ice_water_phase=self.ice_water_phase,
            temp_phase_switch=self.temp_phase_switch,
            temp_phase_switch_unit=self.temp_phase_switch_unit,
            dependency_check=True,
            reduce_df=False,
        ).compute()

        # A noter que l'option dependency_check est a True pour l'appel a TemperatureDewPoint:
        #       On veut eviter de faire le nettoyage des metadata inutilement puisqu'il a deja ete fait.
        #       Aussi, puisque l'option est a true, on doit verifier si le dataframe est vide suite a
        #       l'appel (pas de resultats calcules) car si c'est le cas, le plugin ne retournera pas une erreur
        if td_df.empty:
            raise DewPointDepressionError(
                "No results produced by DewPointDepression, unable to calculate TemperatureDewPoint!"
            )
        td_df = get_from_dataframe(td_df, "TD")
        return td_df

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=DewPointDepression.__name__, parents=[Plugin.base_parser], add_help=False)

        parser.add_argument(
            "--iceWaterPhase",
            type=str,
            required=True,
            choices=["WATER", "BOTH"],
            dest="ice_water_phase",
            help="Switch to determine which phase to consider: ice and water, or, water only.",
        )
        parser.add_argument(
            "--temperaturePhaseSwitch",
            type=str,
            help="Temperature at which to change from the ice phase to the water phase.\nMandatory if '--iceWaterPhase BOTH' is usedwithout '--RPN'. \nNot accepted if '--RPN is used'.",
        )
        parser.add_argument(
            "--RPN", action="store_true", default=False, dest="rpn", help="Use of the RPN TdPack functions"
        )

        parsed_arg = vars(parser.parse_args(preprocess_negative_args(args.split(), ["--temperaturePhaseSwitch"])))

        check_and_format_humidity_parsed_arguments(parsed_arg, error_class=DewPointDepressionError)

        return parsed_arg
