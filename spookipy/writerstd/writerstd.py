# -*- coding: utf-8 -*-

import argparse
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
        no_modification_flag:bool=False, # TODO implement this
        writing_mode:str="APPENDOVERWRITE",
        encode_ip2_and_ip3:bool=False,
        ignore_extended:bool=False,
        override_pds_label:bool=False,
        run_id:str=None,
        implementation:str=None,
        ):

        if pd.Series(self.df['nomvar'].str.len() > 4).any():
            raise WriterStdError("CANNOT WRITE FIELD TO AN RPN STRANDARD FILE DUE TO THE LENGTH OF THE "+
                                "FIELD'S NAME (_pdsName). THE FIELD'S NAME IS LIMITED TO A MAXIMUM OF "+
                                "4 CHARACTERS IN RPN STANDARD FILES.")

        VALID_WRITING_MODE=["NOPREVIOUS","APPEND","APPENDOVERWRITE","NEWFILEONLY"]
        if self.writing_mode not in VALID_WRITING_MODE:
            raise WriterStdError("The writing mode needs to be in {}, the value {} is invalid".format(VALID_WRITING_MODE,self.writing_mode))

        dir = os.path.dirname(self.output)

        if not dir:
            dir = os.getcwd()

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

        self.df_input = self.df

        self.df = fstpy.add_columns(self.df)

        restore_5005_record(self.df)

        self.df['ip1'], self.df['ip2'], self.df['ip3'] = vectorized_encode_ip123(self.df['nomvar'],
                                                                    self.df['ip1'],self.df['ip2'],self.df['ip3'],
                                                                    self.df['ip1_kind'],self.df['ip2_kind'],self.df['ip3_kind'],
                                                                    self.df['level'],self.df['ip2_dec'],self.df['ip3_dec'],
                                                                    self.df['interval'],ip1_encoding_newstyle,encode_ip2_and_ip3)
        
        if ignore_extended:
            df['typvar'] = df.apply(lambda row: row['typvar'][0], axis=1)

        if run_id:
            self.df['run'] = run_id

        if implementation:
            self.df['implementation'] = implementation

        self.df['etiket'] = self.df.apply(lambda row: fstpy.create_encoded_standard_etiket(
                                                                row['label'], 
                                                                row['run'], 
                                                                row['implementation'], 
                                                                row['ensemble_member'], 
                                                                row['etiket_format'],
                                                                ignore_extended=ignore_extended,
                                                                override_pds_label=override_pds_label,
                                                                ), axis=1)

        self.df.drop(columns=['label', 'run', 'implementation', 'ensemble_member', 'etiket_format'])

        self.mode = self.writing_mode.lower() if self.writing_mode in ["APPEND","APPENDOVERWRITE"] else "write"

        # TODO verifier unit

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
            fstpy.StandardFileWriter(self.output,self.no_meta_df,overwrite=True,no_meta=True,mode=self.mode).to_fst()
        elif self.metadata_only:
            fstpy.StandardFileWriter(self.output,self.meta_df,overwrite=True,meta_only=True,mode=self.mode).to_fst()
        else:
            fstpy.StandardFileWriter(self.output,self.df,overwrite=True,mode=self.mode).to_fst()
            
        return self.df_input

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """
        parser = argparse.ArgumentParser(prog=WriterStd.__name__, parents=[Plugin.base_parser])

        parser.add_argument('--output',type=str,required=True, help="Output file name\nEx: --output /tmp/output.std")
        parser.add_argument('--IP1EncodingStyle',type=str,default="NEWSTYLE",choices=["NEWSTYLE","OLDSTYLE"],dest='ip1_encoding_newstyle', help="IP1 encoding style")
        parser.add_argument('--metadataOnly',action='store_true',default=False,dest="metadata_only", help="Write only meta-information fields e.g. >>, ^^, ^>, HY, PO, PT, E1, !!, !!SF")
        parser.add_argument('--noMetadata',action='store_true',default=False,dest="no_metadata", help="No writing of meta-information fields e.g. >>, ^^, ^>, HY, PO, PT, E1, !!, !!SF")
        parser.add_argument('--noUnitConversion',action='store_true',default=False,dest="no_unit_conversion", help="No unit conversion before fields are written")
        parser.add_argument('--noModificationFlag',action='store_true',default=False,dest="no_modification_flag", help="Write raw unmodified typvar.")
        parser.add_argument('--writingMode',type=str,default="APPENDOVERWRITE",choices=["NOPREVIOUS","APPEND","APPENDOVERWRITE","NEWFILEONLY"],dest='writing_mode', help="Writing mode.")
        parser.add_argument('--runID',type=str,dest='run_id', help="Run ID, 2 caractères. Exemples: r1, g1")
        parser.add_argument('--implementation',type=str,choices=["N","P","X"],dest='implementation', help="Implementation")
        parser.add_argument('--ignoreExtended',action='store_true',default=False,dest="ignore_extended", help=argparse.SUPPRESS)
        parser.add_argument('--encodeIP2andIP3',action='store_true',default=False,dest="encode_ip2_and_ip3", help=argparse.SUPPRESS)
        parser.add_argument('--overridePdsLabel',action='store_true',default=False,dest="override_pds_label", help=argparse.SUPPRESS)

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg['ignore_extended']:
            enable_ignore_extended = os.environ.get('SPOOKI_ENABLE_IGNORE_EXTENDED_ONE_LAST_TIME')
    
            if enable_ignore_extended is not None and enable_ignore_extended == '1':
                warnings.warn("With 'SPOOKI_ENABLE_IGNORE_EXTENDED_ONE_LAST_TIME=1', '--ignoreExtended' parameter can be used one last time.\nIn a coming version, the parameter will be removed entirely and your code will need to be updated.")
            else:
                raise WriterStdError("IN PLUGIN: 'WriterStd', THE PARAMETER '--ignoreExtended' CAN'T BE USED WITHOUT 'SPOOKI_ENABLE_IGNORE_EXTENDED_ONE_LAST_TIME=1'")

        parsed_arg['ip1_encoding_newstyle'] = parsed_arg['ip1_encoding_newstyle'] == "NEWSTYLE"

        if parsed_arg['run_id'] is not None and len(parsed_arg['run_id']) > 2:
            raise WriterStdError("RUN_ID INVALID! - {}".format(parsed_arg['run_id']))

        return parsed_arg


def applyIgnoreExtended(df):
    df['label'] = df['etiket']
    return df
