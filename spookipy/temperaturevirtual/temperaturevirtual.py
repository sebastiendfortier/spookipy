# -*- coding: utf-8 -*-
import logging

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..science import vt_from_qv
from ..utils import (create_empty_result, final_results, existing_results,
                     get_dependencies,  get_existing_result, get_from_dataframe,
                     initializer, DependencyError)

class TemperatureVirtualError(Exception):
    pass

class TemperatureVirtual(Plugin):
    """Calculates the virtual temperature as a function of temperature and water vapour mixing ratio.

    :param df: input DataFrame  
    :type df: pd.DataFrame 
    :param dependency_check: Indicates the plugin is being called from another one who checks dependencies , defaults to False
    :type dependency_check: bool, optional   
    """
    nomvar = "VT"
    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        dependency_check=False
        ):

        self.plugin_mandatory_dependencies = [
            {
                'TT': {'nomvar': 'TT', 'unit': 'kelvin'},
                'QV': {'nomvar': 'QV', 'unit': 'kilogram_per_kilogram'}
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
                columns=['unit', 'forecast_hour', 'ip_info'])

        self.nomvar_groups = self.no_meta_df.groupby(by=['grid', 'datev','ip1_kind'])

        # check if result already exists
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'TemperatureVitrual',
                self.existing_result_df,
                self.meta_df)

        logging.info('TemperatureVirtual - compute')

        df_list=[]
        try:
            self.dependencies_list = get_dependencies(
                self.nomvar_groups,
                self.meta_df,
                'TemperatureVirtual',
                self.plugin_mandatory_dependencies,
                intersect_levels=True)
        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f'{TemperatureVirtual} - No matching dependencies found')
        else:
  
            for dependencies_df, option in self.dependencies_list:

                qvkgkg_df = get_from_dataframe(dependencies_df, 'QV')
                ttk_df    = get_from_dataframe(dependencies_df, 'TT')

                vt_df = create_empty_result(
                    qvkgkg_df,
                    self.plugin_result_specifications['VT'],
                    all_rows=True)

                for i in qvkgkg_df.index:
                    qvkgkg = qvkgkg_df.at[i, 'd']
                    ttk   = ttk_df.at[i, 'd']
                    vt_df.at[i, 'd'] = vt_from_qv(tt=ttk, qv=qvkgkg).astype(np.float32)
        
                df_list.append(vt_df)
        finally:
            return final_results(df_list, TemperatureVirtualError, self.meta_df, self.dependency_check)
