# -*- coding: utf-8 -*-                                 # always use utf8 encoding when editing files        

from spookipy.utils import initializer
import fstpy.all as fstpy
import numpy as np
import pandas as pd
import logging                                                               # use logging for console output, logging.debug, logging.info, logging.warning, logging.critical
                                                                             # ex.: logging.info('ExamplePlugin - compute')
from ..plugin import Plugin                                                  # interface class for all plugins
from ..utils import (create_empty_result, existing_results, final_results,   # plugin tools
                     get_dependencies, get_existing_result,
                     get_from_dataframe)
from .fortran_function import fortran_function




def python_algorithm(a:np.ndarray,b:np.ndarray) -> np.ndarray:
    """Comment the function

    :param a: a  - dataframe data field
    :type a: np.ndarray
    :param b: b - dataframe data field
    :type b: np.ndarray
    :return: python_algorithm
    :rtype: np.ndarray
    """
    return (a**2 + b**2)**.5

class ExamplePluginError(Exception):                                             # define an exception to use in this plugin
    pass

class ExamplePlugin(Plugin):
    # @initializer                                                                this decorator can be used when you have multiple parameters, it will automatically initialize self. class variable
    def __init__(self,df:pd.DataFrame):
        self.plugin_mandatory_dependencies = [{                                  # define one or more filed dependencies specifications
        'UU':{'nomvar':'UU','unit':'knot'},                                      # in this case we want uu and vv in knots from the dataframe
        'VV':{'nomvar':'VV','unit':'knot'},                                      # if the field dependency is computable, the system will try to run the plugin
        }]                                                                       # as an example PX can be conputed, 'PX':{'nomvar':'PX','unit':'hectoPascal'}
                                                                                 # if the field is computable you can choose to select it instead of trying to compute
                                                                                 # with the special key value pair 'select_only':True
                                                                                 # 'PX':{'nomvar':'PX','unit':'hectoPascal', 'select_only':True}
                                                                                 # also any column of the dataframe can be included in the specification
                                                                                 # as an example, if you wanted to select the surface level only, you could add 'surface':True
                                                                                 # 'UU':{'nomvar':'UU','unit':'knot', 'surface':True}
                                                                                 # units are stored in fstpy.UNITS, >>> fstpy.UNITS to print the contents
                                                                                 # see get_plugin_dependencies funtion documentation for computable dependencies
                                                                                 
        self.plugin_result_specifications = {                                    # define the resulting fields specifications
        'UV':{'nomvar':'UV','etiket':'WNDMOD','unit':'knot'}                     # in this case, we want the comvar to be UV, the etiket to be WNDMOD
        }                                                                        # and since the result is in knots, we want to set the unit to knots
           
        self.df = df                                                             # here, since we didn't use the @initializer decorator, we have to set the class variable manually

        self.validate_input()                                                    # here we validate our paramters ans other things befor the calculations


    def validate_input(self):                           
        if self.df.empty:                                                        # always check our dataframe is not empty
            raise  ExamplePluginError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)                                # cleaup the metadata fields that we received with the dataframe

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)   # keep the metadata to be added at the end

        self.df = fstpy.add_columns(self.df,True, columns=['unit','forecast_hour','ip_info'])   # add some columns if they are not already in the dataframe
                                                                                           # this helps with sorting and grouping the data
                                                                                           # ip_info tag includes the decoding (gets the kind and value) of ip1, ip2 ip3
                                                                                           # the virtical coordinate type, the surface flag, the virtical coordinate type 
                                                                                           # and the ascending value for the type of level

         #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications) # this function will look in the dataframe to see if the result isn't already present

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True) # get dataframe without metadata

        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])


    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:                                               # return the existing results if we found them
            return existing_results('ExamplePlugin',self.existing_result_df,self.meta_df)

        logging.info('ExamplePlugin - compute')
        df_list = []
        dependencies_list = get_dependencies(self.groups,self.meta_df,'ExamplePlugin',self.plugin_mandatory_dependencies,intersect_levels=True)
                                                                                            # search in every group for the dependencies and create a list of matching dataframes
        for dependencies_df,_ in dependencies_list:
            dependencies_df = fstpy.load_data(dependencies_df)                              # get the 'd' (numpy.ndarray) part from the file if data wasnn't already loaded

            uu_df = get_from_dataframe(dependencies_df,'UU')                                # get a specific field (as a dataframe) from the dataframe, make sure is sorted and reindexed
            vv_df = get_from_dataframe(dependencies_df,'VV')
            uv_df = create_empty_result(vv_df,self.plugin_result_specifications['UV'],all_rows=True) # make a copy (in this case all rows) of the vv dataframe, and apply the column specification changes
                                                                                                     # in this case, according to the plugin_result_specifications, 
                                                                                                     # we will change the nomvar to 'UV'
                                                                                                     # change the etiket to 'WNDMOD' 
                                                                                                     # and change the unit to 'knot' 

            for i in uv_df.index:                                                                    # using a loop for easier reading, number of rows in dataframe is small
                uu = uu_df.at[i,'d']                                                                 # get a variable corresponding to uu array 
                vv = vv_df.at[i,'d']                                                                 # get a variable corresponding to uu array 
                uv_df.at[i,'d'] = python_algorithm(uu,vv)                                            # compute in python and store the result in our new dataframe
                # or 
                ni = uv_df.at[i,'d'].shape[0]
                nj = uv_df.at[i,'d'].shape[1]
                uv_df.at[i,'d'] = fortran_function(uu,vv,ni,nj)                                      # compute in fortran and store the result in our new dataframe
                
            df_list.append(uv_df)                                                                    # keep the results of this group

        return final_results(df_list,ExamplePluginError, self.meta_df)                               # concatenate all the dataframes together with the original metadata
