# -*- coding: utf-8 -*-create_grid_set
import warnings
import fstpy
import numpy as np
import pandas as pd
from typing import List
from ..plugin import Plugin, PluginParser
from ..utils import initializer, to_dask, to_numpy

from ..interpolationutils import (find_index_of_lat_lon_not_in_grid,
                                  keep_intact_hy_field, keep_toctoc,
                                  scalar_interpolation,
                                  scalar_interpolation_parallel,
                                  set_interpolation_type_options,
                                  select_input_grid_source_data, 
                                  vectorial_interpolation, vectorial_interpolation_parallel)

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
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """

    grid_types          = ['A', 'B', 'G', 'L', 'N', 'S']
    extrapolation_types = ['maximum', 'minimum', 'value', 'abort']
    interpolation_types = ['nearest', 'bi-linear', 'bi-cubic']

    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            interpolation_type: str    = 'bi-cubic',
            extrapolation_type: str    = 'maximum',
            extrapolation_value: float = None,
            parallel: bool             = False,
            reduce_df                  = True):
        
        super().__init__(self.df)
        self.df = fstpy.metadata_cleanup(self.df)
        self.prepare_groups()

    def prepare_groups(self):

        self.lat_lon_df = self.df.loc[self.df.nomvar.isin(["LAT", "LON"])]
 
        if self.lat_lon_df.empty:
            raise InterpolationHorizontalPointError('Missing latitudes and longitudes')
        
        self.validate_params()
        set_interpolation_type_options(self.interpolation_type)

        self.define_output_grid()

        self.groups = self.df.groupby('grid')

    def define_output_grid(self):
        if ('LON' in self.lat_lon_df.nomvar.to_list()) and \
           ('LAT' in self.lat_lon_df.nomvar.to_list()):
            self.lat_lon_df = self.lat_lon_df.loc[self.lat_lon_df.nomvar.isin(["LAT", "LON"])].reset_index(drop=True)

            (ni, nj, _, ax, ay, 
             ig1, ig2, ig3, ig4)    = (fstpy.get_grid_parameters_from_latlon_fields(self.lat_lon_df))

            # Lorsqu'on recoit un array avec une seule dimension( cas des donnees provenant du ReaderCsv)
            # on doit le modifier pour avoir 2 dimensions.
            # Ex: on veut ax = [[-44.75], [-73.38], [-123.18]] au lieu de ax = [-44.75,-73.38,-123.18]
            if ax.ndim == 1:
                ax = ax.reshape(ni, 1)
            if ay.ndim == 1:
                ay = ay.reshape(ni, 1)

            infos_grid              = fstpy.define_grid('Y', 'L', ni, nj, ig1, ig2, ig3, ig4, ax, ay, None)
            self.output_grid,*other = infos_grid

            self.lat         = self.lat_lon_df.loc[self.lat_lon_df.nomvar == "LAT"].reset_index(drop=True).at[0,'d']
            self.lat         = to_numpy(self.lat)    
            self.lon         = self.lat_lon_df.loc[self.lat_lon_df.nomvar == "LON"].reset_index(drop=True).at[0,'d']
            self.lon         = to_numpy(self.lon) 

            self.lat_lon_df.loc[self.lat_lon_df.nomvar == "LAT", 'nomvar'] = '^^'
            self.lat_lon_df.loc[self.lat_lon_df.nomvar == "LON", 'nomvar'] = '>>'
            self.lat_lon_df.loc[:, 'grtyp']   = 'L'
            self.lat_lon_df.loc[:, 'ig1']     = 100
            self.lat_lon_df.loc[:, 'ig2']     = 100
            self.lat_lon_df.loc[:, 'ig3']     = 9000
            self.lat_lon_df.loc[:, 'ig4']     = 0
   
            # Initialisation de champs, necessaire lors de la reduction de colonnes
            self.lat_lon_df['etiket']         = '  '
            self.lat_lon_df['run']            = '__'
            self.lat_lon_df['implementation'] = 'X'
            self.lat_lon_df['etiket_format']  = ''
            self.lat_lon_df['label']          = 'INTHPT'
            self.lat_lon_df['typvar']         = "X"

        else:
            raise InterpolationHorizontalPointError('Missing longitudes and/or latitudes to process')

    def validate_params(self):
        if self.interpolation_type not in self.interpolation_types:
            raise InterpolationHorizontalPointError(
                f'Interpolation_type {self.interpolation_type} not in {self.interpolation_types}')
        if self.extrapolation_type not in self.extrapolation_types:
            raise InterpolationHorizontalPointError(
                f'Extrapolation_type {self.extrapolation_type} not in {self.extrapolation_types}')

    def compute(self) -> pd.DataFrame:
        results = []
        no_mod  = []
        for _, current_group in self.groups:

            keep_intact_hy_field(current_group, no_mod)

            keep_toctoc(current_group, results)

            vect_df   = current_group.loc[current_group.nomvar.isin(['UU', 'VV'])].reset_index(drop=True)

            others_df = current_group.loc[~current_group.nomvar.isin(
                        ['UU', 'VV', 'PT', 'LAT', 'LON', '>>', '^^', '^>', '!!', 'HY'])].reset_index(drop=True)

            pt_df     = current_group.loc[current_group.nomvar == 'PT'].reset_index(drop=True)

            source_df, grtyp = select_input_grid_source_data(vect_df, others_df, pt_df)

            if source_df.empty:
                continue

            meta_df    = current_group.loc[current_group.nomvar.isin(['>>', '^^', '^>'])].reset_index(drop=True)

            if grtyp == 'U':
                infos_grid = fstpy.define_input_grid(grtyp, source_df, meta_df)
                if len(infos_grid) != 3:
                    raise InterpolationHorizontalPointError(f'Problem with definition of grid of type U')
                    
                input_grid, subgridId1, subgridId2 = infos_grid 
            else:
                
                infos_grid         = fstpy.define_input_grid(grtyp, source_df, meta_df)
                input_grid, *other = infos_grid

            grids_are_equal = fstpy.check_grid_equality(input_grid, self.output_grid)

            if grids_are_equal:
                no_mod.append(current_group)
                continue

            fstpy.create_grid_set(input_grid, self.output_grid)

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

            indexes = find_index_of_lat_lon_not_in_grid(input_grid, ni, nj, self.lat, self.lon)

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

            for i in res_df.index:
                if res_df.at[i, 'nomvar'] == '!!':
                    continue

                res_df.at[i, 'd']   = to_dask(res_df.at[i, 'd'])
                res_df              = fstpy.add_flag_values(res_df)
                res_df.interpolated = True

        no_mod_df = pd.DataFrame(dtype=object)

        if len(no_mod):
            no_mod_df = pd.concat(no_mod, ignore_index=True)

        toctoc_res_df = fstpy.set_new_grid_identifiers_for_toctoc(res_df, 0, 0)

        other_res_df  = fstpy.set_new_grid_identifiers( res_df,
                                                        'Y',
                                                        len(self.lat),
                                                        1,
                                                        self.lat_lon_df.iloc[0]['ip1'],
                                                        self.lat_lon_df.iloc[0]['ip2'],
                                                        self.lat_lon_df.iloc[0]['ip3'],
                                                        0)

        if not toctoc_res_df.empty:
            other_res_df = pd.concat([other_res_df, toctoc_res_df], ignore_index=True)

        if not no_mod_df.empty:
            other_res_df = pd.concat([other_res_df, no_mod_df], ignore_index=True)

        other_res_df     = pd.concat([other_res_df, self.lat_lon_df], ignore_index=True)

        other_res_df.loc[other_res_df.nomvar != 'HY', 'grid'] = '00000000'

        other_res_df     = fstpy.metadata_cleanup(other_res_df)

        # Traitement necessaire pour preparer les donnees avant le final_results;
        # ajout des colonnes reliees a l'etiket
        other_res_df = fstpy.add_columns(other_res_df, columns=['etiket'])

        # Necessaire car on doit remettre a jour self.meta_df
        self.meta_df = other_res_df.loc[other_res_df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "PT"])].reset_index(drop=True) 
        # Separation des donnees des metadonnees avant l'appel a final_results
        res_no_meta_df = other_res_df.loc[~other_res_df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY"])].reset_index(drop=True)

        return self.final_results([res_no_meta_df], 
                                InterpolationHorizontalPointError, 
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
        parser = PluginParser(prog=InterpolationHorizontalPoint.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--interpolationType',type=str,default="BI-CUBIC",choices=["NEAREST","BI-LINEAR","BI-CUBIC"],dest='interpolation_type', help="Type of interpolation.")
        parser.add_argument('--extrapolationType',type=str,default="MAXIMUM",dest='extrapolation_type',help="Type of extrapolation.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['interpolation_type']      = parsed_arg['interpolation_type'].lower()

        if parsed_arg['extrapolation_type'] in ["MAXIMUM","MINIMUM","ABORT"]:
            parsed_arg['extrapolation_type']  = parsed_arg['extrapolation_type'].lower()
        elif parsed_arg['extrapolation_type'].startswith("VALUE="):
            parsed_arg['extrapolation_value'] = float(parsed_arg['extrapolation_type'].replace("VALUE=",""))
            parsed_arg['extrapolation_type']  = "value"

        return parsed_arg

def scalar_interpolation_pt(df: pd.DataFrame, results: List[pd.DataFrame], ni: int) -> None:
    """
    Performs scalar interpolation and appends the result to a results list.

    :param df: The input DataFrame containing the data to be interpolated.
    :type df: pandas.DataFrame
    :param results: A list to append the processed DataFrame to.
    :type results: list[pandas.DataFrame]
    :param ni: The size of the numpy array to create for the target point's value.
    :type ni: int
    """
    if df.empty:
        return
    
    # scalar except PT
    int_df       = df.copy(deep=True)
    int_df       = int_df.reset_index(drop=True)
    df.at[0,'d'] = to_numpy(df.at[0,'d'])

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        arr = np.expand_dims(np.full(ni, df.at[0,'d'].flat[0], dtype=np.float32, order='F'), axis=-1)
    for i in df.index:  # should only be one
        int_df.at[i, 'd'] = arr

    results.append(int_df)
