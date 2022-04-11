from turtle import pd
import rpnpy.librmn.all as rmn
import argparse
from spookipy.plugin import Plugin
import pandas as pd
import numpy as np
import fstpy.all as fstpy
from spookipy.utils import (create_empty_result, existing_results, final_results,
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
    cordinate type:
    'SIGMA_1001': VerticalCoordType.SIGMA_1001,SIGMA_COORDINATE
    'ETA_1002': VerticalCoordType.ETA_1002,ETA_COORDINATE
    'HYBRID_NORMALIZED_1003': VerticalCoordType.HYBRID_NORMALIZED_1003,
    "PRESSURE_2001": VerticalCoordType.PRESSURE_2001,PRESSURE_COORDINATE
    "HYBRID_5001": VerticalCoordType.HYBRID_5001,HYBRID_COORDINATE
    "HYBRID_5002": VerticalCoordType.HYBRID_5002,HYBRID_STAGGERED_COORDINATE
    "HYBRID_5003": VerticalCoordType.HYBRID_5003,
    "HYBRID_5004": VerticalCoordType.HYBRID_5004,
    "HYBRID_5005": VerticalCoordType.HYBRID_5005,
    "UNKNOWN": VerticalCoordType.UNKNOWN,


    :param df: dataframe with the data
    :type df: pd.DataFrame
    :param base: Base of the thickness layer (model or pressure level)
    :type base: float
    :param top: Top of the thickness layer (model or pressure level)
    :type top: float
    :param coordinate_type: Type of vertical coordinate. choices: SIGMA_1001, ETA_1002, HYBRID_NORMALIZED_1003, PRESSURE_2001,HYBRID_5001, HYBRID_5002, HYBRID_5003, HYBRID_5004, HYBRID_5005, METER_SEA_LEVEL, METER_GROUND_LEVEL, UNKNOWN
    :type coordinate_type: str
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
                'GZ': {'nomvar': 'GZ','unit':'decameter'}
            }
        ]

        self.plugin_result_specifications = {
            'DZ': {'nomvar': 'DZ','unit':'decameter','etiket':'THCKNS'}
        }

        df = fstpy.set_vertical_coordinate_type(df)
        print(df.drop(columns='d').to_string())
        # self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(df)
        self.prepare_groups()
        self.verify_parameters_values()
        

    def prepare_groups(self):
        
        # self.no_meta_df = fstpy.set_vertical_coordinate_type(self.no_meta_df)
        # self.no_meta_df = fstpy.compute(self.no_meta_df)
        print("no_meta df:")
        print(self.no_meta_df.drop(columns="d").to_string())
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)
        self.groups = self.no_meta_df.groupby(['grid', 'vctype','ip1_kind'])

       
    def verify_parameters_values(self):
        self.verify_top_base_values()
        self.verify_vctype()

    def verify_vctype(self):
        """Verify that the type of vertical coordinates is accurate

        :raises VctypesError: raises an error when the type of vertical coordinates is not accurate
        """
        
        if self.coordinate_type not in fstpy.vctype_dict.keys():
            raise VctypesError('The vctypes values in the dataframe are not supported')
        else:
            self.coordinate = fstpy.vctype_dict[self.coordinate_type]


    def verify_top_base_values(self):
        """Verify that the top and base values are not negative or equal to the other value
        """

        if (self.base > 0) and (self.top > 0):
            if self.base == self.top:
                raise ParametersValuesError("The base value is equal to the top value")
            else:
                return True

        else:
            raise ParametersValuesError("The base value or the top value is negative")


    def compute(self)-> pd.DataFrame:
        logging.info('Thickness - compute')
        df_list = []

        # If a row DZ already exists in the dataframe we return the result
        if not self.existing_result_df.empty:
            return existing_results(
                'Thickness',
                self.existing_result_df,
                self.meta_df)

        try:
            self.plugin_mandatory_dependencies[0]["GZ"]["vctype"]=self.coordinate
            print("plugin_mandatory_dependencies:")
            print(self.plugin_mandatory_dependencies)

            dependencies_list = get_dependencies(
                self.groups,
                self.meta_df,
                'Thickness',
                self.plugin_mandatory_dependencies,
                intersect_levels=False)
            print("dependencies list:")
            print(dependencies_list)

        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f'{Thickness} - No matching dependencies found')
                
        else:
            for dependencies_df, _ in dependencies_list:
                print("ok................")
                gz_df = get_from_dataframe(dependencies_df, 'GZ')
                print("gz_df")
                print(gz_df)
                gz_top_df = gz_df.loc[gz_df.level == self.top]
                top_ip = gz_top_df.iloc[0].ip1
                print("top")
                print(gz_top_df[['nomvar','typvar','ip1','ip3','vctype','ip1_kind','ip2','level']])
                # print(gz_top_df.drop(columns='d'))
                gz_base_df = gz_df.loc[gz_df.level == self.base]
                base_ip = gz_base_df.iloc[0].ip1
                print("base:")
                # print(gz_base_df.drop(columns='d'))
                print(gz_base_df[['nomvar','typvar','ip1','ip3','vctype','ip1_kind','ip2','level']])



                # dz_df = create_empty_result(
                #     gz_df,
                #     self.plugin_result_specifications['DZ'],
                #     all_rows=False)
                if (self.base < self.top):
                    b_inf = top_ip
                    b_sup = base_ip
                else:
                    b_inf = base_ip
                    b_sup = top_ip

                dz_df = create_result_container(gz_df,b_inf,b_sup,self.plugin_result_specifications)
    
                array = np.abs(gz_top_df.iloc[0].d - gz_base_df.iloc[0].d).astype(np.float32)
                dz_df["d"] = [array]
                print("dz")
                # print(dz_df.drop(columns='d'))
                print(dz_df[['nomvar','typvar','ip1','ip3','vctype','ip1_kind','ip2']])

            df_list.append(dz_df)

        finally:
            return final_results(df_list, ThicknessError, self.meta_df, dependency_check=True)


    


    @staticmethod
    def parse_config(args: str) -> dict:

        parser = argparse.ArgumentParser(prog=Thickness.__name__, parents=[Plugin.base_parser])
        # parser.add_argument('--df',pd.DataFrame,help="dataframe with the data")
        parser.add_argument('--base',type=float)
        parser.add_argument('--top',type=float)
        parser.add_argument('--coordinateType',type=str,choices=['SIGMA_1001', 'ETA_1002', 'HYBRID_NORMALIZED_1003', 
                                                                'PRESSURE_2001', 'HYBRID_5001', 'HYBRID_5002', 'HYBRID_5003',
                                                                'HYBRID_5004', 'HYBRID_5005', 'METER_SEA_LEVEL',
                                                                'METER_GROUND_LEVEL', 'UNKNOWN'])     


def create_result_container(df, b_inf, b_sup, dict1):
    print("start...")
    ip1 = b_inf
    print(ip1)
    ip3 = b_sup
    ip2 = df.ip2[0]
    # print(ip2)
    # kind = int(ip1_kind)
    
    # ip1_enc = rmn.ip1_val(ip1, kind)
    # print(ip1_enc)
    # ip3_enc = rmn.ip1_val(ip3, kind)
    # ip2_enc = rmn.ip1_val(ip2,rmn.KIND_HOURS)
    # print(ip3_enc)

    dict1["DZ"]["ip1"] = ip1
    dict1["DZ"]["ip2"] = ip2
    dict1["DZ"]["ip3"] = ip3
    print(dict1)
    print("dict1 a compile")

    res_df = create_empty_result(df, dict1['DZ'],all_rows=False)
    print("res_df")
    # print(res_df.drop(columns='d').to_string())
    print(res_df[['nomvar','typvar','ip1','ip3','vctype','ip1_kind','ip2']])
    
    return res_df
