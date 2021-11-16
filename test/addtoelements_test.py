# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/AddToElement/testsFiles/'


def test_1(plugin_test_dir):
    """test_offset1"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_zeros_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute AddToElement
    df = spooki.AddToElement(src_df0, value=4).compute()
    # [ReaderStd --input {sources[0]}] >> [AddToElement --value +4.0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "offset_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """test_offset2"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_zeros_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute AddToElement
    df = spooki.AddToElement(src_df0, value=-2).compute()
    # [ReaderStd --input {sources[0]}] >> [AddToElement --value -2.0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "offset2_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
