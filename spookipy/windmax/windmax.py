# -*- coding: utf-8 -*-
import logging
import fstpy

from typing import Tuple
import warnings

import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_empty_result, existing_results, get_3d_array,
                     get_dependencies, get_existing_result, get_from_dataframe)


class WindMaxError(Exception):
    pass


def wind_max(uu_3d: np.ndarray,vv_3d: np.ndarray,uv_3d: np.ndarray,px_3d: np.ndarray) -> Tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray]:
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
    # uvmax = np.expand_dims(np.argmax(uv_3d,axis=0),axis=0)
    uvmax = np.argmax(uv_3d, axis=0)[np.newaxis]
    # match index
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        uu_max = np.take_along_axis(uu_3d, uvmax, axis=0)
        vv_max = np.take_along_axis(vv_3d, uvmax, axis=0)
        uv_max = np.take_along_axis(uv_3d, uvmax, axis=0)
        px_max = np.take_along_axis(px_3d, uvmax, axis=0)
        
    return uu_max, vv_max, uv_max, px_max


class WindMax(Plugin):
    """Calculation of the maximum value of the wind modulus determined according to the vertical, as well as the horizontal components of the wind and the corresponding pressure level

    :param df: input DataFrame
    :type df: pd.DataFrame
    """
    def __init__(self, df: pd.DataFrame):
        self.plugin_mandatory_dependencies = [
                {
                'UV': {'nomvar': 'UV', 'unit': 'knot'},
                'UU': {'nomvar': 'UU', 'unit': 'knot'},
                'VV': {'nomvar': 'VV', 'unit': 'knot'},
                'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'},  
                 }
        ]
        self.plugin_result_specifications = {
            'UV': {'nomvar': 'UV', 'label': 'WNDMAX', 'unit': 'knot', 'ip1': 0},
            'UU': {'nomvar': 'UU', 'label': 'WNDMAX', 'unit': 'knot', 'ip1': 0},
            'VV': {'nomvar': 'VV', 'label': 'WNDMAX', 'unit': 'knot', 'ip1': 0},
            'PX': {'nomvar': 'PX', 'label': 'WNDMAX', 'unit': 'hectoPascal', 'ip1': 0},
        }
        self.df = fstpy.metadata_cleanup(df)      
        super().__init__(self.df)
        self.prepare_groups()

    # might be able to move
    def prepare_groups(self):

        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        # check if result already exists
        self.existing_result_df = get_existing_result(
            self.no_meta_df, self.plugin_result_specifications)

        self.groups = self.no_meta_df.groupby(
            ['grid', 'datev', 'vctype'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'WindMax', self.existing_result_df, self.meta_df)

        logging.info('WindMax - compute')
        # holds data from all the groups
        df_list = []

        dependencies_list = get_dependencies(
            self.groups,
            self.meta_df,
            'WindMax',
            self.plugin_mandatory_dependencies,
            intersect_levels=True)

        for dependencies_df, _ in dependencies_list:

            uu_df = get_from_dataframe(dependencies_df,'UU')
            uu_res_df = create_empty_result(uu_df,self.plugin_result_specifications['UU'])

            vv_df = get_from_dataframe(dependencies_df,'VV')
            vv_res_df = create_empty_result(vv_df,self.plugin_result_specifications['VV'])

            uv_df = get_from_dataframe(dependencies_df,'UV')
            uv_res_df = create_empty_result(uv_df,self.plugin_result_specifications['UV'])

            px_df = get_from_dataframe(dependencies_df,'PX')
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

        return self.final_results(df_list, WindMaxError,
                                  copy_input=False)
