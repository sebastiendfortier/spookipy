# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "GridPointDistance"

def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDistance_X_centered"""
    # open and read source
    source0 = plugin_test_path / "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDistance --axis X --differenceType CENTERED] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XCentered_file2cmp_rmn19_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDistance_Y_centered"""
    # open and read source
    source0 = plugin_test_path / "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['y'], 
                                    difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis Y --differenceType CENTERED] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "YCentered_file2cmp_rmn19_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDistance_X_forward"""
    # open and read source
    source0 = plugin_test_path / "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='forward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDistance --axis X --differenceType FORWARD] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XForward_file2cmp_rmn12_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDistance_Y_forward"""
    # open and read source
    source0 = plugin_test_path / "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['y'], 
                                    difference_type='forward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDistance --axis Y --differenceType FORWARD] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "YForward_file2cmp_rmn12_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDistance_X_backward"""
    # open and read source
    source0 = plugin_test_path / "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='backward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDistance --axis X --differenceType BACKWARD] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XBackward_file2cmp_rmn12_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDistance_Y_backward"""
    # open and read source
    source0 = plugin_test_path / "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['y'], 
                                    difference_type='backward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDistance --axis Y --differenceType BACKWARD] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "YBackward_file2cmp_rmn12_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDistance_XY_centered"""
    # open and read source
    source0 = plugin_test_path / "ps5x4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x','y'], 
                                    difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDistance --axis X,Y --differenceType CENTERED] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_7.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XYCentered_file2cmp_rmn19_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Grille globale reduite; repetition de la 1ere longitude.  Test pour l'axe des X, difference centree. """
    # open and read source    
    source0 = plugin_test_path / "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "GlbPres_test8_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Grille globale reduite; repetition de la 1ere longitude.  Test pour l'axe des X, difference AVANT. """
    # open and read source    
    source0 = plugin_test_path / "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='forward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType FORWARD] >> ",
#                 "[WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "GlbPres_test9_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """Grille globale reduite; repetition de la 1ere longitude.  Test pour l'axe des X, difference ARRIERE. """
    # open and read source    
    source0 = plugin_test_path / "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='backward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType BACKWARD] >> ",
#                 "[WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_10.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "GlbPres_test10_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de distance centree avec un fichier global reduit (grille type L avec longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_11.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "GlbPresL1_test11_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de distance arriere avec un fichier global reduit (grille type L avec longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='backward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType BACKWARD] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_12.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "GlbPresL1_test12_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de distance avant avec un fichier global reduit (grille type L avec longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='forward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType FORWARD] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_13.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "GlbPresL1_test13_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de distance centree avec un fichier global reduit (grille type L avec 1ere longitude qui se repete a la fin)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_14.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "GlbPresL2_test14_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de distance arriere avec un fichier global reduit (grille type L avec longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='backward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType BACKWARD] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_15.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "GlbPresL2_test15_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de distance centree avec un fichier global reduit (grille type G avec longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_path / "GlbHyb_gridG_reduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_16.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "GlbHybG_test16_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de distance centree avec un fichier global reduit (grille type A, longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridA.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >>",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_17.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "GlbPresA_test17_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_18(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de distance centree avec un fichier global reduit (grille type B, 1ere longitude qui se repete a la fin)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridB.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x'], 
                                    difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDistance --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_18.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "GlbPresB_test18_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_19(plugin_test_path, test_tmp_path, call_fstcomp):
    """Distance centree avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_path / "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x','y'], 
                                    difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDifference --axis X,Y --differenceType CENTERED] >> 
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_19.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()
    # print(results_file)

    # open and read comparison file
    file_to_compare = plugin_test_path / "XYCentered_YY_file2cmp_py_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_20(plugin_test_path, test_tmp_path, call_fstcomp):
    """Distance vers l'avant (forward) avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_path / "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x','y'], 
                                    difference_type='forward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDistance --axis X,Y --differenceType FORWARD] >> 
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_20.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XYForward_YY_file2cmp_py_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_21(plugin_test_path, test_tmp_path, call_fstcomp):
    """Distance vers l'arriere  avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_path / "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDistance
    df = spookipy.GridPointDistance(src_df0, 
                                    axis=['x','y'], 
                                    difference_type='backward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [GridPointDistance --axis X,Y --differenceType BACKWARD] >> 
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_21.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XYBackward_YY_file2cmp_py_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)    
