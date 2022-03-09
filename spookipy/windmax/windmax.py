# -*- coding: utf-8 -*-
import logging
from typing import Tuple
import warnings

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (create_result_container, existing_results, final_results,
                     get_dependencies, get_existing_result, to_dask)


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
        self.plugin_mandatory_dependencies = [{
            'UV': {'nomvar': 'UV', 'unit': 'knot'},
            'UU': {'nomvar': 'UU', 'unit': 'knot'},
            'VV': {'nomvar': 'VV', 'unit': 'knot'},
            'PX': {'nomvar': 'PX', 'unit': 'hectoPascal'},
        }]
        self.plugin_result_specifications = {
            'UV': {'nomvar': 'UV', 'etiket': 'WNDMAX', 'unit': 'knot', 'ip1': 0},
            'UU': {'nomvar': 'UU', 'etiket': 'WNDMAX', 'unit': 'knot', 'ip1': 0},
            'VV': {'nomvar': 'VV', 'etiket': 'WNDMAX', 'unit': 'knot', 'ip1': 0},
            'PX': {'nomvar': 'PX', 'etiket': 'WNDMAX', 'unit': 'hectoPascal', 'ip1': 0},
        }
        self.df = df
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise WindMaxError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = fstpy.add_columns(
            self.df, columns=[
                'unit', 'forecast_hour', 'ip_info'])

        # check if result already exists
        self.existing_result_df = get_existing_result(
            self.df, self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.groups = self.df.groupby(
            ['grid', 'dateo', 'forecast_hour', 'ip1_kind'])

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

            dependencies_df.sort_values(by='level',ascending=dependencies_df.ascending.unique()[0],inplace=True)
            ds = fstpy.to_cmc_xarray(dependencies_df)

            uvmaxpos = ds.UV.compute().argmax(dim='level') # if no compute xarray and dask dont work atm
            uumax = ds.UU.isel({'level':uvmaxpos})
            vvmax = ds.VV.isel({'level':uvmaxpos})
            uvmax = ds.UV.isel({'level':uvmaxpos})
            pxmax = ds.PX.isel({'level':uvmaxpos})
            
            uu_res_df = create_result_container(dependencies_df,self.plugin_result_specifications, 'UU')
            vv_res_df = create_result_container(dependencies_df,self.plugin_result_specifications, 'VV')
            uv_res_df = create_result_container(dependencies_df,self.plugin_result_specifications, 'UV')
            px_res_df = create_result_container(dependencies_df,self.plugin_result_specifications, 'PX')
            
            uu_res_df.at[0, 'd'] = to_dask(uumax.values)
            vv_res_df.at[0, 'd'] = to_dask(vvmax.values)
            uv_res_df.at[0, 'd'] = to_dask(uvmax.values)
            px_res_df.at[0, 'd'] = to_dask(pxmax.values)
            
            df_list.append(uu_res_df)
            df_list.append(vv_res_df)
            df_list.append(uv_res_df)
            df_list.append(px_res_df)

        return final_results(df_list, WindMaxError, self.meta_df)
