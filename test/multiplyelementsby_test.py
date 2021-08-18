# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH, convip
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki
import rpnpy.librmn.all as rmn

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/MultiplyElementBy/testsFiles/'


def test_1(plugin_test_dir):
    """Test #1 : test_factor1"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_1_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute MultiplyElementsBy
    df = spooki.MultiplyElementsBy(src_df0, value=3).compute()
    #[ReaderStd --input {sources[0]}] >> [MultiplyElementsBy --value 3.0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df = convip(df,style=rmn.CONVIP_ENCODE_OLD)
    #write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "factor_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Test #2 : test_factor2"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_1_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute MultiplyElementsBy
    df = spooki.MultiplyElementsBy(src_df0, value=0.333).compute()
    #[ReaderStd --input {sources[0]}] >> [MultiplyElementsBy --value 0.333] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df = convip(df,style=rmn.CONVIP_ENCODE_OLD)
    #write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "factor2_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
