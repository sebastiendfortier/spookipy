# -*- coding: utf-8 -*-
from spookipy.utils import DependencyError
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import pandas as pd
import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/WindChill/testsFiles/'


def test_regtest_1(plugin_test_dir):
    """Test #1 : Calculate with a simple test data """
    # open and read source
    source0 = plugin_test_dir + "UUVVTT_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()

    uv_df = spooki.WindModulus(src_df0).compute()
    
    uv_src_df=pd.concat([src_df0,uv_df],ignore_index=True)
    #compute WindChill
    df = spooki.WindChill(uv_src_df).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindChill] >> [WriterStd --output {destination_path} --ignoreExtended]

    df['ip1']=0
    df['etiket']='WNDCHL'
    #write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windChill_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_2(plugin_test_dir):
    """Test #2 : Spooki must fail when no surface level is found """
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()
    print(src_df0[['nomvar','typvar','etiket','ni','nj','nk','dateo','d']])
    print(src_df0.nomvar.unique())

    uv_df = src_df0.query('nomvar in ["UU","VV"]').reset_index(drop=True)
    uv_df = spooki.WindModulus(uv_df).compute()
    uv_src_df=pd.concat([src_df0,uv_df],ignore_index=True)

    src_df0 = uv_src_df.query('level!=1.0').reset_index(drop=True)
    # print(src_df0[['level','surface']])

    #compute WindChill
    with pytest.raises(DependencyError):
        _ = spooki.WindChill(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 1.0 --exclude] >> [WindChill]


def test_regtest_3(plugin_test_dir):
    """Test #3 : Spooki must fail when input are in millibars"""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()

    #compute WindChill
    with pytest.raises(DependencyError):
        _ = spooki.WindChill(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>[WindChill]

