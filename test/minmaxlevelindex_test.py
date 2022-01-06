# -*- coding: utf-8 -*-
from operator import concat
import pandas as pd
from test import TEST_PATH, TMP_PATH
from spookipy.minmaxlevelindex.minmaxlevelindex import  MinMaxLevelIndexError
import fstpy.all as fstpy
import pytest
import spookipy.all as spooki

from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/MinMaxLevelIndex/testsFiles/'

def test_1(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); recherche MIN, direction ASCENDING, nomvar_min IND """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    # df = src_df0
    df = spooki.MinMaxLevelIndex(
        src_df0,
        nomvar="TT",
        min=True,
        ascending=True,
        nomvar_min='IND').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> 
    # [MinMaxLevelIndex --minMax MIN --direction ASCENDING --outputFieldName1 IND] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    # label = "MMLVLI"
    # df = spooki.convip(df,spooki.rmn.CONVIP_ENCODE,'ip2')

    df_tt = df[df.nomvar == 'TT'].iloc[0]

    # etiket  = create_encoded_etiket(run=df_tt.run,label=label,ensemble_member=df_tt.ensemble_member,implementation=df_tt.implementation)
    # etiket2 = create_encoded_etiket(run='__',label=label,ensemble_member=df_tt.ensemble_member,implementation='X')

    etiket  = "R1MMLVLIN"
    etiket2 = "__MMLVLIX"
    df.loc[df.nomvar == "IND",'etiket'] = etiket2
    df.loc[df.nomvar == "TT",'etiket']  = etiket

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test1_20210915.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)


def test_2(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); recherche MAX, direction ASCENDING, nomvar_max IND """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        nomvar="TT",
        max=True,
        ascending=True,
        nomvar_max='IND').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> 
    # [MinMaxLevelIndex --minMax MAX --direction ASCENDING --outputFieldName2 IND] 
    # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    etiket  = "R1MMLVLIN"
    etiket2 = "__MMLVLIX"

    df.loc[df.nomvar == "IND",'etiket'] = etiket2
    df.loc[df.nomvar == "TT",'etiket']  = etiket

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test2_20210915.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)

def test_3(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); recherche BOTH, direction DESCENDING, nomvar_min MIN, nomvar_max MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        nomvar="TT",
        min=True,
        max=True,
        ascending=False,
        nomvar_min='MIN',
        nomvar_max='MAX').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> 
    # [MinMaxLevelIndex --minMax BOTH --direction DESCENDING --outputFieldName1 MIN --outputFieldName2 MAX] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    etiket  = "R1MMLVLIN"
    etiket2 = "__MMLVLIX"

    df.loc[df.nomvar.isin(["MIN", "MAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "TT",'etiket']              = etiket

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test3_20210915.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)

def test_4(plugin_test_dir):
    """ 7 niveaux de GZ (valeurs croissantes en montant); recherche BOTH, direction ASCENDING, nomvar_min MIN, nomvar_max MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        nomvar="GZ",
        min=True,
        max=True,
        nomvar_min='MIN',
        nomvar_max='MAX').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName GZ] >> 
    # [MinMaxLevelIndex --minMax BOTH --direction ASCENDING --outputFieldName1 MIN --outputFieldName2 MAX] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]"

    etiket  = "R1MMLVLIN"
    etiket2 = "__MMLVLIX"
    df.loc[df.nomvar.isin(["MIN", "MAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "GZ",'etiket']              = etiket

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = TMP_PATH + "test_4.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test4-5_20210915.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)

def test_5(plugin_test_dir):
    """ 7 niveaux de GZ (valeurs croissantes en montant); recherche BOTH, direction DESCENDING, nomvar_min MIN, nomvar_max MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        nomvar="GZ",
        min=True,
        max=True,
        ascending=False,
        nomvar_min='MIN',
        nomvar_max='MAX').compute()
#     # [ReaderStd --input {sources[0]}] >> [Select --fieldName GZ] >> 
#     # [MinMaxLevelIndex --minMax BOTH --direction ASCENDING --outputFieldName1 MIN --outputFieldName2 MAX] >>
#     # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    etiket  = "R1MMLVLIN"
    etiket2 = "__MMLVLIX"
    df.loc[df.nomvar.isin(["MIN", "MAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "GZ",'etiket']              = etiket

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test4-5_20210915.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)

def test_6(plugin_test_dir):
    """ 7 niveaux de UU (valeurs desordonnees); recherche BOTH, direction DESCENDING, nomvar_min MIN, nomvar_max MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        nomvar="UU",
        min=True,
        max=True,
        ascending=False,
        nomvar_min='MIN',
        nomvar_max='MAX').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> 
    # [MinMaxLevelIndex --minMax BOTH --direction DESCENDING --outputFieldName1 MIN --outputFieldName2 MAX] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]"

    etiket  = "R1MMLVLIN"
    etiket2 = "__MMLVLIX"
    df.loc[df.nomvar.isin(["MIN", "MAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "UU",'etiket']              = etiket

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test6-7_20210915.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)

def test_7(plugin_test_dir):
    """ 7 niveaux de UU (valeurs desordonnees); recherche BOTH, direction ASCENDING, nomvar_min MIN, nomvar_max MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        nomvar="UU",
        min=True,
        max=True,
        ascending=False,
        nomvar_min='MIN',
        nomvar_max='MAX').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> 
    # [MinMaxLevelIndex --minMax BOTH --direction DESCENDING --outputFieldName1 MIN --outputFieldName2 MAX] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]"

    etiket  = "R1MMLVLIN"
    etiket2 = "__MMLVLIX"
    df.loc[df.nomvar.isin(["MIN", "MAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "UU",'etiket']              = etiket

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test6-7_20210915.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)

def test_9(plugin_test_dir):
    """3 niveaux de ICGA (sortie du plugin IcingRimeAppleman); BOUNDED, recherche MAX, direction ASCENDING, nomvar_max IND"""
    # open and read source
    source = plugin_test_dir + "test_ICGA.std"
    # source90 = plugin_test_dir + "minmax_DOWNWARD_bounded_input"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df,
        nomvar="ICGA",
        max=True,
        bounded=True,
        nomvar_max='IND').compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [spooki.MinMaxLevelIndex --bounded --minMax MAX --outputFieldName2 IND] >>
    # [Zap --pdsLabel MinMaxBoundedIndexLevel --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    etiket  = "MINMAXX"
    etiket2 = "__MINMAXX"
    df.loc[df.nomvar == 'ICGA','etiket']   = etiket
    df.loc[df.nomvar == 'IND' ,'etiket']   = etiket2

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)
    
    # write the result
    results_file = TMP_PATH + "test_9.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test_ICGA_file2cmp_20201202.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)

def test_10(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); BOUNDED, recherche BOTH, direction ASCENDING, nomvar_min MIN, nomvar_max MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    # src_df0.loc[src_df0.level.between(200,1000, inclusive=True)]
    source1 = plugin_test_dir + "KbasKtop.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df = pd.concat([src_df0 , src_df1])
    
    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df,
        nomvar="TT",
        bounded=True,
        min=True,
        max=True).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,KBAS,KTOP] >> 
    # [MinMaxLevelIndex --bounded --minMax BOTH --direction ASCENDING] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    etiket  = "R1MMLVLIN"
    etiket2 = "__MMLVLIX"
    df.loc[df.nomvar.isin(["KMIN", "KMAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "TT",'etiket']                = etiket

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)
        
    # write the result
    results_file = TMP_PATH + "test_10.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test10-11_20210915.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    # fstpy.delete_file(results_file)
    
    assert(res)

def test_11(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); BOUNDED, recherche BOTH, direction DESCENDING, nomvar_min MIN, nomvar_max MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_dir + "KbasKtop.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df = pd.concat([src_df0 , src_df1])
    
    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df,
        nomvar="TT",
        bounded=True,
        ascending=False,
        min=True,
        max=True).compute()
#     # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,KBAS,KTOP] >> 
#     # [MinMaxLevelIndex --bounded --minMax BOTH --direction ASCENDING] >>
#     # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    etiket  = "R1MMLVLIN"
    etiket2 = "__MMLVLIX"
    df.loc[df.nomvar.isin(["KMIN", "KMAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "TT",'etiket']                = etiket

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)
        
    # write the result
    results_file = TMP_PATH + "test_11.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test10-11_20210915.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)


def test_12(plugin_test_dir):
    """Invalid request -- missing mandatory fields KBAS and KTOP with bounded option """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    with pytest.raises(MinMaxLevelIndexError):
        spooki.MinMaxLevelIndex(
            src_df0, 
            nomvar="TT", 
            bounded=True).compute()

def test_13(plugin_test_dir):
    """Invalid request -- missing mandatory fields KBAS and KTOP with bounded option, on the same grid as field UU  """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_dir + "KbasKtop_v2.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df = pd.concat([src_df0 , src_df1])

    # compute spooki.MinMaxLevelIndex
    with pytest.raises(MinMaxLevelIndexError):
        spooki.MinMaxLevelIndex(
            src_df, 
            nomvar="UU", 
            bounded=True).compute()
