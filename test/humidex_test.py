# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1, pytest.mark.humidity]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "Humidex"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidex avec un fichier d'entree normal qui a des TT,TD et SVP."""
    # open and read source
    source0 = plugin_test_path / "2016060312_024_000_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Humidex
    df = spookipy.Humidex(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [Humidex] >> [WriterStd --output {destination_path} --noMetadata]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2016060312_024_000_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.1)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidex avec un fichier d'entree HMX."""
    # open and read source
    source0 = plugin_test_path / "inputFile6x6_file2cmp.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Humidex
    df = spookipy.Humidex(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [Humidex] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "inputFile6x6_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """2 groupes de TT avec dates d'origine differentes mais dates de validity identiques"""

    source = plugin_test_path / "Regeta_TTHUES_differentDateoSameDatev.std"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    # compute Humidex
    df = spookipy.Humidex(src_df).compute()

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    file_to_compare = plugin_test_path / "Regeta_test3_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
