# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd
import dask.array as da

from spookipy.configparsingutils.configparsingutils import apply_lambda_to_list

from ..plugin import Plugin, PluginParser
from ..science import hmx_from_svp
from ..utils import (
    create_empty_result,
    existing_results,
    get_dependencies,
    get_existing_result,
    get_from_dataframe,
    initializer,
    find_common_levels,
)


class ArithmeticPercentileByPointError(Exception):
    pass


class ArithmeticPercentileByPoint(Plugin):
    """ArithmeticPercentileByPoint calculation.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param percentiles: list of percentiles to calculate
    :type percentiles: list[float]
    :param method: interpolation method of numpy percentile https://numpy.org/doc/1.24/reference/generated/numpy.percentile.html
    :type method: str
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """

    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        percentiles: "list[float]",
        method="linear",
        ignore_mask=False,
        copy_input=False,
        reduce_df=True,
    ):
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
        for p in self.percentiles:
            if p < 0.0 or p > 100.0:
                raise ArithmeticPercentileByPointError(
                    f"Percentiles need to be between 0 and 100, invalid percentile {p}."
                )
        # group by grid, dateo-v
        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=["etiket", "ip_info", "flags"])

        self.groups = self.no_meta_df.groupby(["grid", "datev", "dateo", "nomvar"])

    def compute(self) -> pd.DataFrame:
        df_list = []
        for _, df_group in self.groups:
            # create empty container here?
            common_level_df = find_common_levels(
                df_group, list_values_to_match=df_group.ensemble_member.unique(), column_to_match="ensemble_member"
            )
            level_groups = common_level_df.groupby(
                "level"
            )  # ensemble_groups = self.no_meta_df.groupby(['ensemble_member'])
            for l, level_df in level_groups:
                data = level_df["d"]
                all_ensemble_data = np.stack(data, axis=0)
                if type(all_ensemble_data) == da.core.Array:
                    all_ensemble_data = all_ensemble_data.compute()
                all_ensemble_data_result = np.percentile(
                    all_ensemble_data, self.percentiles, axis=0, method=self.method
                )

                i = 0
                for x in all_ensemble_data_result:
                    percentile_res_df = create_empty_result(
                        level_df,
                        {
                            "label": make_label(self.percentiles[i]),
                            "ensemble_member": "ALL",
                            "ensemble_extra_info": True,  # add ! to typvar
                            "unit": "scalar",
                        },
                    )
                    percentile_res_df["d"] = [x]
                    i += 1
                    df_list.append(percentile_res_df)

        r = self.final_results(
            df_list, ArithmeticPercentileByPointError, copy_input=self.copy_input, reduce_df=self.reduce_df
        )

        return r

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=ArithmeticPercentileByPoint.__name__, parents=[Plugin.base_parser], add_help=False)
        # should we add the option to chose what to group by??? like the others
        # # add option to group on member and allow a list of multiple group by
        # parser.add_argument('--groupBy',type=str,choices=['FORECAST_HOUR','FIELD_NAME'],dest='group_by', help="Option to group fields by attribute when performing calculation.")
        parser.add_argument(
            "--percentiles",
            required=True,
            type=str,
            help="Liste des percentiles (float) à calculer. De 0 à 100 inclusivement",
        )
        parser.add_argument(
            "--ignore_mask",
            action="store_true",
            default=False,
            help="Par défaut , on vérifie s'il y a un masque à tenir compte dans les calcul. Cette option ignore les masques.",
        )
        parser.add_argument(
            "--method",
            default="linear",
            choices=[
                "inverted_cdf",
                "averaged_inverted_cdf",
                "closest_observation",
                "interpolated_inverted_cdf",
                "hazen",
                "weibull",
                "linear",
                "median_unbiased",
                "normal_unbiased",
            ],
            help="Methode d'interpolation de numpy percentile",
        )

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg["percentiles"] = apply_lambda_to_list(parsed_arg["percentiles"].split(","), lambda a: float(a))

        return parsed_arg


def make_label(percentile) -> str:
    percentile_str = str(percentile)

    # Check if the number is an integer (i.e., does not contain a decimal point)
    if "." in percentile_str:
        percentile_str = percentile_str.rstrip("0")
        # Check if the string ends with a decimal point and remove it if necessary
        if percentile_str.endswith("."):
            percentile_str = percentile_str[:-1]

    label = "C" + percentile_str + "_____"

    return label[:6]
