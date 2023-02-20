# -*- coding: utf-8 -*-
import argparse
import copy
from typing import Final
import logging
import numpy as np
import pandas as pd

import fstpy
from ..plugin import Plugin
from ..utils import create_empty_result, initializer, final_results, to_numpy

NOMVAR_X: Final[str] = 'FDX'
NOMVAR_Y: Final[str] = 'FDY'
NOMVAR_Z: Final[str] = 'FDZ'
ETIKET: Final[str] = 'GPTDIF'

def centered_difference(data: np.ndarray, is_global: bool = False, grid_wraps: bool = False) -> np.ndarray:
    center_res = (data[2:] - data[0:-2])
    if is_global and (not grid_wraps):

        data1 = np.roll(data, 1, axis=0)
        data2 = np.roll(data, -1, axis=0)
        res = (data2[0:] - data1[0:])
    
    elif grid_wraps:
        first_res = (data[1] - data[-2])
        last_res = copy.deepcopy(first_res)
        before_last_res = (data[0] -  data[-3])
        res = np.vstack([first_res,center_res[:-1],before_last_res,last_res])

    else:
        first_res = (data[1] - data[0])
        last_res = (data[-1] - data[-2])
        res = np.vstack([first_res,center_res,last_res])
    
    return res

def forward_difference(data: np.ndarray, is_global: bool = False, grid_wraps: bool = False) -> np.ndarray:
    first_res = (data[1:] - data[0:-1])
    if grid_wraps:
        before_last_res = (data[0] - data[-2])
        last_res = (data[1] - data[0])
        res = np.vstack([first_res[:-1],before_last_res,last_res])
    else:
        last_res = (data[-1] - data[-2])
        res = np.vstack([first_res,last_res])

    return res

def backward_difference(data: np.ndarray, is_global: bool = False, grid_wraps: bool = False) -> np.ndarray:
    center_res = (data[1:] - data[0:-1])
    if grid_wraps:
        flres = (data[0] - data[-2])
        res = np.vstack([flres,center_res[:-1],flres])
    else:
        first_res = (data[1] - data[0])
        res = np.vstack([first_res,center_res])
    return res


def centered_difference_z(data_3d: np.ndarray) -> np.ndarray:
    res_list = []
    res_list.append(data_3d[1,:,:] - data_3d[0,:,:])
    for i in range(0,data_3d.shape[0]-2):
        res_list.append(data_3d[i+2,:,:] - data_3d[i,:,:])
    res_list.append(data_3d[-1,:,:] - data_3d[-2,:,:])
    d = np.zeros(len(res_list), dtype=object)
    for i in range(len(d)):
        d[i] = res_list[i]
    return d

def forward_difference_z(data_3d: np.ndarray):
    res_list = []
    for i in range(0,data_3d.shape[0]-1):
        res_list.append(data_3d[i+1,:,:] - data_3d[i,:,:])
    res_list.append(data_3d[-1,:,:] - data_3d[-2,:,:])
    d = np.zeros(len(res_list), dtype=object)
    for i in range(len(d)):
        d[i] = res_list[i]
    return d

def backward_difference_z(data_3d: np.ndarray):
    res_list = []
    res_list.append(data_3d[1,:,:] - data_3d[0,:,:])
    for i in range(0,data_3d.shape[0]-1):
        res_list.append(data_3d[i+1,:,:] - data_3d[i,:,:])
    d = np.zeros(len(res_list), dtype=object)
    for i in range(len(d)):
        d[i] = res_list[i]
    return d


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
        self.change_nomvar = False  
        self.validate_params()
        if 'level' not in self.df.columns:
            self.no_meta_df = fstpy.add_columns(self.no_meta_df, 'ip_info')
          
        self.groups = self.no_meta_df.groupby(['grid','datev','nomvar','etiket', 'ip1_kind', 'grtyp'])


    def validate_params(self):
        if isinstance(self.axis, str):
            self.axis = [self.axis]
        for axis in self.axis:
            if axis not in ['x', 'y', 'z']:
                raise GridPointDifferenceError(f"Invalid axis specification! {axis} not in  {['x', 'y', 'z']}")
        if self.difference_type not in ['centered', 'forward', 'backward']:
            raise GridPointDifferenceError(f"Invalid difference type specification! {self.difference_type} not in {['centered', 'forward', 'backward']}")
            
        if len(self.axis)>1:
            self.change_nomvar = True


    def compute(self):
        logging.info('GridPointDifference - compute')
        df_list = []
        for (grid, datev, nomvar, etiket, ip1_kind, grtyp), nomvar_df in self.groups:
            if ('x' in self.axis) and (len(np.squeeze(nomvar_df.iloc[0].d).shape) < 2):
                raise GridPointDifferenceError('For X axis, need at least 2 dimensions')
            if ('y' in self.axis) and (len(np.squeeze(nomvar_df.iloc[0].d).shape) < 2):
                raise GridPointDifferenceError('For Y axis, need at least 2 dimensions')
            if ('z' in self.axis) and (not len(nomvar_df.index) >= 2):
                raise GridPointDifferenceError('For Z axis, need at least 2 levels')
            if ('z' in self.axis) and (self.difference_type == 'centered') and (not len(nomvar_df.index) >= 2):    
                raise GridPointDifferenceError('For Z axis centered, need at least 4 levels')

            grid_params = fstpy.get_grid_definition_params(nomvar_df)
            (_, lon) = fstpy.get_2d_lat_lon_arr(grid_params)

            if ((grtyp != 'U') or (grtyp != 'X')) and ('x' in self.axis):
                is_global, repetitions = fstpy.is_global_grid(grid_params, lon)
            else:
                is_global = False
                repetitions = False
            
            grid_wraps = (is_global and repetitions)
            

            model_df = create_empty_result(nomvar_df, self.plugin_result_specifications)
            model_df['etiket'] = ETIKET

            if 'x' in self.axis or 'y' in self.axis:
                for row in nomvar_df.itertuples():
                    data = row.d
                    model_df['ip1'] = row.ip1
                    if self.change_nomvar:
                        model_df['nomvar'] = NOMVAR_X
                    fdx_df = copy.deepcopy(model_df)
                    if self.change_nomvar:
                        model_df['nomvar'] = NOMVAR_Y
                    fdy_df = copy.deepcopy(model_df)
                    if grtyp != 'U':
                        if self.difference_type == 'centered':
                            if 'x' in self.axis:
                                fdx_df['d'] = [centered_difference(data, is_global, grid_wraps)]
                                df_list.append(fdx_df)

                            if 'y' in self.axis:
                                fdy_df['d'] = [centered_difference(data.T).T]
                                df_list.append(fdy_df)

                        elif self.difference_type == 'forward':
                            if 'x' in self.axis:
                                fdx_df['d'] = [forward_difference(data, is_global, grid_wraps)]
                                df_list.append(fdx_df)

                            if 'y' in self.axis:
                                fdy_df['d'] = [forward_difference(data.T).T]
                                df_list.append(fdy_df)

                        elif self.difference_type == 'backward':
                            if 'x' in self.axis:
                                fdx_df['d'] = [backward_difference(data, is_global, grid_wraps)]
                                df_list.append(fdx_df)

                            if 'y' in self.axis:
                                fdy_df['d'] = [backward_difference(data.T).T]
                                df_list.append(fdy_df)
                    else: # grtyp == 'U'
                        if self.difference_type == 'centered':
                            if 'x' in self.axis:
                                res1 = centered_difference(data[:,0:int(data.shape[1]/2)], is_global, grid_wraps)
                                res2 = centered_difference(data[:,int(data.shape[1]/2):], is_global, grid_wraps)
                                fdx_df['d'] = [np.hstack([res1, res2])]
                                df_list.append(fdx_df)

                            if 'y' in self.axis:
                                res1 = centered_difference(data[:,0:int(data.shape[1]/2)].T).T
                                res2 = centered_difference(data[:,int(data.shape[1]/2):].T).T
                                fdy_df['d'] = [np.hstack([res1, res2])]
                                df_list.append(fdy_df)

                        elif self.difference_type == 'forward':
                            if 'x' in self.axis:
                                res1 = forward_difference(data[:,0:int(data.shape[1]/2)], is_global, grid_wraps)
                                res2 = forward_difference(data[:,int(data.shape[1]/2):], is_global, grid_wraps)
                                fdx_df['d'] = [np.hstack([res1, res2])]
                                df_list.append(fdx_df)

                            if 'y' in self.axis:
                                res1 = forward_difference(data[:,0:int(data.shape[1]/2)].T).T
                                res2 = forward_difference(data[:,int(data.shape[1]/2):].T).T
                                fdy_df['d'] = [np.hstack([res1, res2])]
                                df_list.append(fdy_df)

                        elif self.difference_type == 'backward':
                            if 'x' in self.axis:
                                res1 = backward_difference(data[:,0:int(data.shape[1]/2)], is_global, grid_wraps)
                                res2 = backward_difference(data[:,int(data.shape[1]/2):], is_global, grid_wraps)
                                fdx_df['d'] = [np.hstack([res1, res2])]
                                df_list.append(fdx_df)

                            if 'y' in self.axis:
                                res1 = backward_difference(data[:,0:int(data.shape[1]/2)].T).T
                                res2 = backward_difference(data[:,int(data.shape[1]/2):].T).T
                                fdy_df['d'] = [np.hstack([res1, res2])]
                                df_list.append(fdy_df)

            elif 'z' in self.axis:
                fdz_df = create_empty_result(nomvar_df, self.plugin_result_specifications, all_rows=True)
                if self.change_nomvar:
                    fdz_df['nomvar'] = NOMVAR_Z
                fdz_df = fdz_df.sort_values(by='level', ascending=fdz_df.iloc[0].ascending)
                data = np.stack(fdz_df.d)
                if self.difference_type == 'centered':
                    fdz_df['d'] = centered_difference_z(data)
                elif self.difference_type == 'forward':
                    fdz_df['d'] = forward_difference_z(data)
                elif self.difference_type == 'backward':
                    fdz_df['d'] = backward_difference_z(data)

                df_list.append(fdz_df)

        return final_results(df_list, GridPointDifferenceError, self.meta_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=GridPointDifference.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--differenceType',type=str,default="CENTERED",choices=['CENTERED','FORWARD','BACKWARD'],dest='difference_type', help="Type of difference.")
        parser.add_argument('--axis',type=str,required=True,help="Comma separated list of axis on which the differences will be calculated.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['axis'] = parsed_arg['axis'].lower().split(',')
        parsed_arg['difference_type'] = parsed_arg['difference_type'].lower()

        return parsed_arg
