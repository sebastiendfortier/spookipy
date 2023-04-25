# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import numpy as np
import fstpy
import pytest
import spookipy
import secrets

from ci_fstcomp import fstcomp
from spookipy.applyunary.applyunary import ApplyUnaryError

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/ApplyUnary/testsFiles/'


def test_1(plugin_test_dir):
    """Test avec racine carree, avec nomvar_in et nomvar_out"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ApplyUnary
    df = spookipy.ApplyUnary(src_df0,
                             function=np.sqrt,
                             nomvar_in='UU*',
                             nomvar_out='UUSQ',
                             etiket='SQRT'
                             ).compute()


    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Test1_sqrt_file2Cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_2(plugin_test_dir):
    """Utilisation de nomvar_out avec plusieurs champs d'entree - requete invalide"""
    
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ApplyUnary
    with pytest.raises(ApplyUnaryError):
        _ = spookipy.ApplyUnary(src_df0,
                                function=np.sqrt,
                                nomvar_out='SQ',
                                etiket='SQRT'
                                ).compute()

def test_3(plugin_test_dir):
    """Test avec racine carree, plusieurs champs d'entree, sans nomvar_out """
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ApplyUnary
    df = spookipy.ApplyUnary(src_df0,
                             function=np.sqrt,
                             etiket='SQRT'
                             ).compute()

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Test3_sqrt_file2Cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
