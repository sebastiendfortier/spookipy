# -*- coding: utf-8 -*-
import logging
from typing import Final

import fstpy
import numpy as np
import pandas as pd
from ..plugin import Plugin, PluginParser
from ..utils import create_empty_result, get_3d_array, initializer, validate_nomvar


STATS: Final[dict] = {
    "MEAN": "MEAN",
    "STD": "SSTD",
    "PERCENTILES": "C",
    "INTERPERCENTILES": "I",
    "THRESHOLDS": "",
    "NORMTHRESHOLDS": "",
}


class StatisticsVerticallyError(Exception):
    pass


# [MEAN|STD|PERCENTILES:FLOAT[0 to 100]|INTERPERCENTILES:FLOAT[0 to 100]:FLOAT[0 to 100]|THRESHOLDS:STRING[LT, LE, EQ, GE, GT, NE]:FLOAT[-infinity to infinity]|STRING[VARNAME]]]
class StatisticsVertically(Plugin):
    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        nomvar: list = None,
        percentiles: list = None,
        interpercentiles_lower: list = None,
        interpercentiles_upper: list = None,
        threshold_operators: list = None,
        threshold_values: list = None,
        norm_operators: list = None,
        norm_nomvars: list = None,
        stats: list = "ALL",
    ):
        super().__init__(self.df)
        self.validate_params()
        self.prepare_groups()

    def prepare_groups(self):
        if not (self.nomvar is None):
            df_list = []
            for nomvar in self.nomvar:
                if nomvar in self.no_meta_df.nomvar.unique():
                    df = self.no_meta_df.loc[self.no_meta_df.nomvar == nomvar]
                    df_list.append(df)
                else:
                    raise StatisticsVerticallyError(f"nomvar must be present in dataframe")

            if len(df_list):
                self.no_meta_df = pd.safe_concat(df_list)

        self.no_meta_df = fstpy.add_columns(self.no_meta_df, "forecast_hour")
        self.groups = self.no_meta_df.groupby(["grid", "nomvar", "forecast_hour"])

    def validate_params(self):
        if not isinstance(self.stats, list):
            self.stats = [self.stats]
        if "ALL" in self.stats:
            self.stats = STATS.keys()

        if not (self.nomvar is None):
            if not isinstance(self.nomvar, list):
                self.nomvar = [self.nomvar]
            for nomvar in self.nomvar:
                validate_nomvar(nomvar, "StatisticsVertically", StatisticsVerticallyError)

        self.validate_options(
            ["MEAN", "STD", "PERCENTILES", "INTERPERCENTILES", "THRESHOLDS", "NORMTHRESHOLDS"], "stats"
        )
        self.validate_lists_of_numbers("PERCENTILES", "percentiles")
        self.validate_thresholds()
        self.validate_interpercentiles()
        self.validate_norm()

    def validate_options(self, options, option_name):
        for option in getattr(self, option_name):
            if option not in options:
                raise StatisticsVerticallyError(f"Invalid option name: {option} not in {options}")

    def validate_lists_of_numbers(self, stat, parameter):
        if stat in self.stats:
            if getattr(self, parameter) is None:
                raise StatisticsVerticallyError(f"{parameter} must be a list of ints or floats")

            if not isinstance(getattr(self, parameter), list):
                setattr(self, parameter, [getattr(self, parameter)])

            if np.array(getattr(self, parameter)).dtype not in ["int64", "float64"]:
                raise StatisticsVerticallyError(f"{parameter} must be a list of ints or floats")

            if not len(getattr(self, parameter)):
                raise StatisticsVerticallyError(f"{parameter} must have a length of at least 1")

    def validate_norm(self):
        if "NORMTHRESHOLDS" in self.stats:
            if self.norm_operators is None:
                raise StatisticsVerticallyError(f"norm_operators must be a list of strings")

            if not isinstance(self.norm_operators, list):
                self.norm_operators = [self.norm_operators]

            if self.norm_nomvars is None:
                raise StatisticsVerticallyError(f"norm_nomvars must be a list of strings")

            if not isinstance(self.norm_nomvars, list):
                self.norm_nomvars = [self.norm_nomvars]

            if ~np.all([isinstance(v, str) for v in self.norm_operators]):
                raise StatisticsVerticallyError(f"norm_operators must be a list of strings")

            if ~np.all([isinstance(v, str) for v in self.norm_nomvars]):
                raise StatisticsVerticallyError(f"norm_nomvars must be a list of strings")

            if len(self.norm_operators) != len(self.norm_nomvars):
                raise StatisticsVerticallyError(f"norm_operators and norm_nomvars must be of same lenght")

            self.validate_options(["LT", "LE", "EQ", "GE", "GT", "NE"], "norm_operators")

            for nomvar in self.norm_nomvars:
                if nomvar not in self.no_meta_df.nomvar.unique():
                    raise StatisticsVerticallyError(f"norm_nomvars must be present in dataframe")

    def validate_thresholds(self):
        self.validate_lists_of_numbers("THRESHOLDS", "threshold_values")
        if "THRESHOLDS" in self.stats:
            if self.threshold_operators is None:
                raise StatisticsVerticallyError(f"threshold_operators must be a list of strings")

            if not isinstance(self.threshold_operators, list):
                self.threshold_operators = [self.threshold_operators]

            if ~np.all([isinstance(v, str) for v in self.threshold_operators]):
                raise StatisticsVerticallyError(f"threshold_operators must be a list of strings")

            if len(self.threshold_operators) != len(self.threshold_values):
                raise StatisticsVerticallyError(f"threshold_values and threshold_operators must be of same lenght")

            self.validate_options(["LT", "LE", "EQ", "GE", "GT", "NE"], "threshold_operators")

    def validate_interpercentiles(self):
        if "INTERPERCENTILES" in self.stats:
            if self.interpercentiles_lower is None:
                raise StatisticsVerticallyError(f"interpercentiles_lower must be a list of numbers")
            if self.interpercentiles_upper is None:
                raise StatisticsVerticallyError(f"interpercentiles_upper must be a list of numbers")

            self.validate_lists_of_numbers("INTERPERCENTILES", "interpercentiles_lower")
            self.validate_lists_of_numbers("INTERPERCENTILES", "interpercentiles_upper")

            if len(self.interpercentiles_lower) != len(self.interpercentiles_upper):
                raise StatisticsVerticallyError(
                    f"interpercentiles_lower and interpercentiles_upper must be of same lenght"
                )

    def INTERPERCENTILES(self, df) -> pd.DataFrame:
        array_3d = get_3d_array(df)
        df_list = []
        for pl, pu in zip(self.interpercentiles_lower, self.interpercentiles_upper):
            new_etiket = create_etiket(
                df, "".join([STATS["INTERPERCENTILES"], str(remove_decimals(pl))[:2], str(remove_decimals(pu))[:2]])
            )
            res_df = create_empty_result(df, {"label": new_etiket})
            plres = np.percentile(array_3d, pl, axis=0)
            pures = np.percentile(array_3d, pu, axis=0)
            res = pures - plres
            res_df["d"] = [res]
            df_list.append(res_df)
        res_df = pd.safe_concat(df_list)
        return res_df

    def THRESHOLDS(self, df) -> pd.DataFrame:
        array_3d = get_3d_array(df)
        df_list = []
        for op, val in zip(self.threshold_operators, self.threshold_values):
            new_etiket = create_etiket(df, "".join([op, str(remove_decimals(val))]))
            res_df = create_empty_result(df, {"label": new_etiket, "unit": "%"})
            if op == "LT":
                tresh = np.sum(array_3d < val, axis=0) * 100.0 / array_3d.shape[0]
            elif op == "LE":
                tresh = np.sum(array_3d <= val, axis=0) * 100.0 / array_3d.shape[0]
            elif op == "EQ":
                tresh = np.sum(array_3d == val, axis=0) * 100.0 / array_3d.shape[0]
            elif op == "GE":
                tresh = np.sum(array_3d >= val, axis=0) * 100.0 / array_3d.shape[0]
            elif op == "GT":
                tresh = np.sum(array_3d > val, axis=0) * 100.0 / array_3d.shape[0]
            elif op == "NE":
                tresh = np.sum(array_3d != val, axis=0) * 100.0 / array_3d.shape[0]
            res_df["d"] = [tresh]

            df_list.append(res_df)

        res_df = pd.safe_concat(df_list)
        return res_df

    def PERCENTILES(self, df) -> pd.DataFrame:
        array_3d = get_3d_array(df)
        df_list = []
        for p in self.percentiles:
            new_etiket = create_etiket(df, "".join([STATS["PERCENTILES"], str(remove_decimals(p))]))
            res_df = create_empty_result(df, {"label": new_etiket})
            df_list.append(res_df)
        res_df = pd.safe_concat(df_list)
        res = np.percentile(array_3d, self.percentiles, axis=0)
        res_df["d"] = np.split(res, res.shape[0])
        return res_df

    def STD(self, df) -> pd.DataFrame:
        new_etiket = create_etiket(df, STATS["STD"])
        array_3d = get_3d_array(df)
        res_df = create_empty_result(df, {"label": new_etiket})
        res = np.std(array_3d, axis=0, ddof=1)
        res_df["d"] = [res]
        return res_df

    def MEAN(self, df) -> pd.DataFrame:
        new_etiket = create_etiket(df, STATS["MEAN"])

        array_3d = get_3d_array(df)
        res_df = create_empty_result(df, {"label": new_etiket})
        res = np.mean(array_3d, axis=0)
        res_df["d"] = [res]
        return res_df

    def compute(self) -> pd.DataFrame:
        logging.info("StatisticsVertically - compute")
        df_list = []
        for (grid, nomvar, forecast_hour), nomvar_df in self.groups:
            # print(nomvar_df.drop(columns='d'))
            # print(fstpy.compute(nomvar_df)[fstpy.BASE_COLUMNS].to_string())
            for stat in self.stats:
                res_df = getattr(self, stat)(fstpy.compute(nomvar_df))

                df_list.append(res_df)

        return self.final_results(df_list, StatisticsVerticallyError, copy_input=False)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=StatisticsVertically.__name__, parents=[Plugin.base_parser], add_help=False)
        parser.add_argument(
            "--outputFieldName",
            type=str,
            dest="nomvar_out",
            help="Option to give the output field a different name from the input field name.",
        )
        parser.add_argument(
            "--direction",
            required=True,
            type=str,
            default="ASCENDING",
            choices=["ASCENDING", "DESCENDING"],
            help="Direction of vertical iteration.",
        )

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg["direction"] = parsed_arg["direction"].lower()

        if parsed_arg["nomvar_out"] is not None:
            validate_nomvar(parsed_arg["nomvar_out"], "StatisticsVertically", StatisticsVerticallyError)

        return parsed_arg


def get_etiket_parts(df):
    _, run, implementation, _ = fstpy.get_parsed_etiket(df.iloc[0].etiket)
    return run, implementation


def create_etiket(df, prod):
    run, implementation = get_etiket_parts(df)
    new_etiket = "".join([run, prod])
    new_etiket = "".join([f"{new_etiket:_<8}", implementation, "ALL"])
    return new_etiket


def remove_decimals(p):
    pvalue = int(p) if float(p) == int(p) else p
    return pvalue
