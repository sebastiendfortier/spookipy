# -*- coding: utf-8 -*-
from operator import concat
import pandas as pd
from test import TEST_PATH, TMP_PATH
from spookipy.minmaxlevelindex.minmaxlevelindex import  MinMaxLevelIndexError
from fstpy.std_enc import create_encoded_etiket, create_encoded_ip2
import fstpy.all as fstpy
import rpnpy.librmn.all as rmn  # A ENLEVER
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
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()

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

    label = "MMLVLI"
    # df = spooki.convip(df,spooki.rmn.CONVIP_ENCODE,'ip2')

    df_tt = df[df.nomvar == 'TT'].iloc[0]

    etiket  = create_encoded_etiket(run=df_tt.run,label=label,ensemble_member=df_tt.ensemble_member,implementation=df_tt.implementation)
    etiket2 = create_encoded_etiket(run='__',label=label,ensemble_member=df_tt.ensemble_member,implementation='X')

    df.loc[df.nomvar == "IND",'etiket'] = etiket2
    df.loc[df.nomvar == "TT",'etiket']  = etiket

    # Champs input
    df_tt = df.loc[df.nomvar == 'TT']
    df_tt = spooki.encode_ip1_and_ip3(df_tt)

    # Encodage des ip2
    for row in df.itertuples():
        if row.nomvar in ['>>', '^^', '^>', '!!', 'P0', 'PT']:
            continue 

        ip2_encoded = create_encoded_ip2(row.ip2,10)
        df.at[row.Index,'ip2'] = ip2_encoded

    # write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test1_20210915.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    # fstpy.delete_file(results_file)
    
    assert(res)

def test_2(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); recherche MAX, direction ASCENDING, nomvar_max IND """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()

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

    label = "MMLVLI"
    df_tt = df[df.nomvar == 'TT'].iloc[0]
    etiket  = create_encoded_etiket(run=df_tt.run,label=label,ensemble_member=df_tt.ensemble_member,implementation=df_tt.implementation)
    etiket2 = create_encoded_etiket(run='__',label=label,ensemble_member=df_tt.ensemble_member,implementation='X')

    df.loc[df.nomvar == "IND",'etiket'] = etiket2
    df.loc[df.nomvar == "TT",'etiket']  = etiket

    # Encodage des ip2
    for row in df.itertuples():
        if row.nomvar in ['>>', '^^', '^>', '!!', 'P0', 'PT']:
            continue 

        ip2_encoded            = create_encoded_ip2(row.ip2,10)
        df.at[row.Index,'ip2'] = ip2_encoded

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
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()

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

    label = "MMLVLI"
    df_tt = df[df.nomvar == 'TT'].iloc[0]
    etiket  = create_encoded_etiket(run=df_tt.run,label=label,ensemble_member=df_tt.ensemble_member,implementation=df_tt.implementation)
    etiket2 = create_encoded_etiket(run='__',label=label,ensemble_member=df_tt.ensemble_member,implementation='X')

    df.loc[df.nomvar.isin(["MIN", "MAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "TT",'etiket']              = etiket

    # Encodage des ip2
    for row in df.itertuples():
        if row.nomvar in ['>>', '^^', '^>', '!!', 'P0', 'PT']:
            continue 
        ip2_encoded            = create_encoded_ip2(row.ip2,10)
        df.at[row.Index,'ip2'] = ip2_encoded

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
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()

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

    label   = "MMLVLI"
    df      = spooki.convip(df,spooki.rmn.CONVIP_ENCODE,'ip2')
    df_gz   = df[df.nomvar == 'GZ'].iloc[0]
    etiket  = create_encoded_etiket(run=df_gz.run, label=label, ensemble_member=df_gz.ensemble_member, implementation=df_gz.implementation)
    etiket2 = create_encoded_etiket(run='__',label=label, ensemble_member=df_gz.ensemble_member, implementation='X')

    df.loc[df.nomvar.isin(["MIN", "MAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "GZ",'etiket']              = etiket

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
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()

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

    label   = "MMLVLI"
    df      = spooki.convip(df,spooki.rmn.CONVIP_ENCODE,'ip2')
    df_gz   = df[df.nomvar == 'GZ'].iloc[0]
    etiket  = create_encoded_etiket(run=df_gz.run, label=label, ensemble_member=df_gz.ensemble_member, implementation=df_gz.implementation)
    etiket2 = create_encoded_etiket(run='__',label=label, ensemble_member=df_gz.ensemble_member, implementation='X')

    df.loc[df.nomvar.isin(["MIN", "MAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "GZ",'etiket']              = etiket

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
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()

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

    label   = "MMLVLI"
    df      = spooki.convip(df,spooki.rmn.CONVIP_ENCODE,'ip2')
    df_uu   = df[df.nomvar == 'UU'].iloc[0]
    etiket  = create_encoded_etiket(run=df_uu.run, label=label, ensemble_member=df_uu.ensemble_member, implementation=df_uu.implementation)
    etiket2 = create_encoded_etiket(run='__',label=label, ensemble_member=df_uu.ensemble_member, implementation='X')

    df.loc[df.nomvar.isin(["MIN", "MAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "UU",'etiket']              = etiket

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
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()

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

    label   = "MMLVLI"
    df      = spooki.convip(df,spooki.rmn.CONVIP_ENCODE,'ip2')
    df_uu   = df[df.nomvar == 'UU'].iloc[0]
    etiket  = create_encoded_etiket(run=df_uu.run, label=label, ensemble_member=df_uu.ensemble_member, implementation=df_uu.implementation)
    etiket2 = create_encoded_etiket(run='__',label=label, ensemble_member=df_uu.ensemble_member, implementation='X')

    df.loc[df.nomvar.isin(["MIN", "MAX"]),'etiket'] = etiket2
    df.loc[df.nomvar == "UU",'etiket']              = etiket

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
    """--bounded --minMax MAX --outputFieldName2 IND"""
    # open and read source
    # source = plugin_test_dir + "test_ICGA.std"
    # # source90 = plugin_test_dir + "minmax_DOWNWARD_bounded_input"
    # src_df = fstpy.StandardFileReader(source, decode_metadata=True).to_pandas()

    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()
    # src_df0.loc[src_df0.level.between(200,1000, inclusive=True)]
    source1 = plugin_test_dir + "KbasKtop.std"
    src_df1 = fstpy.StandardFileReader(source1, decode_metadata=True).to_pandas()
    src_df = pd.concat([src_df0 , src_df1])

    var_df = fstpy.compute(src_df.loc[src_df.nomvar == "TT"])
    var_df = var_df.sort_values(by='level',ascending=var_df.ascending.unique()[0])
    levels=var_df.level.unique()
    num_levels = len(levels)
    print(f'\n\nLevels : \n {levels} \n\n')
    borne_inf=levels[0]
    borne_sup=levels[-1]
    # ip1_kind     =var_df.ip1_kind[0]

    # ip1 = float(borne_inf)
    # ip3 = float(borne_sup)
    # ip2 = 0
    # kind = int(ip1_kind)
    
    # print(f'RECU -- ip1 = {ip1} ip2 = {ip2} ip3 = {ip3} Kind = {kind}')
    # ip1_enc = rmn.ip1_val(ip1, kind)
    # ip3_enc = rmn.ip1_val(ip3, kind)
    ip1_enc = 41744464 
    ip3_enc = 41094464
    # kmin_df = spooki.create_empty_result(src_df, {'nomvar':'KMIN', 'etiket':'MMLVLI', 'ip1': ip1_enc, 'ip3': ip3_enc})
    # kmax_df = spooki.create_empty_result(src_df, {'nomvar':'KMAX', 'etiket':'MMLVLI', 'ip1': ip1_enc, 'ip3': ip3_enc})
    kmin_df = spooki.create_empty_result(src_df, {'nomvar':'KMIN', 'etiket':'MMLVLI', 'ip3': ip3_enc})
    kmax_df = spooki.create_empty_result(src_df, {'nomvar':'KMAX',  'etiket':'MMLVLI','ip3': ip3_enc })
    # print(f'ip1 = {ip1_enc}  ip3 = {ip3_enc}')
    
    kres_df = kmax_df
    kres_df = kres_df.append(kmin_df)

    # write the result
    results_file = TMP_PATH + "test_9.std"
    fstpy.delete_file(results_file) 
    fstpy.StandardFileWriter(results_file, kres_df).to_fst()

    # print(f'\n\n\n Src_test - TT : {src_df}\n\n')
    # compute spooki.MinMaxLevelIndex
    # df = spooki.MinMaxLevelIndex(
    #     src_df,
    #     nomvar="ICGA",
    #     max=True,
    #     bounded=True,
    #     nomvar_max='IND').compute()


    # print(f'df - Apres appel : \n {df} \n\n')
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [spooki.MinMaxLevelIndex --bounded --minMax MAX --outputFieldName2 IND] >>
    # [Zap --pdsLabel MinMaxBoundedIndexLevel --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]


    # ################# A faire disparaitre lorsque un writer a la Spooki sera disponible
    # label    = 'MINMAX'
    # df_input = df[df.nomvar == 'ICGA'].iloc[0]
    # etiket   = create_encoded_etiket(run=df_input.run, label=label, ensemble_member=df_input.ensemble_member, implementation='X')
    # etiket2  = create_encoded_etiket(run='__',label=label, ensemble_member=df_input.ensemble_member, implementation='X')

    # df.loc[df.nomvar == 'ICGA','etiket']   = etiket
    # df.loc[df.nomvar == 'IND' ,'etiket']   = etiket2

    # # Encodage des ip2
    # for row in df.itertuples():
    #     if row.nomvar in ['>>', '^^', '^>', '!!', 'P0', 'PT']:
    #         continue 

    #     ip2_encoded            = create_encoded_ip2(row.ip2,10)
    #     df.at[row.Index,'ip2'] = ip2_encoded

    # # Champs input
    # # df_res = df.loc[df.nomvar == 'ICGA']

    # df_res = spooki.encode_ip1_and_ip3_version2(df.loc[df.nomvar == 'ICGA'])

    # df_res = df_res.append(df.loc[df.nomvar == 'IND'])
    # ################

    # # write the result
    # results_file = TMP_PATH + "test_9.std"
    # fstpy.delete_file(results_file)
    # fstpy.StandardFileWriter(results_file, df_res).to_fst()

    # # open and read comparison file
    # file_to_compare = plugin_test_dir + "test_ICGA_file2cmp_20201202.std"

    # # compare results
    # res = fstcomp(results_file, file_to_compare)
    # # fstpy.delete_file(results_file)

    # # assert(res)
    assert(False)

def test_10(plugin_test_dir):
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()
    # src_df0.loc[src_df0.level.between(200,1000, inclusive=True)]
    source1 = plugin_test_dir + "KbasKtop.std"
    src_df1 = fstpy.StandardFileReader(source1, decode_metadata=True).to_pandas()
    src_df = pd.concat([src_df0 , src_df1])
    df = spooki.AddToElements(src_df, value=4).compute()

    assert(False)

# def test_10(plugin_test_dir):
#     """ 7 niveaux de TT (valeurs decroissantes en montant); BOUNDED, recherche BOTH, direction ASCENDING, nomvar_min MIN, nomvar_max MAX """
#     # open and read source
#     source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
#     src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()
#     # src_df0.loc[src_df0.level.between(200,1000, inclusive=True)]
#     source1 = plugin_test_dir + "KbasKtop.std"
#     src_df1 = fstpy.StandardFileReader(source1, decode_metadata=True).to_pandas()
#     src_df = pd.concat([src_df0 , src_df1])
    
#     # compute spooki.MinMaxLevelIndex
#     df = spooki.MinMaxLevelIndex(
#         src_df,
#         nomvar="TT",
#         bounded=True,
#         min=True,
#         max=True).compute()
#     # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,KBAS,KTOP] >> 
#     # [MinMaxLevelIndex --bounded --minMax BOTH --direction ASCENDING] >>
#     # [WriterStd --output {destination_path} --encodeIP2andIP3]",

#     label   = 'MMLVLI'

#     df_tt   = df[df.nomvar == 'TT'].iloc[0]
#     etiket  = create_encoded_etiket(run=df_tt.run,label=label,ensemble_member=df_tt.ensemble_member,implementation=df_tt.implementation)
#     etiket2 = create_encoded_etiket(run='__',label=label,ensemble_member=df_tt.ensemble_member,implementation='X')

#     df.loc[df.nomvar.isin(["KMIN", "KMAX"]),'etiket'] = etiket2
#     df.loc[df.nomvar == "TT",'etiket']                = etiket

#     # Encodage des ip2
#     for row in df.itertuples():
#         if row.nomvar in ['>>', '^^', '^>', '!!', 'P0', 'PT']:
#             continue 

#         ip2_encoded            = create_encoded_ip2(row.ip2,10)
#         df.at[row.Index,'ip2'] = ip2_encoded
        
#     # write the result
#     results_file = TMP_PATH + "test_10.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "MinMax_file2cmp_test10-11_20210915.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     # fstpy.delete_file(results_file)
    
#       # assert(res)
#     assert(False)

# def test_11(plugin_test_dir):
#     """ 7 niveaux de TT (valeurs decroissantes en montant); BOUNDED, recherche BOTH, direction ASCENDING, nomvar_min MIN, nomvar_max MAX """
#     # open and read source
#     source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
#     src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()
#     # src_df0.loc[src_df0.level.between(200,1000, inclusive=True)]
#     source1 = plugin_test_dir + "KbasKtop.std"
#     src_df1 = fstpy.StandardFileReader(source1, decode_metadata=True).to_pandas()
#     src_df = pd.concat([src_df0 , src_df1])
    
#     # compute spooki.MinMaxLevelIndex
#     df = spooki.MinMaxLevelIndex(
#         src_df,
#         nomvar="TT",
#         bounded=True,
#         min=True,
#         max=True).compute()
#     # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,KBAS,KTOP] >> 
#     # [MinMaxLevelIndex --bounded --minMax BOTH --direction ASCENDING] >>
#     # [WriterStd --output {destination_path} --encodeIP2andIP3]",

#     label   = 'MMLVLI'

#     df_tt   = df[df.nomvar == 'TT'].iloc[0]
#     etiket  = create_encoded_etiket(run=df_tt.run,label=label,ensemble_member=df_tt.ensemble_member,implementation=df_tt.implementation)
#     etiket2 = create_encoded_etiket(run='__',label=label,ensemble_member=df_tt.ensemble_member,implementation='X')

#     df.loc[df.nomvar.isin(["KMIN", "KMAX"]),'etiket'] = etiket2
#     df.loc[df.nomvar == "TT",'etiket']                = etiket

#     # Encodage des ip2
#     for row in df.itertuples():
#         if row.nomvar in ['>>', '^^', '^>', '!!', 'P0', 'PT']:
#             continue 

#         ip2_encoded            = create_encoded_ip2(row.ip2,10)
#         df.at[row.Index,'ip2'] = ip2_encoded
        
#     # write the result
#     results_file = TMP_PATH + "test_10.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "MinMax_file2cmp_test10-11_20210915.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     # fstpy.delete_file(results_file)
    
#       # assert(res)
#     assert(False)

# def test_11(plugin_test_dir):
#     """ 7 niveaux de TT (valeurs decroissantes en montant); BOUNDED, recherche BOTH, direction DESCENDING, nomvar_min MIN, nomvar_max MAX """
#     # open and read source
#     source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
#     src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()
#     source1 = plugin_test_dir + "KbasKtop.std"
#     src_df1 = fstpy.StandardFileReader(source1, decode_metadata=True).to_pandas()
#     src_df = pd.concat([src_df0 , src_df1])

#     # compute spooki.MinMaxLevelIndex
#     df = spooki.MinMaxLevelIndex(
#         src_df,
#         nomvar="TT",
#         bounded=True,
#         ascending=False,
#         min=True,
#         max=True).compute()
#     # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,KBAS,KTOP] >> 
#     # [MinMaxLevelIndex --bounded --minMax BOTH --direction ASCENDING] >>
#     # [WriterStd --output {destination_path} --encodeIP2andIP3]",

#     df = spooki.convip(df,spooki.rmn.CONVIP_ENCODE,'ip2')
#     df_tt = df[df.nomvar == 'TT'].iloc[0]
#     etiket  = create_encoded_etiket(run=df_tt.run,label=df_tt.etiket,ensemble_member=df_tt.ensemble_member,implementation=df_tt.implementation)
#     etiket2 = create_encoded_etiket(run='__',label=df_tt.etiket,ensemble_member=df_tt.ensemble_member,implementation='X')

#     df.loc[df.nomvar.isin(["KMIN", "KMAX"]),'etiket'] = etiket2
#     df.loc[df.nomvar == "TT",'etiket'] = etiket

#     # write the result
#     results_file = TMP_PATH + "test_11.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "MinMax_file2cmp_test10-11_20210915.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     # fstpy.delete_file(results_file)
    
#     assert(res)

# def test_10(plugin_test_dir):
#     """--bounded --minMax BOTH"""
#     # open and read source
#     source0 = plugin_test_dir + "TT_bounded_minmax.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute spooki.MinMaxLevelIndex
#     df = spooki.MinMaxLevelIndex(
#         src_df0, 
#         nomvar="TT", 
#         bounded=True).compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.MinMaxLevelIndex --bounded --minMax BOTH] >> [Select --fieldName KBAS,KTOP --exclude] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

#     df['ip2'] = 24
#     # write the result
#     results_file = TMP_PATH + "test_10.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "TT_bounded_minmax_file2cmp.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     # fstpy.delete_file(results_file)
#     assert(res)




#  AJOUTER PAR GUYLAINE - RENOMMER TESTS

def test_21(plugin_test_dir):
    """Invalid request -- missing fields KBAS and KTOP with bounded option """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    with pytest.raises(MinMaxLevelIndexError):
        spooki.MinMaxLevelIndex(
            src_df0, 
            nomvar="TT", 
            bounded=True).compute()

def test_22(plugin_test_dir):
    """Invalid request -- missing fields KBAS and KTOP on the same grid with bounded option """
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


# def test_23(plugin_test_dir):
#     """Fichier d'entrée contenant plusieurs champs """
#     # open and read source
#     source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()
#     source1 = plugin_test_dir + "KbasKtop.std"
#     src_df1 = fstpy.StandardFileReader(source1).to_pandas()
#     src_df = pd.concat([src_df0 , src_df1])
#     cols=(['nomvar','d'])
#     # print(src_df[cols])

#     # compute spooki.MinMaxLevelIndex

#     df = spooki.MinMaxLevelIndex(
#             src_df, 
#             bounded=True).compute()

#     k_df = df.loc[(df.nomvar.isin(["TT","KMIN","KMAX"]))].reset_index(drop=True)
#     k_data = fstpy.compute(k_df)
#     print(k_data[cols])
#     # print(df[cols])
#     # write the result
#     results_file = TMP_PATH + "test_22.std"
#     fstpy.delete_file(results_file)
#     # print(f'Fichier temporaire cree: {results_file}')
#     fstpy.StandardFileWriter(results_file, df).to_fst()
#     assert(False)

    # # open and read comparison file
    # file_to_compare = plugin_test_dir + "TT_bounded_minmax_file2cmp.std"

    # # compare results
    # res = fstcomp(results_file, file_to_compare)
    # fstpy.delete_file(results_file)
    # assert(res)
