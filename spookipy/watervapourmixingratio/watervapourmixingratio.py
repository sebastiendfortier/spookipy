# -*- coding: utf-8 -*-
import logging

import fstpy.all as fstpy
import numpy as np
import pandas as pd

from ..humidityutils import get_temp_phase_switch, validate_humidity_parameters
from ..plugin import Plugin

from ..utils import (create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result,
                     get_from_dataframe, initializer)

from ..science import qv_from_hu, qv_from_vppr

class WaterVapourMixingRatioError(Exception):
    pass

class WaterVapourMixingRatio(Plugin):


    @initializer
    def __init__(self,df:pd.DataFrame, ice_water_phase=None, temp_phase_switch=None,temp_phase_switch_unit='celsius', rpn=False):
        self.plugin_params={'ice_water_phase':self.ice_water_phase,'temp_phase_switch':self.temp_phase_switch,'temp_phase_switch_unit':self.temp_phase_switch_unit,'rpn':self.rpn}

        self.plugin_mandatory_dependencies_rpn = [
            {
                'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram'},
            }
        ]
        self.plugin_mandatory_dependencies = [
            {
                'HU':{'nomvar':'HU','unit':'kilogram_per_kilogram','select_only':True},
            },
            {
                'VPPR':{'nomvar':'VPPR','unit':'hectoPascal'},
                'PX':{'nomvar':'PX','unit':'hectoPascal'},
            }
        ]


        self.plugin_result_specifications = {
            'QV':{'nomvar':'QV','etiket':'WVMXRT','unit':'gram_per_kilogram'}
            }
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise  WaterVapourMixingRatioError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.df = fstpy.add_columns(self.df, columns=['unit','forecast_hour','ip_info'])

        validate_humidity_parameters(WaterVapourMixingRatioError,self.ice_water_phase,self.temp_phase_switch,self.temp_phase_switch_unit)

        self.temp_phase_switch = get_temp_phase_switch(WaterVapourMixingRatioError, self.ice_water_phase=='both', self.temp_phase_switch, self.temp_phase_switch_unit, self.rpn)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        # remove meta data from DataFrame
        self.df = self.df.loc[~self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.groups = self.df.groupby(['grid','dateo','forecast_hour','ip1_kind'])



    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('WaterVapourMixingRatio',self.existing_result_df,self.meta_df)

        logging.info('WaterVapourMixingRatio - compute')
        df_list = []

        if self.rpn:
            dependencies_list = get_dependencies(self.groups,self.meta_df,'WaterVapourMixingRatio',self.plugin_mandatory_dependencies_rpn,self.plugin_params, intersect_levels=True)
        else:
            dependencies_list = get_dependencies(self.groups,self.meta_df,'WaterVapourMixingRatio',self.plugin_mandatory_dependencies,self.plugin_params, intersect_levels=True)

        for dependencies_df,option in dependencies_list:
            if option==0:
                qv_df = self.watervapourmixingratio_from_hu(dependencies_df,option)
            else:
                qv_df = self.watervapourmixingratio_from_vppr(dependencies_df, option)

            df_list.append(qv_df)

        return final_results(df_list, WaterVapourMixingRatioError, self.meta_df)


    def watervapourmixingratio_from_vppr(self, dependencies_df, option):
        logging.info(f'option {option+1}')
        # dependencies_df = get_intersecting_levels(dependencies_df,self.plugin_mandatory_dependencies[option])

        vppr_df = get_from_dataframe(dependencies_df,'VPPR')
        px_df = get_from_dataframe(dependencies_df,'PX')
        qv_df = create_empty_result(vppr_df,self.plugin_result_specifications['QV'],all_rows=True)
        vpprpa_df = fstpy.unit_convert(vppr_df,'pascal')
        pxpa_df = fstpy.unit_convert(px_df,'pascal')
        for i in qv_df.index:
            vpprpa = vpprpa_df.at[i,'d']
            pxpa = pxpa_df.at[i,'d']
            qv_df.at[i,'d'] = qv_from_vppr(px=pxpa,vppr=vpprpa).astype(np.float32)
        return qv_df

    def watervapourmixingratio_from_hu(self, dependencies_df, option):
        logging.info(f'option {option+1}')

        hu_df = get_from_dataframe(dependencies_df,'HU')
        qv_df = create_empty_result(hu_df,self.plugin_result_specifications['QV'],all_rows=True)
        for i in qv_df.index:
            hu = hu_df.at[i,'d']
            qv_df.at[i,'d'] = qv_from_hu(hu=hu).astype(np.float32)
        return qv_df
