# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.skip]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/Helicity/testsFiles/'


def test_1(plugin_test_dir):
    """Test du plugin Helicity"""
    # open and read source
    source0 = plugin_test_dir + "UUVVGZ77x57x54_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Helicity
    df = spooki.Helicity(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Helicity] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "helicity3_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
