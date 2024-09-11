# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "SetUpperBoundary"

def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """PLUSIEURS champs en entree SANS l'option --outputFieldName."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_8_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SetUpperBoundary
    df = spookipy.SetUpperBoundary(src_df0, value=5.).compute()
    # [ReaderStd --input {sources[0]}] >> [SetUpperBoundary --value 5] >>
    #  [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test1_maximum_file2cmp_20210413.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """UN seul champ en entree SANS l'option --outputFieldName."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_8_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0,['UU'])

    # compute SetUpperBoundary
    df = spookipy.SetUpperBoundary(src_df, value=0.).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> 
    # [SetUpperBoundary --value 0] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test2_maximum_file2cmp_20210413.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_3(plugin_test_path):
    """PLUSIEURS champs en entree AVEC l'option --outputFieldName. """
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_8_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SetUpperBoundary
    with pytest.raises(spookipy.SetUpperBoundaryError):
        _ = spookipy.SetUpperBoundary(src_df0, value=0., nomvar_out='TEST').compute()
    # [ReaderStd --input {sources[0]}] >> [SetUpperBoundary --value 0 --outputFieldName TEST]


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """UN seul champ en entree AVEC l'option --outputFieldName. """
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_8_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0,['UU'])

    # compute SetUpperBoundary
    df = spookipy.SetUpperBoundary(src_df, value=0., nomvar_out='TEST').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >>
    # [SetUpperBoundary --value 0 --outputFieldName TEST] >> 
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test4_maximum_file2cmp_20210413.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)
