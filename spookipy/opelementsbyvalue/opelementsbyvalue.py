# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, initializer, validate_nomvar)


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
    :param unit: unit to apply to results, defaults to 'scalar'
    :type unit: str, optional
    :param label: label to apply to results, defaults to None (keep the same label)
    :type label: str, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            operator,
            value,
            operation_name='OpElementsByValue',
            exception_class=OpElementsByValueError,
            nomvar_out=None,
            unit='scalar',
            label=None):

        if self.label is None:
            self.label = self.operation_name

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)

        self.prepare_groups()

    def prepare_groups(self):
 
        if not (self.nomvar_out is None):
            validate_nomvar(
                self.nomvar_out,
                self.operation_name,
                self.exception_class)

        if not (self.nomvar_out is None):
            self.plugin_result_specifications = {
                'ALL': {
                    'nomvar': self.nomvar_out,
                    'unit'  : self.unit
                    }
                }
        else:
            self.plugin_result_specifications = {
                'ALL': {'unit': self.unit}}
            
        if self.label:
            self.plugin_result_specifications["ALL"]["label"] = self.label

    def compute(self) -> pd.DataFrame:
        logging.info('OpElementsByValue - compute')
        df_list = []
        res_df = create_empty_result(
            self.no_meta_df,
            self.plugin_result_specifications['ALL'],
            all_rows=True)

        res_df['d'] = self.operator(res_df['d'], self.value)
        df_list.append(res_df)

        return self.final_results(df_list, self.exception_class, copy_input=False)
