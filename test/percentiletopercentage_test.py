# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy.all as fstpy
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + "/PercentageToPercentile/testsFiles/"


def test_1(plugin_test_dir):
    """Test with default options """
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.PercentileToPercentage(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [PercentileToPercentage] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "PercentileToPercentage_file1cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Test with an incorrect eteiket name"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.PercentileToPercentageError):
        _ = spookipy.PercentileToPercentage(src_df0, etiket='wrong_etiket_name').compute()
    # [ReaderStd --input {sources[0]}] >> [Etiket --etiket wrong_etiket_name] >> [PercentileToPercentage] >> [Raise Exception]


def test_3(plugin_test_dir):
    """Test with changes to nomvar and operator"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.PercentileToPercentage(src_df0, threshold=0.3, operator='le',
                                       nomvar='SSH8').compute()
    # [ReaderStd --input {sources[0]}] >> [Threshold --threshold 0.3, Operator --operator le, Nomvar --nomvar SSH8, >> [PercentileToPercentage] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir+ "PercentileToPercentage_file3cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_4(plugin_test_dir):
    """Test with non valid percentile_step"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.PercentileToPercentageError):
        _ = spookipy.PercentileToPercentage(src_df0, nomvar="empty_nomvar").compute()
    # [ReaderStd --input {sources[0]}] >> [Nomvar --nomvar empty_nomvar] >> [PercentileToPercentage] >> [Raise Exception]


def test_5(plugin_test_dir):
    """Test with negative threshold value and SSH8 nomvar"""
    
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.PercentileToPercentage(src_df0, threshold=-0.3, nomvar='SSH8').compute()
    # [ReaderStd --input {sources[0]}] >> [Threshold --threshold -0.3, Nomvar --nomvar SSH8] >> [PercentileToPercentage] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "PercentileToPercentage_file5cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_6(plugin_test_dir):
    """Test with non valid etiket length of 11"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.PercentileToPercentageError):
        _ = spookipy.PercentileToPercentage(src_df0, etiket="GEST1__PALL").compute()
    # [ReaderStd --input {sources[0]}] >> [Etiket --etiket GEST1__PALL] >> [PercentileToPercentage] >> [Raise Exception]

def test_7(plugin_test_dir):
    """Test with non valid etiket ending"""
    # open and read source
    source0 = plugin_test_dir + "2022021100_out.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.PercentileToPercentageError):
        _ = spookipy.PercentileToPercentage(src_df0, etiket="GEST1___PBLL").compute()
    # [ReaderStd --input {sources[0]}] >> [Etiket --etiket GEST1___PBLL] >> [PercentileToPercentage] >> [Raise Exception]
