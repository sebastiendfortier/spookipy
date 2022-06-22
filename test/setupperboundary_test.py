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
    return TEST_PATH + '/SetUpperBoundary/testsFiles/'


def test_1(plugin_test_dir):
    """PLUSIEURS champs en entree SANS l'option --outputFieldName."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_8_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SetUpperBoundary
    df = spookipy.SetUpperBoundary(src_df0, value=5.).compute()
    # [ReaderStd --input {sources[0]}] >> [SetUpperBoundary --value 5] >> [WriterStd --output {destination_path} ]

    df['etiket'] = '__SETUPRX'
    df['typvar'] = 'PB'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test1_maximum_file2cmp_20201019.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_2(plugin_test_dir):
    """UN seul champ en entree SANS l'option --outputFieldName."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_8_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0,['UU'])

    # compute SetUpperBoundary
    df = spookipy.SetUpperBoundary(src_df, value=0.).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetUpperBoundary --value 0] >> [WriterStd --output {destination_path}]

    df['etiket'] = '__SETUPRX'
    df['typvar'] = 'PB'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test2_maximum_file2cmp_20201019.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_3(plugin_test_dir):
    """PLUSIEURS champs en entree AVEC l'option --outputFieldName. """
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_8_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SetUpperBoundary
    with pytest.raises(spookipy.SetUpperBoundaryError):
        _ = spookipy.SetUpperBoundary(src_df0, value=0., nomvar_out='TEST').compute()
    # [ReaderStd --input {sources[0]}] >> [SetUpperBoundary --value 0 --outputFieldName TEST]


def test_4(plugin_test_dir):
    """UN seul champ en entree AVEC l'option --outputFieldName. """
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_8_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0,['UU'])

    # compute SetUpperBoundary
    df = spookipy.SetUpperBoundary(src_df, value=0., nomvar_out='TEST').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetUpperBoundary --value 0 --outputFieldName TEST] >> [WriterStd --output {destination_path} --noUnitConversion]

    df['etiket'] = '__SETUPRX'
    df['typvar'] = 'PB'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test4_maximum_file2cmp_20201019.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
