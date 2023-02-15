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
    return TEST_PATH + '/CoriolisParameter/testsFiles/'


def test_1(plugin_test_dir):
    """Calculate with a simple test data """
    # open and read source
    source0 = plugin_test_dir + "UUVVTT_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute CoriolisParameter
    df = spookipy.CoriolisParameter(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [CoriolisParameter] >> [WriterStd --output {destination_path} ]
    df.loc[:, 'etiket'] = 'R1558V0_N'
    df.loc[df.nomvar == 'CORP', 'etiket'] = '__CORIOPX'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "coriop_file2cmp_test_1_20230124.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)  # ,e_max=0.13)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Spooki must succeed when inputs are in millibars"""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ["UU"])

    # compute CoriolisParameter
    df = spookipy.CoriolisParameter(src_df0).compute()
    
    df.loc[:, 'etiket'] = 'R1580V0_N'
    df.loc[df.nomvar == 'CORP', 'etiket'] = '__CORIOPX'
    
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "coriop_file2cmp_test_2_20230124.std"

    # compare results
    res = fstcomp(results_file, file_to_compare) 
    fstpy.delete_file(results_file)
    assert(res)
