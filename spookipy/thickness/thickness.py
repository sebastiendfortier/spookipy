from mimetypes import init
from turtle import pd
from spookipy.utils import initializer
from ..plugin.plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
from ..utils import (create_empty_result, existing_results,  # plugin tools
                     final_results, get_dependencies, get_existing_result,
                     get_from_dataframe)

class ThicknessError(Exception):
    pass


class Thickness(Plugin):
    """Check that the vertical coordinate type of the input field corresponds to the "coordinate_type" key passed as a parameter
    if so, look in the input field for the levels passed as a parameter and do at each point:
    DZ = ABS ( GZ(top) - GZ(base) )
    rename the values concerned (nomvar) without changing other values


    :param df: dataframe with the data
    :type df: pd.DataFrame
    :param base: Base of the thickness layer (model or pressure level)
    :type base: float
    :param top: Top of the thickness layer (model or pressure level)
    :type top: float
    :param coordinate_type: Type of vertical coordinate
    :type coordinate_type: str
    """

    """
    cordinate type
    'SIGMA_1001': VerticalCoordType.SIGMA_1001,
    'ETA_1002': VerticalCoordType.ETA_1002,
    'HYBRID_NORMALIZED_1003': VerticalCoordType.HYBRID_NORMALIZED_1003,
    "PRESSURE_2001": VerticalCoordType.PRESSURE_2001,
    "HYBRID_5001": VerticalCoordType.HYBRID_5001,
    "HYBRID_5002": VerticalCoordType.HYBRID_5002,
    "HYBRID_5003": VerticalCoordType.HYBRID_5003,
    "HYBRID_5004": VerticalCoordType.HYBRID_5004,
    "HYBRID_5005": VerticalCoordType.HYBRID_5005,
    "UNKNOWN": VerticalCoordType.UNKNOWN,
    """

    @initializer
    def __init__(self,df: pd.DataFrame,
                base: float,
                top: float,
                coordinate_type: str):
        self.plugin_mandatory_dependencies = [
            {
                # in this case we want gz in decameter from the dataframe
                # dont forget to add GZ to the get_plugin_dependencies lists
                'GZ': {'nomvar': 'GZ', 'unit': 'decameter'},
            }
        ]

        self.plugin_result_specifications = {
            'GZ': {
                'nomvar': 'GZ', 'unit': 'decameter'}
        }
        
        self.validate_input(self)

    def validate_input(self):
        if self.df.empty:
            raise ThicknessError('No data to process')

        # cleaup the metadata fields that we received with the dataframe
        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(
            drop=True)   # keep the metadata to be added at the end

        # add some columns if they are not already in the dataframe
        self.df = fstpy.add_columns(
            self.df, columns=['ip_info'])

        # this helps with sorting and grouping the data
        # ip_info tag includes the decoding (gets the kind and value) of ip1, ip2 ip3
        # the virtical coordinate type, the surface flag, the virtical coordinate type
        # and the ascending value for the type of level

        # check if result already exists
        # this function will look in the dataframe to see if the result isn't
        # already present
        self.existing_result_df = get_existing_result(
            self.df, self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(
            drop=True)  # get dataframe without metadata

        self.groups = self.df.groupby(
            ['vctype','ip1_kind'])



    def compute():


        pass




