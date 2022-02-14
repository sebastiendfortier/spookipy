# -*- coding: utf-8 -*-
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..science import vt_from_qv
from ..utils import (create_empty_result, final_results,
                     get_dependencies,  get_existing_result, get_from_dataframe)

class TemperatureVirtualError(Exception):
    pass

class TemperatureVirtual(Plugin):
    """Calculates the virtual temperature as a function of temperature and water vapour mixing ratio.

    :param df: input DataFrame  
    :type df: pd.DataFrame  
    """
    def __init__(
        self,
        df: pd.DataFrame
        ):

        self.plugin_mandatory_dependencies = [
            {
                'TT': {'nomvar': 'TT'},
                'QV': {'nomvar': 'QV'}
            }
        ]

        self.plugin_result_specifications = {
                'VT': {
                'nomvar': 'VT',
                'etiket': 'VIRTT',
                'unit': 'celsius',
                'nbits': 16,
                'datyp': 1}}

        self.df = fstpy.metadata_cleanup(df)

        super().__init__(df)
        self.prepare_groups()

    def prepare_groups(self):

        self.no_meta_df = fstpy.add_columns(self.no_meta_df, 
                columns=[
                'unit', 'forecast_hour', 'ip_info'])

        self.nomvar_groups = self.no_meta_df.groupby(by=['grid', 'datev','ip1_kind'])

        self.dependencies_list = get_dependencies(
            self.nomvar_groups,
            self.meta_df,
            'TemperatureVirtual',
            self.plugin_mandatory_dependencies,
            intersect_levels=True)

    def compute(self, test_dependency = False) -> pd.DataFrame:
        logging.info('TemperatureVirtual - compute')
 
        # check if result already exists
        self.existing_result_df = get_existing_result(
            self.no_meta_df, self.plugin_result_specifications)

        df_list=[]
        for dependencies_df, option in self.dependencies_list:

            qv_df = get_from_dataframe(dependencies_df, 'QV')
            tt_df = get_from_dataframe(dependencies_df, 'TT')

            vt_df = create_empty_result(
                qv_df,
                self.plugin_result_specifications['VT'],
                all_rows=True)

            tt_kelvin_df = fstpy.unit_convert(tt_df, 'kelvin')
            qv_kgkg_df   = fstpy.unit_convert(qv_df, 'kilogram_per_kilogram')

            for i in qv_kgkg_df.index:
                qvkgkg = qv_kgkg_df.at[i, 'd']
                tt_k   = tt_kelvin_df.at[i, 'd']
                vt_df.at[i, 'd'] = vt_from_qv(tt=tt_k, qv=qvkgkg).astype(np.float32)
    
            df_list.append(vt_df)

        return final_results(df_list, TemperatureVirtualError, self.meta_df)
