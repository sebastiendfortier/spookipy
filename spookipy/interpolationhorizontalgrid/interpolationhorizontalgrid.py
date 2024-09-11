# -*- coding: utf-8 -*-
import fstpy
import pandas as pd
import rpnpy.librmn.all as rmn
from typing import List, Tuple, Optional
from ..plugin import Plugin, PluginParser
from ..utils import initializer
from ..interpolationutils import (keep_intact_hy_field, keep_toctoc, 
                                  set_interpolation_type_options,
                                  scalar_interpolation,
                                  scalar_interpolation_parallel,
                                  select_input_grid_source_data,
                                  vectorial_interpolation, vectorial_interpolation_parallel)


class InterpolationHorizontalGridError(Exception):
    pass


class InterpolationHorizontalGrid(Plugin):
    """Horizontal Interpolation of fields to a target grid

    :param df: Input dataframe  
    :type df : pd.DataFrame  
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

        self.groups = self.df.groupby('grid')

    def define_output_grid(self):
        self.all_meta_df = pd.DataFrame(dtype=object)

        if self.method == 'user':

            if self.grtyp in ['L', 'N', 'S']:
                self.ig1, self.ig2, self.ig3, self.ig4 = rmn.cxgaig(self.grtyp,
                                                                    self.param1, self.param2, 
                                                                    self.param3, self.param4)

                infos_grid = fstpy.define_grid( self.grtyp,
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
                self.output_grid,*other = infos_grid
            else:
                self.ig1   = int(self.param1)
                self.ig2   = int(self.param2)
                self.ig3   = int(self.param3)
                self.ig4   = int(self.param4)

                infos_grid = fstpy.define_grid( self.grtyp, 
                                                '', 
                                                self.ni, 
                                                self.nj,
                                                self.ig1,
                                                self.ig2,
                                                self.ig3,
                                                self.ig4, None, None, None )
                self.output_grid,*other = infos_grid
                
        else:  # method field defined
            if self.nomvar is None:
                raise InterpolationHorizontalGridError('A nomvar must be supplied with FIELD defined method')

            field_df         = self.df.loc[self.df.nomvar == self.nomvar].reset_index(drop=True)

            # check for more than one definition for the field method
            if len(field_df.grid.unique()) > 1:
                raise InterpolationHorizontalGridError('Reference field found for multiple grids')

            # get grtyp from the field
            self.grtyp       = field_df.iloc[0]['grtyp']

            (self.ni, self.nj, 
             self.ig1, self.ig2, 
             self.ig3, self.ig4) = (fstpy.set_grid_parameters(field_df))

            # get meta for this fields grid
            grid             = field_df.iloc[0]['grid']

            meta_df          = self.df.loc[(self.df.nomvar.isin(['>>', '^^', '^>'])) & 
                                           (self.df.grid == grid)].reset_index(drop=True)

            self.all_meta_df = meta_df.copy(deep=True)

            # define grid from meta
            if not meta_df.empty:
                if ('>>' in meta_df.nomvar.to_list()) and \
                   ('^^' in meta_df.nomvar.to_list()):
                    
                    (self.ni, self.nj, grref, ax, ay, 
                     self.ig1, self.ig2, 
                     self.ig3, self.ig4)    = (fstpy.get_grid_parameters_from_positional_records(meta_df))

                    infos_grid              = fstpy.define_grid(self.grtyp,grref,self.ni,self.nj,
                                                                self.ig1,self.ig2,self.ig3,self.ig4,ax,ay,None)
                    self.output_grid,*other = infos_grid
                    (self.ig1, self.ig2, 
                     self.ig3, self.ig4)    = (set_output_column_values(meta_df, field_df))

                elif ('^>' in meta_df.nomvar.to_list()):

                    self.output_grid, *other = fstpy.define_u_grid(meta_df, self.grtyp)
                    (self.ig1, self.ig2, 
                     self.ig3, self.ig4)     = (set_output_column_values(meta_df, field_df))

            # define grid from field
            else:
                infos_grid              = fstpy.define_grid(self.grtyp, '', self.ni, self.nj, 
                                                            self.ig1, self.ig2, self.ig3, self.ig4, None, None, None)
                self.output_grid,*other = infos_grid

            # remove all ref fields from source grid from processing
            if (self.output_fields == 'interpolated') and (self.method != 'user'):
                to_remove   = self.df.loc[self.df.grid == grid].reset_index(drop=True)
                self.df     = pd.concat([self.df, to_remove], ignore_index=True).drop_duplicates(keep=False)

            # remove all ref fields except ref field itself from source grid from processing
            if (self.output_fields == 'reference') and (self.method != 'user'):
                to_remove   = self.df.loc[self.df.grid == grid].reset_index(drop=True)
                to_remove   = to_remove.loc[(to_remove.nomvar != self.nomvar) & 
                                            (to_remove.grid == grid)].reset_index(drop=True)
                self.df     = pd.concat([self.df, to_remove], ignore_index=True).drop_duplicates(keep=False)


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
            raise InterpolationHorizontalGridError(f'Method {self.method} not in {self.methods}')
        if self.method == 'user':
            if self.grtyp not in self.grid_types:
                raise InterpolationHorizontalGridError(f'Grtyp {self.grtyp} not in {self.grid_types}')

    def compute(self) -> pd.DataFrame:
        results = []
        no_mod = []
        for _, current_group in self.groups:

            keep_intact_hy_field(current_group, no_mod)

            keep_toctoc(current_group, results)

            vect_df          = current_group.loc[current_group.nomvar.isin(['UU', 'VV'])].reset_index(drop=True)

            others_df        = (current_group
                                .loc[~current_group.nomvar.isin(['UU', 'VV', 'PT', '>>', '^^', '^>', '!!', 'HY', '!!SF'])]
                                .reset_index(drop=True))

            pt_df            = current_group.loc[current_group.nomvar == 'PT'].reset_index(drop=True)

            source_df, grtyp = select_input_grid_source_data(vect_df, others_df, pt_df)

            if source_df.empty:
                continue
 
            meta_df         = current_group.loc[current_group.nomvar.isin(['>>', '^^', '^>'])].reset_index(drop=True)
            if grtyp == 'U':
                infos_grid = fstpy.define_input_grid(grtyp, source_df, meta_df)
                if len(infos_grid) != 3:
                        raise InterpolationHorizontalGridError(f'Problem with definition of grid of type U')
                    
                input_grid, subgridId1, subgridId2 = infos_grid 
            else:
                
                infos_grid         = fstpy.define_input_grid(grtyp, source_df, meta_df)
                input_grid, *other = infos_grid

            grids_are_equal = fstpy.check_grid_equality(input_grid, self.output_grid)

            if grids_are_equal:
                no_mod.append(current_group)
                continue

            fstpy.create_grid_set(input_grid, self.output_grid)
            
            if self.parallel:
                vectorial_interpolation_parallel(vect_df,  results, input_grid, self.output_grid, None, None, None)
                scalar_interpolation_parallel   (others_df,results, input_grid, self.output_grid, None, None, None)
            else:    
                vectorial_interpolation(vect_df,  results, input_grid, self.output_grid, None, None, None)
                scalar_interpolation   (others_df,results, input_grid, self.output_grid, None, None, None)

            scalar_interpolation_pt(pt_df, results, input_grid, self.output_grid)

            if grtyp == 'U':
                rmn.gdrls(subgridId1)
                rmn.gdrls(subgridId2)
            # Plante dans le cas des autres grilles.  
            # Pas necessaire absolument.
            # else:
            #     rmn.gdrls(input_grid)

        res_df = pd.DataFrame(dtype=object)
        if len(results):
            res_df = pd.concat(results, ignore_index=True)
            res_df = fstpy.set_new_grid_identifiers(res_df,
                                                    self.grtyp,
                                                    self.ni,
                                                    self.nj,
                                                    self.ig1,
                                                    self.ig2,
                                                    self.ig3,
                                                    self.ig4)
            
            res_df = fstpy.add_flag_values(res_df)
            res_df.interpolated = True

        no_mod_df  = pd.DataFrame(dtype=object)

        if len(no_mod):
            no_mod_df = pd.concat(no_mod, ignore_index=True)

        if not no_mod_df.empty:
            res_df = pd.concat([res_df, no_mod_df], ignore_index=True)

        if not self.all_meta_df.empty:
            res_df = pd.concat([res_df, self.all_meta_df], ignore_index=True)

        if not self.toctoc_df.empty:

            self.toctoc_df = fstpy.set_new_grid_identifiers_for_toctoc(self.toctoc_df, self.ig1, self.ig2)
            res_df         = pd.concat([res_df, self.toctoc_df], ignore_index=True)

        if not self.hy_df.empty:

            res_df = pd.concat([res_df, self.hy_df], ignore_index=True)

        res_df = fstpy.metadata_cleanup(res_df)

        # Ajout des colonnes reliees a l'etiket
        res_df = fstpy.add_columns(res_df, columns=['etiket'])

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

def set_extrapolation_type_options(extrapolation_type: str, extrapolation_value: Optional[float]) -> None:
    """
    Sets the options for extrapolation based on the specified type and value.

    :param extrapolation_type: The type of extrapolation to configure ('value' or other).
    :type extrapolation_type: str
    :param extrapolation_value: The value to use for extrapolation when the type is 'value'. Can be None.
    :type extrapolation_value: Optional[float]
    """
    if extrapolation_type == 'value':
        if extrapolation_value is None:
            raise InterpolationHorizontalGridError(
                f'Extrapolation_value {extrapolation_value} is not set')
        rmn.ezsetval('EXTRAP_VALUE', extrapolation_value)
        rmn.ezsetopt('EXTRAP_DEGREE', 'VALUE')
    else:
        # print( self.extrapolation_type.upper())
        rmn.ezsetopt('EXTRAP_DEGREE', extrapolation_type.upper())   


def scalar_interpolation_pt(df: pd.DataFrame, results: List[pd.DataFrame], input_grid: int, output_grid: int) -> None:
    """
    Performs scalar interpolation on a dataframe containing "PT".  PT is always extrapolated with NEAREST.

    This function temporarily sets the extrapolation degree to 'NEAREST'.  

    :param df: The input DataFrame containing the data to be interpolated.
    :type df: pandas.DataFrame
    :param results: A list to append the processed DataFrames to.
    :type results: list[pandas.DataFrame]
    :param input_grid: Input gridid
    :type input_grid: int
    :param output_grid: Output gridid
    :type output_grid: int
    """ 
    if df.empty:
        return

    extrap_degree = rmn.ezgetopt(rmn.EZ_OPT_EXTRAP_DEGREE, vtype=str)
    rmn.ezsetopt('EXTRAP_DEGREE', 'NEAREST')

    scalar_interpolation(df, results, input_grid, output_grid, None, None, None)

    rmn.ezsetopt('EXTRAP_DEGREE', extrap_degree)

def set_output_column_values(meta_df: pd.DataFrame, field_df: pd.DataFrame) -> Tuple[float, float, float, float]:
    """
    Extracts specific column values from the first row of two DataFrames and raises an error if either DataFrame is empty.

    This function retrieves the values of columns 'ip1', 'ip2', 'ig3', and 'ig4' from the first row of both `meta_df` and `field_df`. If either DataFrame is empty, it raises an `InterpolationHorizontalGridError`.

    :param meta_df: The metadata DataFrame containing the 'ip1' and 'ip2' columns.
    :type meta_df: pandas.DataFrame
    :param field_df: The field DataFrame containing the 'ig3' and 'ig4' columns.
    :type field_df: pandas.DataFrame
    :return: A tuple containing the extracted values from the first rows of both DataFrames.
    :rtype: tuple[float, float, float, float]
    :raises InterpolationHorizontalGridError: If either `meta_df` or `field_df` is empty.
    """
    if meta_df.empty or field_df.empty:
        raise InterpolationHorizontalGridError('Missing data in meta_df or field_df')
    
    ig1 = meta_df.iloc[0]['ip1']
    ig2 = meta_df.iloc[0]['ip2']
    ig3 = field_df.iloc[0]['ig3']
    ig4 = field_df.iloc[0]['ig4']
    
    return ig1, ig2, ig3, ig4
