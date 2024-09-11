# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy

pytestmark = [pytest.mark.regressions]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "WindChill"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calculate with a simple test data """
    # open and read source
    source0   = plugin_test_path / "UUVVTT_fileSrc.std"
    src_df0   = fstpy.StandardFileReader(source0).to_pandas()

    uv_df     = spookipy.WindModulus(src_df0).compute()

    uv_src_df = pd.concat([src_df0, uv_df], ignore_index=True)

    # compute WindChill
    df = spookipy.WindChill(uv_src_df).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [WindChill] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "windChill_file2cmp.std+PY20240313"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_2(plugin_test_path):
    """Spooki must fail when no surface level is found """
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
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


def test_3(plugin_test_path):
    """Spooki must fail when input are in millibars"""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WindChill
    with pytest.raises(spookipy.WindChillError):
        _ = spookipy.WindChill(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>[WindChill]

def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """2 groupes de UU,VV,TT avec dates d'origine differentes mais dates de validity identiques """

    source  = plugin_test_path / "Regpres_UUVVTT_differentDateoSameDatev.std"
    src_df  = fstpy.StandardFileReader(source).to_pandas()

    # compute WindChill
    df = spookipy.WindChill(src_df).compute()
    
     # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_diffDateoSameDatev_file2cmp.std"

    # compare results 
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)
