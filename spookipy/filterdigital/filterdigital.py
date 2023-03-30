# -*- coding: utf-8 -*-
import argparse
import logging
from multiprocessing.pool import ThreadPool

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin, PluginParser
from ..utils import (final_results, get_split_value, initializer, to_dask, validate_nomvar)
from .f_stenfilt import f_stenfilt

class FilterDigitalError(Exception):
    pass


class FilterDigital(Plugin):
    """Apply a digital filter of Stencil type on a data set

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param filter: stencil filter, list of odd length of ints
    :type filter: list
    :param repetitions: number of repetition to apply filter, defaults to 1
    :type repetitions: int, optional
    :param nomvar_out: nomvar for output result, defaults to None
    :type nomvar_out: str, optional
    :param parallel: execute in parallel, defaults to False
    :type parallel: bool, optional
    """
    @initializer
    def __init__(
            self,
            df: pd.DataFrame,
            filter: list,
            repetitions: int = 1,
            nomvar_out=None,
            parallel: bool = False):

        self.plugin_result_specifications = {
            'ALL': {'filtered': True}
            # 'etiket':'FLTRDG',
        }

        self.validate_input()

    def validate_input(self):
        if self.df.empty:
            raise FilterDigitalError('No data to process')

        if not (self.nomvar_out is None):
            validate_nomvar(self.nomvar_out, 'FilterDigital', FilterDigitalError)

        if not len(self.filter):
            raise FilterDigitalError('Filter must contain at least 1 value')

        if len(self.filter) % 2 == 0:
            raise FilterDigitalError('Filter lenght must be odd, not even')

        if not (self.repetitions > 0):
            raise FilterDigitalError('Repetitions must be a positive integer')

        self.meta_df = self.df.loc[self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

        self.df = self.df.loc[~self.df.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

    def compute(self) -> pd.DataFrame:
        logging.info('FilterDigital - compute')

        # if not (self.nomvar_out is None):
        #     self.plugin_result_specifications['ALL']['nomvar'] = self.nomvar_out

        # self.df = fstpy.compute(self.df)

        if not (self.nomvar_out is None):
            self.df['nomvar'] = self.nomvar_out
        self.df['filtered'] = True

        # new_df = create_empty_result(self.df,self.plugin_result_specifications['ALL'],all_rows=True)

        filter_len = len(self.filter)

        filter_arr = np.array(self.filter, dtype=np.int32, order='F')

        if self.parallel:
            df_list = apply_filter_parallel(self.df, self.repetitions, filter_arr, filter_len)
        else:    
            df_list = apply_filter(self.df, self.repetitions, filter_arr, filter_len)


        return final_results(df_list, FilterDigitalError, self.meta_df)

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = PluginParser(prog=FilterDigital.__name__, parents=[Plugin.base_parser],add_help=False)
        parser.add_argument('--filter',type=str,required=True, help="List of weights that define the filter.")
        parser.add_argument('--repetitions',type=int,required=True, help="The number of times the filter will be applied.")
        parser.add_argument('--outputFieldName',type=str,dest="nomvar_out", help="Option to give the output field a different name from the input field name.")

        parsed_arg = vars(parser.parse_args(args.split()))

        parsed_arg['filter'] = parsed_arg['filter'].split(",")

        if parsed_arg['nomvar_out'] is not None:
            validate_nomvar(parsed_arg['nomvar_out'],"FilterDigital",FilterDigitalError)

        return parsed_arg


# [1 1 1 2 2 1 1 1 1]

# 1 - 9.09090936E-02, 0.00000000,  0.00000000,  0.00000000,  0.00000000
# 1 - 9.09090936E-02, 0.111111112, 0.00000000,  0.00000000,  0.00000000
# 1 - 9.09090936E-02, 0.111111112, 0.142857149, 0.00000000,  0.00000000
# 2 - 0.181818187,    0.222222224, 0.285714298, 0.400000006, 0.00000000
# 2 - 0.181818187,    0.222222224, 0.285714298, 0.400000006, 0.00000000
# 1 - 9.09090936E-02, 0.111111112, 0.142857149, 0.200000003, 0.00000000
# 1 - 9.09090936E-02, 0.111111112, 0.142857149, 0.00000000,  0.00000000
# 1 - 9.09090936E-02, 0.111111112, 0.00000000,  0.00000000,  0.00000000
# 1 - 9.09090936E-02, 0.00000000,  0.00000000,  0.00000000,  0.00000000





# def get_factors(stencil_filter):
#     _l = stencil_filter.size

#     _nb_elem = int((_l+1)/2)

#     factors = np.zeros(((_nb_elem + 2),(_l + 1)))
#     print(factors.shape)

#     newnb_elem = (_nb_elem - 1)

#     for j in range(1,newnb_elem+1):
#         sum = 0.0
#         for i in range(-j,j+1):
#             sum += stencil_filter[i+_nb_elem - 1]

#         for i in range(-j, j+1):
#             factors[_nb_elem-j][i] = stencil_filter[i+_nb_elem - 1] / sum
#     return factors

# def filter_data (input, ni, nj, factors, repetitions, filter_len):
#     import copy
#     result1 = np.zeros((ni + 1))
#     result2 = np.zeros((nj + 1))
#     newni = (ni-1)
#     newnj = (nj-1)
#     res = copy.deepcopy(input)

#     for _ in range(1, repetitions+1):
#         for  j in range(1,nj+1):
#             for i in range(2,newni+1):
#                 temp = 0.0
#                 index = i-1 if (i-1 < ni-i) else ni-i
#                 nb_elm = index if (index < filter_len/2) else filter_len/2

#                 for k in range(-nb_elm, nb_elm+1):
#                     temp = temp + res[(((j)-1)*ni)+((i+k)-1)] * factors[k][(filter_len/2+1)-nb_elm]

#                 result1[i] = temp

#             for i in range(2, newni+1):
#                 res[(((j)-1)*ni)+((i)-1)] = result1[i]


#         for i in range(1, ni+1):
#             for j in range(2, newnj+1):
#                 temp=0.0
#                 index = j-1 if (j-1 < nj-j) else nj-j
#                 nb_elm = index if (index < filter_len/2) else filter_len/2
#                 for k in range(-nb_elm, nb_elm + 1):
#                     temp = temp + res[(((j+k)-1)*ni)+((i)-1)] * factors[k][(filter_len/2+1)-nb_elm]
#                 result2[j] = temp
#             for j in range(2, newnj + 1):
#                 res[(((j)-1)*ni)+((i)-1)] = result2[j]
#     return res

def apply_filter(df, repetitions, filter_arr, filter_len):
    # import sys
    # print(filter_arr)
    # factors = get_factors(filter_arr)
    # for i in range(-4,5):
    #     for j in range(0,5):
    #         print(f'factors[{i}][{j+1}] =  {factors[i][j]}')
    # nb_elem = int((filter_arr.size+1)/2)
    # for i in range(filter_arr.size):
    #     for j in range(nb_elem):
    #         print(f'facteur({i-4},{j+1}) {factors[i][j]}')

    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)
    results = []
    for df in df_list:
        df = fstpy.compute(df)
        for i in df.index:
            ni = df.at[i, 'd'].shape[0]
            nj = df.at[i, 'd'].shape[1]
            arr = f_stenfilt(slab=df.at[i,'d'],ni=ni,nj=nj,npass=repetitions,list=filter_arr,l=filter_len)
            # arr = stenfilt (df.at[i,'d'], ni, nj, repetitions, factors, filter_arr.size)
            # arr1 = filter_data(df.at[i,'d'].flatten(),ni,nj,factors,repetitions,filter_len)
            df.at[i, 'd'] = to_dask(arr)

        results.append(df)
    return results

class ListWrapper:
    def __init__(self, arr):
        self.arr = arr
    def get(self):
        return self.arr

def filter_wrapper(data,repetitions,filter_arr,filter_len):
    ni = data.shape[0]
    nj = data.shape[1]
    return f_stenfilt(slab=data,ni=ni,nj=nj,npass=repetitions,list=filter_arr.get(),l=filter_len)

def apply_filter_parallel(df, repetitions, filter, filter_len):

    split_value = get_split_value(df)

    df_list = np.array_split(df, split_value)
    results = []
    for df in df_list:
        df = fstpy.compute(df)
        
        repetitions_arr = [repetitions for _ in range(len(df.index))]
        filter_arr = [ListWrapper(filter) for _ in range(len(df.index))]
        filter_len_arr = [filter_len for _ in range(len(df.index))]

        with ThreadPool() as tp:
            filter_results = tp.starmap(filter_wrapper,zip(df.d.to_list(),repetitions_arr,filter_arr,filter_len_arr))

        df['d'] = [to_dask(r) for r in filter_results]

        results.append(df)

    return results

# def get_factors(filter):
#     # print(filter)
#     l = filter.size
#     nb_elem = int((l+1)/2)

#     istart = -nb_elem + 1
#     iend = nb_elem -1
#     facteur = np.zeros((l, nb_elem))
#     # for j in range(1, nb_elem):
#     #     print(j)
#     #     for i in range(istart,iend):
#     #         facteur[i][j] = 0.0

#     for j in range(0, nb_elem):
#         # print(f'j = {j}')
#         sum = 0.0
#         # print(range(-j,j+1))
#         # print('i = ', end='')
#         for i in range(-j,j+1):
#             # print(f'{i}\t',end='')
#             sum = sum + filter[i+nb_elem-1]
#         if j == 0:
#             sum += 1.
#         # print('')     
#         # print(f'sum = {sum}')
#         for i in range(-j,j+1):
#             # print(f'{i} - {nb_elem-j-1}')
#             facteur[i][nb_elem-j-1] = 1.*filter[i+nb_elem-1] / sum

#     return facteur        

# def stenfilt (slab, ni, nj, npass, facteur, l):
#     import copy
#     #   integer ni, nj
#     #   integer l,list(l)
#     #   real,intent(in) :: slab(ni ,nj)
#     #   real,intent(out) :: res(ni ,nj)
#     #   real facteur(-8:8,10)
#     #   real temp
#     #   integer k,i,j
#     #   integer nb_elm
#     #   integer npass, pass
#     #   integer nb_elem, istart, iend
#     #   real sum
#     #   real result1(ni), result2(nj)
#     result1 = np.zeros((ni))
#     result2 = np.zeros((nj))
#     res = copy.deepcopy(slab)

#     # nb_elem = (l+1)/2
#     # istart = -nb_elem + 1
#     # iend = nb_elem -1

#     # for j in range(1, nb_elem):
#     #     for i in range(istart,iend):
#     #         facteur(i,j) = 0.0

#     # for j in range(1, nb_elem-1):
#     #     sum = 0.0
#     #     for i in range(-j,j):
#     #         sum = sum + list(i+nb_elem)
         

#     #     for i in range(-j,j):
#     #         facteur(i,nb_elem-j) = list(i+nb_elem) / sum


#     for _ in range(0, npass):
#         for j in range(0, nj+1):
#             for i in range(1, ni):
#                 temp = 0.0
#                 nb_elm = min(i-1,ni-i,int(l/2))
#                 for k in range(-nb_elm, nb_elm+1):
#                     temp = temp + res[i+k][j] * facteur[k][(int((l+1)/2)-nb_elm)-2]

#                 result1[i] = temp
            
#             for i in range(1, ni-1+1):
#                 res[i][j] = result1[i]
            
#         for i in range(0, ni+1):
#             for j in range(1, nj):
#                temp=0.0
#                nb_elm = min(j-1,nj-j,l/2)
#                for k in range(-nb_elm, nb_elm+1):
#                    temp = temp + res[i][j+k] * facteur[k][(l/2+1)-nb_elm]

#                result2[j] = temp
            
#             for j in range(1, nj):
#                 res[i][j] = result2[j]
#     return res           
