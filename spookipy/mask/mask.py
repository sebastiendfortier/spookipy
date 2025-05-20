# -*- coding: utf-8 -*-
import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin, PluginParser
from ..utils import create_empty_result, initializer, validate_nomvar
from ..configparsingutils import preprocess_negative_args, apply_lambda_to_list


class MaskError(Exception):
    pass


class Mask(Plugin):
    """This plug-in creates a mask according to the threshold value(s) given.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param thresholds: List of threshold values to take into account., defaults to None
    :type thresholds: list(float), optional
    :param values: List of values the mask will take (will be used in the same order as the threshold values), defaults to None
    :type values: list(float), optional
    :param operators: List of comparison operators (will be used in the same order as the threshold values), defaults to None
    :type operators: list(str), optional
    :param nomvar_out: nomvar for output result, defaults to None
    :type nomvar_out: str, optional
    """

    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        thresholds=None,
        values=None,
        operators=None,
        nomvar_out=None,
        binary_mask=False,
        reduce_df=True,
    ):
        self.plugin_result_specifications = {"ALL": {"label": "MASK"}}
        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.validate_params()

    def validate_params(self):
        if self.nomvar_out is not None:
            self.groups = self.no_meta_df.groupby(["grid", "datev", "dateo", "level"])
            for _, current_group in self.groups:
                if len(current_group.index) > 1:
                    raise MaskError(' More than one input field, cannot use "nomvar_out" ')

        length = len(self.thresholds)
        if not all(len(lst) == length for lst in [self.values, self.operators]):
            raise MaskError("Threshholds, values and operators lists, must have the same lenght")

        ops = [">", ">=", "==", "<=", "<", "!="]
        for op in self.operators:
            if op not in ops:
                raise MaskError(f"Operators must have values included in {ops} {op} is an invalid entry\n")

        if self.binary_mask:
            if not all(x in {0.0, 1.0} for x in self.values):
                raise MaskError("When creating a binary mask, all values must be either 0.0 or 1.0")

    def compute(self) -> pd.DataFrame:
        df_list = []

        res_df = create_empty_result(self.no_meta_df, self.plugin_result_specifications["ALL"], all_rows=True)

        if self.binary_mask:
            res_df = fstpy.add_flag_values(res_df)
            res_df.masks = True
            res_df["datyp"] = 2  # Pour correspondre a I1
            res_df["nbits"] = 1

        if self.nomvar_out is not None:
            res_df["nomvar"] = self.nomvar_out

        df_list = apply_mask(res_df, self.values[::-1], self.operators[::-1], self.thresholds[::-1])

        return self.final_results(df_list, MaskError, copy_input=False, reduce_df=self.reduce_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=Mask.__name__, parents=[Plugin.base_parser], add_help=False)
        parser.add_argument(
            "--thresholds", type=str, required=True, help="List of threshold values to take into account."
        )
        parser.add_argument(
            "--values",
            type=str,
            required=True,
            help="List of values the mask will take (will be used in the same order as the threshold values).",
        )
        parser.add_argument(
            "--operators",
            type=str,
            required=True,
            help="List of comparison operators (will be used in the same order as the threshold values).",
        )
        parser.add_argument(
            "--outputFieldName",
            dest="nomvar_out",
            type=str,
            help="Option to give the output field a different name from the input field name (works only with 1 input field).",
        )
        parser.add_argument(
            "--binaryMask",
            dest="binary_mask",
            action="store_true",
            default=False,
            help="Set TypeOfField to MASK (typvar = @@). When using --binaryMask, all values of --values must be 0.0 or 1.0",
        )

        parsed_arg = vars(parser.parse_args(preprocess_negative_args(args.split(), ["--thresholds", "--values"])))

        if parsed_arg["nomvar_out"] is not None:
            validate_nomvar(parsed_arg["nomvar_out"], "Mask", MaskError)

        op_dict = {"GT": ">", "GE": ">=", "EQ": "==", "LE": "<=", "LT": "<", "NE": "!="}
        parsed_arg["operators"] = apply_lambda_to_list(parsed_arg["operators"].split(","), lambda a: op_dict[a])
        parsed_arg["values"] = apply_lambda_to_list(parsed_arg["values"].split(","), lambda a: float(a))
        parsed_arg["thresholds"] = apply_lambda_to_list(parsed_arg["thresholds"].split(","), lambda a: float(a))

        return parsed_arg


def lt(value, threshold):
    return value < threshold


def le(value, threshold):
    return value <= threshold


def eq(value, threshold):
    return (value >= threshold - 0.4) & (value <= threshold + 0.4)


def ge(value, threshold):
    return value >= threshold


def gt(value, threshold):
    return value > threshold


def ne(value, threshold):
    return value != threshold


def apply_mask(df, values, operators, thresholds):
    ops = {">": gt, ">=": ge, "==": eq, "<=": le, "<": lt, "!=": ne}

    results = []
    for row in df.itertuples():
        df.at[row.Index, "d"] = process_array(values, operators, thresholds, ops, df.at[row.Index, "d"]).astype(
            "float32"
        )

    results.append(df)

    return results


def process_array(values, operators, thresholds, ops, arr):
    for i in range(len(operators) - 1, -1, -1):
        if i == len(operators) - 1:
            a = np.where(ops[operators[i]](arr, thresholds[i]), values[i], 0.0)
        else:
            a = np.where(ops[operators[i]](arr, thresholds[i]), values[i], a)
    return a
