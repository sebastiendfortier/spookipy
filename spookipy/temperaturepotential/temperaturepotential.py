# -*- coding: utf-8 -*-
import logging
from typing import Final

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (
    create_empty_result,
    existing_results,
    get_dependencies,
    get_existing_result,
    get_from_dataframe,
    initializer,
    DependencyError,
)


RD: Final[float] = 287.04  # the gas constant for dry air (RD = 287.04 J/(kg*K)),
"""Gas constant for dry air (RD = 287.04 J/(kg*K))"""


CPD: Final[float] = 1005.46  # the specific heat of dry air (CPD = 1005.46 J/(kg*K))
"""Specific heat of dry air (CPD = 1005.46 J/(kg*K))"""


class TemperaturePotentialError(Exception):
    pass


class TemperaturePotential(Plugin):
    """Calculates the potential temperature, which is the temperature
        of an air parcel following adiabatic expansion or compression
        to a reference pressure. On a tephigram such a process can be
        visualized by raising or lowering a parcel along a dry adiabat.
        Note: The reference pressure used here is 1000 hPa.

    :param df: input dataframe
    :type df: pd.DataFrame
    :param dependency_check: Indicates the plugin is being called from another one who checks dependencies , defaults to False
    :type dependency_check: bool, optional
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """

    computable_plugin = "TH"

    @initializer
    def __init__(self, df: pd.DataFrame, dependency_check=False, copy_input=False, reduce_df=True):
        self.plugin_mandatory_dependencies = [
            {
                "TT": {"nomvar": "TT", "unit": "kelvin"},
                "PX": {"nomvar": "PX", "unit": "hPa"},
            }
        ]

        self.plugin_result_specifications = {"TH": {"nomvar": "TH", "label": "PTNLTT", "unit": "kelvin"}}

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=["unit", "forecast_hour", "ip_info"])

        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(["grid", "datev", "dateo", "vctype"])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results("TemperaturePotential", self.existing_result_df, self.meta_df)

        logging.info("TemperaturePotential - compute")
        df_list = []
        try:
            dependencies_list = get_dependencies(
                self.groups,
                self.meta_df,
                "TemperaturePotential",
                self.plugin_mandatory_dependencies,
                intersect_levels=True,
            )
        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f"{TemperaturePotential} - No matching dependencies found")
        else:
            for dependencies_df, _ in dependencies_list:
                tt_df = get_from_dataframe(dependencies_df, "TT")
                px_df = get_from_dataframe(dependencies_df, "PX")
                th_df = create_empty_result(tt_df, self.plugin_result_specifications["TH"], all_rows=True)

                for i in th_df.index:
                    ttk = tt_df.at[i, "d"]
                    px = px_df.at[i, "d"]
                    th_df.at[i, "d"] = (ttk * (1000.0 / px) ** (RD / CPD)).astype(np.float32)
                df_list.append(th_df)

        finally:
            return self.final_results(
                df_list,
                TemperaturePotentialError,
                dependency_check=self.dependency_check,
                copy_input=self.copy_input,
                reduce_df=self.reduce_df,
            )
