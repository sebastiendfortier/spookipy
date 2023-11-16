# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions, pytest.mark.humidity]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/HumidityRelativeWeightedMean/testsFiles/'

def test_1(plugin_test_dir):
    """Test avec un petit fichier contenant des valeurs verifiees a la main."""

    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.HumidityRelativeWeightedMean(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [HumidityRelativeWeightedMean ] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Test1_file2Cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_2(plugin_test_dir):
    """Test avec une sortie de modele."""

    # open and read source
    source = plugin_test_dir + "2020030412_024"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    df = spookipy.HumidityRelativeWeightedMean(src_df).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [HumidityRelativeWeightedMean ] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2020030412_test2_encoded_file2Cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)

def test_3(plugin_test_dir):
    """Test avec une sortie de modele avec une valeur pour capper les resultats."""

    # open and read source
    source = plugin_test_dir + "2020030412_024"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    df = spookipy.HumidityRelativeWeightedMean(src_df, capped_value=1.0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [HumidityRelativeWeightedMean --capped 1.0] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2020030412_test3_encoded_file2Cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)
