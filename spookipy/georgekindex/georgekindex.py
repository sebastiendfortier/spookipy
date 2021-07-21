# -*- coding: utf-8 -*-
from ..utils import create_empty_result, get_existing_result, get_plugin_dependencies, prepare_existing_results, remove_load_data_info
from ..plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
import numpy as np
import sys

class GeorgeKIndexError(Exception):
    pass

def george_k_index(tt850:np.ndarray, tt500:np.ndarray, td850:np.ndarray, tt700:np.ndarray, td700:np.ndarray) -> np.ndarray:
    return (tt850 - tt500) + td850 - (tt700 - td700)

class GeorgeKIndex(Plugin):
    plugin_requires = '(nomvar in ["TT","TD"]) and (level in [850,700,500]) and (ip1_pkind =="mb")' 
    plugin_mandatory_dependencies = {
        'TT1':{'nomvar':'TT','unit':'celsius','surface':500,'ip1_pkind':'mb'},
        'TT2':{'nomvar':'TT','unit':'celsius','surface':700,'ip1_pkind':'mb'},
        'TT3':{'nomvar':'TT','unit':'celsius','surface':850,'ip1_pkind':'mb'},
        'TD1':{'nomvar':'TD','unit':'celsius','surface':500,'ip1_pkind':'mb'},
        'TD2':{'nomvar':'TD','unit':'celsius','surface':700,'ip1_pkind':'mb'},
        'TD3':{'nomvar':'TD','unit':'celsius','surface':850,'ip1_pkind':'mb'},
    }
    plugin_result_specifications = {
        'KI':{'nomvar':'KI','etiket':'GeorgeKIndex','unit':'scalar'}
        }

    def __init__(self,df:pd.DataFrame):
        self.df = df
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise GeorgeKIndexError('No data to process') 

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])     
        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies)
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return prepare_existing_results('GeorgeKIndex',self.existing_result_df,self.meta_df)

        sys.stdout.write('GeorgeKIndex - compute')    
        df_list=[]
        for _,current_fhour_group in self.fhour_groups:
            current_fhour_group = fstpy.load_data(current_fhour_group)
            tt850_df = current_fhour_group.query( '(nomvar=="TT") and (level==850)').reset_index(drop=True)
            tt700_df = current_fhour_group.query( '(nomvar=="TT") and (level==700)').reset_index(drop=True)
            tt500_df = current_fhour_group.query( '(nomvar=="TT") and (level==500)').reset_index(drop=True)
            td850_df = current_fhour_group.query( '(nomvar=="TD") and (level==850)').reset_index(drop=True)
            td700_df = current_fhour_group.query( '(nomvar=="TD") and (level==700)').reset_index(drop=True)
            ki_df = create_empty_result(td700_df,self.plugin_result_specifications['KI'])

            ki_df.iloc[0]['d'] = george_k_index(tt850_df.iloc[0]['d'],tt500_df.iloc[0]['d'],td850_df.iloc[0]['d'],tt700_df.iloc[0]['d'],td700_df.iloc[0]['d'])
            df_list.append(ki_df)


        if not len(df_list):
            raise GeorgeKIndexError('No results were produced')

        self.meta_df = fstpy.load_data(self.meta_df)
        df_list.append(self.meta_df)    
        # merge all results together
        res_df = pd.concat(df_list,ignore_index=True)

        res_df = remove_load_data_info(res_df)
        res_df = fstpy.metadata_cleanup(res_df)

        return res_df