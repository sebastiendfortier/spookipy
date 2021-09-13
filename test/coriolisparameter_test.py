# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/CoriolisParameter/testsFiles/'



def test_1(plugin_test_dir):
    """Calculate with a simple test data """
    # open and read source
    source0 = plugin_test_dir + "UUVVTT_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute CoriolisParameter
    df = spooki.CoriolisParameter(src_df0).compute()
    #[ReaderStd --input {sources[0]}] >> [CoriolisParameter] >> [WriterStd --output {destination_path} ]
    df.loc[:,'etiket'] = 'R1558V0_N'
    df.loc[df.nomvar=='CORP','ip1'] = 32505856
    df.loc[df.nomvar=='CORP','etiket'] = '__CORIOPX'

    # df.loc[:,'datyp'] = 5
    # df.loc[:,'nbits'] = 32

    #write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "coriop_file2cmp_test_1.std"
    # file_to_compare = '/home/sbf000/data/testFiles/CoriolisParameter/test_1'

    #compare results
    res = fstcomp(results_file,file_to_compare)#,e_max=0.13)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Spooki must succeed when inputs are in millibars"""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute CoriolisParameter
    df = spooki.CoriolisParameter(src_df0).compute()
    #[ReaderStd --input {sources[0]}] >>[CoriolisParameter]

    assert(not df.empty)
