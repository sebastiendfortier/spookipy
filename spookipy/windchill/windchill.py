from spookipy.utils import get_existing_result, get_intersecting_levels, get_plugin_dependencies
import pandas as pd
import numpy as np
import fstpy.all as fstpy
from spookipy.plugin.plugin import Plugin

class WindChillError(Exception):
    pass

def wind_chill(tt:np.ndarray,uv:np.ndarray) ->np.ndarray:
    return np.where( (tt <= 0) & (uv >= 5), 13.12 + 0.6215 * tt + ( 0.3965 * tt - 11.37) * ( uv**0.16 ), tt)

class WindChill(Plugin):
    plugin_mandatory_dependencies = {
        'UV':{'nomvar':'UV','unit':'knot','surface':True},
        'TT':{'nomvar':'TT','unit':'celsius','surface':True},
    }

    plugin_result_specifications = {'RE':{'nomvar':'RE','etiket':'WindChill','unit':'celsius'}}
    
    def __init__(self,df:pd.DataFrame):
        self.df = df
        print(df)
        self.validate_input()
        
        
    # might be able to move    
    def validate_input(self):
        if self.df.empty:
            raise  WindChillError( 'WindChil - no data to process')

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,self.plugin_mandatory_dependencies)
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','forecast_hour'])


    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return self.existing_result_df
        #holds data from all the groups
        results = []
        for _,current_fhour_group in self.fhour_groups:
            current_fhour_group = fstpy.load_data(current_fhour_group)
            
            #print('-1-','\n',current_fhour_group[['nomvar','level','fhour']])        
            tt_df = current_fhour_group.query('nomvar == "TT"').reset_index(drop=True)
            uv_df = current_fhour_group.query('nomvar == "UV"').reset_index(drop=True)
            uv_df = fstpy.unit_convert(uv_df,'kilometer_per_hour')
            re_df = uv_df.copy(deep=True)
            # re_df = fstpy.zap(re_df, **self.plugin_result_specifications)
            for k,v in self.plugin_result_specifications['RE'].items():re_df[k] = v
            for i in re_df.index:
                tt = (tt_df.at[i,'d'])
                uv = (uv_df.at[i,'d'])
                re_df.at[i,'d'] = wind_chill(tt,uv)

            results.append(re_df)
        # merge all results together
        result = pd.concat(results,ignore_index=True)
        return result

