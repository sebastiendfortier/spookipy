# -*- coding: utf-8 -*-
from ..plugin import Plugin
from ..utils import create_empty_result, get_existing_result, get_intersecting_levels, get_plugin_dependencies, existing_results, final_results
import pandas as pd
import fstpy.all as fstpy
import numpy as np
import sys
import math

class WindDirectionError(Exception):
    pass

def wind_direction(uu:np.ndarray,vv:np.ndarray) -> np.ndarray:
    result = np.where( (uu == 0.),np.where(vv >= 0.,1800.,0.),270.0 - (180.0/math.pi)*np.arctan2(vv, uu))
    result = np.fmod(np.fmod(result,360.0)+360.0,360.0)
    return np.where(result == 0.,360.,result)


class WindDirection(Plugin):
    plugin_mandatory_dependencies = {
        'UU':{'nomvar':'UU','unit':'knot'},
        'VV':{'nomvar':'VV','unit':'knot'},
    }
    plugin_result_specifications = {
        'WD':{'nomvar':'WD','etiket':'WNDDIR','unit':'degree'}
        }

    def __init__(self,df:pd.DataFrame):
        self.df = df
        #ajouter forecast_hour et unit
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise  WindDirectionError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)


        self.df = fstpy.add_columns(self.df, decode=True, columns=['unit','forecast_hour','ip_info'])

         #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,None,self.plugin_mandatory_dependencies)
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','dateo','forecast_hour','grtyp'])


    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('WindDirection',self.existing_result_df,self.meta_df)

        sys.stdout.write('WindDirection - compute\n')
        df_list = []
        for _,current_fhour_group in self.fhour_groups:
            grid = current_fhour_group.grid.unique()[0]
            pos_df = self.meta_df.loc[((self.meta_df.nomvar=='>>')|(self.meta_df.nomvar=='^>')) & (self.meta_df.grid==grid)]
            meta_grtyp = ''
            if not pos_df.empty:
                meta_grtyp = pos_df.grtyp.unique()[0]
            grtyp = current_fhour_group.grtyp.unique()[0]
            if grtyp not in ['A','B','E','G','L','N','S','U','Y','Z']:
                raise  WindDirectionError('Cannot calculate meteorological direction for grid type {grtyp}\n')
            if (grtyp=='Y') and (meta_grtyp!='L'):
                raise  WindDirectionError('Only positional records of type: L are supported with grid type: Y.\n')
            current_fhour_group = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies)
            if current_fhour_group.empty:
                sys.stderr.write('WindDirection - no intersecting levels found')
                continue
            current_fhour_group = fstpy.load_data(current_fhour_group)
            uu_df = current_fhour_group.loc[current_fhour_group.nomvar=="UU"].reset_index(drop=True)
            vv_df = current_fhour_group.loc[current_fhour_group.nomvar=="VV"].reset_index(drop=True)
            wd_df = create_empty_result(vv_df,self.plugin_result_specifications['UV'],all_rows=True)

            for i in wd_df.index:
                uu = uu_df.at[i,'d']
                vv = vv_df.at[i,'d']
                # if grtyp == 'Y':
                #     wd_df.at[i,'d'] = wind_direction(uu,vv)
                # if grtyp == 'U':
                #     RpnFunctions::defineSubGrids(gds, subGrdId1, subGrdId2, gridNi, gridNj);
                #     c_gdll(subGrdId1, latGrid1.get(), lonGrid1.get())
                #     c_gdll(subGrdId2, latGrid2.get(), lonGrid2.get())
                #     calc_mod_dir_rpn_gridU(subGrdId1,subGrdId2, latGrid1, latGrid2, lonGrid1, lonGrid2, vecSize, debut)
                #     c_gdwdfuv(_subgdid1, uvVector, wdVector, uuVector, vvVector,_latGrid1, _lonGrid1, (int)_vecSize)
                #     c_gdwdfuv(_subgdid2, &uvVector[debut], &wdVector[debut], &uuVector[debut], &vvVector[debut],_latGrid2, _lonGrid2, (int)vecSize)
                #     wd_df.at[i,'d'] = wind_direction(uu,vv)
                # else:
                #     _gdid = RpnFunctions::defineGrid( gds );
                #     c_gdwdfuv(_gdid, uvVector, wdVector, uuVector, vvVector, _lat, _lon, _vecSize);
                #     wd_df.at[i,'d'] = wind_direction(uu,vv)


            df_list.append(wd_df)

        return final_results(df_list,WindDirectionError, self.meta_df)
