# -*- coding: utf-8 -*-
import argparse
import logging

import fstpy
import pandas as pd

from ..plugin import Plugin, PluginParser
from ..utils import (create_empty_result, existing_results, final_results,
                     get_existing_result, get_intersecting_levels)


class HelicityError(Exception):
    pass


class Helicity(Plugin):
    """Calculation of relative helicity, a necessary tool for forecasting severe thunderstorms

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param z3: vertical level corresponding to ~850mb, defaults to 0.851343
    :type z3: float, optional
    :param z4: vertical level corresponding to ~300mb, defaults to 0.297078
    :type z4: float, optional
    """
    def __init__(self, df: pd.DataFrame, z3=0.851343, z4=0.297078):

        self.plugin_mandatory_dependencies = [{
            'UU': {'nomvar': 'UU', 'unit': 'knot'},
            'VV': {'nomvar': 'VV', 'unit': 'knot'},
        }]
        self.plugin_result_specifications = {
            'UV': {'nomvar': 'UV', 'etiket': 'WNDMOD', 'unit': 'knot'}
        }
        self.df = df
        # ajouter forecast_hour et unit
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise HelicityError('No data to process')

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
        # print(self.df[['nomvar','typvar','etiket','dateo','forecast_hour','ip1_kind','grid']].to_string())
        self.groups = self.df.groupby(
            ['grid', 'datev', 'ip1_kind'])

    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results(
                'Helicity', self.existing_result_df, self.meta_df)

        logging.info('Helicity - compute')
        df_list = []
        for _, current_fhour_group in self.fhour_groups:
            current_fhour_group = get_intersecting_levels(
                current_fhour_group, self.plugin_mandatory_dependencies)
            if current_fhour_group.empty:
                logging.warning('Helicity - no intersecting levels found')
                continue

            uu_df = current_fhour_group.loc[current_fhour_group.nomvar == "UU"].reset_index(
                drop=True)
            vv_df = current_fhour_group.loc[current_fhour_group.nomvar == "VV"].reset_index(
                drop=True)
            uv_df = create_empty_result(
                vv_df, self.plugin_result_specifications['UV'], all_rows=True)

            for i in uv_df.index:
                uu = uu_df.at[i, 'd']
                vv = vv_df.at[i, 'd']
                # uv_df.at[i,'d'] = wind_modulus(uu,vv)

            df_list.append(uv_df)

        return final_results(df_list, HelicityError, self.meta_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=Helicity.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--Z3',type=float,dest='z3', help="First vertical level default 850mb")
        parser.add_argument('--Z4',type=float,dest='z4', help="Last vertical level default 300mb")

        parsed_arg = vars(parser.parse_args(args.split()))

        return parsed_arg

    # struct helicity
    # {
    #     helicity(boost::function<void (void)> f): _f(f) {}
    #     void operator()
    #     (
    #             const vector<IFlatSlice<float>::iterator> & UUNcarrot,
    #             const vector<IFlatSlice<float>::iterator> & VVNcarrot,
    #             const vector<IFlatSlice<float>::iterator> & GZcarrot,
    #             const float & CX,
    #             const float & CY,
    #             const float & Z2,
    #             float & HL
    #     )
    #     {
    #         SPOOKI_ASSERT(UUNcarrot.size() == VVNcarrot.size());
    #         _f();
    #         size_t UUNSize(UUNcarrot.size());
    #         const float & UUNZ1(*(UUNcarrot[0])), UUNZ2(*(UUNcarrot[size_t(Z2)]));
    #         const float & VVNZ1(*(VVNcarrot[0])), VVNZ2(*(VVNcarrot[size_t(Z2)]));
    #         const float & GZZ1(*(GZcarrot[0])), GZZ2(*(GZcarrot[size_t(Z2)]));
    #         float HL1 = ((VVNZ2 - VVNZ1) *  CX) - ((UUNZ2 - UUNZ1) * CY) ;
    #         float HL0(0);

    #         for (size_t Z(0); Z <= (size_t)Z2; ++Z)
    #         {
    #             if((Z + 1) == ((size_t)Z2 + 1) or Z + 1 > UUNSize)
    #             {
    #                 break;
    #             }
    #             const float & UUNZ(*(UUNcarrot[Z])), UUNZP(*(UUNcarrot[Z + 1])), VVNZ(*(VVNcarrot[Z])), VVNZP(*(VVNcarrot[Z + 1]));
    #             HL0 += (UUNZP * VVNZ) - (UUNZ * VVNZP);
    #         }

    #         HL = (HL0 + HL1)*(300/(GZZ2-GZZ1));
    #     }
    #     boost::function<void (void)> _f;
    # };
