# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets
from spookipy.utils import DependencyError

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/WindChill/testsFiles/'


def test_1(plugin_test_dir):
    """Calculate with a simple test data """
    # open and read source
    source0   = plugin_test_dir + "UUVVTT_fileSrc.std"
    src_df0   = fstpy.StandardFileReader(source0).to_pandas()

    uv_df     = spookipy.WindModulus(src_df0).compute()

    uv_src_df = pd.concat([src_df0, uv_df], ignore_index=True)

    # compute WindChill
    df = spookipy.WindChill(uv_src_df).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [WindChill] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windChill_file2cmp_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Spooki must fail when no surface level is found """
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uv_df   = src_df0.loc[src_df0.nomvar .isin(
        ["UU", "VV"])].reset_index(drop=True)
    uv_df   = spookipy.WindModulus(uv_df).compute()
    uv_src_df = pd.concat([src_df0, uv_df], ignore_index=True)

    uv_src_df = fstpy.add_columns(uv_src_df, columns=['ip_info'])
    src_df0   = uv_src_df.loc[uv_src_df.surface == False].reset_index(drop=True)

    # compute WindChill
    with pytest.raises(spookipy.WindChillError):
        _ = spookipy.WindChill(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 1.0 --exclude] >> [WindChill]


def test_3(plugin_test_dir):
    """Spooki must fail when input are in millibars"""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WindChill
    with pytest.raises(spookipy.WindChillError):
        _ = spookipy.WindChill(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>[WindChill]

def test_4(plugin_test_dir):
    """2 groupes de UU,VV,TT avec dates d'origine differentes mais dates de validity identiques """

    source  = plugin_test_dir + "Regpres_UUVVTT_differentDateoSameDatev.std"
    src_df  = fstpy.StandardFileReader(source).to_pandas()

    # compute WindChill
    df = spookipy.WindChill(src_df).compute()
    
     # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    file_to_compare = plugin_test_dir + "Regpres_diffDateoSameDatev_file2cmp.std"

    # compare results 
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
