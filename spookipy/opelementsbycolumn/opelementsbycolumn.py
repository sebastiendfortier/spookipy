# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, get_3d_array,
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
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional 
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
            group_by_nomvar=False,
            nomvar_out=None,
            unit='scalar',
            etiket=None,
            copy_input=False):

        self.plugin_result_specifications = {
            'ALL': {
                'nomvar': self.nomvar_out,
                'etiket': self.operation_name,
                'unit'  : self.unit}}

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df, copy_input)

        if self.etiket is None:
            self.etiket = self.operation_name
        
        self.prepare_groups()

    def prepare_groups(self):

        validate_nomvar(
            self.nomvar_out,
            self.operation_name,
            self.exception_class)

        if len(self.no_meta_df) == 1:
            raise self.exception_class(
                self.operation_name +
                ' - not enough records to process, need at least 2')

        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=['forecast_hour', 'ip_info', 'unit'])

        grouping = ['grid']
        if self.group_by_nomvar:
            grouping.append('nomvar')  
        if self.group_by_forecast_hour:
            grouping.append('datev')
        if self.group_by_level:
            grouping.append('level')

        self.groups = self.no_meta_df.groupby(by=grouping)

    def compute(self) -> pd.DataFrame:
        logging.info('OpElementsByColumn - compute')
        # holds data from all the groups
        df_list = []
        for _, current_group in self.groups:

            # current_group.sort_values(by=['nomvar', 'dateo', 'forecast_hour'], inplace=True)
            current_group.sort_values(by=['nomvar', 'datev'], inplace=True)
            if len(current_group.index) == 1:
                logging.warning(
                    'need more than one field for this operation - skipping')
                continue

            if self.group_by_nomvar:
                self.plugin_result_specifications["ALL"]["nomvar"]         = current_group.iloc[0].nomvar
                self.plugin_result_specifications["ALL"]["ip2"]            = [0]
                self.plugin_result_specifications["ALL"]["forecast_hour"]  = [0]
                self.plugin_result_specifications["ALL"]["npas"]           = [0]

            res_df = create_empty_result(current_group, self.plugin_result_specifications['ALL'])
            
            array_3d = get_3d_array(current_group)

            res_df.at[0, 'd'] = self.operator(array_3d, axis=0).astype(np.float32)

            df_list.append(res_df)

        return self.final_results(df_list, self.exception_class)
