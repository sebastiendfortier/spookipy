# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    # Dans ce cas, on utlise les fichiers de tests du repertoire du plugin Power
    return "Power"


def test_1(plugin_test_path):
    """Traitement de champs differents sur meme grille, meme forecastHour avec nomvar_out - Requete invalide"""
    # Test inexistant du cote Spooki
    # But est de tester l'utilisation de nomvar_out avec plusieurs champs sur la meme grille et meme forecastHour

    source0 = plugin_test_path / "UUVV5x5_2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.OpElementsByValueError):
        _ = spookipy.OpElementsByValue(
            src_df0,
            value=2,
            operator=np.power,
            operation_name="OpElementsByValue",
            exception_class=spookipy.OpElementsByValueError,
            nomvar_out="TOTO",
        ).compute()


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Traitement de champs differents sur des grilles differentes, avec nomvar_out"""
    # Test inexistant du cote Spooki
    # But est de tester l'utilisation de nomvar_out avec des champs sur des grilles differentes

    source = plugin_test_path / "tt_gz_px_2grilles.std"
    src_df = fstpy.StandardFileReader(source).to_pandas()
    ttgz_df = src_df.loc[src_df["nomvar"].isin(["TT", "GZ"])]

    df = spookipy.OpElementsByValue(
        ttgz_df,
        value=5,
        operator=np.add,
        operation_name="OpElementsByValue",
        exception_class=spookipy.OpElementsByValueError,
        label="OPELEM",
        nomvar_out="TOTO",
    ).compute()

    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "test2_opelembyval_py_20250220.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec une fonction power_value definie"""
    # Test inexistant du cote Spooki

    def power_value(a, v):
        return a**v

    source0 = plugin_test_path / "UUVV5x5_2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.OpElementsByValue(
        src_df0,
        value=2,
        operator=power_value,
        operation_name="OpElementsByValue",
        exception_class=spookipy.OpElementsByValueError,
    ).compute()

    # Pour fins de comparaison avec fichier original
    df.loc[:, "etiket"] = "POWER"

    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "exponent_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec la fonction power de numpy"""
    # Test inexistant du cote Spooki

    source0 = plugin_test_path / "UUVV5x5_2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.OpElementsByValue(
        src_df0,
        value=2,
        operator=np.power,
        operation_name="OpElementsByValue",
        exception_class=spookipy.OpElementsByValueError,
    ).compute()

    # Pour fins de comparaison avec fichier original
    df.loc[:, "etiket"] = "POWER"

    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "exponent_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test power des champs, sans parametre "label", pour montrer que les pdslabel sont les memes que la source."""
    # Test inexistant du cote Spooki
    # But est de montrer que l'absence de "label" fait que les label demeurent inchanges dans les champs resultants (meme que la source)

    source0 = plugin_test_path / "UUVV5x5_2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.OpElementsByValue(
        src_df0, value=2, operator=np.power, exception_class=spookipy.OpElementsByValueError
    ).compute()

    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "test5_opelembyval_py_20250220.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res
