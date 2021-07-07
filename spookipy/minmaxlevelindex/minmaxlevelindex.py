# ((minMax,"",           string, TRUE, FALSE, "",                                                                        \
#     "Finds either the maximum or minimum value index or both\n  "                                                      \
#     "Supported types: [ STRING" OPERATION " ]\n  "                                                                       \
#     "Ex: --minMax MIN or --minMax BOTH\n"))                                                                            \
# ((bounded,"",          bool,   TRUE, TRUE, "",                                                                        \
#     "Searches in part of the column (requires fields KBAS and KTOP as inputs)\n  "                                     \
#     "Default: searches the whole column\n"))                                                                           \
# ((direction,"",        string, FALSE, TRUE, "UPWARD",                                                                  \
#     "The level iteration direction (upward or downward)\n  "                                                           \
#     "Supported types: [ STRING" VERTICAL_DIRECTION " ]\n  "                                                                       \
#     "Default: UPWARD\n  "                                                                                              \
#     "Ex: --direction DOWNWARD\n"))                                                                                     \
# ((outputFieldName1,"", string, FALSE, TRUE, OUTPUTFIELDNAME1,                                                          \
#     "Option to change the name of output field " OUTPUTFIELDNAME1 "\n  "                                                 \
#     "Supported types:[ STRING[(2 to 4 characters)] ]\n  "                                                              \
#     "Ex: --outputFieldName1 ABCD\n"))                                                                                  \
# ((outputFieldName2,"", string, FALSE, TRUE, OUTPUTFIELDNAME2,                                                          \
#     "Option to change the name of output field " OUTPUTFIELDNAME2 "\n  "                                                 \
#     "Supported types:[ STRING[(2 to 4 characters)] ]\n  "                                                              \
#     "Ex: --outputFieldName2 ABCD\n"))

# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
from spookipy.utils import initializer, validate_nomvar
import pandas as pd
import numpy as np
import fstpy.all as fstpy


class MinMaxLevelIndexError(Exception):
    pass

class MinMaxLevelIndex(Plugin):
    # plugin_requires = '(nomvar in ["TD","TT"]) and (unit == "celsius")' 
    plugin_result_specifications = {'ALL':{'etiket':'MinMaxLevelIndex','unit':'scalar','ip1':0}}
    @initializer
    def __init__(self,df:pd.DataFrame, ascending=True, min=False, max=False, bounded=False, nomvar_min='KMIN', nomvar_max='KMAX'):
        # self.df = df
        # self.ascending = ascending
        # self.min = min
        # self.max = max
        # self.bounded = bounded
        # self.nomvar_min = nomvar_min
        # self.nomvar_max = nomvar_max
        if (not self.min) and (not self.max):
            self.min = True
            self.max = True
        if df.empty:
            raise MinMaxLevelIndexError('MinMaxLevelIndex' + ' - no data to process') 
        validate_nomvar(nomvar_min, MinMaxLevelIndex, MinMaxLevelIndexError)
        validate_nomvar(nomvar_max, MinMaxLevelIndex, MinMaxLevelIndexError)
        
        # self.df = self.df.query(self.plugin_requires)
        self.df = fstpy.load_data(self.df)
        keep = self.df.query('nomvar not in ["KBAS","KTOP"]')
        self.nomvar_groups= keep.groupby(by=['grid','forecast_hour','nomvar'])
        

    def compute(self) -> pd.DataFrame:
        kminmaxdfs=[]
        for _,group in self.nomvar_groups:
            group = fstpy.load_data(group)


            kmin_df = fstpy.create_1row_df_from_model(group)
            # kmin_df = fstpy.zap(kmin_df,**self.plugin_result_specifications['ALL'], nomvar=self.nomvar_min)
            for k,v in self.plugin_result_specifications['ALL'].items():kmin_df[k] = v
            kmin_df['nomvar']=self.nomvar_min
            kmax_df = fstpy.create_1row_df_from_model(group)
            # kmax_df = fstpy.zap(kmax_df,**self.plugin_result_specifications['ALL'], nomvar=self.nomvar_max)
            for k,v in self.plugin_result_specifications['ALL'].items():kmax_df[k] = v
            kmax_df['nomvar']=self.nomvar_max
            #flatten arrays in group
            for i in group.index:
                group.at[i,'d'] = group.at[i,'d'].flatten()

            #create a multi level array
            array_3d = np.stack(group['d'].to_list())

            # if not ascending, reverse array
            if not self.ascending:
                array_3d = np.flip(array_3d,axis=0)


            if self.bounded:
                # get kbas and ktop for this grid
                kbas = self.df.query('(nomvar=="KBAS") and (grid=="%s")'%group.iloc[0]['grid'])
                ktop = self.df.query('(nomvar=="KTOP") and (grid=="%s")'%group.iloc[0]['grid'])
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
                kminmaxdfs.append(kmin_df)
            if self.max:
                kminmaxdfs.append(kmax_df)
            kminmaxdfs.append(group)    

        res = pd.concat(kminmaxdfs,ignore_index=True)

        return res

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


# print('array_3d','\n',array_3d)
# print('min','\n',min)
# print('max','\n',max)
# print('array_3dr','\n',array_3dr)
# print('minr','\n',minr)
# print('maxr','\n',maxr)

# new_bounded_array = bound_array(array_3d, kbas, ktop)
# new_bounded_arrayr = np.flip(new_bounded_array,axis=0)


# maxb = np.nanargmax(new_bounded_array, axis=0)
# minb = np.nanargmin(new_bounded_array, axis=0)
# maxrb = new_bounded_arrayr.shape[0]-1 - np.nanargmax(new_bounded_arrayr, axis=0)
# minrb = new_bounded_arrayr.shape[0]-1 - np.nanargmin(new_bounded_arrayr, axis=0)
