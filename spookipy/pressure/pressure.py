# -*- coding: utf-8 -*-
import pandas as pd

import fstpy.all as fstpy
from ..plugin import Plugin
from ..utils import final_results, initializer

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
    """

    @initializer
    def __init__( self, df: pd.DataFrame, 
                reference_field=None, 
                standard_atmosphere: bool = False, 
                dependency_check=False):
        super().__init__(df)
        if not (self.reference_field is None):
            self.no_meta_df = self.no_meta_df.loc[self.no_meta_df.nomvar == self.reference_field]
            self.df = pd.concat([self.meta_df,self.no_meta_df], ignore_index=True)
        
        self.df = self.df.drop(columns=['level', 'ip1_kind', 'ip1_pkind', 'ip2_dec', 'ip2_kind', 'ip2_pkind',
                                        'ip3_dec', 'ip3_kind', 'ip3_pkind', 'surface', 'follow_topography',
                                        'ascending', 'interval', 'vctype'],errors='ignore')

        self.qp = fstpy.QuickPressure(self.df,self.standard_atmosphere)


    def compute(self, test_dependency=False) -> pd.DataFrame:
        """groups records by grid->vctype->forecast_hour then applies the appropriate algorithm to compute the pressure

        :return: a dataframe containing available pressure
        :rtype: pd.DataFrame
        """
        res_df = self.qp.compute()
        return final_results([res_df],PressureError,self.meta_df,self.dependency_check)
