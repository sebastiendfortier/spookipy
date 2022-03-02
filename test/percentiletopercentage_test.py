# -*- coding: utf-8 -*-
# from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return "/fs/homeu1/eccc/cmd/cmde/loy000/Desktop/"


def test_1(plugin_test_dir):
    """Test with default options """
    # open and read source
    source0 = plugin_test_dir + "2022021100_out"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spooki.PercentileToPercentage(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [PercentileToPercentage] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = "/fs/homeu1/eccc/cmd/cmde/loy000/Desktop/test_1"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "PercentileToPercentage_file1cmp"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Test with an incorrect eteiket name"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(Exception):
        df = spooki.PercentileToPercentage(src_df0, etiket='wrong_etiket_name').compute()
    # [ReaderStd --input {sources[0]}] >> [Output Etiket Name --etiket wrong_etiket_name] >> [PercentileToPercentage] >> [Raise Exception]


def test_3(plugin_test_dir):
    """Test with changes to nomvar and operator"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spooki.PercentileToPercentage(src_df0, threshold=0.3, operator='le', etiket='GE0_____PALL',
                                       nomvar='SSH8', typvar='P@', percentile_step='0,100,5').compute()
    # [ReaderStd --input {sources[0]}] >> [Threshold --threshold 0.3, Operator --operator le, Etiket --etiket GE0_____PALL, Nomvar --nomvar SSH8, Typvar --typvar P@, Percentile_Step --percentile_step 0,100,5] >> [PercentileToPercentage] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = "/fs/homeu1/eccc/cmd/cmde/loy000/Desktop/test_2"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "PercentileToPercentage_file3cmp"

    # compare results

    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_4(plugin_test_dir):
    """Test with non valid percentile_step"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(Exception):
        df = spooki.PercentileToPercentage(src_df0, percentile_step="wrong_percentile").compute()
    # [ReaderStd --input {sources[0]}] >> [Output Etiket Name --etiket wrong_etiket_name] >> [PercentileToPercentage] >> [Raise Exception]