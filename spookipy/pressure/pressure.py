# -*- coding: utf-8 -*-
import argparse
import pandas as pd
import numpy as np

import fstpy
from ..plugin import Plugin, PluginParser
from ..utils import (initializer, validate_nomvar)

class PressureError(Exception):
    pass
class Pressure(Plugin):
    """creates a pressure field associated to a level for each identified vertical coordinate type

    :param df: input dataframe
    :type df: pd.DataFrame
    :param reference_field: field to use to get levels, defaults to None
    :type reference_field: str, optional
    :param standard_atmosphere: calculate pressure in standard atmosphere if specified, defaults to False
    :type standard_atmosphere: bool, optional
    :param dependency_check: Indicates the plugin is being called from another one who checks dependencies , defaults to False
    :type dependency_check: bool, optional  
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional 
    """

    computable_plugin = "PX"
    @initializer
    def __init__( self, df: pd.DataFrame, 
                reference_field=None, 
                standard_atmosphere: bool = False, 
                dependency_check=False,
                copy_input=False):

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)

        if not (self.reference_field is None):
            self.no_meta_df = self.no_meta_df.loc[self.no_meta_df.nomvar == self.reference_field]
            self.df = pd.concat([self.meta_df,self.no_meta_df], ignore_index=True)

        if 'path' not in df.columns:
            self.dropPath = True
        else:
            self.dropPath = False

        self.df = fstpy.add_path_and_key_columns(self.df)
        self.df.loc[self.df.path.isna(), 'path'] = '/TMP_PATH_TO_MAKE_PRESSURE_WORK'
        self.df["key"] = np.where(self.df.key.isna(), None, self.df.key)

        self.df = self.df.drop(columns=['level', 'ip1_kind', 'ip1_pkind', 'ip2_dec', 'ip2_kind', 'ip2_pkind',
                                        'ip3_dec', 'ip3_kind', 'ip3_pkind', 'surface', 'follow_topography',
                                        'ascending', 'interval', 'vctype'],
                               errors='ignore')

        self.qp = fstpy.QuickPressure(self.df,self.standard_atmosphere)


    def compute(self, test_dependency=False) -> pd.DataFrame:
        """groups records by grid->vctype->forecast_hour then applies the appropriate algorithm to compute the pressure

        :return: a dataframe containing available pressure
        :rtype: pd.DataFrame
        """
        res_df = self.qp.compute()

        # On supprime la colonne path si elle n'etait pas presente initialement dans les donnees en entree
        # car on veut remettre le dataframe dans son etat original (attention dataframe en input et non le resultat)
        if self.dropPath:
            self.df = self.df.drop(columns=['path', 'key'], errors='ignore')
        else:
            self.df["path"] = np.where(self.df["path"] == "/TMP_PATH_TO_MAKE_PRESSURE_WORK", None, self.df.path)

        return self.final_results([res_df], 
                                  PressureError, 
                                  dependency_check = self.dependency_check, 
                                  copy_input = self.copy_input)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=Pressure.__name__, parents=[Plugin.base_parser])
        parser.add_argument('--coordinateType',type=str,dest='coordinate_type', help="Deprecated - default to AUTODETECT ")
        parser.add_argument('--referenceField',type=str,dest='reference_field',help="Reference field used to define the grid on which PX is calculated.")
        parser.add_argument('--standardAtmosphere',dest='standard_atmosphere',action='store_true',default=False, help="Standard atmosphere condition (constant pressure).")
        
        parsed_arg = vars(parser.parse_args(args.split()))
        validate_nomvar(parsed_arg['reference_field'],"Pressure",PressureError)
 
        return parsed_arg
