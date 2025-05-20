# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import create_empty_result, initializer, validate_nomvar


class OpElementsByValueError(Exception):
    pass


class OpElementsByValue(Plugin):
    """Generic plugin used by other plugins to apply specific operations with a value as parameter on a point of data

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param operator: function to apply on a column of data
    :type operator: function
    :param value: value needed by function
    :type value: float
    :param operation_name: name of operation do display for logging, defaults to 'OpElementsByValue'
    :type operation_name: str, optional
    :param exception_class: exception to raise, defaults to OpElementsByValueError
    :type exception_class: type, optional
    :param nomvar_out: nomvar to apply to results, defaults to None
    :type nomvar_out: str, optional
    :param unit: unit to apply to results, defaults to '1' (dimensionless)
    :type unit: str, optional
    :param label: label to apply to results, defaults to None (keep the same label)
    :type label: str, optional
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """

    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        operator,
        value,
        operation_name="OpElementsByValue",
        exception_class=OpElementsByValueError,
        nomvar_out=None,
        unit="1",
        label=None,
        reduce_df=True,
    ):
        self.plugin_result_specifications = {"ALL": {"unit": self.unit}}

        if self.nomvar_out is not None:
            validate_nomvar(self.nomvar_out, self.operation_name, self.exception_class)
            self.plugin_result_specifications["ALL"]["nomvar"] = self.nomvar_out

        if self.label:
            self.plugin_result_specifications["ALL"]["label"] = self.label

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
        if self.nomvar_out is not None:
            self.groups = self.no_meta_df.groupby(["grid", "datev", "dateo", "level"])
            for _, current_group in self.groups:
                if len(current_group.index) > 1:
                    raise self.exception_class(
                        self.operation_name + ' - more than one input field, cannot use "nomvar_out" '
                    )

    def compute(self) -> pd.DataFrame:
        logging.info("OpElementsByValue - compute")
        df_list = []
        res_df = create_empty_result(self.no_meta_df, self.plugin_result_specifications["ALL"], all_rows=True)

        res_df["d"] = self.operator(res_df["d"], self.value)
        df_list.append(res_df)

        return self.final_results(df_list, self.exception_class, copy_input=False, reduce_df=self.reduce_df)
