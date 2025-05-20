# -*- coding: utf-8 -*-
import logging
import fstpy
import numpy as np
import pandas as pd
import numexpr as ne
from typing import List

from ..plugin import Plugin, PluginParser
from ..utils import (
    create_empty_result,
    get_3d_array,
    find_intersecting_levels,
    initializer,
    validate_nomvar,
    spooki_unit_to_cf_unit,
)


class FlatField:
    """
    Class to handle 3D array data from a pandas DataFrame.

    This class takes a pandas DataFrame representing field data and
    transforms it into a flat 1D array for easier manipulation, while
    also storing the original shape of the data for later reconstruction.

    Args:
        field_df (pd.DataFrame): Input DataFrame containing the field data and metadata.
        empty (bool, optional): If True, initialize array1d to None. Defaults to False.

    Attributes:
        row (dict): The first row of the input dataframe, converted to a dictionary.
        levels (numpy.ndarray): A array containing the level values from the input dataframe.
        shape (tuple): The original shape of the 3D array that was flattened to create this object.
        array1d (numpy.ndarray or None): The flat, 1D array representation of the field data (the d column).
    """

    def __init__(self, field_df: pd.DataFrame, empty: bool = False):
        self.row = field_df.iloc[0].to_dict()
        self.row["d"] = None

        self.levels = field_df["level"].values

        if not empty:
            array3d = get_3d_array(field_df)
            self.shape = array3d.shape
            self.array1d = array3d.ravel()
        else:
            self.shape = get_3d_array(field_df).shape
            self.array1d = None

    def __str__(self) -> str:
        row_str = {key: self.row[key] for key in ["nomvar", "typvar", "ni", "nj", "nk", "ip1", "level"]}
        return f"row     : {row_str}\nshape   : {self.shape}\nlevels  : {self.levels}\narray1d : {self.array1d}"

    def get_nomvar(self) -> str:
        return self.row["nomvar"]

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert the FlatField object back into a pandas DataFrame.

        Returns:
            pd.DataFrame: The reconstructed DataFrame containing the field data and metadata.

        Raises:
            ValueError: If the dtype of self.array1d is not a subdtype of numpy.integer or numpy.floating.
        """

        array3d = self.array1d.reshape(self.shape)

        data = []
        for i, values in enumerate(array3d):
            tmp_row = self.row.copy()
            tmp_row["level"] = self.levels[i]

            if np.issubdtype(array3d.dtype, np.integer):
                tmp_row["datyp"] = 2
                tmp_row["d"] = values.astype(np.int32)
            elif np.issubdtype(array3d.dtype, np.floating):
                tmp_row["datyp"] = 5
                tmp_row["d"] = values.astype(np.float32)
            else:
                raise ValueError("Unsupported dtype for array1d")

            data.append(tmp_row)
        return pd.DataFrame(data)


class CalculatorError(Exception):
    pass


class Calculator(Plugin):
    """
    Simple calculator plugin that performs arithmetic operations on input fields and returns the results.

    Args:
        df (pd.DataFrame): The input dataframe to perform calculations on.
        expression (str): String containing a mathematical expression to be evaluated, consisting of nomvars from the input DataFrame.
        nomvar_out (str, optional): The nomvar for the output result. Defaults to "RSLT".
        unit (str, optional): Unit to apply to results. Defaults to "1".
        copy_input (bool, optional): Indicates that the input fields will be returned with the plugin results. Defaults to False.
        reduce_df (bool, optional): Whether or not to to reduce the dataframe to its minimum. Defaults to True.

    Raises:
        CalculatorError: If there is a problem with the calculation
    """

    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        expression: str,
        nomvar_out: str = "RSLT",
        unit: str = "1",
        copy_input: bool = False,
        reduce_df: bool = True,
    ):
        validate_nomvar(self.nomvar_out, "Calculator", CalculatorError)

        self.plugin_result_specifications = {
            "ALL": {"nomvar": self.nomvar_out, "unit": self.unit, "label": "CALCUL", "nbits": 32}
        }

        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=["ip_info", "etiket"])

        grouping = ["grid", "dateo", "datev"]

        # group by ensemble_member if the dataframe only contain fields with ensemble_member
        if self.no_meta_df["ensemble_member"].notnull().all():
            grouping.extend(["ensemble_member"])

        self.groups = self.no_meta_df.groupby(by=grouping)

    @staticmethod
    def _get_first_df(df_group: pd.core.groupby.DataFrameGroupBy) -> pd.DataFrame:
        return next(iter(df_group))[1]

    @staticmethod
    def _compute_group(fields: List[FlatField], expression: str) -> np.ndarray:
        """
        Compute an expression on a group of FlatFields.

        Evaluates the expression using the 1D arrays from the provided FlatField objects as operands,
        and returns the result as a numpy array.

        Args:
            fields (List[FlatField]): List of FlatField objects containing arrays to be used in computation.
            expression (str): Mathematical expression with nomvars from FlatFields.

        Returns:
            np.ndarray: Result of the computed expression as a numpy array.

        Raises:
            CalculatorError: If there is a missing nomvar or syntax error in the expression.

        Example:
            >>> fields = [FlatField(uu_df), FlatField(vv_df)]
            >>> expression = "UU + VV"
            >>> result = Calculator._compute_group(fields, expression)
        """

        operand_dict = {field.get_nomvar(): field.array1d for field in fields}

        try:
            return ne.evaluate(expression, local_dict=operand_dict)
        except KeyError as e:
            logging.error(
                f"Missing nomvar {e}. Make sure all groups that will be formed will contains the nomvar that appear in the expression. \
                            \nexpression: {expression} \
                            \n\ncurrent group:\n {operand_dict.keys()}"
            )
            raise CalculatorError(f"A field with nomvar {e} is in the expression but not in the dataframe.")
        except SyntaxError as e:
            raise CalculatorError(f"SyntaxError in expression '{expression}'\n{e}")

    def compute(self) -> pd.DataFrame:
        logging.info("Calculator - compute")

        df_list = []
        for _, current_group in self.groups:
            # only keep intersecting levels
            current_group = find_intersecting_levels(current_group)
            if current_group.empty:
                logging.warning(
                    f"\n\nNo common levels for this group: \n{current_group[['nomvar', 'typvar', 'ni', 'nj', 'nk', 'ip1']]} \n"
                )
                continue

            current_group_by_nomvar = current_group.groupby("nomvar")

            # create an empty result (FlatField)
            res_ff = FlatField(
                create_empty_result(
                    self._get_first_df(current_group_by_nomvar), self.plugin_result_specifications["ALL"], all_rows=True
                ),
                empty=True,
            )

            # get all operands (list of FlatFields)
            operand_list = []
            for _, nomvar_df in current_group_by_nomvar:
                operand_list.append(FlatField(nomvar_df))

            # do the actual computation
            res_ff.array1d = self._compute_group(operand_list, self.expression)

            # accumulate results
            df_list.append(res_ff.to_dataframe())

        return self.final_results(df_list, CalculatorError, copy_input=self.copy_input, reduce_df=self.reduce_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """
        Method to translate spooki plugin parameters to python plugin parameters

        Args:
            args (str): input unparsed arguments

        Returns:
            dict: a dictionnary of converted parameters
        """
        parser = PluginParser(prog=Calculator.__name__, parents=[Plugin.base_parser], add_help=False)
        parser.add_argument("--expression", required=True, type=str, help="Mathematical expression to evaluate.")
        parser.add_argument(
            "--outputFieldName",
            type=str,
            default="RSLT",
            dest="nomvar_out",
            help="Option to change the name of output field (default: 'RSLT').",
        )
        parser.add_argument(
            "--unit", type=str, default="scalar", help="Unit to apply to the output field (default: 'scalar')."
        )

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg["nomvar_out"]:
            validate_nomvar(parsed_arg["nomvar_out"], "Calculator", CalculatorError)

        if parsed_arg["unit"]:
            parsed_arg["unit"] = spooki_unit_to_cf_unit(parsed_arg["unit"], "Calculator", CalculatorError)

        return parsed_arg
