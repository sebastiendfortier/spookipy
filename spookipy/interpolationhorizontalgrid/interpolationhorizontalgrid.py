# -*- coding: utf-8 -*-
import copy
import multiprocessing

import fstpy
import numpy as np
import pandas as pd
import rpnpy.librmn.all as rmn

from ..plugin import Plugin, PluginParser
from ..utils import get_split_value, initializer, to_dask, to_numpy


class InterpolationHorizontalGridError(Exception):
    pass


class InterpolationHorizontalGrid(Plugin):
    """Horizontal Interpolation of fields to a target grid

    :param df: Input dataframe  
    :type df: pd.DataFrame  
    :param output_fields: sets what fields are included in output, 
                          'interpolated' - interpolated only,  
                          'reference' - add reference field,  
                          'all' - add all fields, defaut is 'all'   
    :type output_fields: str  
    :param method: Manner in how the target grid is defined  
    :type method: str 'field','user'  
    :param interpolation_type: Type of interpolation 'nearest','bi-linear','bi-cubic'  
    :type interpolation_type: str  
    :param extrapolation_type: Type of extrapolation 'nearest','linear','maximum','minimum','value','abort'  
    :type extrapolation_type: str  
    :param grtyp: Type of target grid (see the reference: Grid types supported by RPN Standard Files) 'A','B','G','L','N','S', defaults to None  
    :type grtyp: str, optional  
    :param ni: X dimension of the target grid, defaults to None  
    :type ni: int, optional  
    :param nj: Y dimension of the target grid, defaults to None  
    :type nj: int, optional  
    :param param1: Projection parameter 1, defaults to None  
    :type param1: float, optional  
    :param param2: Projection parameter 2, defaults to None  
    :type param2: float, optional  
    :param param3: Projection parameter 3, defaults to None  
    :type param3: float, optional  
    :param param4: Projection parameter 4, defaults to None  
    :type param4: float, optional  
    :param extrapolation_value: value for extrapolation when type is value, defaults to None  
    :type extrapolation_value: float, optional  
    :param nomvar: Name of the field on the grid to which interpolate, defaults to None  
    :type nomvar: str, optional   
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """

# –outputField arg Choice of output: include interpolated fields only or include reference field with
# interpolated
# fields or include all fields.
# Supported types: [STRING[INTERPOLATED_FIELD_ONLY|INCLUDE_REFERENCE_FIELD|INCLUDE_ALL_FIELDS] ]
# Default: INCLUDE_ALL_FIELDS
# EX: –outputField INCLUDE_REFERENCE_FIELD

    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            method: str,
            interpolation_type: str,
            extrapolation_type: str,
            grtyp: str                 = None,
            ni: int                    = None,
            nj: int                    = None,
            param1: float              = None,
            param2: float              = None,
            param3: float              = None,
            param4: float              = None,
            extrapolation_value: float = None,
            nomvar: str                = None,
            output_fields : str        = 'all',
            parallel: bool             = False,
            reduce_df                  = True):
        

        self.methods                 = ['field', 'user']
        self.grid_types              = ['A', 'B', 'G', 'L', 'N', 'S']
        self.extrapolation_types     = [
                                        'nearest',
                                        'linear',
                                        'maximum',
                                        'minimum',
                                        'value',
                                        'abort']
        self.interpolation_types     = ['nearest', 'bi-linear', 'bi-cubic']
        self.output_fields_selection = ['interpolated', 'reference', 'all']

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):

        self.toctoc_df = self.df.loc[self.df.nomvar == "!!"].reset_index(drop=True)
        self.hy_df     = self.df.loc[self.df.nomvar == "HY"].reset_index(drop=True)

        self.validate_params()

        set_interpolation_type_options(self.interpolation_type)

        set_extrapolation_type_options(self.extrapolation_type,
                                       self.extrapolation_value)

        self.define_output_grid()

        self.groups = self.df.groupby(by=['grid'])

    def define_output_grid(self):
        self.all_meta_df = pd.DataFrame(dtype=object)

        if self.method == 'user':

            if self.grtyp in ['L', 'N', 'S']:
                self.ig1, self.ig2, self.ig3, self.ig4 = rmn.cxgaig(
                    self.grtyp, self.param1, self.param2, self.param3, self.param4)
                self.output_grid = define_grid(
                    self.grtyp,
                    '',
                    self.ni,
                    self.nj,
                    self.ig1,
                    self.ig2,
                    self.ig3,
                    self.ig4,
                    None,
                    None,
                    None)
            else:
                self.ig1 = int(self.param1)
                self.ig2 = int(self.param2)
                self.ig3 = int(self.param3)
                self.ig4 = int(self.param4)

                self.output_grid = define_grid( self.grtyp, 
                                                '', 
                                                self.ni, 
                                                self.nj,
                                                self.ig1,
                                                self.ig2,
                                                self.ig3,
                                                self.ig4, None, None, None )

        else:  # method field defined
            if self.nomvar is None:
                raise InterpolationHorizontalGridError(
                    'You must supply a nomvar with field defined method')

            field_df = self.df.loc[self.df.nomvar ==
                                   self.nomvar].reset_index(drop=True)
            # print('field_df',field_df)
            # check for more than one definition for the field method
            if len(field_df.grid.unique()) > 1:
                raise InterpolationHorizontalGridError(
                    'Reference field found for multiple grids')

            # get grtyp from the field
            self.grtyp = field_df.iloc[0]['grtyp']

            self.ni, self.nj, self.ig1, self.ig2, self.ig3, self.ig4 = set_grid_parameters(field_df)

            # get meta for this fields grid
            grid = field_df.iloc[0]['grid']

            # print('meta_df1',meta_df1)
            meta_df = self.df.loc[(self.df.nomvar.isin(['>>', '^^', '^>'])) & (
                self.df.grid == grid)].reset_index(drop=True)

            self.all_meta_df = meta_df.copy(deep=True)
            # print('meta_df',meta_df)
            # print('grid',grid)
            # print(self.ni,self.nj,self.ig1,self.ig2,self.ig3,self.ig4)

            # define grid from meta
            if not meta_df.empty:
                if ('>>' in meta_df.nomvar.to_list()) and ('^^' in meta_df.nomvar.to_list()):
                    self.ni, self.nj, grref, ax, ay, self.ig1, self.ig2, self.ig3, self.ig4 = get_grid_paramters_from_latlon_fields(meta_df)
                    self.output_grid = define_grid(self.grtyp,grref,self.ni,self.nj,self.ig1,self.ig2,self.ig3,self.ig4,ax,ay,None)
                    self.ig1, self.ig2, self.ig3, self.ig4 = set_output_column_values(meta_df, field_df)

                elif ('^>' in meta_df.nomvar.to_list()):
                    self.output_grid = define_u_grid(meta_df, self.grtyp)
                    self.ig1, self.ig2, self.ig3, self.ig4 = set_output_column_values(meta_df, field_df)
                # meta_data present, load it

            # define grid from field
            else:
                # print(self.grtyp,'',self.ni,self.nj,self.ig1,self.ig2,self.ig3,self.ig4,None,None,None)
                self.output_grid = define_grid(self.grtyp, '', self.ni, self.nj, self.ig1, self.ig2, self.ig3, self.ig4, None, None, None)

            # remove all ref fields from source grid from processing
            if (self.output_fields == 'interpolated') and (self.method != 'user'):
                to_remove = self.df.loc[self.df.grid == grid].reset_index(drop=True)
                self.df = pd.concat([self.df, to_remove], ignore_index=True).drop_duplicates(keep=False)

            # remove all ref fields except ref field itself from source grid
            # from processing
            if (self.output_fields == 'reference') and (self.method != 'user'):
                to_remove = self.df.loc[self.df.grid == grid].reset_index(drop=True)
                to_remove = to_remove.loc[(to_remove.nomvar != self.nomvar) & (to_remove.grid == grid)].reset_index(drop=True)
                self.df = pd.concat([self.df, to_remove], ignore_index=True).drop_duplicates(keep=False)

            # res_df = fstpy.add_flag_values(res_df)

    def validate_params(self):

        if self.output_fields not in self. output_fields_selection:
            raise InterpolationHorizontalGridError(
                f'Output_fields {self.output_fields} not in {self.output_fields_selection}')
        if self.interpolation_type not in self.interpolation_types:
            raise InterpolationHorizontalGridError(
                f'Interpolation_type {self.interpolation_type} not in {self.interpolation_types}')
        if self.extrapolation_type not in self.extrapolation_types:
            raise InterpolationHorizontalGridError(
                f'Extrapolation_type {self.extrapolation_type} not in {self.extrapolation_types}')
        if self.method not in self.methods:
            raise InterpolationHorizontalGridError(
                f'Method {self.method} not in {self.methods}')
        if self.method == 'user':
            if self.grtyp not in self.grid_types:
                raise InterpolationHorizontalGridError(
                    f'Grtyp {self.grtyp} not in {self.grid_types}')

    def compute(self) -> pd.DataFrame:
        results = []
        no_mod = []
        for _, current_group in self.groups:

            keep_intact_hy_field(current_group, no_mod)

            keep_toctoc(current_group, results)

            vect_df   = current_group.loc[current_group.nomvar.isin(['UU', 'VV'])].reset_index(drop=True)

            others_df = current_group.loc[~current_group.nomvar.isin(['UU', 'VV', 'PT', '>>', '^^', '^>', '!!', 'HY', '!!SF'])].reset_index(drop=True)

            pt_df     = current_group.loc[current_group.nomvar == 'PT'].reset_index(drop=True)

            source_df, grtyp = select_input_grid_source_data(vect_df, others_df, pt_df)

            if source_df.empty:
                continue

            meta_df = current_group.loc[current_group.nomvar.isin(['>>', '^^', '^>'])].reset_index(drop=True)
            input_grid = define_input_grid(grtyp, source_df, meta_df)

            grids_are_equal = check_in_out_grid_equality(input_grid, self.output_grid)

            if grids_are_equal:
                no_mod.append(current_group)
                continue

            create_grid_set(input_grid, self.output_grid)

            if self.parallel:
                vectorial_interpolation_parallel(vect_df, results, input_grid, self.output_grid)
                scalar_interpolation_parallel(others_df,results,input_grid,self.output_grid)
            else:    
                vectorial_interpolation(vect_df, results, input_grid, self.output_grid)
                scalar_interpolation(others_df,results,input_grid,self.output_grid)

            scalar_interpolation_pt(pt_df, results, input_grid, self.output_grid)

            # print(input_grid)
            # rmn.gdrls(input_grid)

        res_df = pd.DataFrame(dtype=object)
        if len(results):
            res_df = pd.concat(results, ignore_index=True)
            res_df = set_new_grid_identifiers(
                res_df,
                self.grtyp,
                self.ni,
                self.nj,
                self.ig1,
                self.ig2,
                self.ig3,
                self.ig4)
            
            res_df = fstpy.add_flag_values(res_df)
            res_df.interpolated = True

        no_mod_df = pd.DataFrame(dtype=object)

        if len(no_mod):
            no_mod_df = pd.concat(no_mod, ignore_index=True)

        # print('other_res_df\n',other_res_df[['nomvar','grid']])
        if not no_mod_df.empty:
            res_df = pd.concat([res_df, no_mod_df], ignore_index=True)

        if not self.all_meta_df.empty:
            res_df = pd.concat([res_df, self.all_meta_df], ignore_index=True)

        if not self.toctoc_df.empty:

            self.toctoc_df = set_new_grid_identifiers_for_toctoc(
                self.toctoc_df, self.ig1, self.ig2)
            res_df = pd.concat([res_df, self.toctoc_df], ignore_index=True)

        if not self.hy_df.empty:

            res_df = pd.concat([res_df, self.hy_df], ignore_index=True)

        res_df = fstpy.metadata_cleanup(res_df)

        # Ajout des colonnes reliees a l'etiket
        res_df       = fstpy.add_columns(res_df, columns=['etiket'])

        # Necessaire car on doit remettre a jour self.meta_df avant final_results
        self.meta_df = res_df.loc[res_df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "PT"])].reset_index(drop=True) 
        
        # Dans ce cas-ci, on inclut P0 dans les donnees
        res_no_meta_df = res_df.loc[~res_df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "PT"])].reset_index(drop=True)

        return self.final_results([res_no_meta_df], 
                                  InterpolationHorizontalGridError, 
                                  copy_input = False,
                                  reduce_df = self.reduce_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=InterpolationHorizontalGrid.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--outputGridDefinitionMethod','-m',type=str,dest="method",choices=["FIELD_DEFINED","USER_DEFINED"],required=True, help="Manner in how the target grid is defined")
        parser.add_argument('--fieldName',type=str,dest='nomvar', help="Name of the field on the grid to which interpolate. \nMandatory if '--outputGridDefinitionMethod FIELD_DEFINED' is used.")
        parser.add_argument('--gridType',type=str,choices=["TYPE_A","TYPE_B","TYPE_G","TYPE_L","TYPE_N","TYPE_S"],dest='grtyp', help="Type of target grid (see the reference: Grid types supported by RPN Standard Files). \nMandatory if '--outputGridDefinitionMethod USER_DEFINED' is used.")
        parser.add_argument('--xyDimensions',type=str, help="X and Y dimensions of the target grid. \nMandatory if '--outputGridDefinitionMethod USER_DEFINED' is used.")
        parser.add_argument('--gridProjectionParameters',"-p",type=str, help="Projection parameters 1 to 4 that define the target grid  (see the reference: Grid types supported by RPN Standard Files). \nMandatory if '--outputGridDefinitionMethod USER_DEFINED' is used.")
        parser.add_argument('--interpolationType',type=str,default="BI-CUBIC",choices=["NEAREST","BI-LINEAR","BI-CUBIC"],dest='interpolation_type', help="Type of interpolation.")
        parser.add_argument('--extrapolationType',type=str,default="MAXIMUM",dest='extrapolation_type',help="Type of extrapolation.")
        parser.add_argument('--outputField',type=str,default="INCLUDE_ALL_FIELDS",choices=["INTERPOLATED_FIELD_ONLY","INCLUDE_REFERENCE_FIELD","INCLUDE_ALL_FIELDS"],dest='output_fields',help="Choice of output: include interpolated fields only or include reference field with interpolated fields or include all fields.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['method'] = parsed_arg['method'].replace("_DEFINED","").lower()

        if parsed_arg['method'] == "field" and parsed_arg['nomvar'] is None:
            raise InterpolationHorizontalGridError("--fieldName is mandatory if '--outputGridDefinitionMethod FIELD_DEFINED' is used.")
        elif parsed_arg['method'] == "user":
            if parsed_arg['grtyp'] is None:
                raise InterpolationHorizontalGridError("--gridType is mandatory if '--outputGridDefinitionMethod USER_DEFINED' is used.")
            if parsed_arg['xyDimensions'] is None:
                raise InterpolationHorizontalGridError("--xyDimensions is mandatory if '--outputGridDefinitionMethod USER_DEFINED' is used.")
            if parsed_arg['gridProjectionParameters'] is None:
                raise InterpolationHorizontalGridError("--gridProjectionParameters is mandatory if '--outputGridDefinitionMethod USER_DEFINED' is used.")

        if parsed_arg['gridProjectionParameters'] is not None:
            parsed_arg['gridProjectionParameters'] = parsed_arg['gridProjectionParameters'].split(",")
            parsed_arg['param1'] = float(parsed_arg['gridProjectionParameters'][0])
            parsed_arg['param2'] = float(parsed_arg['gridProjectionParameters'][1])
            parsed_arg['param3'] = float(parsed_arg['gridProjectionParameters'][2])
            parsed_arg['param4'] = float(parsed_arg['gridProjectionParameters'][3])
            if parsed_arg['param1'] < 0 or parsed_arg['param2'] < 0 or parsed_arg['param3'] < 0 or parsed_arg['param4'] < 0:
                raise InterpolationHorizontalGridError("The grid projection parameters need to be higher than 0.")

        if parsed_arg['xyDimensions'] is not None:
            parsed_arg['xyDimensions']        = parsed_arg['xyDimensions'].split(",")
            parsed_arg['ni']                  = int(parsed_arg['xyDimensions'][0])
            parsed_arg['nj']                  = int(parsed_arg['xyDimensions'][1])

        output_fields = {"INTERPOLATED_FIELD_ONLY":"interpolated", "INCLUDE_REFERENCE_FIELD":"reference", "INCLUDE_ALL_FIELDS":"all"}
        parsed_arg['output_fields'] = output_fields[parsed_arg['output_fields']]

        if parsed_arg['grtyp'] is not None:
            parsed_arg['grtyp']               = parsed_arg['grtyp'].replace("TYPE_","")

        parsed_arg['interpolation_type']      = parsed_arg['interpolation_type'].lower()

        if parsed_arg['extrapolation_type'] in ["MAXIMUM","MINIMUM","ABORT","NEAREST","LINEAR"]:
            parsed_arg['extrapolation_type']  = parsed_arg['extrapolation_type'].lower()

        elif parsed_arg['extrapolation_type'].startswith("VALUE="):
            parsed_arg['extrapolation_value'] = float(parsed_arg['extrapolation_type'].replace("VALUE=",""))
            parsed_arg['extrapolation_type']  = "value"

        return parsed_arg

##########################################################################
##########################################################################


def set_extrapolation_type_options(extrapolation_type, extrapolation_value):
    if extrapolation_type == 'value':
        if extrapolation_value is None:
            raise InterpolationHorizontalGridError(
                f'Extrapolation_value {extrapolation_value} is not set')
        rmn.ezsetval('EXTRAP_VALUE', extrapolation_value)
        rmn.ezsetopt('EXTRAP_DEGREE', 'VALUE')
    else:
        # print( self.extrapolation_type.upper())
        rmn.ezsetopt('EXTRAP_DEGREE', extrapolation_type.upper())


def set_interpolation_type_options(interpolation_type):
    if interpolation_type == 'nearest':
        rmn.ezsetopt('INTERP_DEGREE', 'NEAREST')
    elif interpolation_type == 'bi-linear':
        rmn.ezsetopt('INTERP_DEGREE', 'LINEAR')
    elif interpolation_type == 'bi-cubic':
        rmn.ezsetopt('INTERP_DEGREE', 'CUBIC')


def scalar_interpolation(df, results, input_grid, output_grid):
    if df.empty:
        return
    # scalar except PT
    int_df      = copy.deepcopy(df)

    split_value = get_split_value(df)

    df_list     = np.array_split(df, split_value)

    int_df_list = np.array_split(int_df, split_value)

    for df,int_df in zip(df_list,int_df_list):
        df = fstpy.compute(df)

        for i in df.index:
            arr = rmn.ezsint(output_grid, input_grid, df.at[i, 'd'])
            int_df.at[i, 'd'] = to_dask(arr)

        results.append(int_df)

def scalar_interp(output_grid,input_grid,data):
    return rmn.ezsint(int(output_grid), int(input_grid), data)

def scalar_interpolation_parallel(df, results, input_grid, output_grid):
    if df.empty:
        return
    # scalar except PT
    int_df      = copy.deepcopy(df)
    
    split_value = get_split_value(df)

    df_list     = np.array_split(df, split_value)

    int_df_list = np.array_split(int_df, split_value)

    for df,int_df in zip(df_list,int_df_list):
        df = fstpy.compute(df)
        output_grid_arr = [output_grid for _ in range(len(df.index))]
        input_grid_arr  = [input_grid  for _ in range(len(df.index))]
        with multiprocessing.Pool() as pool:
            interp_res = pool.starmap(scalar_interp, zip(output_grid_arr, input_grid_arr, df.d.to_list()))

        int_df['d']     = [to_dask(r) for r in interp_res]

        results.append(int_df)    


def scalar_interpolation_pt(df, results, input_grid, output_grid):
    if df.empty:
        return

    extrap_degree = rmn.ezgetopt(rmn.EZ_OPT_EXTRAP_DEGREE, vtype=str)
    rmn.ezsetopt('EXTRAP_DEGREE', 'NEAREST')

    scalar_interpolation(df, results, input_grid, output_grid)

    rmn.ezsetopt('EXTRAP_DEGREE', extrap_degree)



def vectorial_interpolation(vect_df, results, input_grid, output_grid):
    if vect_df.empty:
        return
    uu_df = vect_df.loc[vect_df.nomvar == 'UU'].sort_values('level',ascending=vect_df.iloc[0].ascending).reset_index(drop=True)
    vv_df = vect_df.loc[vect_df.nomvar == 'VV'].sort_values('level',ascending=vect_df.iloc[0].ascending).reset_index(drop=True)

    if (uu_df.empty) or (vv_df.empty):
        return

    uu_int_df = copy.deepcopy(uu_df)
    vv_int_df = copy.deepcopy(vv_df)

    split_value = get_split_value(uu_df)

    uu_df_list     = np.array_split(uu_df, split_value)
    vv_df_list     = np.array_split(vv_df, split_value)
    uu_int_df_list = np.array_split(uu_int_df, split_value)
    vv_int_df_list = np.array_split(vv_int_df, split_value)

    for uu_df,vv_df,uu_int_df,vv_int_df in zip(uu_df_list,vv_df_list,uu_int_df_list,vv_int_df_list):
        uu_df = fstpy.compute(uu_df)
        vv_df = fstpy.compute(vv_df)

        for i in uu_df.index:
            (uu_int_df.at[i, 'd'], vv_int_df.at[i, 'd']) = rmn.ezuvint(output_grid, input_grid, uu_df.at[i, 'd'], vv_df.at[i, 'd'])
    
            uu_int_df.at[i, 'd'] = to_dask(uu_int_df.at[i, 'd'])
            vv_int_df.at[i, 'd'] = to_dask(vv_int_df.at[i, 'd'])
            
        results.append(uu_int_df)
        results.append(vv_int_df)


def vect_interp(output_grid,input_grid,uu_data,vv_data):
    return rmn.ezuvint(int(output_grid),int(input_grid),uu_data,vv_data)


def vectorial_interpolation_parallel(vect_df, results, input_grid, output_grid):
    
    if vect_df.empty:
        return
    uu_df = vect_df.loc[vect_df.nomvar == 'UU'].sort_values('level',ascending=vect_df.iloc[0].ascending).reset_index(drop=True)
    vv_df = vect_df.loc[vect_df.nomvar == 'VV'].sort_values('level',ascending=vect_df.iloc[0].ascending).reset_index(drop=True)

    if (uu_df.empty) or (vv_df.empty):
        return

    uu_int_df = copy.deepcopy(uu_df)
    vv_int_df = copy.deepcopy(vv_df)

    split_value = get_split_value(uu_df)

    uu_df_list     = np.array_split(uu_df, split_value)
    vv_df_list     = np.array_split(vv_df, split_value)
    uu_int_df_list = np.array_split(uu_int_df, split_value)
    vv_int_df_list = np.array_split(vv_int_df, split_value)

    for uu_df,vv_df,uu_int_df,vv_int_df in zip(uu_df_list,vv_df_list,uu_int_df_list,vv_int_df_list):
        uu_df           = fstpy.compute(uu_df)
        vv_df           = fstpy.compute(vv_df)
        output_grid_arr = [output_grid for _ in range(len(uu_df.index))]
        input_grid_arr  = [input_grid for _ in range(len(uu_df.index))]
        with multiprocessing.Pool() as pool:
            interp_res = pool.starmap(vect_interp, zip(output_grid_arr, input_grid_arr, uu_df.d.to_list(), vv_df.d.to_list()))

        uu_int_df['d']  = [to_dask(r[0]) for r in interp_res]
        vv_int_df['d']  = [to_dask(r[1]) for r in interp_res]

        results.append(uu_int_df)
        results.append(vv_int_df)


def create_grid_set(input_grid, output_grid):
    rmn.ezdefset(output_grid, input_grid)


def check_in_out_grid_equality(input_grid, output_grid):
    in_params  = rmn.ezgxprm(input_grid)
    in_params.pop('id')
    out_params = rmn.ezgxprm(output_grid)
    out_params.pop('id')

    return in_params == out_params


def select_input_grid_source_data(vect_df, others_df, pt_df):
    grtyp = ''
    if not vect_df.empty:
        grtyp     = vect_df.iloc[0]['grtyp']
        source_df = vect_df
    elif not others_df.empty:
        grtyp     = others_df.iloc[0]['grtyp']
        source_df = others_df
    elif not pt_df.empty:
        grtyp     = pt_df.iloc[0]['grtyp']
        source_df = pt_df
    else:
        source_df = pd.DataFrame(dtype=object)

    return source_df, grtyp


def define_input_grid(grtyp, source_df, meta_df):
    ni, nj, ig1, ig2, ig3, ig4 = set_grid_parameters(source_df)

    if not meta_df.empty:
        if ('>>' in meta_df.nomvar.to_list()) and ('^^' in meta_df.nomvar.to_list()):
            ni, nj, grref, ax, ay, ig1, ig2, ig3, ig4 = get_grid_paramters_from_latlon_fields(meta_df)
            input_grid = define_grid(grtyp, grref, ni, nj, ig1, ig2, ig3, ig4, ax, ay, None)

        elif ('^>' in meta_df.nomvar.to_list()):
            input_grid = define_u_grid(meta_df, grtyp)

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

def define_u_grid(meta_df, grtyp):

    tictac_df            = meta_df.loc[meta_df.nomvar == "^>"].reset_index(drop=True)
    tictac_df.at[0, 'd'] = to_numpy(tictac_df.at[0, 'd'])

    return define_grid(grtyp, '', 0, 0, 0, 0, 0, 0, None, None, tictac_df.at[0, 'd'])


def keep_intact_hy_field(current_group, no_mod):

    hy_df = current_group.loc[current_group.nomvar == 'HY'].reset_index(drop=True)
    if not hy_df.empty:
        no_mod.append(hy_df)


def keep_toctoc(current_group, results):

    toctoc_df = current_group.loc[current_group.nomvar == '!!'].reset_index(drop=True)
    # we can add toctoc from input grid
    if not toctoc_df.empty:
        results.append(toctoc_df)


def get_grid_paramters_from_latlon_fields(meta_df):

    lon_df = meta_df.loc[meta_df.nomvar == ">>"].reset_index(drop=True)
    lat_df = meta_df.loc[meta_df.nomvar == "^^"].reset_index(drop=True)
    if lat_df.empty or lon_df.empty:
        raise InterpolationHorizontalGridError('No data in lat_df or lon_df')
    
    return get_grid_parameters(lat_df, lon_df)


def get_grid_parameters(lat_df, lon_df):

    if lat_df.empty or lon_df.empty:
        raise InterpolationHorizontalGridError('No data in lat_df or lon_df')
    lat_df           = lat_df.reset_index(drop=True)
    lon_df           = lon_df.reset_index(drop=True)
    nj               = lat_df.iloc[0]['nj']
    ni               = lon_df.iloc[0]['ni']
    grref            = lat_df.iloc[0]['grtyp']
    lat_df.at[0,'d'] = to_numpy(lat_df.at[0,'d'])
    lon_df.at[0,'d'] = to_numpy(lon_df.at[0,'d'])
   
    ay = lat_df.at[0,'d']
    ax = lon_df.at[0,'d']
    ig1 = lat_df.iloc[0]['ig1']
    ig2 = lat_df.iloc[0]['ig2']
    ig3 = lat_df.iloc[0]['ig3']
    ig4 = lat_df.iloc[0]['ig4']

    return ni, nj, grref, ax, ay, ig1, ig2, ig3, ig4


def set_grid_parameters(df):

    if df.empty:
        raise InterpolationHorizontalGridError('No data in df')
    ni   = df.iloc[0]['ni']
    nj  = df.iloc[0]['nj']
    ig1 = df.iloc[0]['ig1']
    ig2 = df.iloc[0]['ig2']
    ig3 = df.iloc[0]['ig3']
    ig4 = df.iloc[0]['ig4']

    return ni, nj, ig1, ig2, ig3, ig4


def set_output_column_values(meta_df, field_df):

    if meta_df.empty or field_df.empty:
        raise InterpolationHorizontalGridError(
            'Missing data in meta_df or field_df')
    ig1 = meta_df.iloc[0]['ip1']
    ig2 = meta_df.iloc[0]['ip2']
    ig3 = field_df.iloc[0]['ig3']
    ig4 = field_df.iloc[0]['ig4']
    
    return ig1, ig2, ig3, ig4


def set_new_grid_identifiers_for_toctoc(res_df, ig1, ig2):

    toctoc_res_df = res_df.loc[res_df.nomvar == "!!"].reset_index(drop=True)
    if toctoc_res_df.empty:
        return pd.DataFrame(dtype=object)
    toctoc_res_df['ip1']  = ig1
    toctoc_res_df['ip2']  = ig2
    toctoc_res_df['grid'] = ''.join([str(ig1), str(ig2)])

    return toctoc_res_df


def set_new_grid_identifiers(res_df, grtyp, ni, nj, ig1, ig2, ig3, ig4):

    other_res_df = res_df.loc[res_df.nomvar != "!!"].reset_index(drop=True)
    if other_res_df.empty:
        return pd.DataFrame(dtype=object)
    shape_list                   = [(ni, nj) for _ in range(len(other_res_df.index))]
    other_res_df["shape"]        = shape_list
    other_res_df['ni']           = ni
    other_res_df['nj']           = nj
    other_res_df['grtyp']        = grtyp
    other_res_df['interpolated'] = True
    other_res_df['ig1']          = ig1
    other_res_df['ig2']          = ig2
    other_res_df['ig3']          = ig3
    other_res_df['ig4']          = ig4
    other_res_df['grid']         = ''.join([str(ig1), str(ig2)])

    return other_res_df


def define_grid(
        grtyp : str,
        grref : str,
        ni    : int,
        nj    : int,
        ig1   : int,
        ig2   : int,
        ig3   : int,
        ig4   : int,
        ax    : np.ndarray,
        ay    : np.ndarray,
        tictac: np.ndarray) -> int:
    #longitude = X
    grid_types = ['A', 'B', 'E', 'G', 'L', 'N', 'S', 'U', 'X', 'Y', 'Z', '#']
    grid_id    = -1

    if grtyp not in grid_types:
        raise InterpolationHorizontalGridError(
            f'Grtyp {grtyp} not in {grid_types}')

    if grtyp in ['Y', 'Z', '#']:

        grid_params = {
            'grtyp': grtyp,
            'grref': grref,
            'ni'   : int(ni),
            'nj'   : int(nj),
            'ay'   : ay,
            'ax'   : ax,
            'ig1'  : int(ig1),
            'ig2'  : int(ig2),
            'ig3'  : int(ig3),
            'ig4'  : int(ig4)}
        grid_id = rmn.ezgdef_fmem(grid_params)

    elif grtyp == 'U':
        ni, nj, sub_grid_id_1, sub_grid_id_2 = create_type_u_sub_grids(tictac, 
                                                                       ni, nj, 
                                                                       ig1, ig2, 
                                                                       ig3, ig4, 
                                                                       ax, ay)

        vercode     = 1
        grtyp       = 'U'
        grref       = ''
        grid_params = {
            'grtyp'    : grtyp,
            'grref'    : grref,
            'ni'       : int(ni),
            'nj'       : int(2 * nj),
            'vercode'  : vercode,
            'subgridid': (
                sub_grid_id_1,
                sub_grid_id_2)}
        # grid_id = rmn.ezgdef_supergrid(ni, 2*nj, grtyp, grref, vercode, (sub_grid_id_1,sub_grid_id_2))
        grid_id    = rmn.ezgdef_supergrid(**grid_params)

    else:
        grid_params = {
            'grtyp': grtyp,
            'ni'   : int(ni),
            'nj'   : int(nj),
            'ig1'  : int(ig1),
            'ig2'  : int(ig2),
            'ig3'  : int(ig3),
            'ig4'  : int(ig4),
            'iunit': 0}
        grid_id = rmn.ezqkdef(grid_params)

    return grid_id


def create_type_u_sub_grids(tictac, ni, nj, ig1, ig2, ig3, ig4, ax, ay):
    start_pos = 5
    tictac = tictac.ravel(order='F')

    ni, nj, ig1, ig2, ig3, ig4, ay, ax, next_pos = get_grid_parameters_from_tictac_offset(
                                                        tictac, start_pos, ni, nj, ig1, ig2, ig3, ig4, ax, ay)

    grid_params = {
        'grtyp': 'Z',
        'grref': 'E',
        'ni'   : ni,
        'nj'   : nj,
        'ig1'  : ig1,
        'ig2'  : ig2,
        'ig3'  : ig3,
        'ig4'  : ig4,
        'ay'   : ay,
        'ax'   : ax}

    # Definition de la 1ere sous-grille
    sub_grid_id_1 = rmn.ezgdef_fmem(grid_params)

    start_pos = next_pos
    ni, nj, ig1, ig2, ig3, ig4, ay, ax, _ = get_grid_parameters_from_tictac_offset(
                                                        tictac, start_pos, ni, nj, ig1, ig2, ig3, ig4, ax, ay)

    grid_params = {
        'grtyp': 'Z',
        'grref': 'E',
        'ni'   : ni,
        'nj'   : nj,
        'ig1'  : ig1,
        'ig2'  : ig2,
        'ig3'  : ig3,
        'ig4'  : ig4,
        'ay'   : ay,
        'ax'   : ax}

    # Definition de la 1ere sous-grille
    sub_grid_id_2 = rmn.ezgdef_fmem(grid_params)

    return ni, nj, sub_grid_id_1, sub_grid_id_2


def get_grid_parameters_from_tictac_offset(tictac, start_pos, ni, nj, ig1, ig2, ig3, ig4, ax, ay):

    ni           = int(tictac[start_pos])
    nj           = int(tictac[start_pos + 1])
    encoded_ig1  = tictac[start_pos + 6]
    encoded_ig2  = tictac[start_pos + 7]
    encoded_ig3  = tictac[start_pos + 8]
    encoded_ig4  = tictac[start_pos + 9]
    position_ax  = start_pos + 10
    position_ay  = position_ax + ni
    sub_grid_ref = 'E'
    ig1, ig2, ig3, ig4 = rmn.cxgaig(sub_grid_ref, encoded_ig1, encoded_ig2, encoded_ig3, encoded_ig4)
    next_pos     = position_ay + nj
    ax           = tictac[position_ax:position_ay]
    ay           = tictac[position_ay:next_pos]

    return ni, nj, ig1, ig2, ig3, ig4, ay, ax, next_pos
