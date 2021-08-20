# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki


pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/TotalTotalsIndex/testsFiles/'


def test_1(plugin_test_dir):
    """Calcul de l'indice total-total avec TT à 850 et 500 mb et ES à 850 mb."""
    # open and read source
    source0 = plugin_test_dir + "TT850_500_ES_850_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # print(src_df0[['nomvar','ip1']])
    #compute TotalTotalsIndex
    df = spooki.TotalTotalsIndex(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TotalTotalsIndex] >> [WriterStd --output {destination_path} --ignoreExtended]

    df['nbits']=32
    df['datyp']=5
    #write the result
    results_file = TMP_PATH + "test_straight_tti2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "TotalTotalsIndex_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/TotalTotalsIndex/result_test_1'

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)
