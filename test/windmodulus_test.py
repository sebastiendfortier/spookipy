# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import pandas as pd
import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/WindModulusAndDirection/testsFiles/'

def test_regtest_1(plugin_test_dir):
    """Test #1 : test_read_select_write_UV"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()

    #compute WindModulus
    df = spooki.WindModulus(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "windmodulus_test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windModulus_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_2(plugin_test_dir):
    """Test #2 : test_read_select_write_UV2"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()


    #compute WindModulus
    df = spooki.WindModulus(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "windmodulus_test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windModulus3D_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_3(plugin_test_dir):
    """Test #3 : test_read_select_write_UVWD"""
    # open and read source
    source0 = plugin_test_dir + "windModulusAndDirection_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()


    #compute WindModulus
    df = spooki.WindModulus(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    df['etiket'] = "WNDMAD"
    #write the result
    results_file = TMP_PATH + "windmodulus_test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windModulusAndDirection_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,allclose=True)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_4(plugin_test_dir):
    """Test #4 : test_read_select_write_UV_already_calculated"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_UV_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()


    #compute WindModulus
    df = spooki.WindModulus(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "windmodulus_test_4.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windModulus_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_5(plugin_test_dir):
    """Test #5 : test_read_select_write_UV_already_calculated_without_UU_VV"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_UV_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()


    #compute WindModulus
    df = spooki.WindModulus(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UV,UU,VV] >> [WindModulus --optimizationLevel 1] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "windmodulus_test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windModulus_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_6(plugin_test_dir):
    """Test #6 : test_read_select_write_UV_already_calculated2"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_UV_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()


    #compute WindModulus
    df = spooki.WindModulus(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "windmodulus_test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windModulus3D_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)



def test_regtest_9(plugin_test_dir):
    """Test #9 : test_read_select_write_UV_GRID_X"""
    # open and read source
    source0 = plugin_test_dir + "uu_850.std"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()

    source1 = plugin_test_dir + "vv_850.std"
    src_df1 = fstpy.StandardFileReader(source1,decode_metadata=True).to_pandas()

    src_df=pd.concat([src_df0,src_df1], ignore_index=True)

    #compute WindModulus
    df = spooki.WindModulus(src_df).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]} {sources[1]}] >> [WindModulus] >> [WriterStd --output {destination_path} --ignoreExtended]
    #pourquoi ca devrait pas fonctionner?

    #write the result
    results_file = TMP_PATH + "windmodulus_test_9.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windmodulus3D850_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)

