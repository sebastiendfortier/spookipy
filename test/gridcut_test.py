# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH, convip
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki
import pandas as pd


pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH +"GridCut/testsFiles/"

def test_reggc_test_1(plugin_test_dir):
    """Test #1 : Tester sur une zone de 3x4 depuis une extremite de la matrice."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute GridCut
    df = spooki.GridCut(src_df0,start_point=(0,0), end_point=(2,3)).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 0,0 --end_point 2,3] >> [WriterStd --output {destination_path} --ignoreExtended]

    df = convip(df)
    #write the result
    results_file = TMP_PATH + "gc_test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "gc_test_1.std"
    

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_reggc_test_2(plugin_test_dir):
    """Test #2 : Tester sur une zone de 3x4 depuis un point quelconque de la matrice"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute GridCut
    df = spooki.GridCut(src_df0, start_point=(2,1), end_point=(4,4)).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 2,1 --end_point 4,4] >> [WriterStd --output {destination_path} --ignoreExtended]

    df = convip(df)
    #write the result
    results_file = TMP_PATH + "gc_test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "gc_test_2.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_reggc_test_3(plugin_test_dir):
    """Test #3 : Test selection de toute la matrice"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute GridCut
    df = spooki.GridCut(src_df0,start_point=(0,0),end_point=(4,4)).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 0,0 --end_point 4,4] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "gc_test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "UUVV5x5x2_fileSrc.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_reggc_test_4(plugin_test_dir):
    """Test #4 : Tester sur une zone plus grande que la matrice d'origine"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute GridCut
    with pytest.raises(spooki.GridCutError):
        _ = spooki.GridCut(src_df0,start_point=(0,0),end_point=(4,5)).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 0,0 --end_point 4,5]


def test_reggc_test_5(plugin_test_dir):
    """Test #5 : Tester sur une zone de 25x25 avec meta products et depuis un point quelconque de la matrice"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_reghyb_TT.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute GridCut
    df = spooki.GridCut(src_df0,start_point=(4,6),end_point=(28,30)).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 4,6 --end_point 28,30] >> [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "gc_test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "gc_test_5.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_reggc_test_6(plugin_test_dir):
    """Test #6 : Tester coupure en 2 avec !! 64 bits"""
    # open and read source
    source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute GridCut
    df = spooki.GridCut(src_df0,start_point=(0,0),end_point=(511,399)).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 0,0 --end_point 511,399] >> [WriterStd --output {destination_path} --ignoreExtended]

    #temp fix for missing !!
    toctoc = df.query('(nomvar=="!!") and (ig1==5002)').reset_index(drop=True)
    df = df.query('nomvar!="!!"').reset_index(drop=True)
    df = pd.concat([toctoc,df],ignore_index=True)
    #write the result
    results_file = TMP_PATH + "gc_test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "gc_test_6.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


# def test_14(plugin_test_dir):
#     """Test #14 : Interpolation Verticale 1/16 pieces 649x672 664Mo"""
#     # open and read source
#     source0 = plugin_test_dir + "2011100712_012_regpres"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     source1 = plugin_test_dir + "2011100712_012_reghyb"
#     src_df1 = fstpy.StandardFileReader(source1).to_pandas()

#     src_df = pd.concat([src_df0,src_df1],ignore_index=True)

#     #compute GridCut
#     df = spooki.GridCut(src_df,start_point=(0,0),end_point=(648,42)).compute()
#     #[ReaderStd --input {sources[0]}] + ([ReaderStd --input {sources[1]}] >> 
#     # ([Select --fieldName GZ --verticalLevel SURFACE] + [Select --metadataFieldName P0] )) >> 
#     # [Select --xAxisMatrixSize 649 --yAxisMatrixSize 672] >> 
#     # (([GridCut --start_point 0,0 --end_point 648,42] >> 
# [InterpolationVertical -m FIELD_DEFINED --outputField INCLUDE_ALL_FIELDS --extrapolationType FIXED --valueAbove -300 --valueBelow -300 --referenceFieldName TT]) +
# ([GridCut --start_point 0,43 --end_point 648,84] >> 
# [InterpolationVertical -m FIELD_DEFINED --outputField INCLUDE_ALL_FIELDS --extrapolationType FIXED --valueAbove -300 --valueBelow -300 --referenceFieldName TT]) ) >> 
# [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

#     #write the result
#     results_file = TMP_PATH + "test_14.std"
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "2011100712_012_regpres_ud850_file2cmp.std+20210517"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     assert(res == True)

# same as 1, no multithread in python
# def test_reggc_test_15(plugin_test_dir):
#     """Test #15 : Tester SingleThread. Comme le test 1 mais en singlethread"""
#     # open and read source
#     source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #compute GridCut
#     df = spooki.GridCut(src_df0, start_point=(0,0), end_point=(2,3)).compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
#     # [GridCut -T 1 --start_point 0,0 --end_point 2,3] >>
#     #  [WriterStd --output {destination_path} --ignoreExtended]
#     df = convip(df)
#     #write the result
#     results_file = TMP_PATH + "gc_test_15.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "gc_test_1.std"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res == True)


