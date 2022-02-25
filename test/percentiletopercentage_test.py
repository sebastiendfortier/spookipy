# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import sys
sys.path.insert(1, str('/usr/bin/pytest'))
import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
# ExamplePlugin/testsFiles is a folder that should be created in ~spst900/ppp3TestFiles/ and ~spst900/ppp4TestFiles/
    return TEST_PATH +"PercentileToPercentage/testsFiles/"

def test_1(plugin_test_dir):
    """ """
    # open and read source
    source0 = plugin_test_dir + "2022021100_out"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spooki.PercentileToPercentage(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [PercentileToPercentage] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "PercentileToPercentage_file1cmp"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_2(plugin_test_dir):
    """ """
    # open and read source
    source0 = plugin_test_dir + "2022021100_out"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(Exception):
        df = spooki.PercentileToPercentage(src_df0, etiket='wrong_etiket_name').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> [UnitConvert --unit kelvin] >> [TemperaturePotential] >> [WriterStd --output {destination_path} ]

def test_3(plugin_test_dir):
    """"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spooki.PercentileToPercentage(src_df0, threshold=0.3, operator='le', etiket='GE0_____ALL', nomvar='SSH8', typvar='P@', percentile_step='0,100,5').compute()
    # [ReaderStd --input {sources[0]}] >> [PercentileToPercentage] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "PercentileToPercentage_file3cmp"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
