# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/SetLowerBoundary/testsFiles/'


def test_1(plugin_test_dir):
    """PLUSIEURS champs en entree SANS l'option --outputFieldName."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SetLowerBoundary
    df = spookipy.SetLowerBoundary(src_df0, value=0.).compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SetLowerBoundary --value 0] 

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test1_minimum_file2cmp_20210413.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_2(plugin_test_dir):
    """UN seul champ en entree SANS l'option --outputFieldName."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0,['UU'])

    # compute SetLowerBoundary
    df = spookipy.SetLowerBoundary(src_df, value= 0.).compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [Select --fieldName UU] >> 
    # [SetLowerBoundary --value 0] 

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test2_minimum_file2cmp_20210413.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_3(plugin_test_dir):
    """PLUSIEURS champs en entree AVEC l'option --outputFieldName. """
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SetLowerBoundary
    with pytest.raises(spookipy.SetLowerBoundaryError):
        _ = spookipy.SetLowerBoundary(src_df0, value=0., nomvar_out='TEST').compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SetLowerBoundary --value 0 --outputFieldName TEST]

def test_4(plugin_test_dir):
    """UN seul champ en entree AVEC l'option --outputFieldName. """
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0,['UU'])

    # compute SetLowerBoundary
    df = spookipy.SetLowerBoundary(src_df, value=0., nomvar_out='TEST').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> 
    # [SetLowerBoundary --value 0 --outputFieldName TEST] >> 
    # [WriterStd --output {destination_path} --noUnitConversion ]
    # [SetLowerBoundary --value 0 --outputFieldName TEST] 

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test4_minimum_file2cmp_20210413.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_5(plugin_test_dir):
    """Valeur trop longue pour --outputFieldName. """
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0,['UU'])
    # compute SetLowerBoundary
    with pytest.raises(spookipy.SetLowerBoundaryError):
        _ = spookipy.SetLowerBoundary(src_df, value=0., nomvar_out='TROPLONG').compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [Select --fieldName UU] >> 
    # [SetLowerBoundary --value 0 --outputFieldName TROPLONG]

def test_6(plugin_test_dir):
    """Valeur trop courte pour --outputFieldName. """
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0,['UU'])
    # compute SetLowerBoundary
    with pytest.raises(spookipy.SetLowerBoundaryError):
        _ = spookipy.SetLowerBoundary(src_df, value=0., nomvar_out='T').compute() 
    # [SetLowerBoundary --value 0 --outputFieldName T]
