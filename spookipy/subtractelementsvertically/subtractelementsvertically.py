# -*- coding: utf-8 -*-
import logging
from typing import Final
import fstpy.all as fstpy
import numpy as np
import pandas as pd
from ..plugin import Plugin
from ..utils import create_empty_result, final_results, initializer, validate_nomvar
import rpnpy.librmn.all as rmn

ETIKET: Final[str] =  'SUBEVY'

class SubtractElementsVerticallyError(Exception):
    pass


class SubtractElementsVertically(Plugin):
    """From a field value for a chosen level (either the lowest or the highest), subtract the values from all the other levels of the same field.

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param nomvar_out: nomvar for output result
    :type nomvar_out: str, optional
    """
    @initializer
    def __init__(self, df: pd.DataFrame, direction: str='ascending', nomvar_out: str = None):
        self.plugin_result_specifications = {'etiket': ETIKET}
        super().__init__(df)
        self.no_meta_df = fstpy.add_columns(self.no_meta_df,'ip_info')
        self.validate_params()

    def validate_params(self):
        if self.direction not in ['ascending', 'descending']:
            raise SubtractElementsVerticallyError("Invalid value '{self.direction}' for direction, valid values are {['ascending', 'descending']}")
        if (self.no_meta_df.nomvar.unique().size > 1) and (not (self.nomvar_out is None)):
            raise SubtractElementsVerticallyError('nomvar_out can only be used when only 1 field is present')

        if (self.no_meta_df.nomvar.unique().size == 1) and (not (self.nomvar_out is None)):
            validate_nomvar(self.nomvar_out, 'SubtractElementsVertically', SubtractElementsVerticallyError)

        if len(self.no_meta_df.loc[~self.no_meta_df.interval.isna()].index) > 0:
            raise SubtractElementsVerticallyError('Dataframe cannot contain rows with intervals!')

    def compute(self) -> pd.DataFrame:    
        logging.info('SubtractElementsVertically - compute')
        df_list=[]
        groups = self.no_meta_df.groupby(['grid','datev','nomvar'])
        for (grid,datev,nomvar), nomvar_df in groups:
            res_df = create_empty_result(nomvar_df, self.plugin_result_specifications)
            
            if self.direction == 'descending':
                nomvar_df = nomvar_df.sort_values(by='level',ascending=nomvar_df.ascending.unique()[0])
            else:
                nomvar_df = nomvar_df.sort_values(by='level',ascending=(not nomvar_df.ascending.unique()[0]))

            # print(nomvar_df[fstpy.BASE_COLUMNS].to_string())
            # first_level = list(nomvar_df.level)[0]
            # last_level = list(nomvar_df.level)[-1]
            first_level = nomvar_df.level.min()
            last_level = nomvar_df.level.max()

            if res_df.iloc[0].ip1 >= 32768: 
                first_level = rmn.convertIp(rmn.CONVIP_ENCODE, first_level, int(res_df.iloc[0].ip1_kind))
                last_level = rmn.convertIp(rmn.CONVIP_ENCODE, last_level, int(res_df.iloc[0].ip1_kind))
            res_df['ip1'] = int(last_level)
            res_df['ip3'] = int(first_level)

            
            if  (self.no_meta_df.nomvar.unique().size == 1) and (not (self.nomvar_out is None)):
                res_df['nomvar'] = self.nomvar_out

            data = np.stack(nomvar_df.d)
            data0 = data[-1]
            data = -1*data
            data = np.vstack([data0[np.newaxis],data[:-1]])
            # print(nomvar,data, data.shape)
            if data.shape[0]>1:
                res_df['d'] = [np.sum(data, axis=0)]


            df_list.append(res_df)

        return final_results(df_list, SubtractElementsVerticallyError, self.meta_df)
    