# -*- coding: utf-8 -*-
from ..plugin import Plugin
from ..utils import create_empty_result, get_3d_array, initializer, final_results, validate_nomvar
import pandas as pd
import numpy as np
import sys
import fstpy.all as fstpy

class MatchLevelIndexToValueError(Exception):
    pass

class MatchLevelIndexToValue(Plugin):
    plugin_result_specifications = {'ALL':{'etiket':'MLIVAL','ip1':0}}
    @initializer
    def __init__(self,df:pd.DataFrame, error_value=-1, nomvar_out=None, nomvar_index='IND'):
        self.validate_input()


    def validate_input(self):
        if self.df.empty:
            raise MatchLevelIndexToValueError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        validate_nomvar(self.nomvar_out, 'MatchLevelIndexToValue', MatchLevelIndexToValueError)
        validate_nomvar(self.nomvar_index, 'MatchLevelIndexToValue', MatchLevelIndexToValueError)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(self.df, decode=True, columns=['forecast_hour','ip_info'])

        keep = self.df.loc[~self.df.nomvar.isin(["KBAS","KTOP"])].reset_index(drop=True)

        self.groups= keep.groupby(by=['grid','forecast_hour'])

    def compute(self) -> pd.DataFrame:
        sys.stdout.write('MatchLevelIndexToValue - compute\n')
        df_list=[]
        for _,group in self.groups:
            group = fstpy.load_data(group)
            ind_df = group.loc[group.nomvar==self.nomvar_index].reset_index(drop=True)
            ind = np.expand_dims(ind_df.iloc[0]['d'].flatten().astype(np.int32),axis=0)
            others_df = group.loc[group.nomvar!=self.nomvar_index].reset_index(drop=True)
            nomvars = others_df.nomvar.unique()
            if not(self.nomvar_out is None) and (len(nomvars)>1):
                raise MatchLevelIndexToValueError('whenever parameter nomvar_out is specified, only 2 inputs are allowed: IND and another field; got {nomvars} in input')

            for nomvar in nomvars:
                # get current var
                var_df = group.loc[group.nomvar==nomvar]

                # sort values by level
                var_df = var_df.sort_values(by='level',ascending=var_df.ascending.unique()[0]).reset_index(drop=True)
                print(var_df.level)
                print(var_df.d)
                print(ind)
                res_df = create_empty_result(var_df,self.plugin_result_specifications['ALL'])

                if not(self.nomvar_out is None):
                    res_df.loc[:,'nomvar'] = self.nomvar_out

                # get the valid index range from our current variable
                num_levels = len(var_df.index)

                levels_range = list(range(0,num_levels))
                # create a mask of valid indexes
                mask = np.isin(ind,levels_range)

                # replace invalid indexes by error_row index
                valid_ind = np.where(mask,ind,num_levels)

                # create 3d array of our variable
                error_row = var_df.iloc[0]
                error_row['d'] = np.full_like(error_row['d'],self.error_value)

                var_df = var_df.append(error_row).reset_index(drop=True)
                print(var_df[['ascending','level']])
                arr_3d = get_3d_array(var_df)

                res_df.at[0,'d'] = np.take_along_axis(arr_3d,valid_ind,axis=0)

                df_list.append(res_df)

        return final_results(df_list, MatchLevelIndexToValueError, self.meta_df)
