# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..science import hmx_from_svp
from ..utils import (
    create_empty_result,
    existing_results,
    get_dependencies,
    get_existing_result,
    get_from_dataframe,
    initializer,
)


class HumidexError(Exception):
    pass


class Humidex(Plugin):
    """Humidex calculation. The humidex index aims to quantify the discomfort caused by a combination of heat and humidity.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param dependency_check: Indicates the plugin is being called from another one who checks dependencies , defaults to False
    :type dependency_check: bool, optional
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """

    computable_plugin = "HMX"

    @initializer
    def __init__(self, df: pd.DataFrame, dependency_check=False, copy_input=False, reduce_df=True):
        self.plugin_mandatory_dependencies = [
            {
                "TT": {"nomvar": "TT", "unit": "celsius", "surface": True},
                "TD": {"nomvar": "TD", "unit": "celsius", "select_only": False, "surface": True},
            }
        ]

        self.plugin_result_specifications = {
            "HMX": {"nomvar": "HMX", "label": "HUMIDX", "unit": "celsius", "level": 0, "ip1_kind": 2, "surface": True}
        }
        self.plugin_params = {"ice_water_phase": "water"}

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=["unit", "forecast_hour", "ip_info"])

        # check if result already exists
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)

        # select surface only
        self.no_meta_df_sfc = self.no_meta_df.loc[self.no_meta_df.surface]

        self.groups = self.no_meta_df_sfc.groupby(["grid", "datev", "dateo", "vctype"])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results("Humidex", self.existing_result_df, self.meta_df)

        logging.info("Humidex - compute")
        df_list = []
        dependencies_list = get_dependencies(
            self.groups,
            self.meta_df,
            "Humidex",
            self.plugin_mandatory_dependencies,
            self.plugin_params,
            intersect_levels=True,
            dependency_check=self.dependency_check,
        )

        for dependencies_df, option in dependencies_list:
            if option == 0:
                # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                td_df = get_from_dataframe(dependencies_df, "TD")
                hmx_df = self.humidex_from_tt_svp(dependencies_df, td_df, option)

            else:
                # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
                td_df = self.compute_td(dependencies_df)
                hmx_df = self.humidex_from_tt_svp(dependencies_df, td_df, option)

            df_list.append(hmx_df)

        return self.final_results(
            df_list,
            HumidexError,
            dependency_check=self.dependency_check,
            copy_input=self.copy_input,
            reduce_df=self.reduce_df,
        )

    def humidex_from_tt_svp(self, dependencies_df, td_df, option):
        from ..saturationvapourpressure.saturationvapourpressure import SaturationVapourPressure

        logging.info(f"Humidex - option {option + 1}")

        tt_df = get_from_dataframe(dependencies_df, "TT")
        hmx_df = create_empty_result(tt_df, self.plugin_result_specifications["HMX"], all_rows=True)
        rentd_df = td_df
        rentd_df.loc[rentd_df.nomvar == "TD", "nomvar"] = "TT"

        # A noter que l'option dependency_check est a True pour l'appel a SaturationVapourPressure:
        #       On veut eviter de faire le nettoyage des metadata inutilement puisqu'il a deja ete fait.
        #       Aussi, puisque l'option est a true, on doit verifier si le dataframe est vide suite a
        #       l'appel (pas de resultats calcules) car si c'est le cas, le plugin ne retournera pas une erreur.
        svp_df = SaturationVapourPressure(
            rentd_df, ice_water_phase="water", dependency_check=True, reduce_df=False
        ).compute()

        if svp_df.empty:
            raise HumidexError("No results produced by SaturationVapourPressure, unable to calculate Humidex!")

        svp_df = get_from_dataframe(svp_df, "SVP")

        for i in hmx_df.index:
            tt = tt_df.at[i, "d"]
            svp = svp_df.at[i, "d"]
            hmx_df.at[i, "d"] = hmx_from_svp(tt=tt, svp=svp).astype(np.float32)
        return hmx_df

    def compute_td(self, dependencies_df):
        from ..temperaturedewpoint.temperaturedewpoint import TemperatureDewPoint

        td_df = TemperatureDewPoint(
            pd.safe_concat([dependencies_df, self.meta_df]), ice_water_phase="water", reduce_df=False
        ).compute()
        return td_df
