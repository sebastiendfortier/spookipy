# -*- coding: utf-8 -*-
from operator import concat
import pandas as pd
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

from spookipy.minmaxlevelindex.minmaxlevelindex import  MinMaxLevelIndex, MinMaxLevelIndexError
import fstpy
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/MinMaxLevelIndex/testsFiles/'

def test_1(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); recherche MIN, direction ASCENDING, nomvar_min_idx IND """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    # df = src_df0
    df = spookipy.MinMaxLevelIndex(
        src_df0,
        nomvar="TT",
        min=True,
        ascending=True,
        nomvar_min_idx='IND').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> 
    # [MinMaxLevelIndex --minMax MIN --direction ASCENDING --outputFieldName1 IND] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    # Conserver car on encode les ip2/ip3 de tous les champs, pas juste les champs resultats
    df = spookipy.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test1_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); recherche MAX, direction ASCENDING, nomvar_max_idx IND """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxLevelIndex(
        src_df0,
        nomvar="TT",
        max=True,
        ascending=True,
        nomvar_max_idx='IND').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> 
    # [MinMaxLevelIndex --minMax MAX --direction ASCENDING --outputFieldName2 IND] 
    # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    # Conserver car on encode les ip2/ip3 de tous les champs, pas juste les champs resultats
    df = spookipy.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test2_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_3(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); recherche BOTH, direction DESCENDING, nomvar_min_idx MIN, nomvar_max_idx MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxLevelIndex(
        src_df0,
        nomvar="TT",
        min=True,
        max=True,
        ascending=False,
        nomvar_min_idx='MIN',
        nomvar_max_idx='MAX').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> 
    # [MinMaxLevelIndex --minMax BOTH --direction DESCENDING --outputFieldName1 MIN --outputFieldName2 MAX] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    # Conserver car on encode les ip2/ip3 de tous les champs, pas juste les champs resultats
    df = spookipy.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test3_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_4(plugin_test_dir):
    """ 7 niveaux de GZ (valeurs croissantes en montant); recherche BOTH, direction ASCENDING, nomvar_min_idx MIN, nomvar_max_idx MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxLevelIndex(
        src_df0,
        nomvar="GZ",
        min=True,
        max=True,
        nomvar_min_idx='MIN',
        nomvar_max_idx='MAX').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName GZ] >> 
    # [MinMaxLevelIndex --minMax BOTH --direction ASCENDING --outputFieldName1 MIN --outputFieldName2 MAX] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]"

    # Conserver car on encode les ip2/ip3 de tous les champs, pas juste les champs resultats
    df = spookipy.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test4-5_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_5(plugin_test_dir):
    """ 7 niveaux de GZ (valeurs croissantes en montant); recherche BOTH, direction DESCENDING, nomvar_min_idx MIN, nomvar_max_idx MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxLevelIndex(
        src_df0,
        nomvar="GZ",
        min=True,
        max=True,
        ascending=False,
        nomvar_min_idx='MIN',
        nomvar_max_idx='MAX').compute()
#     # [ReaderStd --input {sources[0]}] >> [Select --fieldName GZ] >> 
#     # [MinMaxLevelIndex --minMax BOTH --direction ASCENDING --outputFieldName1 MIN --outputFieldName2 MAX] >>
#     # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    # Conserver car on encode les ip2/ip3 de tous les champs, pas juste les champs resultats
    df = spookipy.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test4-5_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)

def test_6(plugin_test_dir):
    """ 7 niveaux de UU (valeurs desordonnees); recherche BOTH, direction DESCENDING, nomvar_min_idx MIN, nomvar_max_idx MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxLevelIndex(
        src_df0,
        nomvar="UU",
        min=True,
        max=True,
        ascending=False,
        nomvar_min_idx='MIN',
        nomvar_max_idx='MAX').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> 
    # [MinMaxLevelIndex --minMax BOTH --direction DESCENDING --outputFieldName1 MIN --outputFieldName2 MAX] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]"

    # Conserver car on encode les ip2/ip3 de tous les champs, pas juste les champs resultats
    df = spookipy.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test6-7_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)

def test_7(plugin_test_dir):
    """ 7 niveaux de UU (valeurs desordonnees); recherche BOTH, direction ASCENDING, nomvar_min_idx MIN, nomvar_max_idx MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxLevelIndex(
        src_df0,
        nomvar="UU",
        min=True,
        max=True,
        ascending=False,
        nomvar_min_idx='MIN',
        nomvar_max_idx='MAX').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> 
    # [MinMaxLevelIndex --minMax BOTH --direction DESCENDING --outputFieldName1 MIN --outputFieldName2 MAX] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]"

    # Conserver car on encode les ip2/ip3 de tous les champs, pas juste les champs resultats
    df = spookipy.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test6-7_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)

def test_9(plugin_test_dir):
    """3 niveaux de ICGA (sortie du plugin IcingRimeAppleman); BOUNDED, recherche MAX, direction ASCENDING, nomvar_max_idx IND"""
    # open and read source
    source = plugin_test_dir + "test_ICGA.std"
    # source90 = plugin_test_dir + "minmax_DOWNWARD_bounded_input"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxLevelIndex(
        src_df,
        nomvar="ICGA",
        max=True,
        bounded=True,
        nomvar_max_idx='IND').compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [MinMaxLevelIndex --bounded --minMax MAX --outputFieldName2 IND] >>
    # [Zap --pdsLabel MinMaxBoundedIndexLevel --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]]

    # On conserve ces modif pour respecter le zap du test en C++
    etiket  = "MINMAXX"
    etiket2 = "__MINMAXX"
    df.loc[df.nomvar == 'ICGA','etiket']   = etiket
    df.loc[df.nomvar == 'IND' ,'etiket']   = etiket2

    # Conserver car on encode les ip2/ip3 de tous les champs, pas juste les champs resultats
    df = spookipy.encode_ip2_and_ip3_height(df)
    
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test_ICGA_file2cmp_20201202.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)

def test_10(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); BOUNDED, recherche BOTH, direction ASCENDING, nomvar_min_idx MIN, nomvar_max_idx MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    # src_df0.loc[src_df0.level.between(200,1000, inclusive=True)]
    source1 = plugin_test_dir + "KbasKtop.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df = pd.concat([src_df0 , src_df1])
    
    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxLevelIndex(
        src_df,
        nomvar="TT",
        bounded=True,
        min=True,
        max=True).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,KBAS,KTOP] >> 
    # [MinMaxLevelIndex --bounded --minMax BOTH --direction ASCENDING] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    # Conserver car on encode les ip2/ip3 de tous les champs, pas juste les champs resultats
    df = spookipy.encode_ip2_and_ip3_height(df)
        
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test10-11_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)

def test_11(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); BOUNDED, recherche BOTH, direction DESCENDING, nomvar_min_idx MIN, nomvar_max_idx MAX """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_dir + "KbasKtop.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df = pd.concat([src_df0 , src_df1])
    
    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxLevelIndex(
        src_df,
        nomvar="TT",
        bounded=True,
        ascending=False,
        min=True,
        max=True).compute()
#     # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,KBAS,KTOP] >> 
#     # [MinMaxLevelIndex --bounded --minMax BOTH --direction ASCENDING] >>
#     # [WriterStd --output {destination_path} --encodeIP2andIP3]",

    # Conserver car on encode les ip2/ip3 de tous les champs, pas juste les champs resultats
    df = spookipy.encode_ip2_and_ip3_height(df)
        
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test10-11_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    
    assert(res)

def test_12(plugin_test_dir):
    """Invalid request -- missing mandatory fields KBAS and KTOP with bounded option """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    with pytest.raises(MinMaxLevelIndexError):
        spookipy.MinMaxLevelIndex(
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

    # compute spookipy.MinMaxLevelIndex
    with pytest.raises(spookipy.DependencyError):
        spookipy.MinMaxLevelIndex(
            src_df, 
            nomvar="UU", 
            bounded=True).compute()

# Saut de numeros de test pour ne pas interferer avec les ancients tests existants dans version Spooki
def test_20(plugin_test_dir):
    """Test avec des fichiers ayant des grilles differentes mais contenant les meme champs; recherche min et max, indices et valeurs. """
    # open and read source
    source0 = plugin_test_dir + "200906290606_TT_grid1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_dir + "200906290606_TT_grid2.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1])
    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxLevelIndex(
        src_df, 
        nomvar="TT",
        value_to_return=True).compute()

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_20.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test20_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_21(plugin_test_dir):
    """Requete partiellement reussie -- 2 groupes de champs dont 1 groupe incomplet car il manque les champs KBAS et KTOP  """
    # Test identique au test 11 pour ce qui concerne le groupe complet. 
    # On veut s'assurer que la requete s'execute en ignorant le groupe qui est incomplet

    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_dir + "KbasKtop.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    source2 = plugin_test_dir + "200906290606_TT_grid2.std"
    src_df2 = fstpy.StandardFileReader(source2).to_pandas()
    src_df = pd.concat([src_df0 , src_df1, src_df2])

    df = spookipy.MinMaxLevelIndex(
        src_df, 
        nomvar="TT",
        bounded=True).compute()
    
     # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_21.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test21_20231026.std"

    # compare results 
    res = fstcomp(results_file, file_to_compare) 
    fstpy.delete_file(results_file)
    assert(res)
    
def test_22(plugin_test_dir):
    """ 7 niveaux de TT (valeurs decroissantes en montant); recherche MIN, direction ASCENDING, nomvar_min_idx IND """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxLevelIndex(
        src_df0,
        nomvar="TT",
        min=True,
        ascending=True,
        nomvar_min_idx='IND',
        copy_input=True).compute()

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_22.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test22_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

# Creation du fichier d'input pour le test
# Repertoires de donnees:  /space/hall5/sitestore/eccc/prod/ops/gridpt/dbase/prog/regpres
# spooki_run.py 
# "([ReaderStd --input .../2024012000_024]  >> [Select --fieldName TT,HU,ES --verticalLevel 900@1000 --verticalLevelType MILLIBARS]) +
#  ([ReaderStd --input .../2024012100_000] >>  [Select --fieldName TT,HU,ES --verticalLevel 900@1000 --verticalLevelType MILLIBARS]) >>
#  [GridCut --startPoint 0,0 --endPoint 20,20]  >>
#  [WriterStd --output Regpres_TTHUES_differentDateoSameDatev.std]"
def test_23(plugin_test_dir):
    """2 groupes de TT avec dates d'origine differentes mais dates de validity identiques """

    source  = plugin_test_dir + "Regpres_TTHUES_differentDateoSameDatev.std"
    src_df  = fstpy.StandardFileReader(source).to_pandas()

    df      = spookipy.MinMaxLevelIndex(src_df, 
                                        nomvar="TT").compute()
    
     # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_23.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMax_file2cmp_test23.std"

    # compare results 
    res = fstcomp(results_file, file_to_compare) 
    fstpy.delete_file(results_file)
    assert(res)
