# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions, pytest.mark.humidity]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/TemperaturePotential/testsFiles/'



def test_1(plugin_test_dir):
    """ Calcul de la température potentielle à partir d'un fichier standard."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_reghyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TemperaturePotential
    df = spookipy.TemperaturePotential(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [TemperaturePotential] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "TemperaturePotential_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_2(plugin_test_dir):
    """ Calcul de la température potentielle à partir d'un fichier standard."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_reghyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df   = fstpy.select_with_meta(src_df0,['TT'])

    ttk_df  = fstpy.unit_convert(tt_df, to_unit_name='kelvin')

    # compute TemperaturePotential
    df = spookipy.TemperaturePotential(ttk_df).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> 
    # [UnitConvert --unit kelvin] >> [TemperaturePotential] >> 
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "TemperaturePotential_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
