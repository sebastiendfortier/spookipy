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
    return "PowerValueByElement"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec une valeur entiere"""

    source0 = plugin_test_path / "UUVV5x5_2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.PowerValueByElement(src_df0, value=3).compute()

    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "Exponent_test1_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec une valeur en reel (float)"""

    source0 = plugin_test_path / "UUVV5x5_2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.PowerValueByElement(src_df0, value=0.333).compute()

    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "Exponent_test2_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec une valeur negative"""

    source0 = plugin_test_path / "UUVV5x5_2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.PowerValueByElement(src_df0, value=-3).compute()

    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "Exponent_test3_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec une valeur egale a 0"""

    source0 = plugin_test_path / "UUVV5x5_2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.PowerValueByElement(src_df0, value=0).compute()

    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "Exponent_test4_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier contenant des valeurs de 0 seulement"""

    source0 = plugin_test_path / "input0.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.PowerValueByElement(src_df0, value=3).compute()

    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "Exponent_test5_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res
