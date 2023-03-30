# -*- coding: utf-8 -*-
import argparse
import copy
import multiprocessing
import warnings

import fstpy
import numpy as np
import pandas as pd
import rpnpy.librmn.all as rmn

from ..plugin import Plugin, PluginParser
from ..utils import get_split_value, initializer, to_dask, to_numpy


class InterpolationHorizontalPointError(Exception):
    pass


class InterpolationHorizontalPoint(Plugin):
    """Horizontal Interpolation of fields to a set of latitudes and longitudes

    :param df: Input dataframe
    :type df: pd.DataFrame
    :param interpolation_type: Type of interpolation 'nearest','bi-linear','bi-cubic', default 'bi-cubic'
    :type interpolation_type: str
    :param extrapolation_type: Type of extrapolation 'nearest','linear','maximum','minimum','value','abort', default 'maximum'
    :type extrapolation_type: str
    :param extrapolation_value: value for extrapolation when type is value, defaults to None
    :type extrapolation_value: float, optional
    """

    grid_types = ['A', 'B', 'G', 'L', 'N', 'S']
    extrapolation_types = ['maximum', 'minimum', 'value', 'abort']
    interpolation_types = ['nearest', 'bi-linear', 'bi-cubic']

    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            interpolation_type: str = 'bi-cubic',
            extrapolation_type: str = 'maximum',
            extrapolation_value: float = None,
            parallel: bool = False):
        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise InterpolationHorizontalPointError('No data to process')

        self.lat_lon_df = self.df.loc[self.df.nomvar.isin(["LAT", "LON"])]

        self.df = fstpy.metadata_cleanup(self.df)
        # print('self.df\n',self.df[['nomvar', 'typvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'datyp', 'nbits', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4','grid']].to_string())

        if self.lat_lon_df.empty:
            raise InterpolationHorizontalPointError(
                'Missing latitudes and longitudes')
        self.validate_params()
        set_interpolation_type_options(self.interpolation_type)
        # set_extrapolation_type_options(self.extrapolation_type,self.extrapolation_value)
        self.define_output_grid()

        self.groups = self.df.groupby(by=['grid'])

# lon >> ni
# lat ^^ nj
# 3       1       Y       L       100     100     9000    0
# 576     641     Z       E       1480    750     56000   44000
# gds:TYPE_Y,0,1,2

# pds:LAT,LATLON ax
# level:1.0
# 45.73,43.40,49.18

# pds:LON,LATLON
# level:1.0
# -73.75,-79.38,-123.18

    def define_output_grid(self):
        if ('LON' in self.lat_lon_df.nomvar.to_list()) and (
                'LAT' in self.lat_lon_df.nomvar.to_list()):
            self.lat_lon_df = self.lat_lon_df.loc[self.lat_lon_df.nomvar.isin(
                ["LAT", "LON"])].reset_index(drop=True)

            ni, nj, _, ax, ay, ig1, ig2, ig3, ig4 = get_grid_paramters_from_latlon_fields(
                self.lat_lon_df)
            self.output_grid = define_grid('Y', 'L', ni, nj, ig1, ig2, ig3, ig4, ax, ay, None)
            self.lat = self.lat_lon_df.loc[self.lat_lon_df.nomvar == "LAT"].reset_index(drop=True).at[0,'d']
            self.lat = to_numpy(self.lat)    
            self.lon = self.lat_lon_df.loc[self.lat_lon_df.nomvar == "LON"].reset_index(drop=True).at[0,'d']
            self.lon = to_numpy(self.lon)    
            self.lat_lon_df.loc[self.lat_lon_df.nomvar == "LAT", 'nomvar'] = '^^'
            self.lat_lon_df.loc[self.lat_lon_df.nomvar == "LON", 'nomvar'] = '>>'
            self.lat_lon_df.loc[:, 'grtyp'] = 'L'
            self.lat_lon_df.loc[:, 'ig1'] = 100
            self.lat_lon_df.loc[:, 'ig2'] = 100
            self.lat_lon_df.loc[:, 'ig3'] = 9000
            self.lat_lon_df.loc[:, 'ig4'] = 0
            self.lat_lon_df.loc[:, 'etiket'] = 'INTHPT'


        else:
            raise InterpolationHorizontalPointError(
                'Missing longitudes and/or latitudes to process')

    def validate_params(self):
        if self.interpolation_type not in self.interpolation_types:
            raise InterpolationHorizontalPointError(
                f'Interpolation_type {self.interpolation_type} not in {self.interpolation_types}')
        if self.extrapolation_type not in self.extrapolation_types:
            raise InterpolationHorizontalPointError(
                f'Extrapolation_type {self.extrapolation_type} not in {self.extrapolation_types}')

    def compute(self) -> pd.DataFrame:
        results = []
        no_mod = []
        for _, current_group in self.groups:

            keep_intact_hy_field(current_group, no_mod)

            keep_toctoc(current_group, results)

            vect_df = current_group.loc[current_group.nomvar.isin(
                ['UU', 'VV'])].reset_index(drop=True)

            others_df = current_group.loc[~current_group.nomvar.isin(
                ['UU', 'VV', 'PT', 'LAT', 'LON', '>>', '^^', '^>', '!!', 'HY'])].reset_index(drop=True)

            pt_df = current_group.loc[current_group.nomvar == 'PT'].reset_index(
                drop=True)

            source_df, grtyp = select_input_grid_source_data(
                vect_df, others_df, pt_df)

            if source_df.empty:
                continue

            meta_df = current_group.loc[current_group.nomvar.isin(
                ['>>', '^^', '^>'])].reset_index(drop=True)

            input_grid = define_input_grid(grtyp, source_df, meta_df)

            grids_are_equal = check_in_out_grid_equality(
                input_grid, self.output_grid)

            if grids_are_equal:
                no_mod.append(current_group)
                continue

            create_grid_set(input_grid, self.output_grid)

            if not vect_df.empty:
                ni = vect_df.iloc[0]['ni']
                nj = vect_df.iloc[0]['nj']
                # print(others_df.iloc[0]['ni'],others_df.iloc[0]['nj'])
            elif not others_df.empty:
                ni = others_df.iloc[0]['ni']
                nj = others_df.iloc[0]['nj']
            else:
                ni = pt_df.iloc[0]['ni']
                nj = pt_df.iloc[0]['nj']

            indexes = find_index_of_lat_lon_not_in_grid(
                input_grid, ni, nj, self.lat, self.lon)

            if self.parallel:
                vectorial_interpolation_parallel(
                vect_df,
                results,
                input_grid,
                self.output_grid,
                self.extrapolation_type,
                self.extrapolation_value,
                indexes)
                scalar_interpolation_parallel(
                    others_df,
                    results,
                    input_grid,
                    self.output_grid,
                    self.extrapolation_type,
                    self.extrapolation_value,
                    indexes)
            else:
                vectorial_interpolation(
                    vect_df,
                    results,
                    input_grid,
                    self.output_grid,
                    self.extrapolation_type,
                    self.extrapolation_value,
                    indexes)
                scalar_interpolation(
                    others_df,
                    results,
                    input_grid,
                    self.output_grid,
                    self.extrapolation_type,
                    self.extrapolation_value,
                    indexes)

            scalar_interpolation_pt(pt_df, results, self.lat.size)

        res_df = pd.DataFrame(dtype=object)

        if len(results):
            res_df = pd.concat(results, ignore_index=True)
            # res_df.loc[:,'etiket'] = 'INTHPT'
            for i in res_df.index:
                if res_df.at[i, 'nomvar'] == '!!':
                    continue
                res_df.at[i, 'd'] = to_dask(res_df.at[i, 'd'])

        no_mod_df = pd.DataFrame(dtype=object)

        if len(no_mod):
            no_mod_df = pd.concat(no_mod, ignore_index=True)

        toctoc_res_df = set_new_grid_identifiers_for_toctoc(res_df, 0, 0)

        other_res_df = set_new_grid_identifiers(res_df,
                                                'Y',
                                                len(self.lat),
                                                1,
                                                self.lat_lon_df.iloc[0]['ip1'],
                                                self.lat_lon_df.iloc[0]['ip2'],
                                                self.lat_lon_df.iloc[0]['ip3'],
                                                0)

        if not toctoc_res_df.empty:
            other_res_df = pd.concat(
                [other_res_df, toctoc_res_df], ignore_index=True)

        if not no_mod_df.empty:
            other_res_df = pd.concat(
                [other_res_df, no_mod_df], ignore_index=True)

        # official etiket

        other_res_df = pd.concat(
            [other_res_df, self.lat_lon_df], ignore_index=True)

        other_res_df.loc[other_res_df.nomvar != 'HY', 'grid'] = '00000000'

        other_res_df = fstpy.metadata_cleanup(other_res_df)

        return other_res_df

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=InterpolationHorizontalPoint.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--interpolationType',type=str,default="BI-CUBIC",choices=["NEAREST","BI-LINEAR","BI-CUBIC"],dest='interpolation_type', help="Type of interpolation.")
        parser.add_argument('--extrapolationType',type=str,default="MAXIMUM",dest='extrapolation_type',help="Type of extrapolation.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['interpolation_type'] = parsed_arg['interpolation_type'].lower()

        if parsed_arg['extrapolation_type'] in ["MAXIMUM","MINIMUM","ABORT"]:
            parsed_arg['extrapolation_type'] = parsed_arg['extrapolation_type'].lower()
        elif parsed_arg['extrapolation_type'].startswith("VALUE="):
            parsed_arg['extrapolation_value'] = float(parsed_arg['extrapolation_type'].replace("VALUE=",""))
            parsed_arg['extrapolation_type'] = "value"

        return parsed_arg

##########################################################################
##########################################################################
# def set_extrapolation_type_options(extrapolation_type,extrapolation_value):
#     if extrapolation_type == 'value':
#         if extrapolation_value is None:
#             raise InterpolationHorizontalPointError(f'InterpolationHorizontalPoint - extrapolation_value {extrapolation_value} is not set')
#         rmn.ezsetval('EXTRAP_VALUE', extrapolation_value)
#         rmn.ezsetopt('EXTRAP_DEGREE', 'VALUE')
#     else:
#         # print( self.extrapolation_type.upper())
#         rmn.ezsetopt('EXTRAP_DEGREE', extrapolation_type.upper())


def set_interpolation_type_options(interpolation_type):
    if interpolation_type == 'nearest':
        rmn.ezsetopt('INTERP_DEGREE', 'NEAREST')
    elif interpolation_type == 'bi-linear':
        rmn.ezsetopt('INTERP_DEGREE', 'LINEAR')
    elif interpolation_type == 'bi-cubic':
        rmn.ezsetopt('INTERP_DEGREE', 'CUBIC')



def scalar_interpolation(
        df,
        results,
        input_grid,
        output_grid,
        extrapolation_type,
        extrapolation_value,
        indexes=None):
    if df.empty:
        return
    # scalar except PT
    int_df = copy.deepcopy(df)

    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)

    int_df_list = np.array_split(int_df, split_value)

    for df,int_df in zip(df_list,int_df_list):
        df = fstpy.compute(df)

        for i in df.index:

            arr = rmn.ezsint(output_grid, input_grid, df.at[i, 'd'])

            if len(indexes):
                arr = do_extrapolation(arr, df.at[i, 'd'], indexes, extrapolation_type, extrapolation_value)

            int_df.at[i, 'd'] = to_dask(arr)

        results.append(int_df)

def scalar_interp(out_grid, in_grid, data):
    arr = rmn.ezsint(int(out_grid), int(in_grid), data)
    return arr    

class ListWrapper:
    """Helper class to hide the list"""
    def __init__(self, indexes):
        self.indexes = indexes
    def get(self):
        return self.indexes

def scalar_interp_with_extrapolation(out_grid, in_grid, data, index, extp_type, extp_value):
    arr = rmn.ezsint(int(out_grid), int(in_grid), data)
    arr = do_extrapolation(arr, data, index.get(), extp_type, extp_value)
    return arr    
    
def scalar_interpolation_parallel(
        df,
        results,
        input_grid,
        output_grid,
        extrapolation_type,
        extrapolation_value,
        indexes=None):
    if df.empty:
        return
    # scalar except PT
    int_df = copy.deepcopy(df)

    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)

    int_df_list = np.array_split(int_df, split_value)

    for df,int_df in zip(df_list,int_df_list):
        df = fstpy.compute(df)

        output_grid_arr = [output_grid for _ in range(len(df.index))]
        input_grid_arr = [input_grid for _ in range(len(df.index))]

        if len(indexes):
            indexes_arr = [ListWrapper(indexes) for _ in range(len(df.index))] #np.full((len(df.index)),ListWrapper(indexes))
            extrapolation_type_arr = [extrapolation_type for _ in range(len(df.index))] #np.full((len(df.index)),extrapolation_type)
            extrapolation_value_arr = [extrapolation_value for _ in range(len(df.index))] #np.full((len(df.index)),extrapolation_value)

        with multiprocessing.Pool() as pool:
            if len(indexes): 
                interp_res = pool.starmap(scalar_interp_with_extrapolation, zip(output_grid_arr, input_grid_arr, df.d.to_list(), indexes_arr, extrapolation_type_arr, extrapolation_value_arr))
            else:    
                interp_res = pool.starmap(scalar_interp, zip(output_grid_arr, input_grid_arr, df.d.to_list()))

            int_df['d'] = [to_dask(r) for r in interp_res]

        results.append(int_df)    


def scalar_interpolation_pt(df, results, ni):
    if df.empty:
        return
    # scalar except PT
    int_df = df.copy(deep=True)
    int_df = int_df.reset_index(drop=True)
    df.at[0,'d'] = to_numpy(df.at[0,'d'])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        arr = np.expand_dims(np.full(ni, df.at[0,'d'].flat[0], dtype=np.float32, order='F'), axis=-1)
    for i in df.index:  # should only be one
        int_df.at[i, 'd'] = arr

    results.append(int_df)


def vectorial_interpolation(
        vect_df,
        results,
        input_grid,
        output_grid,
        extrapolation_type,
        extrapolation_value,
        indexes=None):

    if vect_df.empty:
        return

    uu_df = vect_df.loc[vect_df.nomvar == 'UU'].sort_values('level',ascending=vect_df.iloc[0].ascending).reset_index(drop=True)
    vv_df = vect_df.loc[vect_df.nomvar == 'VV'].sort_values('level',ascending=vect_df.iloc[0].ascending).reset_index(drop=True)

    if (uu_df.empty) or (vv_df.empty):
        return

    uu_int_df = copy.deepcopy(uu_df)
    vv_int_df = copy.deepcopy(vv_df)

    split_value = get_split_value(uu_df)

    uu_df_list = np.array_split(uu_df, split_value)
    vv_df_list = np.array_split(vv_df, split_value)
    uu_int_df_list = np.array_split(uu_int_df, split_value)
    vv_int_df_list = np.array_split(vv_int_df, split_value)

    for uu_df,vv_df,uu_int_df,vv_int_df in zip(uu_df_list,vv_df_list,uu_int_df_list,vv_int_df_list):
        uu_df = fstpy.compute(uu_df)
        vv_df = fstpy.compute(vv_df)

        for i in uu_df.index:
            
            (uu, vv) = rmn.ezuvint(output_grid, input_grid, uu_df.at[i, 'd'], vv_df.at[i, 'd'])
                                
            if len(indexes):
                uu = do_extrapolation(uu, uu_int_df.at[i, 'd'], indexes, extrapolation_type, extrapolation_value)
                vv = do_extrapolation(vv, vv_int_df.at[i, 'd'], indexes, extrapolation_type, extrapolation_value)

            uu_int_df.at[i, 'd'] = uu
            vv_int_df.at[i, 'd'] = vv

        results.append(uu_int_df)
        results.append(vv_int_df)

def vect_interp_with_extrapolation(out_grid, in_grid, uu_data, vv_data, indexes, extp_type, extp_value):
    (uu,vv) =  rmn.ezuvint(int(out_grid),int(in_grid),uu_data, vv_data)
    uu = do_extrapolation(uu, uu_data, indexes.get(), extp_type, extp_value)
    vv = do_extrapolation(vv, vv_data, indexes.get(), extp_type, extp_value)
    return uu,vv

def vect_interp(output_grid, input_grid, uu_data, vv_data):
    return rmn.ezuvint(int(output_grid),int(input_grid),uu_data,vv_data)

def vectorial_interpolation_parallel(
        vect_df,
        results,
        input_grid,
        output_grid,
        extrapolation_type,
        extrapolation_value,
        indexes=None):
    if vect_df.empty:
        return

    uu_df = vect_df.loc[vect_df.nomvar == 'UU'].sort_values('level',ascending=vect_df.iloc[0].ascending).reset_index(drop=True)
    vv_df = vect_df.loc[vect_df.nomvar == 'VV'].sort_values('level',ascending=vect_df.iloc[0].ascending).reset_index(drop=True)

    if (uu_df.empty) or (vv_df.empty):
        return

    uu_int_df = copy.deepcopy(uu_df)
    vv_int_df = copy.deepcopy(vv_df)

    split_value = get_split_value(uu_df)

    uu_df_list = np.array_split(uu_df, split_value)
    vv_df_list = np.array_split(vv_df, split_value)
    uu_int_df_list = np.array_split(uu_int_df, split_value)
    vv_int_df_list = np.array_split(vv_int_df, split_value)

    for uu_df,vv_df,uu_int_df,vv_int_df in zip(uu_df_list,vv_df_list,uu_int_df_list,vv_int_df_list):
        uu_df = fstpy.compute(uu_df)
        vv_df = fstpy.compute(vv_df)

        output_grid_arr = [output_grid for _ in range(len(uu_df.index))]
        input_grid_arr = [input_grid for _ in range(len(uu_df.index))]

        if len(indexes):
            indexes_arr = [ListWrapper(indexes) for _ in range(len(uu_df.index))] 
            extrapolation_type_arr = [extrapolation_type for _ in range(len(uu_df.index))] 
            extrapolation_value_arr = [extrapolation_value for _ in range(len(uu_df.index))] 

        with multiprocessing.Pool() as pool:
            if len(indexes):
                interp_res = pool.starmap(vect_interp_with_extrapolation, zip(output_grid_arr, input_grid_arr, uu_df.d.to_list(), vv_df.d.to_list(), indexes_arr, extrapolation_type_arr, extrapolation_value_arr))
            else:    
                interp_res = pool.starmap(vect_interp, zip(output_grid_arr, input_grid_arr, uu_df.d.to_list(), vv_df.d.to_list()))


            uu_int_df['d'] = [to_dask(r[0]) for r in interp_res]
            vv_int_df['d'] = [to_dask(r[1]) for r in interp_res]

        results.append(uu_int_df)
        results.append(vv_int_df)

def create_grid_set(input_grid, output_grid):
    rmn.ezdefset(output_grid, input_grid)


def check_in_out_grid_equality(input_grid, output_grid):
    in_params = rmn.ezgxprm(input_grid)
    in_params.pop('id')
    out_params = rmn.ezgxprm(output_grid)
    out_params.pop('id')
    return in_params == out_params


def select_input_grid_source_data(vect_df, others_df, pt_df):
    grtyp = ''
    if not vect_df.empty:
        grtyp = vect_df.iloc[0]['grtyp']
        source_df = vect_df
    elif not others_df.empty:
        grtyp = others_df.iloc[0]['grtyp']
        source_df = others_df
    elif not pt_df.empty:
        grtyp = pt_df.iloc[0]['grtyp']
        source_df = pt_df
    else:
        source_df = pd.DataFrame(dtype=object)
    return source_df, grtyp


def define_input_grid(grtyp, source_df, meta_df):
    ni, nj, ig1, ig2, ig3, ig4 = set_grid_parameters(source_df)

    if not meta_df.empty:
        if ('>>' in meta_df.nomvar.to_list()) and ('^^' in meta_df.nomvar.to_list()):
            ni, nj, grref, ax, ay, ig1, ig2, ig3, ig4 = get_grid_paramters_from_tictictactac_fields(meta_df)
            input_grid = define_grid(grtyp, grref, ni, nj, ig1, ig2, ig3, ig4, ax, ay, None)

        elif ('^>' in meta_df.nomvar.to_list()):
            tictac_df = meta_df.loc[meta_df.nomvar =="^>"].reset_index(drop=True)
            tictac_df.at[0,'d'] = to_numpy(tictac_df.at[0,'d'])
            input_grid = define_grid(
                grtyp,
                '',
                0,
                0,
                0,
                0,
                0,
                0,
                None,
                None,
                tictac_df.at[0,'d'])

    else:
        input_grid = define_grid(
            grtyp,
            ' ',
            ni,
            nj,
            ig1,
            ig2,
            ig3,
            ig4,
            None,
            None,
            None)

    return input_grid


def keep_intact_hy_field(current_group, no_mod):
    hy_df = current_group.loc[current_group.nomvar == 'HY'].reset_index(drop=True)
    if not hy_df.empty:
        no_mod.append(hy_df)


def keep_toctoc(current_group, results):
    toctoc_df = current_group.loc[current_group.nomvar == '!!'].reset_index(drop=True)
    # we can add toctoc from input grid
    if not toctoc_df.empty:
        results.append(toctoc_df)


def get_grid_paramters_from_tictictactac_fields(meta_df):
    lon_df = meta_df.loc[meta_df.nomvar == ">>"].reset_index(drop=True)
    lat_df = meta_df.loc[meta_df.nomvar == "^^"].reset_index(drop=True)
    return get_grid_parameters(lat_df, lon_df)


def get_grid_paramters_from_latlon_fields(meta_df):
    lat_df = meta_df.loc[meta_df.nomvar == "LAT"].reset_index(drop=True)
    lon_df = meta_df.loc[meta_df.nomvar == "LON"].reset_index(drop=True)
    return get_grid_parameters(lat_df, lon_df)


def get_grid_parameters(lat_df, lon_df):
    lat_df.at[0,'d'] = to_numpy(lat_df.at[0,'d'])
    lon_df.at[0,'d'] = to_numpy(lon_df.at[0,'d'])
    nj = lat_df.iloc[0]['nj']
    ni = lon_df.iloc[0]['ni']
    grref = lat_df.iloc[0]['grtyp']
    ay = lat_df.at[0,'d']
    ax = lon_df.at[0,'d']
    ig1 = lat_df.iloc[0]['ig1']
    ig2 = lat_df.iloc[0]['ig2']
    ig3 = lat_df.iloc[0]['ig3']
    ig4 = lat_df.iloc[0]['ig4']
    return ni, nj, grref, ax, ay, ig1, ig2, ig3, ig4


def set_grid_parameters(df):
    ni = df.iloc[0]['ni']
    nj = df.iloc[0]['nj']
    ig1 = df.iloc[0]['ig1']
    ig2 = df.iloc[0]['ig2']
    ig3 = df.iloc[0]['ig3']
    ig4 = df.iloc[0]['ig4']
    return ni, nj, ig1, ig2, ig3, ig4


def set_output_column_values(meta_df, field_df):
    ig1 = meta_df.iloc[0]['ip1']
    ig2 = meta_df.iloc[0]['ip2']
    ig3 = field_df.iloc[0]['ig3']
    ig4 = field_df.iloc[0]['ig4']
    return ig1, ig2, ig3, ig4


def set_new_grid_identifiers_for_toctoc(res_df, ig1, ig2):
    toctoc_res_df = res_df.loc[res_df.nomvar == "!!"].reset_index(drop=True)
    toctoc_res_df['ip1'] = ig1
    toctoc_res_df['ip2'] = ig2
    return toctoc_res_df


def set_new_grid_identifiers(res_df, grtyp, ni, nj, ig1, ig2, ig3, ig4):
    other_res_df = res_df.loc[res_df.nomvar != "!!"].reset_index(drop=True)
    shape_list = [(ni, nj) for _ in range(len(other_res_df.index))]
    other_res_df["shape"] = shape_list
    other_res_df['ni'] = ni
    other_res_df['nj'] = nj
    other_res_df['grtyp'] = grtyp
    other_res_df['interpolated'] = True
    other_res_df['ig1'] = ig1
    other_res_df['ig2'] = ig2
    other_res_df['ig3'] = ig3
    other_res_df['ig4'] = ig4
    return other_res_df


def define_grid(
        grtyp: str,
        grref: str,
        ni: int,
        nj: int,
        ig1: int,
        ig2: int,
        ig3: int,
        ig4: int,
        ax: np.ndarray,
        ay: np.ndarray,
        tictac: np.ndarray) -> int:
    #longitude = X

    grid_types = ['A', 'B', 'E', 'G', 'L', 'N', 'S', 'U', 'X', 'Y', 'Z', '#']
    grid_id = -1

    if grtyp not in grid_types:
        raise InterpolationHorizontalPointError(
            f'Grtyp {grtyp} not in {grid_types}')

    if grtyp in ['Y', 'Z', '#']:
        if ax.ndim == 1:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                ax = np.expand_dims(ax, axis=-1)

        if ay.ndim == 1:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                ay = np.expand_dims(ay, axis=-1)

        # print('ax\n',ax)
        # print('ay\n',ay)
        # print({'ni':ni,'nj':nj})
        grid_params = {
            'grtyp': grtyp,
            'grref': grref,
            'ni': int(ni),
            'nj': int(nj),
            'ay': ay,
            'ax': ax,
            'ig1': int(ig1),
            'ig2': int(ig2),
            'ig3': int(ig3),
            'ig4': int(ig4)}
        grid_id = rmn.ezgdef_fmem(grid_params)

    elif grtyp == 'U':
        if not len(tictac):
            raise InterpolationHorizontalPointError('Missing tictac')
        ni, nj, sub_grid_id_1, sub_grid_id_2 = create_type_u_sub_grids(
            tictac, ni, nj, ig1, ig2, ig3, ig4, ax, ay)

        vercode = 1
        grtyp = 'U'
        grref = ''

        grid_id = rmn.ezgdef_supergrid(
            ni, 2 * nj, grtyp, grref, vercode, (sub_grid_id_1, sub_grid_id_2))

    else:
        grid_params = {
            'grtyp': grtyp,
            'ni': int(ni),
            'nj': int(nj),
            'ig1': int(ig1),
            'ig2': int(ig2),
            'ig3': int(ig3),
            'ig4': int(ig4),
            'iunit': 0}
        grid_id = rmn.ezqkdef(grid_params)

    # print(rmn.ezgxprm(grid_id))
    return grid_id


def create_type_u_sub_grids(tictac, ni, nj, ig1, ig2, ig3, ig4, ax, ay):
    start_pos = 5
    tictac = tictac.ravel(order='F')

    ni, nj, ig1, ig2, ig3, ig4, ay, ax, next_pos = get_grid_parameters_from_tictac_offset(
        tictac, start_pos, ni, nj, ig1, ig2, ig3, ig4, ax, ay)

    grid_params = {
        'grtyp': 'Z',
        'grref': 'E',
        'ni': ni,
        'nj': nj,
        'ig1': ig1,
        'ig2': ig2,
        'ig3': ig3,
        'ig4': ig4,
        'ay': ay,
        'ax': ax}

    # Definition de la 1ere sous-grille
    sub_grid_id_1 = rmn.ezgdef_fmem(grid_params)

    start_pos = next_pos
    ni, nj, ig1, ig2, ig3, ig4, ay, ax, _ = get_grid_parameters_from_tictac_offset(
        tictac, start_pos, ni, nj, ig1, ig2, ig3, ig4, ax, ay)

    grid_params = {
        'grtyp': 'Z',
        'grref': 'E',
        'ni': ni,
        'nj': nj,
        'ig1': ig1,
        'ig2': ig2,
        'ig3': ig3,
        'ig4': ig4,
        'ay': ay,
        'ax': ax}

    # Definition de la 1ere sous-grille
    sub_grid_id_2 = rmn.ezgdef_fmem(grid_params)
    return ni, nj, sub_grid_id_1, sub_grid_id_2


def get_grid_parameters_from_tictac_offset(
        tictac, start_pos, ni, nj, ig1, ig2, ig3, ig4, ax, ay):
    ni = int(tictac[start_pos])
    nj = int(tictac[start_pos + 1])
    encoded_ig1 = tictac[start_pos + 6]
    encoded_ig2 = tictac[start_pos + 7]
    encoded_ig3 = tictac[start_pos + 8]
    encoded_ig4 = tictac[start_pos + 9]
    position_ax = start_pos + 10
    position_ay = position_ax + ni
    sub_grid_ref = 'E'
    ig1, ig2, ig3, ig4 = rmn.cxgaig(
        sub_grid_ref, encoded_ig1, encoded_ig2, encoded_ig3, encoded_ig4)
    next_pos = position_ay + nj
    ax = tictac[position_ax:position_ay]
    ay = tictac[position_ay:next_pos]
    return ni, nj, ig1, ig2, ig3, ig4, ay, ax, next_pos


def find_index_of_lat_lon_not_in_grid(
        input_grid,
        grid_horizontal_dimension,
        grid_vertical_dimension,
        latitudes,
        longitudes):
    # get X and Y position of all latitudes longitudes coordinate ( to later check if latlon are in the source grid )
    # xy = {
    #        'id' : grid id, same as input arg
    #        'x'  : list of points x-coor (numpy.ndarray)
    #        'y'  : list of points y-coor (numpy.ndarray)
    #    }

    coords = rmn.gdxyfll(input_grid, latitudes.ravel(order='F'), longitudes.ravel(order='F'))
    # print('coords',coords)
    # print(coords['x'][0])
    # print(coords['y'][0])
    # RpnFunctions::ezGetXYPositionFromLatLon(input_grid, x, y, latitudes,
    # longitudes)

    x_grid_lower_bound = 0.5
    x_grid_upper_bound = grid_horizontal_dimension + 0.5
    y_grid_lower_bound = 0.5
    y_grid_upper_bound = grid_vertical_dimension + 0.5

    # print('x_grid_lower_bound ',x_grid_lower_bound)
    # print('x_grid_upper_bound ',x_grid_upper_bound)
    # print('y_grid_lower_bound ',y_grid_lower_bound)
    # print('y_grid_upper_bound ',y_grid_upper_bound)

    # find index of latlon not in input grid limits
    epsilon = 0.00002
    indexes = []
    for i in range(len(latitudes)):
        # need an epsilon
        # ex: for the south pole ezscint can return something like 0.499987 instead of 0.5
        # print("coords['x'][i]",coords['x'][i],"coords['y'][i]",coords['y'][i])
        if(_lt_(coords['x'][i], x_grid_lower_bound, epsilon)
           or _gt_(coords['x'][i], x_grid_upper_bound, epsilon)
           or _lt_(coords['y'][i], y_grid_lower_bound, epsilon)
           or _gt_(coords['y'][i], y_grid_upper_bound, epsilon)):

            # print('index ',i)
            # print("latlon coordinate %.2f, %.2f outside input grid."%(latitudes[i] , longitudes[i]))
            # sys.stdout.write(f"x_grid_lower_bound={x_grid_lower_bound} , x_grid_upper_bound={x_grid_upper_bound}, y_grid_lower_bound={y_grid_lower_bound}, y_grid_upper_bound={y_grid_upper_bound}\n")
            # sys.stdout.write(f"ezscint value for X is:{coords['x'][i]}\n")
            # sys.stdout.write(f"ezscint value for Y is:{coords['y'][i]}\n")
            # sys.stdout.write(f"epsilon:{epsilon}\n")
            indexes.append(i)
    return indexes


def do_extrapolation(
        interpolated_data,
        data_before_interpolation,
        indexes,
        extrapolation_type,
        extrapolation_value):
    if extrapolation_type == "value":
        # replace value at latlon outside grid by a fixed value
        for i in indexes:
            interpolated_data[i] = extrapolation_value

    elif extrapolation_type == "maximum":
        min, max = find_min_max(data_before_interpolation)
        max = max + (max - min) * 0.05

        # replace value at latlon outside grid by the max value of the fields
        for i in indexes:
            interpolated_data[i] = max

    elif extrapolation_type == "minimum":
        min, max = find_min_max(data_before_interpolation)
        min = min - (max - min) * 0.05

        # replace value at latlon outside grid by the min value of the fields
        for i in indexes:
            interpolated_data[i] = min

    elif extrapolation_type == "abort":
        raise InterpolationHorizontalPointError(
            "ABORTED AS REQUESTED BY THE USE OF THE 'extrapolation_type ABORT' OPTION.\n")

    return interpolated_data


def find_min_max(array):
    return np.min(array), np.max(array)


def _eq_(value, threshold, epsilon=0.00001):
    return (abs(value - threshold) <= epsilon)


def _ge_(value, threshold, epsilon=0.00001):
    return ((value > threshold) or _eq_(value, threshold, epsilon))


def _lt_(value, threshold, epsilon=0.00001):
    return (not _ge_(value, threshold, epsilon))


def _le_(value, threshold, epsilon=0.00001):
    return (value < threshold or _eq_(value, threshold, epsilon))


def _gt_(value, threshold, epsilon=0.00001):
    return (not _le_(value, threshold, epsilon))
