# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/AddToElement/testsFiles/'


def test_regtest_1(plugin_test_dir):
    """Test #1 : test_offset1"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_zeros_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute AddToElements
    df = spooki.AddToElements(src_df0, value=4).compute()
    #[ReaderStd --input {sources[0]}] >> [AddToElements --value +4.0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    df['etiket'] = "ADDTOE"
    #write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "offset_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_2(plugin_test_dir):
    """Test #2 : test_offset2"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_zeros_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AddToElements
    df = spooki.AddToElements(src_df0, value=-2).compute()
    #[ReaderStd --input {sources[0]}] >> [AddToElements --value -2.0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    df['etiket'] = "ADDTOE"
    #write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "offset2_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)
