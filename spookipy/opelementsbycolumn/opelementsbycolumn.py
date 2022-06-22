# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, final_results, get_3d_array,
                     initializer, validate_nomvar)


class OpElementsByColumnError(Exception):
    pass


class OpElementsByColumn(Plugin):
    """Generic plugin used by other plugins to apply specific operations on a column of data

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    :param operator: function to apply on a column of data
    :type operator: function
    :param operation_name: name of operation do display for logging, defaults to 'OpElementsByColumn'
    :type operation_name: str, optional
    :param exception_class: exception to raise, defaults to OpElementsByColumnError
    :type exception_class: type, optional
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param group_by_level: group fields by level, defaults to False
    :type group_by_level: bool, optional
    :param nomvar_out: nomvar to apply to results, defaults to None
    :type nomvar_out: str, optional
    :param unit: unit to apply to results, defaults to 'scalar'
    :type unit: str, optional
    :param etiket: etiket to apply to results, defaults to None
    :type etiket: str, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            operator,
            operation_name='OpElementsByColumn',
            exception_class=OpElementsByColumnError,
            group_by_forecast_hour=False,
            group_by_level=False,
            nomvar_out=None,
            unit='scalar',
            etiket=None):

        if self.etiket is None:
            self.etiket = self.operation_name
        self.validate_input()
        self.plugin_result_specifications = {
            'ALL': {
                'nomvar': self.nomvar_out,
                'etiket': self.operation_name,
                'unit': self.unit}}

    def validate_input(self):
        if self.df.empty:
            raise self.exception_class(
                self.operation_name + ' - no data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        validate_nomvar(
            self.nomvar_out,
            self.operation_name,
            self.exception_class)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        if len(self.df) == 1:
            raise self.exception_class(
                self.operation_name +
                ' - not enough records to process, need at least 2')

        self.df = fstpy.add_columns(
            self.df, columns=[
                'forecast_hour', 'ip_info'])

        grouping = ['grid']
        if self.group_by_forecast_hour:
            grouping.append('dateo')
            grouping.append('forecast_hour')
        if self.group_by_level:
            grouping.append('level')

        self.groups = self.df.groupby(by=grouping)

    def compute(self) -> pd.DataFrame:
        logging.info('OpElementsByColumn - compute')
        # holds data from all the groups
        df_list = []
        for _, current_group in self.groups:

            current_group.sort_values(by=['nomvar', 'dateo', 'forecast_hour'], inplace=True)
            if len(current_group.index) == 1:
                logging.warning(
                    'need more than one field for this operation - skipping')
                continue

            res_df = create_empty_result(current_group, self.plugin_result_specifications['ALL'])

            array_3d = get_3d_array(current_group)

            res_df.at[0, 'd'] = self.operator(array_3d, axis=0).astype(np.float32)

            df_list.append(res_df)

        return final_results(df_list, self.exception_class, self.meta_df)
