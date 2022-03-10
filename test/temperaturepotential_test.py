# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions, pytest.mark.humidity]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/TemperaturePotential/testsFiles/'



def test_1(plugin_test_dir):
    """ Calcule de la température potentiel à partir d'un fichier standard."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_reghyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TemperaturePotential
    df = spooki.TemperaturePotential(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [TemperaturePotential] >> [WriterStd --output {destination_path} ]

    df.loc[df.nomvar=='TH','etiket']= '__PTNLTTX'
    df.loc[df.nomvar!='TH','etiket']= 'R1580V0_N'

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
    """ Calcule de la température potentiel à partir d'un fichier standard."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_reghyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0,['TT'])

    ttk_df = fstpy.unit_convert(tt_df, to_unit_name='kelvin')
    # print(ttk_df.loc[ttk_df.nomvar=='TT'].unit.unique()[0])
    # compute TemperaturePotential
    df = spooki.TemperaturePotential(ttk_df).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> [UnitConvert --unit kelvin] >> [TemperaturePotential] >> [WriterStd --output {destination_path} ]

    df.loc[df.nomvar=='TH','etiket']= '__PTNLTTX'
    df.loc[df.nomvar!='TH','etiket']= 'R1580V0_N'

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
