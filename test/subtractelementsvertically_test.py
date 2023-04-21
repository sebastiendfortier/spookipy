# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import pandas as pd
import fstpy
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets
import rpnpy.librmn.all as rmn

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/SubtractElementsVertically/testsFiles/'

def test_1(plugin_test_dir):
    """Utilisation de --outputFieldName avec une valeur > 4 caractères - requete invalide."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    with pytest.raises(spookipy.SubtractElementsVerticallyError):
        _ = spookipy.SubtractElementsVertically(src_df0, direction='ascending', nomvar_out='TROPLONG').compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SubtractElementsVertically --outputFieldName TROPLONG --direction ASCENDING]

def test_2(plugin_test_dir):
    """Effectue un test avec --outputFieldName mais plusieurs champs en entrée - requete invalide."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    with pytest.raises(spookipy.SubtractElementsVerticallyError):
        _ = spookipy.SubtractElementsVertically(src_df0, direction='ascending', nomvar_out='ABCD').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [SubtractElementsVertically --outputFieldName ABCD --direction ASCENDING]


def test_3(plugin_test_dir):
    """Test avec 2 champs et 2 niveaux, option --direction ASCENDING"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    df = spookipy.SubtractElementsVertically(src_df0, direction='ascending').compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SubtractElementsVertically --direction ASCENDING] >> 
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    df = spookipy.encode_ip2_and_ip3_height(df)
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "SubVert_test3_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare,columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])
    fstpy.delete_file(results_file)
    assert(res)

def test_4(plugin_test_dir):
    """Test avec un fichier de 2 champs et 2 niveaux, option --direction DESCENDING"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    df = spookipy.SubtractElementsVertically(src_df0, direction='descending').compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SubtractElementsVertically --direction DESCENDING] >> 
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]
    df = spookipy.encode_ip2_and_ip3_height(df)
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "SubVert_test4_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare,columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])
    fstpy.delete_file(results_file)
    assert(res)

def test_5(plugin_test_dir):
    """Test avec un fichier de 2 champs; selection d'un champ et --direction ASCENDING"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0,'ip_info')
    meta_df = src_df0.loc[src_df0.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

    src_df0 = src_df0.loc[src_df0.level==500.]
    src_df = pd.concat([meta_df,src_df0], ignore_index=True)

    # compute SubtractElementsVertically
    df = spookipy.SubtractElementsVertically(src_df, direction='ascending').compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [Select --verticalLevel 500] >> 
    # [SubtractElementsVertically --direction ASCENDING] >> 
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]
    df = spookipy.encode_ip2_and_ip3_height(df)
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "SubVert_test5_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare,columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])#, exclude_meta=True)
    fstpy.delete_file(results_file)
    assert(res)

def test_6(plugin_test_dir):
    """Test sur un fichier dont les champs possèdent des intervalles - requete invalide."""
    # open and read source
    source0 = plugin_test_dir + "inputTest6.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    with pytest.raises(spookipy.SubtractElementsVerticallyError):
        _ = spookipy.SubtractElementsVertically(src_df0, direction='ascending').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [SubtractElementsVertically --direction ASCENDING]


def test_7(plugin_test_dir):
    """Test avec 2 champs, plusieurs niveaux, differents forecastHours et --direction ASCENDING"""
    # open and read source
    source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    df = spookipy.SubtractElementsVertically(src_df0, direction='ascending').compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SubtractElementsVertically --direction ASCENDING] >> 
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]
    df = spookipy.encode_ip2_and_ip3_height(df)
    df.loc[~df.nomvar.isin(['ES','TT']), 'etiket'] = '_V700_'
    df.loc[df.nomvar.isin(['ES','TT']), 'typvar'] = 'P'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "SubVert_test7_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare,columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])#, exclude_meta=True)
    fstpy.delete_file(results_file)
    assert(res)

def test_8(plugin_test_dir):
    """Test avec 2 champs, plusieurs niveaux, differents forecastHours et --direction DESCENDING"""
    # open and read source
    source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    df = spookipy.SubtractElementsVertically(src_df0, direction='descending').compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SubtractElementsVertically --direction DESCENDING] >> 
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]
    df = spookipy.encode_ip2_and_ip3_height(df)
    df.loc[~df.nomvar.isin(['ES','TT']), 'etiket'] = '_V700_'
    df.loc[df.nomvar.isin(['ES','TT']), 'typvar'] = 'P'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "SubVert_test8_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare,columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])#, exclude_meta=True)
    fstpy.delete_file(results_file)
    assert(res)
