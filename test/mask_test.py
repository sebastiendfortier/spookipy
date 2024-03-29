# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import rpnpy.librmn.all as rmn
import spookipy
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/Mask/testsFiles/'


def test_1(plugin_test_dir):
    """seuils: 0,10,15,20 valeurs: 0,10,15,20 ops: ge,ge,ge,ge"""
    # open and read source
    source0 = plugin_test_dir + "new_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Mask
    df = spookipy.Mask(
        src_df0, thresholds=[
            0.0, 10.0, 15.0, 20.0], values=[
            0.0, 10.0, 15.0, 20.0], operators=[
                '>=', '>=', '>=', '>=']).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Mask --thresholds 0.0,10.0,15.0,20.0 --values 0.0,10.0,15.0,20.0 --operators ge,ge,ge,ge] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df = spookipy.convip(df, rmn.CONVIP_ENCODE_OLD)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest1_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """seuils: -15,-15,-5,10,20 valeurs: -20,-15,-5,10,20 ops: le,ge,ge,ge,ge"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Mask
    df = spookipy.Mask(src_df0, thresholds=[-15, -15, -5, 10, 20], values=[-20, -
                     15, -5, 10, 20], operators=['<=', '>=', '>=', '>=', '>=']).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Mask --thresholds -15,-15,-5,10,20 --values -20,-15,-5,10,20 --operators le,ge,ge,ge,ge] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest2_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_3(plugin_test_dir):
    """seuils: -10,0,10 valeurs: 1,2,3 ops: le,eq,gt"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Mask
    df = spookipy.Mask(src_df0,
                     thresholds=[-10,
                                 0,
                                 10],
                     values=[1,
                             2,
                             3],
                     operators=['<=',
                                '==',
                                '>']).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Mask --thresholds -10,0,10 --values 1,2,3 --operators le,eq,gt] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest3_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_4(plugin_test_dir):
    """ERREUR: pas le meme nombre de valeurs associe a seuils, valeurs, et ops"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.MaskError):
        # compute Mask
        _ = spookipy.Mask(
            src_df0, thresholds=[-10, 0, 10], values=[1, 2], operators=['<=', '==']).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds -10,0,10 --values 1,2 --operators le,eq] >>
        # [WriterStd --output {destination_path} --noUnitConversion]

def test_5(plugin_test_dir):
    """ERREUR: valeur invalide associee a operators (TT)"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.MaskError):
        # compute Mask
        _ = spookipy.Mask(
            src_df0, thresholds=[-0, 10], values=[0, 10], operators=['<=', 'TT']).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds -0,10 --values 0,10 --operators le,'TT'] >>
        # [WriterStd --output {destination_path} --noUnitConversion]


def test_6(plugin_test_dir):
    """seuils: -10,0,10 valeurs: 1,2,3 ops: le,eq,gt + outputFieldName=TOTO"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Mask
    df = spookipy.Mask(src_df0,
                     thresholds=[-10, 0, 10],
                     values=[1, 2, 3],
                     operators=['<=', '==', '>'],
                     nomvar_out='TOTO').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    #  [Mask --thresholds -10,0,10 --values 1,2,3 --operators le,eq,gt --outputFieldName TOTO] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest6_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
