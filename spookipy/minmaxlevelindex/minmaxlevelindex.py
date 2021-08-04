# -*- coding: utf-8 -*-
from ..plugin import Plugin
from ..utils import create_empty_result, get_3d_array, initializer, final_results, remove_load_data_info, validate_nomvar
import pandas as pd
import numpy as np
import sys
import fstpy.all as fstpy


class MinMaxLevelIndexError(Exception):
    pass

class MinMaxLevelIndex(Plugin):
    # plugin_requires = '(nomvar in ["TD","TT"]) and (unit == "celsius")' 
    plugin_result_specifications = {'ALL':{'etiket':'MinMaxLevelIndex','unit':'scalar','ip1':0}}
    @initializer
    def __init__(self,df:pd.DataFrame, ascending=True, min=False, max=False, bounded=False, nomvar_min='KMIN', nomvar_max='KMAX'):
        self.validate_input()
        
        
    def validate_input(self):
        if self.df.empty:
            raise MinMaxLevelIndexError('No data to process') 
        
        self.df = fstpy.metadata_cleanup(self.df)
        
        validate_nomvar(self.nomvar_min, MinMaxLevelIndex, MinMaxLevelIndexError)
        validate_nomvar(self.nomvar_max, MinMaxLevelIndex, MinMaxLevelIndexError)
        
        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True) 

        self.df = self.df.query('nomvar not in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True) 

        if (not self.min) and (not self.max):
            self.min = True
            self.max = True

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['forecast_hour'])
        
        keep = self.df.query(f'nomvar not in ["KBAS","KTOP"]').reset_index(drop=True)

        self.nomvar_groups= keep.groupby(by=['grid','forecast_hour','nomvar'])

    def compute(self) -> pd.DataFrame:
        sys.stdout.write('MinMaxLevelIndex - compute\n')
        df_list=[]
        for _,group in self.nomvar_groups:
            group = fstpy.load_data(group)

            kmin_df = create_empty_result(group,self.plugin_result_specifications['ALL'])
            kmin_df['nomvar']=self.nomvar_min
            # for k,v in self.plugin_result_specifications['ALL'].items():kmin_df[k] = v

            
            kmax_df = create_empty_result(group,self.plugin_result_specifications['ALL'])
            kmax_df['nomvar']=self.nomvar_max
            # for k,v in self.plugin_result_specifications['ALL'].items():kmax_df[k] = v
           
            
            array_3d = get_3d_array(group)

            # if not ascending, reverse array
            if not self.ascending:
                array_3d = np.flip(array_3d,axis=0)


            if self.bounded:
                # get kbas and ktop for this grid
                kbas = self.df.query('(nomvar=="KBAS") and (grid=="%s")'%group.iloc[0]['grid']).reset_index(drop=True)
                kbas = fstpy.load_data(kbas)
                ktop = self.df.query('(nomvar=="KTOP") and (grid=="%s")'%group.iloc[0]['grid']).reset_index(drop=True)
                ktop = fstpy.load_data(ktop)
                kbas_arr = kbas.iloc[0]['d'].flatten().astype('int64')
                kbas_mask = kbas_arr == -1

                kbas_arr_missing = np.where(kbas_arr == -1 , np.nan, kbas_arr)
                ktop_arr = ktop.iloc[0]['d'].flatten().astype('int64')
                ktop_mask = kbas_arr == -1
                ktop_arr_missing = np.where(ktop_arr == -1, np.nan, ktop_arr)

                array_3d = bound_array(array_3d, kbas_arr_missing, ktop_arr_missing)
                

            if self.ascending:
                kmin_df.at[0,'d'] = np.nanargmin(array_3d, axis=0).astype('float32')
                kmax_df.at[0,'d'] = np.nanargmax(array_3d, axis=0).astype('float32')
            
            else:
                kmin_df.at[0,'d'] = (array_3d.shape[0]-1 - np.nanargmin(array_3d, axis=0)).astype('float32')
                kmax_df.at[0,'d'] = (array_3d.shape[0]-1 - np.nanargmax(array_3d, axis=0)).astype('float32')

            if self.bounded:
                mask = kbas_mask | ktop_mask
                kmin_df.at[0,'d'] = np.where(mask,-1.0,kmin_df.at[0,'d'])
                kmax_df.at[0,'d'] = np.where(mask,-1.0,kmax_df.at[0,'d'])

            if self.min:
                df_list.append(kmin_df)
            if self.max:
                df_list.append(kmax_df)
            df_list.append(group)

        return final_results(df_list, MinMaxLevelIndexError, self.meta_df)
        # if not len(df_list):
        #     raise MinMaxLevelIndexError('No results were produced')

        # self.meta_df = fstpy.load_data(self.meta_df)
        # df_list.append(self.meta_df)    
        # # merge all results together
        # res_df = pd.concat(df_list,ignore_index=True)

        # res_df = remove_load_data_info(res_df)
        # res_df = fstpy.metadata_cleanup(res_df)

        # return res_df


def fix_ktop(ktop, array_max_index):
    newktop = (array_max_index-1)-ktop
    return newktop

def bound_array(a, kbas, ktop):
    arr=a.copy()
    newktop = fix_ktop(ktop, arr.shape[0])
    arr = np.rot90(arr)
    arr[np.flip(kbas[:,None]) > np.arange(arr.shape[1])] = np.nan
    arr = np.rot90(arr,k=2)
    arr[newktop[:,None] > np.arange(arr.shape[1])] = np.nan
    arr = np.rot90(arr,k=-3)
    return arr

