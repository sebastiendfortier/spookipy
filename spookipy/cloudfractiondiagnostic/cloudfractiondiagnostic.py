# -*- coding: utf-8 -*-
from ..utils import create_empty_result, get_existing_result, get_plugin_dependencies, existing_results, final_results, initializer
from ..plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
import sys
import numpy as np
import math


def calc_diagnostic_cloud_fraction_threshold(level):
    return 1 - 2 * level + math.pow(level, 2) + math.pow(level, 3) + math.sqrt(3.0) * level * (1 - 3 * level + 2 * math.pow(level, 2))

def calc_diagnostic_cloud_fraction(hr,threshold):
    cld = np.full_like(hr, -1,dtype=np.float32)
    cld = np.where(hr <= threshold, 0, cld)
    cld = np.where((threshold < hr) & (hr < 1), ((hr - threshold) / (1 - threshold))**2, cld)
    cld = np.where(hr >= 1, 1, cld)
    return cld.astype(np.float32)

class CloudFractionDiagnosticError(Exception):
    pass

class CloudFractionDiagnostic(Plugin):

    @initializer
    def __init__(self,df:pd.DataFrame,use_constant=None):
        self.plugin_mandatory_dependencies = {
            'HR':{'nomvar':'HR','unit':'scalar','select_only':True},
        }

        self.plugin_result_specifications = {
            'CLD':{'nomvar':'CLD','etiket':'CloudFractionDiagnostic','unit':'scalar'}
        }

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise CloudFractionDiagnosticError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])

        # print(self.df[['nomvar','typvar','etiket','unit','surface','grid','forecast_hour']].sort_values(by=['grid','nomvar']).to_string())
        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,None,self.plugin_mandatory_dependencies)
            self.groups = self.dependencies_df.groupby(['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('CloudFractionDiagnostic',self.existing_result_df,self.meta_df)

        sys.stdout.write('CloudFractionDiagnostic - compute\n')
        df_list=[]
        for _, group in self.groups:
            group = fstpy.load_data(group)

            cld_df = create_empty_result(group,self.plugin_result_specifications['CLD'],copy=True)

            if not (self.use_constant is None):
                for  i in cld_df.index:
                    cld_df.at[i,'d'] = np.full_like(cld_df.at[i,'d'],0.8,dtype=np.float32)
            else:
                for  i in cld_df.index:
                    level = cld_df.at[i,'level']
                    hr = np.copy(cld_df.at[i,'d'])
                    threshold = calc_diagnostic_cloud_fraction_threshold(level)
                    cld_df.at[i,'d'] = calc_diagnostic_cloud_fraction(hr,threshold)

            df_list.append(cld_df)

        return final_results(df_list, CloudFractionDiagnosticError, self.meta_df)
