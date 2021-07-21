# -*- coding: utf-8 -*-
from ..plugin import Plugin
from ..utils import create_empty_result, get_existing_result, get_intersecting_levels, get_plugin_dependencies, prepare_existing_results, remove_load_data_info
import pandas as pd
import fstpy.all as fstpy
import numpy as np
import sys


class WindModulusError(Exception):
    pass
 
def wind_modulus(uu:np.ndarray,vv:np.ndarray) -> np.ndarray:
    """Computes thw wind modulus from the wind components

    :param uu: U wind component
    :type uu: np.ndarray
    :param vv: V wind component
    :type vv: np.ndarray
    :return: wind modulus
    :rtype: np.ndarray
    """
    return (uu**2 + vv**2)**.5 

class WindModulus(Plugin):
    plugin_mandatory_dependencies = {
        'UU':{'nomvar':'UU','unit':'knot'},
        'VV':{'nomvar':'VV','unit':'knot'},
    }
    plugin_result_specifications = {
        'UV':{'nomvar':'UV','etiket':'WindModulus','unit':'knot'}
        }

    def __init__(self,df:pd.DataFrame):
        self.df = df
        #ajouter forecast_hour et unit
        self.validate_input()
        
    # might be able to move    
    def validate_input(self):
        if self.df.empty:
            raise  WindModulusError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)    

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True)    

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour'])    

         #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies)
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','forecast_hour'])
           

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return prepare_existing_results('WindModulus',self.existing_result_df,self.meta_df)

        sys.stdout.write('WindModulus - compute')      
        df_list = []
        for _,current_fhour_group in self.fhour_groups:
            current_fhour_group = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies)
            if current_fhour_group.empty:
                sys.stderr.write('WindModulus - no intersecting levels found')
                continue
            current_fhour_group = fstpy.load_data(current_fhour_group)
            # print('windmodulus\n',current_fhour_group)
            uu_df = current_fhour_group.query('nomvar == "UU"').reset_index(drop=True)
            vv_df = current_fhour_group.query('nomvar == "VV"').reset_index(drop=True)
            uv_df = create_empty_result(vv_df,self.plugin_result_specifications['UV'],copy=True)


            for i in uv_df.index:
                uu = uu_df.at[i,'d']
                vv = vv_df.at[i,'d']
                uv_df.at[i,'d'] = wind_modulus(uu,vv)

            df_list.append(uv_df)

        if not len(df_list):
            raise WindModulusError('No results were produced')

        self.meta_df = fstpy.load_data(self.meta_df)
        df_list.append(self.meta_df)    
        # merge all results together
        res_df = pd.concat(df_list,ignore_index=True)

        res_df = remove_load_data_info(res_df)
        res_df = fstpy.metadata_cleanup(res_df)
        
        return res_df


    

