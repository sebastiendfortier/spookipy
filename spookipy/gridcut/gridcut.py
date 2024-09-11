# -*- coding: utf-8 -*-
import logging

import fstpy
import pandas as pd

from ..plugin import Plugin, PluginParser
from ..utils import initializer, to_numpy


class GridCutError(Exception):
    pass


class GridCut(Plugin):
    """Cuts a piece out of a grid, defined by its upper left hand corner and lower right hand corner.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param start_point: The upper left point of the matrix, defaults to (0, 0)
    :type start_point: tuple, optional
    :param end_point: The lower right point of the matrix, defaults to (1, 1)
    :type end_point: tuple, optional
    :param grid_tag: The ip[1-3]/ig[1-3] values to identify the resulting grid. ex (110,240,3). Default will be to increase ip3/ig3 by one.
    :type grid_tag: tuple, optional
    """
    @initializer
    def __init__(self, df: pd.DataFrame, start_point=(0, 0), end_point=(1, 1), grid_tag=None):

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise GridCutError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.validate_coords()

        self.validate_grid_tag()

        self.tictictactac_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>"])].reset_index(drop=True)

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^>", "!!", "!!SF", "HY"])].reset_index(drop=True)

        self.validate_grid()

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^>", ">>", "^^", "!!", "!!SF", "HY"])].reset_index(drop=True)

    def validate_grid(self):
        tictac_df = self.meta_df.loc[self.meta_df.nomvar == "^>"].reset_index(
            drop=True)
        if not tictac_df.empty:
            raise GridCutError('Cannot handle yin yan grids')

    def validate_coords(self):
        if (not isinstance(self.start_point, tuple)):
            raise GridCutError('Start_point must be a tuple of 2 elements')
        if (not isinstance(self.end_point, tuple)):
            raise GridCutError('End_point must be a tuple of 2 elements')
        if len(self.start_point) != 2:
            raise GridCutError('Start_point must be a tuple of 2 elements')
        if len(self.end_point) != 2:
            raise GridCutError('End_point must be a tuple of 2 elements')
        if (self.start_point[0] > self.end_point[0]) or (
                self.start_point[1] > self.end_point[1]):
            raise GridCutError(
                'Start point must be inferior on all axes to end point')

    def validate_grid_tag(self):

        if self.grid_tag == None:
            return # no grid tag specified, default behavior will be used

        # Check if the tuple has exactly three elements
        if len(self.grid_tag) != 3:
            raise GridCutError('grid_tag must be a tuple of 3 positive integers')
        else:
            # Validate each element
            for elem in self.grid_tag:
                if not isinstance(elem, int) or elem <= 0:
                    raise GridCutError(f"grid_tag must have 3 positives integers. '{str(elem)}' is not a positive integer.")


    def compute(self) -> pd.DataFrame:
        logging.info('GridCut - compute')
        cp_df = self.df.copy(deep=True)

        # cp_df["shape"].map(lambda nix, njy: (nix <=  self.end_point[0]) or (njy <= self.end_point[1])).any()
        # cp_df['d'] = cp_df["d"].map(lambda d: d[self.start_point[0]:self.end_point[0]+1,self.start_point[1]:self.end_point[1]+1])
        for i in cp_df.index:
            if (cp_df.at[i, 'ni'] <= self.end_point[0]) or (
                    cp_df.at[i, 'nj'] <= self.end_point[1]):
                raise GridCutError('You asked for more values than exists')
            cp_df.at[i,
                     'd'] = cp_df.at[i,'d'][self.start_point[0]:self.end_point[0] + 1,
                                            self.start_point[1]:self.end_point[1] + 1]

            cp_df.at[i, 'ni'] = cp_df.at[i, 'd'].shape[0]
            cp_df.at[i, 'nj'] = cp_df.at[i, 'd'].shape[1]

        cptic_df = self.tictictactac_df.loc[self.tictictactac_df.nomvar == "^^"].copy(deep=True)

        for i in cptic_df.index:
            # dask has problems with slicing, get the real array
            cptic_df.at[i, 'd'] = to_numpy(cptic_df.at[i, 'd'])

            if cptic_df.at[i, 'd'].ndim == 1:
                cptic_df.at[i, 'd'] = cptic_df.at[i, 'd'].reshape(cptic_df.at[i, 'ni'],cptic_df.at[i, 'nj'])

            cptic_df.at[i, 'd'] = cptic_df.at[i, 'd'][0:1,self.start_point[1]:self.end_point[1] + 1]

            cptic_df.at[i, 'nj'] = cptic_df.at[i, 'd'].shape[1]

        cptac_df = self.tictictactac_df.loc[self.tictictactac_df.nomvar == ">>"].copy(deep=True)

        for i in cptac_df.index:
            # dask has problems with slicing, get the real array
            cptac_df.at[i, 'd'] = to_numpy(cptac_df.at[i, 'd'])
            cptac_df.at[i, 'd'] = cptac_df.at[i,'d'][self.start_point[0]:self.end_point[0] + 1]

            cptac_df.at[i, 'ni'] = cptac_df.at[i, 'd'].shape[0]

        # adjust grid_tag, by default only increment ip3,ig3
        if self.grid_tag:
            cptic_df[['ip1', 'ip2', 'ip3']] = self.grid_tag
            cptac_df[['ip1', 'ip2', 'ip3']] = self.grid_tag
            cp_df.loc[cp_df['grtyp'].isin(['Z', 'Y']), ['ig1','ig2','ig3']] = self.grid_tag
        else:
            cptic_df['ip3'] += 1
            cptac_df['ip3'] += 1
            cp_df.loc[cp_df['grtyp'].isin(['Z', 'Y']), ['ig3']] += 1

        res_df = pd.concat([cp_df, self.meta_df, cptic_df,
                           cptac_df], ignore_index=True)

        # because gridcut manipulate directly the ips/igs, drop all expended columns to keep the changes done to ips/igs
        fstpy.remove_all_expanded_columns(res_df)

        res_df = fstpy.metadata_cleanup(res_df)

        res_df['origin_point'] = [self.start_point] * len(res_df)

        return res_df

    def check_limits(self, shape):
        return (shape[0] <= self.end_point[0]) or (shape[1] <= self.end_point[1])

# if cp_df["shape"].map(check_limits).any():
#     print("Limits are not good ...")

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=GridCut.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--startPoint',type=str,required=True,dest="start_point", help="Starting point of the selected matrix.")
        parser.add_argument('--endPoint',type=str,required=True,dest="end_point", help="Ending point of the selected matrix.")
        parser.add_argument('--gridTag',type=str,required=False,dest="grid_tag", help="The ip[1-3]/ig[1-3] values to identify the resulting grid. ex: --gridTag 110,240,3. Default will be to only increase ip3/ig3 by one")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg["start_point"] = tuple(map(int, parsed_arg["start_point"].split(',')))
        parsed_arg["end_point"] = tuple(map(int, parsed_arg["end_point"].split(',')))

        if parsed_arg["start_point"][0] < 0 or parsed_arg["start_point"][1] < 0 or parsed_arg["end_point"][0] < 0 or parsed_arg["end_point"][1] < 0:
            raise Exception("Start point and end point needs to be positive.")
        # TODO should we check it's >0?

        if parsed_arg["grid_tag"] != None:
            try:
                parsed_arg["grid_tag"] = tuple(map(int, parsed_arg["grid_tag"].split(',')))
            except ValueError:
                raise GridCutError("gridTag parameter must have 3 positives integers separated by comma. ex: --gridTag 4,1000,1002")

        return parsed_arg
