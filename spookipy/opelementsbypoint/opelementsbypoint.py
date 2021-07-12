# -*- coding: utf-8 -*-
from spookipy.plugin import Plugin
from spookipy.utils import validate_nomvar
import pandas as pd
import numpy as np
import sys
import fstpy.all as fstpy



class OpElementsByPointError(Exception):
    pass 

class OpElementsByPoint(Plugin):
    
    def __init__(self, df:pd.DataFrame, operator, operation_name='OpElementsByPoint', exception_class = OpElementsByPointError, group_by_forecast_hour=False, group_by_level=False, nomvar_out='OPER', unit='scalar'):
        self.df = df
        self.operator = operator
        self.operation_name = operation_name
        self.exception_class = exception_class
        self.group_by_forecast_hour = group_by_forecast_hour
        self.group_by_level = group_by_level
        self.nomvar_out = nomvar_out
        self.unit = unit
        validate_nomvar(nomvar_out, operation_name, exception_class)
        if self.df.empty:
            raise  exception_class( operation_name + ' - no data to process')
        if len(self.df) == 1:
            sys.stderr.write(operation_name + ' - not enough records to process, need at least 2')
            raise exception_class(operation_name + ' - not enough records to process, need at least 2') 
        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['forecast_hour','ip_info'])       
        self.df = fstpy.load_data(self.df)

        #group by grid/forecast hour  
        # self.groups = fstpy.get_groups(self.df, self.group_by_forecast_hour, self.group_by_level)
        grouping = ['grid']
        if self.group_by_forecast_hour:
            grouping.append('forecast_hour')
        if self.group_by_level:
            grouping.append('level')    

        self.groups = self.df.groupby(by=grouping)
        self.plugin_result_specifications = {'ALL':{'nomvar':self.nomvar_out,'etiket':self.operation_name,'unit':self.unit}}
        


    def compute(self) -> pd.DataFrame:
        #holds data from all the groups
        results = []
        for _,current_group in self.groups:
            current_group.sort_values(by=['nomvar','forecast_hour'],inplace=True)

            if len(current_group.index) == 1:
                sys.stderr.write('need more than one field for this operation - skipping\n')
                continue
            res_df = fstpy.create_1row_df_from_model(current_group)
            # res_df = fstpy.zap(res_df, nomvar=self.nomvar_out, etiket=self.operation_name, unit=self.unit)
            for k,v in self.plugin_result_specifications['ALL'].items():res_df[k] = v
            res_df.reset_index(drop=True, inplace=True)
            for i in current_group.index:
                current_group.at[i,'d'] = current_group.at[i,'d'].flatten()

            array_3d = np.stack(current_group['d'].to_list())
            
            res = self.operator(array_3d, axis=0)

            #print(res)
            res_df.at[0,'d'] = res

            results.append(res_df)
        # merge all results together
        result = pd.concat(results,ignore_index=True)
        return result



