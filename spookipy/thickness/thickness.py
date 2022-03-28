from ast import Or
from mimetypes import init
from turtle import pd
from spookipy.utils import initializer
from ..plugin.plugin import Plugin
import pandas as pd
import fstpy.all as fstpy
from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe,
                     initializer, DependencyError)
import logging

class ThicknessError(Exception):
    pass

class VctypesError(Exception):
    pass

class ParametersValuesError(Exception):
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
                coordinate_type: str,
                dependency_check = False):

        self.plugin_mandatory_dependencies = [
            {
                # in this case we want gz in decameter from the dataframe
                'GZ': {'nomvar': 'GZ', 'unit': 'decameter'},
            }
        ]

        self.plugin_result_specifications = {
            'DZ': {
                'nomvar': 'DZ', 'unit': 'decameter'}
        }
        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)
        self.prepare_groups(self)

    def prepare_groups(self):
        
        self.no_meta_df = fstpy.set_vertical_coordinate_type(self.no_meta_df)

        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)
        
        self.groups = self.no_meta_df.groupby(['grid', 'vctype'])

       
    def verify_parameters_values(self):
        self.verify_top_base_values(self)
        self.verify_vctype(self)

    def verify_vctype(self):
        
        if self.coordinate_type not in fstpy.vctype_dict.keys():
            raise VctypesError('The vctypes values in the dataframe are not supported')
        else:
            self.coordinate = fstpy.vctype_dict[self.coordinate_type]


    def verify_top_base_values(self):
        if (self.base > 0) and (self.top > 0):
            if self.base > self.top:
                raise ParametersValuesError("The base value is higher than the top value")

            if self.base == self.top:
                raise ParametersValuesError("The base value is equal to the top value")
            
            else:
                return True
        else:
            raise ParametersValuesError("The base value or the top value is negative")

       

    def compute(self):
        if self.df.empty:
            raise ThicknessError('No data to process')
        
        if not self.existing_result_df.empty:
            return existing_results(
                'Thickness',
                self.existing_result_df,
                self.meta_df)

        logging.info('Thickness - compute')
        df_list = []
        try:
            self.plugin_mandatory_dependencies[0]["GZ"]["vctype"]=self.coordinate
            print(self.plugin_mandatory_dependencies)

            dependencies_list = get_dependencies(
                self.groups,
                self.meta_df,
                'Thickness',
                self.plugin_mandatory_dependencies,
                intersect_levels=False)

        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f'{Thickness} - No matching dependencies found')
        else:
            for dependencies_df, _ in dependencies_list:
                gz_df = get_from_dataframe(dependencies_df, 'GZ')
                gz_top_df = gz_df.loc[gz_df.level == self.top]
                gz_base_df = gz_df.loc[gz_df.level == self.base]

                dz_df = create_empty_result(
                    gz_df,
                    self.plugin_result_specifications['DZ'],
                    all_rows=False)
                    
                dz_df = gz_top_df.iloc[0].d - gz_base_df.iloc[0].d

            df_list.append(dz_df)

        finally:
            return final_results(df_list, ThicknessError, self.meta_df, self.dependency_check)






