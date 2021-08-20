# -*- coding: utf-8 -*-
from ..utils import create_empty_result, get_existing_result, get_plugin_dependencies, existing_results, final_results
from ..plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
import numpy as np
import sys

class GeorgeKIndexError(Exception):
    pass

def george_k_index(tt850:np.ndarray, tt700:np.ndarray, tt500:np.ndarray, td850:np.ndarray, td700:np.ndarray) -> np.ndarray:
    return (tt850 - tt500) + td850 - (tt700 - td700)


class GeorgeKIndex(Plugin):
    plugin_mandatory_dependencies = {
        'TT1':{'nomvar':'TT','unit':'celsius','level':500,'ip1_pkind':'mb','select_only':True},
        'TT2':{'nomvar':'TT','unit':'celsius','level':700,'ip1_pkind':'mb','select_only':True},
        'TT3':{'nomvar':'TT','unit':'celsius','level':850,'ip1_pkind':'mb','select_only':True},
        'TD1':{'nomvar':'TD','unit':'celsius','level':700,'ip1_pkind':'mb'},
        'TD2':{'nomvar':'TD','unit':'celsius','level':850,'ip1_pkind':'mb'},
    }
    plugin_result_specifications = {
        'KI':{'nomvar':'KI','etiket':'GEORKI','unit':'scalar','ip1':0}
        }

    def __init__(self,df:pd.DataFrame):
        self.df = df
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise GeorgeKIndexError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])
        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,{'ice_water_phase':'water'},self.plugin_mandatory_dependencies)
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('GeorgeKIndex',self.existing_result_df,self.meta_df)

        sys.stdout.write('GeorgeKIndex - compute\n')
        df_list=[]
        for _,current_fhour_group in self.fhour_groups:
            current_fhour_group = fstpy.load_data(current_fhour_group)
            tt850_df = current_fhour_group.loc[(current_fhour_group.nomvar=='TT') & (current_fhour_group.level==850)].reset_index(drop=True)
            tt700_df = current_fhour_group.loc[(current_fhour_group.nomvar=='TT') & (current_fhour_group.level==700)].reset_index(drop=True)
            tt500_df = current_fhour_group.loc[(current_fhour_group.nomvar=='TT') & (current_fhour_group.level==500)].reset_index(drop=True)
            td850_df = current_fhour_group.loc[(current_fhour_group.nomvar=='TD') & (current_fhour_group.level==850)].reset_index(drop=True)
            td700_df = current_fhour_group.loc[(current_fhour_group.nomvar=='TD') & (current_fhour_group.level==700)].reset_index(drop=True)
            if tt850_df.empty or tt700_df.empty or tt500_df.empty or td850_df.empty or td700_df.empty:
                continue
            ki_df = create_empty_result(tt850_df,self.plugin_result_specifications['KI'])

            for i in ki_df.index:
                ki_df.at[i,'d'] = george_k_index(tt850_df.at[i,'d'],tt700_df.at[i,'d'],tt500_df.at[i,'d'],td850_df.at[i,'d'],td700_df.at[i,'d'])
            df_list.append(ki_df)

        return final_results(df_list, GeorgeKIndexError, self.meta_df)
