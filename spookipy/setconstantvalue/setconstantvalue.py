# -*- coding: utf-8 -*-
from ..utils import initializer, remove_load_data_info
from ..opelementsbyvalue.opelementsbyvalue import OpElementsByValue
from ..plugin import Plugin
import pandas as pd
import fstpy.all as fstpy


def set_value(a,v):
    a[:]=v
    return a

def set_series_value(a:pd.Series, v):
    return a.apply(set_value,args=(v,))

class SetConstantValueError(Exception):
    pass

class SetConstantValue(Plugin):

    @initializer
    def __init__(self, df:pd.DataFrame, value=0, nomvar_out='', min_index=False, max_index=False, nb_levels=False, bi_dimensionnal=False):
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise SetConstantValueError('SetConstantValue - no data to process')

        self.meta_df = self.df.query('nomvar in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True) 

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])    
        self.df = self.df.query('nomvar not in ["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"]').reset_index(drop=True) 

        self.groups=self.df.groupby(by=['grid','nomvar','forecast_hour'])

        l = [self.min_index,self.max_index,self.nb_levels]

        lcount = l.count(True)

        if lcount > 1:
            raise SetConstantValueError('SetConstantValue - too many options selected, you can only choose one option at a time in %s' % ['min_index','max_index','nb_levels'])
        if self.min_index:
            self.value=0


    def compute(self) -> pd.DataFrame:
        df_list = []
        for _,current_group in self.groups: 
            if self.max_index:
                self.value=len(current_group.index)-1
            if self.nb_levels:
                self.value=len(current_group.index)

            res_df= OpElementsByValue(current_group,
            value = self.value,
            operation_name='SetConstantValue',
            nomvar_out= self.nomvar_out,
            operator = set_series_value,
            unit = 'scalar' ,
            exception_class = SetConstantValueError).compute() 
            if self.bi_dimensionnal:
                res_df.drop(res_df.index[1:], inplace=True)
                res_df.loc[:,'ip1'] = 0
            df_list.append(res_df)    


        if not len(df_list):
            raise SetConstantValueError('SetConstantValue - no results where produced')

        self.meta_df = fstpy.load_data(self.meta_df)

        df_list.append(self.meta_df)    
        # merge all results together
        res_df = pd.concat(df_list,ignore_index=True)
        # print('res_df\n',res_df[['nomvar','typvar','etiket','ni','nj','nk','dateo','ip1']])
        res_df = remove_load_data_info(res_df)
        res_df = fstpy.metadata_cleanup(res_df)
        # print('res_df\n',res_df[['nomvar','typvar','etiket','ni','nj','nk','dateo','ip1']])
        return res_df