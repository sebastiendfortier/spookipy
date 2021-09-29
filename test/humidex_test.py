# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.regressions, pytest.mark.humidity]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/Humidex/testsFiles/'


def test_1(plugin_test_dir):
    """Calcul de l'humidex avec un fichier d'entree normal qui a des TT,TD et SVP."""
    # open and read source
    source0 = plugin_test_dir + "2016060312_024_000_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Humidex
    df = spooki.Humidex(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [Humidex] >> [WriterStd --output {destination_path} --noMetadata]

    df.loc[:, 'etiket'] = '__HUMIDXX000'

    # df.loc[df.nomvar!='!!','nbits']=32
    # df.loc[:,'datyp']=5

    # write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2016060312_024_000_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/Humidex/result_test_1'

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Calcul de l'humidex avec un fichier d'entree HMX."""
    # open and read source
    source0 = plugin_test_dir + "inputFile6x6_file2cmp.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Humidex
    df = spooki.Humidex(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [Humidex] >> [WriterStd --output {destination_path} ]

    # df.loc[df.nomvar!='!!','nbits']=32
    # df.loc[:,'datyp']=5

    # write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "inputFile6x6_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/Humidex/result_test_2'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
