# -*- coding: utf-8 -*-
import sys
from typing import Tuple

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, final_results,
                     get_3d_array, get_dependencies,
                     get_existing_result, get_from_dataframe,
                     get_intersecting_levels)


class WindMaxError(Exception):
    pass

def wind_max(uu_3d:np.ndarray,vv_3d:np.ndarray,uv_3d:np.ndarray,px_3d:np.ndarray) -> Tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray]:
    """Computes the maximum values by column for uu,vv,uv and px.

    :param uu_3d: flattened then stacked uu wind component arrays. the array is actually 2d (rows(flattened 2d grid) by levels)
    :type uu_3d: np.ndarray
    :param vv_3d: flattened then stacked vv wind component arrays. the array is actually 2d (rows(flattened 2d grid) by levels)
    :type vv_3d: np.ndarray
    :param uv_3d: flattened then stacked uv wind modulus arrays. the array is actually 2d (rows(flattened 2d grid) by levels)
    :type uv_3d: np.ndarray
    :param px_3d: flattened then stacked px pressure arrays. the array is actually 2d (rows(flattened 2d grid) by levels)
    :type px_3d: np.ndarray
    :return: uu_max,vv_max,uv_max,px_max
    :rtype: Tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray]
    """
    # max index
    uvmax = np.expand_dims(np.argmax(uv_3d,axis=0),axis=0)
    # match index
    uu_max = np.take_along_axis(uu_3d,uvmax,axis=0)
    vv_max = np.take_along_axis(vv_3d,uvmax,axis=0)
    uv_max = np.take_along_axis(uv_3d,uvmax,axis=0)
    px_max = np.take_along_axis(px_3d,uvmax,axis=0)
    return uu_max,vv_max,uv_max,px_max

class WindMax(Plugin):


    def __init__(self,df:pd.DataFrame):
        self.plugin_mandatory_dependencies = [{
            'UV':{'nomvar':'UV','unit':'knot'},
            'UU':{'nomvar':'UU','unit':'knot'},
            'VV':{'nomvar':'VV','unit':'knot'},
            'PX':{'nomvar':'PX','unit':'hectoPascal'},
        }]
        self.plugin_result_specifications = {
            'UV':{'nomvar':'UV','etiket':'WindMax','unit':'knot','ip1':0},
            'UU':{'nomvar':'UU','etiket':'WindMax','unit':'knot','ip1':0},
            'VV':{'nomvar':'VV','etiket':'WindMax','unit':'knot','ip1':0},
            'PX':{'nomvar':'PX','etiket':'WindMax','unit':'hectoPascal','ip1':0},
            }
        self.df = df
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise  WindMaxError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(self.df, decode=True, columns=['unit','forecast_hour','ip_info'])

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])


    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('WindMax',self.existing_result_df,self.meta_df)

        sys.stdout.write('WindMax - compute\n')
        #holds data from all the groups
        df_list = []

        dependencies_list = get_dependencies(self.groups,self.meta_df,'WindMax',self.plugin_mandatory_dependencies)

        for dependencies_df,option in dependencies_list:
            level_intersection_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])
            level_intersection_df = fstpy.load_data(level_intersection_df)

            uu_df = get_from_dataframe(level_intersection_df,'UU')
            uu_res_df = create_empty_result(uu_df,self.plugin_result_specifications['UU'])

            vv_df = get_from_dataframe(level_intersection_df,'VV')
            vv_res_df = create_empty_result(vv_df,self.plugin_result_specifications['VV'])

            uv_df = get_from_dataframe(level_intersection_df,'UV')
            uv_res_df = create_empty_result(uv_df,self.plugin_result_specifications['UV'])

            px_df = get_from_dataframe(level_intersection_df,'PX')
            px_res_df = create_empty_result(px_df,self.plugin_result_specifications['PX'])

            uu_3d = get_3d_array(uu_df)
            vv_3d = get_3d_array(vv_df)
            px_3d = get_3d_array(px_df)
            uv_3d = get_3d_array(uv_df)

            uu_res_df.at[0,'d'],vv_res_df.at[0,'d'],uv_res_df.at[0,'d'],px_res_df.at[0,'d'] = wind_max(uu_3d,vv_3d,uv_3d,px_3d)

            df_list.append(uu_res_df)
            df_list.append(vv_res_df)
            df_list.append(uv_res_df)
            df_list.append(px_res_df)

        return final_results(df_list,WindMaxError, self.meta_df)
