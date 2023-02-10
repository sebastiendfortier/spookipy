# -*- coding: utf-8 -*-

import logging
import os
import warnings
import math
import rpnpy.librmn.all as rmn

import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (DependencyError, create_empty_result, existing_results, final_results,
                     get_dependencies, get_existing_result, get_from_dataframe, restore_5005_record,
                     initializer)
from colorama import Fore, Style


INTERVAL_TYPE_NOT_SET = 0
INTERVAL_TIME = 1
INTERVAL_OTHER = 2
def round_half_down(value,half_down=True):
    if half_down:
        if value < 0:
            return math.ceil(value - 0.4)
        return math.floor(value + 0.4)
    else:
        if value < 0:
            return math.ceil(value - 0.5)
        return math.floor(value + 0.5)

def create_encoded_ip(value: float, kind: int,mode:int=rmn.CONVIP_ENCODE):
    if kind == 100:
        return value
    ip = rmn.convertIp(mode,value,kind)
    if ip < 0:
        mode_str = "CONVIP_ENCODE" if mode==rmn.CONVIP_ENCODE else "CONVIP_ENCODE_OLD"
        print('ip is {} trying different encoding: {}'.format(ip,mode_str))
        other_mode = rmn.CONVIP_ENCODE_OLD if mode == rmn.CONVIP_ENCODE else rmn.CONVIP_ENCODE
        ip = rmn.convertIp(other_mode,value,kind)
        if ip < 0:
            ip = 0
    return ip

def encode_ip123_metadata(nomvar,ip1_kind,ip3_kind,ip1_value,ip2_value,ip3_value,encoding_mode_ip1,encode_ip2_and_ip3):
    result_ip1 = ip1_value if nomvar in ["^>", ">>", "^^", "!!", "!!SF"] else create_encoded_ip(float(ip1_value),int(ip1_kind),mode=encoding_mode_ip1)
    result_ip2 = ip2_value # forecast hour
    result_ip3 = ip3_value # ??? _userDefinedIndex

    if encode_ip2_and_ip3:
        result_ip3 = create_encoded_ip(float(result_ip3),int(ip3_kind),mode=rmn.CONVIP_ENCODE)
        # see spooki StdIO.hpp line 599
        if nomvar == 'HY':
            result_ip2 = round_half_down(result_ip2)

    return result_ip1,result_ip2,result_ip3


def encode_ip123(nomvar,ip1,ip2,ip3,ip1_kind,ip2_kind,ip3_kind,ip1_value,ip2_value,ip3_value,interval,ip1_encoding_newstyle:bool,encode_ip2_and_ip3:bool):
    
    result_ip1 = result_ip2 = result_ip3 = -999
    
    interval_type = INTERVAL_TYPE_NOT_SET
    encoding_mode_ip1 = rmn.CONVIP_ENCODE if ip1_encoding_newstyle else rmn.CONVIP_ENCODE_OLD
    
    # check if there's an interval
    if ip1 >= 32768 or ip1 == 0 and ip2 >= 32768 or ip2 == 0 and ip3 >= 32768 or ip3 == 0:
        if ip2_kind == ip3_kind:
            interval_type = INTERVAL_TIME
        if ip1_kind == ip3_kind:
            interval_type = INTERVAL_OTHER

    if nomvar in ["^>", ">>", "^^", "!!", "!!SF", 'HY']:
        result_ip1,result_ip2,result_ip3 = encode_ip123_metadata(nomvar,ip1_kind,ip3_kind,ip1_value,ip2_value,ip3_value,encoding_mode_ip1,encode_ip2_and_ip3)

    elif interval_type == INTERVAL_TYPE_NOT_SET:
        result_ip1 = create_encoded_ip(float(ip1_value),int(ip1_kind),mode=encoding_mode_ip1)
        result_ip2 = ip2_value # forecast hour
        result_ip3 = ip3_value # ??? _userDefinedIndex

        if encode_ip2_and_ip3:
            result_ip3 = create_encoded_ip(float(result_ip3),int(ip3_kind),mode=rmn.CONVIP_ENCODE)
            result_ip2 = create_encoded_ip(float(result_ip2),int(ip2_kind),mode=rmn.CONVIP_ENCODE)

    elif interval_type == INTERVAL_TIME:
        result_ip1 = create_encoded_ip(float(ip1_value),int(ip1_kind),mode=encoding_mode_ip1)
        result_ip2 = ip2_value if (type(interval) != fstpy.std_dec.Interval) else interval.high
        result_ip3 = ip3_value if (type(interval) != fstpy.std_dec.Interval) else interval.high - interval.low

        if encode_ip2_and_ip3:
            result_ip3 = ip3_value if (type(interval) != fstpy.std_dec.Interval) else interval.low
            result_ip2, result_ip3 = fstpy.one_encode_ip2_and_ip3_as_time_interval(result_ip2,result_ip3)

    elif interval_type == INTERVAL_OTHER:
        result_ip2 = ip2_value # forecast hour
        result_ip1 = ip1_value if (type(interval) != fstpy.std_dec.Interval) else interval.low
        result_ip3 = ip3_value if (type(interval) != fstpy.std_dec.Interval) else interval.high - interval.low
        result_ip1 = create_encoded_ip(float(result_ip1),int(ip1_kind),mode=encoding_mode_ip1)

        if encode_ip2_and_ip3:
            result_ip3 = ip3_value if (type(interval) != fstpy.std_dec.Interval) else interval.high
            result_ip2 = create_encoded_ip(float(result_ip2),int(ip2_kind),mode=rmn.CONVIP_ENCODE)
            result_ip3 = create_encoded_ip(float(result_ip3),int(ip3_kind),mode=rmn.CONVIP_ENCODE)

    if not encode_ip2_and_ip3:
        result_ip2 = round_half_down(result_ip2,False)
        result_ip3 = round_half_down(result_ip3)

    return int(result_ip1), int(result_ip2), int(result_ip3)


vectorized_encode_ip123 = np.vectorize(encode_ip123)

class WriterStdError(Exception):
    pass

class WriterStd(Plugin):
    """Calculation of the wind modulus from its 2 horizontal components

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param output: Output file name
    :type output: str
    """

    @initializer
    def __init__(
        self,
        df:pd.DataFrame,
        output:str,
        ip1_encoding_newstyle:bool=True,
        metadata_only:bool=False,
        no_metadata:bool=False,
        no_unit_conversion:bool=False, # TODO implement this, check that the unit is ok for each field, convert if necessary, check unit_convert/unit_convert_array in fstpy
        writing_mode:str="APPENDOVERWRITE",
        encode_ip2_and_ip3:bool=False,
        ignore_extended:bool=False,
        override_pds_label:bool=False,
        ):

        if pd.Series(self.df['nomvar'].str.len() > 4).any():
            raise WriterStdError("CANNOT WRITE FIELD TO AN RPN STRANDARD FILE DUE TO THE LENGTH OF THE "+
                                "FIELD'S NAME (_pdsName). THE FIELD'S NAME IS LIMITED TO A MAXIMUM OF "+
                                "4 CHARACTERS IN RPN STANDARD FILES.")

        VALID_WRITING_MODE=["NOPREVIOUS","APPEND","APPENDOVERWRITE","NEWFILEONLY"]
        if self.writing_mode not in VALID_WRITING_MODE:
            raise WriterStdError("The writing mode needs to be in {}, the value {} is invalid".format(VALID_WRITING_MODE,self.writing_mode))

        dir = os.path.dirname(self.output)

        if not os.path.exists(dir):
            raise WriterStdError("OUTPUT DIRECTORY '{}' DOESN'T EXIST, YOU HAVE TO CREATE IT BEFOREHAND".format(dir))

        if not os.path.isdir(dir):
            raise WriterStdError("DIRNAME OF OUTPUT PATH '{}' ISN'T A DIRECTORY".format(dir))



        if writing_mode == "NOPREVIOUS" and os.path.exists(self.output):
            raise WriterStdError("{} ALREADY EXIST".format(self.output))

        if writing_mode == "NEWFILEONLY" and os.path.exists(self.output):
            warnings.warn("The output file '{}' already exist." +
                " Because of the parameter '--writingMode NEWFILEONLY', " +
                "the file will be deleted before creating a new one.".format())
            
            fstpy.delete_file(self.output)

        # print(self.df)

        self.df = fstpy.add_columns(self.df)
        # print(self.df)
        # print(self.df[['ip2','ip2_dec','ip2_kind','ip3','ip3_dec','ip3_kind']])
        # print(self.df['ip2'])
        
        # encoding_mode = rmn.CONVIP_ENCODE if self.ip1_encoding_newstyle else rmn.CONVIP_ENCODE_OLD
        # meta = ["^>", ">>", "^^", "!!", "!!SF", "HY"]
        # self.df['ip1'] = self.df.apply(lambda row: row['ip1'] if row['nomvar'] in meta else fstpy.create_encoded_ip1(row['level'],row['ip1_kind'],mode=encoding_mode), axis=1)

        # # print("here")
        # if self.encode_ip2_and_ip3:
        #     # print("encoded ip2 ip3 true")

        #     self.df['ip2'] = self.df.apply(lambda row: int(row['ip2_dec']) if row['nomvar'] in meta else fstpy.create_encoded_ip1(row['ip2_dec'],row['ip2_kind'],mode=rmn.CONVIP_ENCODE), axis=1)
        #     self.df['ip3'] = self.df.apply(lambda row: int(row['ip3_dec']) if row['nomvar'] in meta else fstpy.create_encoded_ip1(row['ip3_dec'],row['ip3_kind'],mode=rmn.CONVIP_ENCODE), axis=1)
        #     # print("ok")
        # else:
        #     # print("encoded ip2 ip3 false")

        #     self.df['ip2'] = self.df.apply(lambda row: math.floor(row['ip2_dec']) if (row['ip2_dec'] - math.floor(row['ip2_dec'])) < 0.5 else math.ceil(row['ip2_dec']), axis=1)#TODO check this
        #     self.df['ip3'] = self.df.apply(lambda row: math.floor(row['ip3_dec']) if (row['ip3_dec'] - math.floor(row['ip3_dec'])) < 0.5 else math.ceil(row['ip3_dec']), axis=1)#TODO check this
        #     # self.df['ip3'] = self.df.apply(lambda row: my_func(row['ip3_dec']), axis=1)
        #     # print("ok")
        # # print(self.df['ip2'])

        # print(self.df)
        restore_5005_record(self.df)
        # print(self.df)
        # raise Exception()

        # nomvar,ip1,ip2,ip3,ip1_kind,ip2_kind,ip3_kind,ip1_value,ip2_value,ip3_value,interval,ip1_encoding_newstyle:bool,encode_ip2_and_ip3:bool

        self.df['ip1'], self.df['ip2'], self.df['ip3'] = vectorized_encode_ip123(self.df['nomvar'],
                                                                    self.df['ip1'],self.df['ip2'],self.df['ip3'],
                                                                    self.df['ip1_kind'],self.df['ip2_kind'],self.df['ip3_kind'],
                                                                    self.df['level'],self.df['ip2_dec'],self.df['ip3_dec'],
                                                                    self.df['interval'],ip1_encoding_newstyle,encode_ip2_and_ip3)

        # format etiket 

        # self.df['etiket_format'] = "2,6,0,1" # test_9 problem with format ?? ask francois
        # self.df['etiket_format'] = ""
        self.df['etiket'] = self.df.apply(lambda row: fstpy.create_encoded_etiket(
                                                                row['label'], 
                                                                # format_label(row['label']), 
                                                                row['run'], 
                                                                row['implementation'], 
                                                                row['ensemble_member'], 
                                                                row['etiket_format'],
                                                                ignore_extended=ignore_extended,
                                                                override_pds_label=override_pds_label,
                                                                ), axis=1)

        # print(self.df.etiket)
        self.df.drop(columns=['label', 'run', 'implementation', 'ensemble_member', 'etiket_format'])
        # label needs to be 6 char

        self.mode = self.writing_mode.lower() if self.writing_mode in ["APPEND","APPENDOVERWRITE"] else "write"


        # TODO make this work wtf?????????
        # # check len of nomvar (max 4)
        # if any(len(df['nomvar'])>4):
        #     for nomvar in df['nomvar'].unique():
        #         if len(nomvar) > 4:
        #             raise WriterStdError("CANNOT WRITE FIELD: '{}'" +
        #                         "TO AN RPN STRANDARD FILE DUE TO THE LENGTH OF THE " +
        #                         "FIELD'S NAME (_pdsName). THE FIELD'S NAME IS LIMITED TO A MAXIMUM OF 4 CHARACTERS " +
        #                         "IN RPN STANDARD FILES.".format(nomvar))

        
        
        # TODO faire un tri des donnees
        # meta-informations, ordre alphabétique de noms de variables, 
        # ordre de niveaux (de bas en haut), ordre temporel
        # print("------------")
        # print("in writer")
        # print(self.df[['nomvar','etiket','ip1','level','ip1_kind','ip2','ip2_dec','ip2_kind','ip3','ip3_dec','ip3_kind','interval']])
        # TODO verifier unit
        # print(self.df)
        super().__init__(self.df)
        
        


    def compute(self) -> pd.DataFrame:
        """Abstract method that should implement the plugin's algorithm.

        :return: dataframe with the results
        :rtype: pd.DataFrame
        """

        # TODO verifier les writing modes avec fstpy
        # modifier au besoin pour avoir les parametre necessaire
        # si on ajoute des parametre a fstpy utiliser
        # la meme nomenclature que pour les fonction des librairie en dessous

        if self.no_metadata:
            print("no metadata")
            # fstpy.StandardFileWriter(self.output,self.df,no_meta=True).to_fst()
            # fstpy.StandardFileWriter(self.output,self.df,no_meta=True).to_fst()
            # print(self.no_meta_df)
            fstpy.StandardFileWriter(self.output,self.no_meta_df,no_meta=True,mode=self.mode).to_fst()
        elif self.metadata_only:
            print("metadata only")
            # print(self.meta_df)
            fstpy.StandardFileWriter(self.output,self.meta_df,meta_only=True,mode=self.mode).to_fst()
            # fstpy.StandardFileWriter(self.output,self.df).to_fst()
        else:
            print("normal")
            # print(self.df)
            fstpy.StandardFileWriter(self.output,self.df,mode=self.mode).to_fst()
            # fstpy.StandardFileWriter(self.output,self.df,meta_only=True).to_fst()
            
        return self.df


# def format_label(label: str):
#     label = label + "______"
#     return  label[:6]


# def my_func(num):
#     return int(num)


