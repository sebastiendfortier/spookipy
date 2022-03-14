# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp
import secrets
import rpnpy.librmn.all as rmn

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/GridPointDistance/testsFiles/'


def test_1(plugin_test_dir):
    """test_gridPointDistance_X_centered"""
    # open and read source
    source0 = plugin_test_dir + "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis X --differenceType CENTERED] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XCentered_file2cmp_rmn19.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_2(plugin_test_dir):
    """test_gridPointDistance_Y_centered"""
    # open and read source
    source0 = plugin_test_dir + "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['y'], difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis Y --differenceType CENTERED] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "YCentered_file2cmp_rmn19.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_3(plugin_test_dir):
    """test_gridPointDistance_X_forward"""
    # open and read source
    source0 = plugin_test_dir + "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='forward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis X --differenceType FORWARD] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XForward_file2cmp_rmn12.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_4(plugin_test_dir):
    """test_gridPointDistance_Y_forward"""
    # open and read source
    source0 = plugin_test_dir + "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['y'], difference_type='forward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis Y --differenceType FORWARD] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "YForward_file2cmp_rmn12.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_5(plugin_test_dir):
    """test_gridPointDistance_X_backward"""
    # open and read source
    source0 = plugin_test_dir + "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='backward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis X --differenceType BACKWARD] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XBackward_file2cmp_rmn12.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_6(plugin_test_dir):
    """test_gridPointDistance_Y_backward"""
    # open and read source
    source0 = plugin_test_dir + "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['y'], difference_type='backward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis Y --differenceType BACKWARD] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "YBackward_file2cmp_rmn12.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_7(plugin_test_dir):
    """test_gridPointDistance_XY_centered"""
    # open and read source
    source0 = plugin_test_dir + "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x','y'], difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis X,Y --differenceType CENTERED] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XYCentered_file2cmp_rmn19.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)



def test_8(plugin_test_dir):
    """Grille globale reduite; repetition de la 1ere longitude.  Test pour l'axe des X, difference centree. """
    # open and read source    
    source0 = plugin_test_dir + "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "GlbPres_test8_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_9(plugin_test_dir):
    """Grille globale reduite; repetition de la 1ere longitude.  Test pour l'axe des X, difference AVANT. """
    # open and read source    
    source0 = plugin_test_dir + "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='forward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType FORWARD] >> ",
#                 "[WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "GlbPres_test9_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_10(plugin_test_dir):
    """Grille globale reduite; repetition de la 1ere longitude.  Test pour l'axe des X, difference ARRIERE. """
    # open and read source    
    source0 = plugin_test_dir + "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='backward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType BACKWARD] >> ",
#                 "[WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_dir + "GlbPres_test10_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_11(plugin_test_dir):
    """Calcul de distance centree avec un fichier global reduit (grille type L avec longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_dir + "GlbPres_gridL1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    df['etiket'] = 'GPTDISX'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "GlbPresL1_test11_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_12(plugin_test_dir):
    """Calcul de distance arriere avec un fichier global reduit (grille type L avec longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_dir + "GlbPres_gridL1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='backward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType BACKWARD] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"
    df['etiket'] = 'GPTDISX'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_dir + "GlbPresL1_test12_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_13(plugin_test_dir):
    """Calcul de distance avant avec un fichier global reduit (grille type L avec longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_dir + "GlbPres_gridL1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='forward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType FORWARD] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"
    df['etiket'] = 'GPTDISX'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "GlbPresL1_test13_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_14(plugin_test_dir):
    """Calcul de distance centree avec un fichier global reduit (grille type L avec 1ere longitude qui se repete a la fin)."""
    # open and read source
    source0 = plugin_test_dir + "GlbPres_gridL2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"
    df['etiket'] = 'GPTDISX'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_14.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "GlbPresL2_test14_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_15(plugin_test_dir):
    """Calcul de distance arriere avec un fichier global reduit (grille type L avec longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_dir + "GlbPres_gridL2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='backward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType BACKWARD] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"
    df['etiket'] = 'GPTDISX'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_15.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "GlbPresL2_test15_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_16(plugin_test_dir):
    """Calcul de distance centree avec un fichier global reduit (grille type G avec longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_dir + "GlbHyb_gridG_reduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"
    df.loc[df.nomvar=='GDX','etiket'] = 'GPTDISX'
    df.loc[~(df.nomvar=='GDX'),'etiket'] = 'Y3H9DNX'
    # df['nbits'] = 32
    # df['datyp'] = 5
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_16.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "GlbHybG_test16_file2cmp.std"
    # file_to_compare = "/home/sbf000/data/testFiles/GridPointDistance/result_test_16"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=4.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_17(plugin_test_dir):
    """Calcul de distance centree avec un fichier global reduit (grille type A, longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_dir + "GlbPres_gridA.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >>",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"
    df['etiket'] = 'GPTDISX'
    # df['nbits'] = 32
    # df['datyp'] = 5
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_17.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "GlbPresA_test17_file2cmp.std"
    # file_to_compare = "/home/sbf000/data/testFiles/GridPointDistance/result_test_17"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=32.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_18(plugin_test_dir):
    """Calcul de distance centree avec un fichier global reduit (grille type B, 1ere longitude qui se repete a la fin)."""
    # open and read source
    source0 = plugin_test_dir + "GlbPres_gridB.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"
    df['etiket'] = 'GPTDISX'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_18.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "GlbPresB_test18_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_19(plugin_test_dir):
    """Distance centree avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x','y'], difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDifference --axis X,Y --differenceType CENTERED] >> 
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_19.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()
    print(results_file)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XYCentered_YY_file2cmp_py.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_20(plugin_test_dir):
    """Distance vers l'avant (forward) avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x','y'], difference_type='forward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDistance --axis X,Y --differenceType FORWARD] >> 
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_20.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XYForward_YY_file2cmp_py.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_21(plugin_test_dir):
    """Distance vers l'arriere  avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spooki.GridPointDistance(src_df0, axis=['x','y'], difference_type='backward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDistance --axis X,Y --differenceType BACKWARD] >> 
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_21.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XYBackward_YY_file2cmp_py.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)    
