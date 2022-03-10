# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + "/PercentageToPercentile/testsFiles/"


def test_1(plugin_test_dir):
    """Test with default options """
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spooki.PercentileToPercentage(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [PercentileToPercentage] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "PercentileToPercentage_file1cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    #fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Test with an incorrect eteiket name"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spooki.PercentileToPercentageError):
        _ = spooki.PercentileToPercentage(src_df0, etiket='wrong_etiket_name').compute()
    # [ReaderStd --input {sources[0]}] >> [Etiket --etiket wrong_etiket_name] >> [PercentileToPercentage] >> [Raise Exception]


def test_3(plugin_test_dir):
    """Test with changes to nomvar and operator"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spooki.PercentileToPercentage(src_df0, threshold=0.3, operator='le', etiket='GE0_____PALL',
                                       nomvar='SSH8', typvar='P@', percentile_step=5).compute()
    # [ReaderStd --input {sources[0]}] >> [Threshold --threshold 0.3, Operator --operator le, Etiket --etiket GE0_____PALL, Nomvar --nomvar SSH8, Typvar --typvar P@, Percentile_Step --percentile_step 0,100,5] >> [PercentileToPercentage] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "PercentileToPercentage_file3cmp.std"

    # compare results

    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    #fstpy.delete_file(results_file)
    assert(res)


def test_4(plugin_test_dir):
    """Test with non valid percentile_step"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spooki.PercentileToPercentageError):
        _ = spooki.PercentileToPercentage(src_df0, percentile_step="wrong_percentile").compute()
    # [ReaderStd --input {sources[0]}] >> [Percentile_Step --percentile_step wrong_percentile] >> [PercentileToPercentage] >> [Raise Exception]


def test_5(plugin_test_dir):
    """Test with negative threshold value and SSH8 nomvar"""
    
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spooki.PercentileToPercentage(src_df0, threshold=-0.3, nomvar='SSH8').compute()
    # [ReaderStd --input {sources[0]}] >> [Threshold --threshold -0.3, Nomvar --nomvar SSH8] >> [PercentileToPercentage] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "PercentileToPercentage_file5cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)