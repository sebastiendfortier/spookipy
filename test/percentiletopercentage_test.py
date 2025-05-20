# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "PercentileToPercentage"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test with default options"""
    # open and read source
    source0 = plugin_test_path / "2022021100_out_etiketStandard.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    ssh_df = fstpy.select_with_meta(src_df0, ["SSH"])

    df = spookipy.PercentileToPercentage(ssh_df, label="STG1__", threshold=0.3, operator="ge").compute()

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "PercentileToPercentage_file1cmp_20240312.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_2(plugin_test_path):
    """Test with an incorrect label length"""
    # open and read source
    source0 = plugin_test_path / "2022021100_out_etiketStandard.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.PercentileToPercentageError):
        _ = spookipy.PercentileToPercentage(src_df0, label="wrong_label_name", threshold=0.3, operator="ge").compute()


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test with changes to nomvar and operator"""
    # open and read source
    source0 = plugin_test_path / "2022021100_out_etiketStandard.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    ssh8_df = fstpy.select_with_meta(src_df0, ["SSH8"])

    df = spookipy.PercentileToPercentage(ssh8_df, label="STG1__", threshold=0.3, operator="le").compute()

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "PercentileToPercentage_file3cmp_20240312.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_4(plugin_test_path):
    """Test with label containing no digits - no data to process"""

    # open and read source
    source0 = plugin_test_path / "2022021100_out_etiketStandard.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df = src_df0.loc[src_df0["etiket"].str.contains("MEAN")]

    with pytest.raises(spookipy.PercentileToPercentageError):
        _ = spookipy.PercentileToPercentage(src_df, threshold=0.3, operator="ge").compute()


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test with negative threshold value and SSH8 nomvar"""

    # open and read source
    source0 = plugin_test_path / "2022021100_out_etiketStandard.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    ssh8_df = fstpy.select_with_meta(src_df0, ["SSH8"])

    df = spookipy.PercentileToPercentage(ssh8_df, label="STG1__", threshold=-0.3, operator="ge").compute()

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "PercentileToPercentage_file5cmp_20240312.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test with new version of default label"""

    # open and read source
    source0 = plugin_test_path / "2022021100_out_etiketStandard.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    ssh8_df = fstpy.select_with_meta(src_df0, ["SSH8"])

    df = spookipy.PercentileToPercentage(ssh8_df, threshold=-0.3, operator="ge").compute()

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "PercentileToPercentage_file6cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
