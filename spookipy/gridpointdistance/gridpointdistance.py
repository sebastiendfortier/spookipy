# -*- coding: utf-8 -*-
import argparse
import copy
import dask.array as da
from typing import Final
import logging
import math
import numpy as np
import pandas as pd

import fstpy
import rpnpy.librmn.all as rmn
from ..plugin import Plugin, PluginParser
from ..utils import create_empty_result, get_0_ip1, initializer, to_dask, final_results


EARTH_RADIUS: Final = 6370997.
M_PI: Final =  3.14159265358979323846

def calc_dist(lat1, lon1, lat2, lon2):
   degre_a_radian = M_PI/180.
   radlat1 = lat1 * degre_a_radian
   radlat2 = lat2 * degre_a_radian
   radlon1 = lon1 * degre_a_radian
   radlon2 = lon2 * degre_a_radian
   return EARTH_RADIUS * math.acos(math.cos(radlat1) * math.cos(radlat2) * math.cos(radlon1 - radlon2) + math.sin(radlat1) * math.sin(radlat2))

def calc_dist2(lat1, lon1, lat2, lon2):
   degre_a_radian = M_PI/180.
   radlat1 = lat1 * degre_a_radian
   radlat2 = lat2 * degre_a_radian
   radlon1 = lon1 * degre_a_radian
   radlon2 = lon2 * degre_a_radian

   dlon = radlon2 - radlon1
   dlat = radlat2 - radlat1
   sindlat = math.sin(dlat*0.5)
   sindlon = math.sin(dlon*0.5)
#    a = sindlat*sindlat + math.cos(radlat1) * math.cos(radlat2) * sindlon*sindlon
   a = sindlat**2 + math.cos(radlat1) * math.cos(radlat2) * sindlon**2
#    c = 2.0 * math.atan2(math.sqrt(a),math.sqrt(1.0-a))
   c = 2.0 * math.asin(math.sqrt(a))
   return c*EARTH_RADIUS

def calc_dist3(lat1, lon1, lat2, lon2):
   degre_a_radian = math.pi/180.
   radlat1 = lat1 * degre_a_radian
   radlat2 = lat2 * degre_a_radian
   radlon1 = lon1 * degre_a_radian
   radlon2 = lon2 * degre_a_radian

   dlon = radlon2 - radlon1
   dlat = radlat2 - radlat1
   sindlat = math.sin(dlat*0.5)
   sindlon = math.sin(dlon*0.5)
#    a = sindlat*sindlat + math.cos(radlat1) * math.cos(radlat2) * sindlon*sindlon
   a = sindlat**2 + math.cos(radlat1) * math.cos(radlat2) * sindlon**2
#    c = 2.0 * math.atan2(math.sqrt(a),math.sqrt(1.0-a))
   c = 2.0 * math.asin(math.sqrt(a))
   return c*EARTH_RADIUS

# print(calc_dist(-4.5,0,-4.5,345.6))
# print(calc_dist2(-4.5,0,-4.5,345.6))
# print(rmn.ezcalcdist(-4.5,0,-4.5,345.6))
VEZCALCDIST_F: Final = np.vectorize(rmn.ezcalcdist)
# VEZCALCDIST_F: Final = np.vectorize(calc_dist)
# VEZCALCDIST_F: Final = np.vectorize(calc_dist3)
# ETIKET: Final[str] = 'GPTDIS'
NOMVAR_X: Final[str] = 'GDX'
NOMVAR_Y: Final[str] = 'GDY'
ETIKET: Final[str] = 'GPTDIS'
def centered_distance(lats: np.ndarray, lons: np.ndarray, is_global: bool = False, grid_wraps: bool = False) -> np.ndarray:
    center_res = VEZCALCDIST_F(lats[2:], lons[2:], lats[:-2], lons[:-2])
    if is_global and (not grid_wraps):
        lats1 = np.roll(lats, 2, axis=0)
        lons1 = np.roll(lons, 2, axis=0)
        res = VEZCALCDIST_F(lats1, lons1, lats, lons)
    
    elif grid_wraps:
        first_res = VEZCALCDIST_F(lats[1], lons[1], lats[-2], lons[-2])
        last_res = copy.deepcopy(first_res)
        before_last_res = VEZCALCDIST_F(lats[0], lons[0], lats[-3], lons[-3])
        res = np.vstack([first_res,center_res[:-1],before_last_res,last_res])

    else:
        first_res = VEZCALCDIST_F(lats[1], lons[1], lats[0], lons[0])
        last_res = VEZCALCDIST_F(lats[-1], lons[-1], lats[-2], lons[-2])
        res = np.vstack([first_res,center_res,last_res])
    
    return res.astype(np.float32)

def forward_distance(lats: np.ndarray, lons: np.ndarray, is_global: bool = False, grid_wraps: bool = False) -> np.ndarray:
    first_res = VEZCALCDIST_F(lats[1:], lons[1:], lats[0:-1], lons[0:-1])
    if grid_wraps:
        before_last_res = VEZCALCDIST_F(lats[0], lons[0], lats[-2], lons[-2])
        last_res = VEZCALCDIST_F(lats[1], lons[1], lats[0], lons[0])
        res = np.vstack([first_res[:-1],before_last_res,last_res])
    else:
        last_res = VEZCALCDIST_F(lats[-1], lons[-1], lats[-2], lons[-2])
        res = np.vstack([first_res,last_res])

    return res.astype(np.float32)

def backward_distance(lats: np.ndarray, lons: np.ndarray, is_global: bool = False, grid_wraps: bool = False) -> np.ndarray:
    center_res = VEZCALCDIST_F(lats[1:], lons[1:], lats[0:-1], lons[0:-1])
    if grid_wraps:
        flres = VEZCALCDIST_F(lats[0], lons[0], lats[-2], lons[-2])
        res = np.vstack([flres,center_res[:-1],flres])
    else:
        first_res = VEZCALCDIST_F(lats[1], lons[1], lats[0], lons[0])
        res = np.vstack([first_res,center_res])
    return res.astype(np.float32)

class GridPointDistanceError(Exception):
    pass

class GridPointDistance(Plugin):
    """Calculation of the distances on a horizontal grid between each point of which we know the latitude and longitude.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param difference_type: a choice in ['centered', 'forward', 'backward'], defaults to None
    :type difference_type: str, optional
    :param axis: a choice in ['x', 'y'], defaults to ['x', 'y']
    :type axis: list, optional
    """
    @initializer
    def __init__(self, df: pd.DataFrame, difference_type: str = None, axis: 'list(str)' = ['x', 'y']):
        self.plugin_result_specifications = {'etiket': ETIKET}
        super().__init__(df)
        self.validate_params()
        if 'path' not in self.df.columns:
            self.df = fstpy.add_path_and_key_columns(self.df)
        self.path_groups = self.df.groupby('path')


    def validate_params(self):
        if isinstance(self.axis, str):
            self.axis = [self.axis]
        for axis in self.axis:
            if axis not in ['x', 'y']:
                raise GridPointDistanceError(f"Invalid axis specification! {axis} not in  {['x', 'y']}")
        if self.difference_type not in ['centered', 'forward', 'backward']:
            raise GridPointDistanceError(f"Invalid difference type specification! {self.difference_type} not in {['centered', 'forward', 'backward']}")

    def compute(self):
        logging.info('GridPointDistance - compute')
        df_list = []
        for _, path_df in self.path_groups:
            
            grid_groups = path_df.groupby(['grid'])
            for _, grid_df in grid_groups:
                no_meta_df = grid_df.loc[~grid_df.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

                if no_meta_df.empty:
                    continue
                
                grtyp_groups = no_meta_df.groupby('grtyp')
                for grtyp, grtyp_df in grtyp_groups:

                    if (grtyp == 'X'):
                        logging.warning(f"{grtyp} is an unsupported grid type!")
                        continue

                    model_df = create_empty_result(grtyp_df, self.plugin_result_specifications)
                    # model_df = pd.DataFrame([grtyp_df.iloc[0].to_dict()])
                    current_ip1 = model_df.iloc[0].ip1
                    model_df['ip1'] = get_0_ip1(current_ip1)
                    model_df['nomvar'] = NOMVAR_X
                    gdx_df = copy.deepcopy(model_df)
                    model_df['nomvar'] = NOMVAR_Y
                    gdy_df = copy.deepcopy(model_df)


                    # print(no_meta_df.columns)
                    grid_params = fstpy.get_grid_definition_params(grtyp_df)
                    (lat, lon) = fstpy.get_2d_lat_lon_arr(grid_params)

                    # longitudes        
                    if (grtyp != 'U') and ('x' in self.axis):
                        is_global, repetitions = fstpy.is_global_grid(grid_params, lon)
                    else:
                        is_global = False
                        repetitions = False

                    grid_wraps = (is_global and repetitions)

                    lat = da.from_array(lat)
                    lon = da.from_array(lon)

                    # print(lat.shape,lon.shape)
                    if grtyp != 'U':

                        if self.difference_type == 'centered':
                            if 'x' in self.axis:
                                gdx_df['d'] = [to_dask(centered_distance(lat, lon, is_global, grid_wraps))]
                                df_list.append(gdx_df)
                            if 'y' in self.axis:
                                gdy_df['d'] = [to_dask(centered_distance(lat.T,lon.T).T)]
                                df_list.append(gdy_df)

                        elif self.difference_type == 'forward':
                            if 'x' in self.axis:
                                gdx_df['d'] = [to_dask(forward_distance(lat,lon, is_global, grid_wraps))]
                                df_list.append(gdx_df)
                            if 'y' in self.axis:
                                gdy_df['d'] = [to_dask(forward_distance(lat.T,lon.T).T)]
                                df_list.append(gdy_df)
                        elif self.difference_type == 'backward':
                            if 'x' in self.axis:
                                gdx_df['d'] = [to_dask(backward_distance(lat,lon, is_global, grid_wraps))]
                                df_list.append(gdx_df)

                            if 'y' in self.axis:
                                gdy_df['d'] = [to_dask(backward_distance(lat.T,lon.T).T)]
                                df_list.append(gdy_df)
                    else: #grtyp == 'U'
                        if self.difference_type == 'centered':
                            if 'x' in self.axis:
                                res1 = centered_distance(lat[:,0:int(lat.shape[1]/2)], lon[:,0:int(lon.shape[1]/2)], is_global, grid_wraps)
                                res2 = centered_distance(lat[:,int(lat.shape[1]/2):], lon[:,int(lon.shape[1]/2):], is_global, grid_wraps)
                                gdx_df['d'] = [to_dask(np.hstack([res1,res2]))]
                                df_list.append(gdx_df)
                            if 'y' in self.axis:
                                res1 = centered_distance(lat[:,0:int(lat.shape[1]/2)].T, lon[:,0:int(lon.shape[1]/2)].T).T
                                res2 = centered_distance(lat[:,int(lat.shape[1]/2):].T, lon[:,int(lon.shape[1]/2):].T).T
                                gdy_df['d'] = [to_dask(np.hstack([res1,res2]))]
                                df_list.append(gdy_df)

                        elif self.difference_type == 'forward':
                            if 'x' in self.axis:
                                res1 = forward_distance(lat[:,0:int(lat.shape[1]/2)], lon[:,0:int(lon.shape[1]/2)], is_global, grid_wraps)
                                res2 = forward_distance(lat[:,int(lat.shape[1]/2):], lon[:,int(lon.shape[1]/2):], is_global, grid_wraps)
                                gdx_df['d'] = [to_dask(np.hstack([res1,res2]))]
                                df_list.append(gdx_df)
                            if 'y' in self.axis:
                                res1 = forward_distance(lat[:,0:int(lat.shape[1]/2)].T, lon[:,0:int(lon.shape[1]/2)].T).T
                                res2 = forward_distance(lat[:,int(lat.shape[1]/2):].T, lon[:,int(lon.shape[1]/2):].T).T
                                gdy_df['d'] = [to_dask(np.hstack([res1,res2]))]
                                df_list.append(gdy_df)
                        elif self.difference_type == 'backward':
                            if 'x' in self.axis:
                                res1 = backward_distance(lat[:,0:int(lat.shape[1]/2)], lon[:,0:int(lon.shape[1]/2)], is_global, grid_wraps)
                                res2 = backward_distance(lat[:,int(lat.shape[1]/2):], lon[:,int(lon.shape[1]/2):], is_global, grid_wraps)
                                gdx_df['d'] = [to_dask(np.hstack([res1,res2]))]
                                df_list.append(gdx_df)

                            if 'y' in self.axis:
                                res1 = backward_distance(lat[:,0:int(lat.shape[1]/2)].T, lon[:,0:int(lon.shape[1]/2)].T).T
                                res2 = backward_distance(lat[:,int(lat.shape[1]/2):].T, lon[:,int(lon.shape[1]/2):].T).T
                                gdy_df['d'] = [to_dask(np.hstack([res1,res2]))]
                                df_list.append(gdy_df)

        return final_results(df_list, GridPointDistanceError, self.meta_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=GridPointDistance.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--differenceType',type=str,default="CENTERED",choices=['CENTERED','FORWARD','BACKWARD'],dest='difference_type', help="Type of difference.")
        parser.add_argument('--axis',type=str,required=True,help="Comma separated list of axis on which the differences will be calculated.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['axis'] = parsed_arg['axis'].lower().split(',')
        parsed_arg['difference_type'] = parsed_arg['difference_type'].lower()

        return parsed_arg
