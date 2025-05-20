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
    # Dans ce cas, on utlise les fichiers de tests du repertoire du plugin AddElementsByPoint
    return "AddElementsByPoint"


def test_1(plugin_test_path):
    """Essaie d'additionner des champs differents en utilisant le meme nomvar_out, avec group_by_nomvar  - Requete invalide"""
    # Test inexistant du cote Spooki
    # But est de tester l'utilisation de nomvar_out avec plusieurs champs; les champs resultants ont des nomvar et forecastHour identiques

    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.OpElementsByColumnError):
        _ = spookipy.OpElementsByColumn(
            src_df0,
            operator=np.sum,
            operation_name="OpElementsByColumn",
            exception_class=spookipy.OpElementsByColumnError,
            group_by_nomvar=True,
            nomvar_out="TOTO",
            label="OPELEM",
        ).compute()


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec des champs a differents forecastHours (TT et UU a 12Z, UU et VV  a 24Z). Additionne les valeurs des TT et UU et celles de UU et VV separement, avec meme nomvar_out = TEST."""
    # Test inexistant du cote Spooki
    # But est de tester l'utilisation de nomvar_out avec plusieurs champs resultants si ceux-ci ont des forecastHour differents

    # Creation d'un df avec TT et VV  a 12Z
    source0 = plugin_test_path / "TTUUVV_12h.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    ttvv_df = src_df0.loc[src_df0["nomvar"].isin(["TT", "VV"])]

    # Creation d'un df avec UU et VV  a 24Z
    source1 = plugin_test_path / "TTUUVV_24h.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    uuvv_df = src_df1.loc[src_df1["nomvar"].isin(["UU", "VV"])]

    src_df = pd.safe_concat([ttvv_df, uuvv_df])

    # Equivalent du plugin AddElementsByPoint
    df = spookipy.OpElementsByColumn(
        src_df,
        operator=np.sum,
        operation_name="OpElementsByColumn",
        exception_class=spookipy.OpElementsByColumnError,
        group_by_forecast_hour=True,
        group_by_level=True,
        nomvar_out="TEST",
        label="OPELEM",
    ).compute()

    # Pour creer fichier de comparaison:
    # "([ReaderStd --input TTUUVV_12h.std] >> [Select --fieldName TT,VV]) +
    # ([ReaderStd --input TTUUVV_24h.std] >> [Select --fieldName UU,VV]) >>
    # [AddElementsByPoint --plugin_language CPP --outputFieldName TEST --groupBy FORECAST_HOUR] >>
    # [Zap --pdsLabel OPELEM --doNotFlagAsZapped] >>
    # [WriterStd --output Test2.std --noMetadata]"

    df.sort_values(by=["nomvar", "level"], ascending=[True, False], inplace=True)

    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test2_opelembycols_py_20250217.std"

    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test l'addition des champs, sans parametre "label", pour montrer que les pdslabel sont les memes que la source."""
    # Test inexistant du cote Spooki
    # But est de montrer que l'absence de "label" fait que les label demeurent inchanges dans les champs resultants (meme que la source)

    # Creation d'un df avec TT et VV  a 12Z
    source0 = plugin_test_path / "TTUUVV_12h.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    ttvv_df = src_df0.loc[src_df0["nomvar"].isin(["TT", "VV"])]

    # Creation d'un df avec UU et VV  a 24Z
    source1 = plugin_test_path / "TTUUVV_24h.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    uuvv_df = src_df1.loc[src_df1["nomvar"].isin(["UU", "VV"])]

    src_df = pd.safe_concat([ttvv_df, uuvv_df])

    # Equivalent du plugin AddElementsByPoint
    df = spookipy.OpElementsByColumn(
        src_df,
        operator=np.sum,
        operation_name="OpElementsByColumn",
        exception_class=spookipy.OpElementsByColumnError,
        group_by_forecast_hour=True,
        group_by_level=True,
    ).compute()

    df.sort_values(by=["nomvar", "level"], ascending=[True, False], inplace=True)

    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test3_opelembycols_py_20250217.std"

    res = call_fstcomp(results_file, file_to_compare)
    assert res
