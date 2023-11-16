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
    return TEST_PATH + '/TotalTotalsIndex/testsFiles/'


def test_1(plugin_test_dir):
    """Calcul de l'indice total-total avec TT à 850 et 500 mb et ES à 850 mb."""
    # open and read source
    source0 = plugin_test_dir + "TT850_500_ES_850_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TotalTotalsIndex
    df = spookipy.TotalTotalsIndex(src_df0).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TotalTotalsIndex] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # Note:  Fichier de comparaison recree en 20231026 en ne tenant pas compte du ignoreExtended.

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "TotalTotalsIndex_file2cmp_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
