# -*- coding: utf-8 -*-
import copy
import dask.array as da
from typing import Final
import logging
import math
from dask.utils import V
import numpy as np
import pandas as pd

import fstpy.all as fstpy
import rpnpy.librmn.all as rmn
from ..plugin import Plugin
from ..utils import create_empty_result, get_0_ip1, initializer, to_dask, final_results

NOMVAR_X: Final[str] = 'FDX'
NOMVAR_Y: Final[str] = 'FDY'
NOMVAR_Z: Final[str] = 'FDZ'
ETIKET: Final[str] = 'GPTDIF'

def centered_difference(data: np.ndarray, is_global: bool = False, grid_wraps: bool = False) -> np.ndarray:
    center_res = (data[2:] - data[:-2])
    if is_global and (not grid_wraps):
        data1 = np.roll(data, 2, axis=0)
        res = (data1, - data)
    
    elif grid_wraps:
        first_res = (data[1] - data[-2])
        last_res = copy.deepcopy(first_res)
        before_last_res = (data[0] -  data[-3])
        res = np.vstack([first_res,center_res[:-1],before_last_res,last_res])

    else:
        first_res = (data[1] - data[0])
        last_res = (data[-1] - data[-2])
        res = np.vstack([first_res,center_res,last_res])
    
    return res.astype(np.float32)

def forward_difference(data: np.ndarray, is_global: bool = False, grid_wraps: bool = False) -> np.ndarray:
    first_res = (data[1:] - data[0:-1])
    if grid_wraps:
        before_last_res = (data[0] - data[-2])
        last_res = (data[1] - data[0])
        res = np.vstack([first_res[:-1],before_last_res,last_res])
    else:
        last_res = (data[-1] - data[-2])
        res = np.vstack([first_res,last_res])

    return res.astype(np.float32)

def backward_difference(data: np.ndarray, is_global: bool = False, grid_wraps: bool = False) -> np.ndarray:
    center_res = (data[1:] - data[0:-1])
    if grid_wraps:
        flres = (data[0] - data[-2])
        res = np.vstack([flres,center_res[:-1],flres])
    else:
        first_res = (data[1] - data[0])
        res = np.vstack([first_res,center_res])
    return res.astype(np.float32)


def centered_difference_z(data: np.ndarray):
    pass
def forward_difference_z(data: np.ndarray):
    pass
def backward_difference_z(data: np.ndarray):
    pass

class GridPointDifferenceError(Exception):
    pass

class GridPointDifference(Plugin):
    """Calculation of value differences of a given field for each grid point.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param difference_type: a choice in ['centered', 'forward', 'backward'], defaults to None
    :type difference_type: str, optional
    :param axis: a choice in ['x', 'y', 'z'], defaults to ['x', 'y', 'z']
    :type axis: list, optional
    """
    @initializer
    def __init__(self, df: pd.DataFrame, difference_type: str = None, axis: 'list(str)' = ['x', 'y']):
        self.plugin_result_specifications = {'etiket': ETIKET}
        super().__init__(df)
        self.validate_params()
        self.groups = self.df.groupby(['grid','datev','nomvar','etiket', 'ip1_kind', 'grtyp'])


    def validate_params(self):
        for axis in self.axis:
            if axis not in ['x', 'y']:
                raise GridPointDifferenceError(f"Invalid axis specification! {axis} not in  {['x', 'y', 'z']}")
        if self.difference_type not in ['centered', 'forward', 'backward']:
            raise GridPointDifferenceError(f"Invalid difference type specification! {self.difference_type} not in {['centered', 'forward', 'backward']}")

    def compute(self):
        logging.info('GridPointDifference - compute')
        df_list = []
        for (grid, datev, nomvar, etiket, ip1_kind, grtyp), nomvar_df in self.groups:
            if ('x' in self.axis) and (np.squeeze(nomvar_df.iloc[0].d).ndims < 2):
                raise GridPointDifferenceError('For X axis, need at least 2 dimensions')
            if ('y' in self.axis) and (np.squeeze(nomvar_df.iloc[0].d).ndims < 2):
                raise GridPointDifferenceError('For Y axis, need at least 2 dimensions')
            if ('z' in self.axis) and (not len(self.nomvar_df.index) > 2):
                raise GridPointDifferenceError('For Z axis, need at least 2 levels')

            grid_params = fstpy.get_grid_definition_params(nomvar_df)
            (_, lon) = fstpy.get_2d_lan_lon_arr(grid_params)

            if (grtyp != 'U') and ('x' in self.axis):
                is_global, repetitions = fstpy.is_global_grid(grid_params, lon)
            else:
                is_global = False
                repetitions = False

            grid_wraps = (is_global and repetitions)
            if 'x' in self.axis or 'y' in self.axis:
                for row in nomvar_df.itertuples():
                    data = row.d
                    model_df = pd.DataFrame([nomvar_df.loc[row.Index].to_dict])
                    model_df['etiket'] = ETIKET
                    if self.difference_type == 'centered':
                        if 'x' in self.axis:
                            model_df['nomvar'] = NOMVAR_X
                            fdx_df = copy.deepcopy(model_df)
                            fdx_df['d'] = [to_dask(centered_difference(data, is_global, grid_wraps))]
                            df_list.append(fdx_df)

                        if 'y' in self.axis:
                            model_df['nomvar'] = NOMVAR_Y
                            fdy_df = copy.deepcopy(model_df)
                            fdy_df['d'] = [to_dask(centered_difference(data.T).T)]
                            df_list.append(fdy_df)

                    elif self.difference_type == 'forward':
                        if 'x' in self.axis:
                            model_df['nomvar'] = NOMVAR_X
                            fdx_df = copy.deepcopy(model_df)
                            fdx_df['d'] = [to_dask(forward_difference(data, is_global, grid_wraps))]
                            df_list.append(fdx_df)

                        if 'y' in self.axis:
                            model_df['nomvar'] = NOMVAR_Y
                            fdy_df = copy.deepcopy(model_df)
                            fdy_df['d'] = [to_dask(forward_difference(data.T).T)]
                            df_list.append(fdy_df)

                    elif self.difference_type == 'backward':
                        if 'x' in self.axis:
                            model_df['nomvar'] = NOMVAR_X
                            fdx_df = copy.deepcopy(model_df)
                            fdx_df['d'] = [to_dask(backward_difference(data, is_global, grid_wraps))]
                            df_list.append(fdx_df)

                        if 'y' in self.axis:
                            model_df['nomvar'] = NOMVAR_Y
                            fdy_df = copy.deepcopy(model_df)
                            fdy_df['d'] = [to_dask(backward_difference(data.T).T)]
                            df_list.append(fdy_df)

            elif 'z' in self.axis:
                model_df = create_empty_result(nomvar_df, self.plugin_result_specifications)
                current_ip1 = model_df.iloc[0].ip1
                model_df['ip1'] = get_0_ip1(current_ip1)
                model_df['nomvar'] = NOMVAR_Z
                fdz_df = copy.deepcopy(model_df)
                data_3d = np.stack(nomvar_df.d)
                if self.difference_type == 'centered':
                    fdz_df['d'] = [to_dask(centered_difference_z(data_3d))]
                if self.difference_type == 'forward':
                    fdz_df['d'] = [to_dask(forward_difference_z(data_3d))]
                if self.difference_type == 'backward':
                    fdz_df['d'] = [to_dask(backward_difference_z(data_3d))]
                df_list.append(fdz_df)

        return final_results(df_list, GridPointDifferenceError, self.meta_df)

