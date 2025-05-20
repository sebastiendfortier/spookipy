# -*- coding: utf-8 -*-
import pandas as pd
from test import check_test_ssm_package

check_test_ssm_package()

import rpnpy.librmn.all as rmn
import fstpy
import pytest
import spookipy
from spookipy.rmn_interface import RmnInterface

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "Calculator"


def fix_grid(df: pd.DataFrame):
    df["grtyp"] = "X"
    df["ig1"] = 0
    df["ig2"] = 0
    df["ig3"] = 0
    df["ig4"] = 0
    return df


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Multiplication de deux valeurs d'un fichier volumineux."""

    # open and read source
    source0 = plugin_test_path / "srcFile1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute
    df = spookipy.Calculator(src_df0, "ZZ*TT", unit="dam").compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    # f16
    df["nbits"] = 16
    df["datyp"] = 134

    # X grid
    df = fix_grid(df)

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "file2Comp1.std+20210929"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """6 variables impliquant plusieurs oprateurs simples (HU+HR+ES)/(VV-(TT*UU))."""

    # open and read source
    source0 = plugin_test_path / "srcFile2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute
    df = spookipy.Calculator(src_df0, "(HU+HR+ES)/(VV-(TT*UU))").compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    # R24
    df["nbits"] = 24
    df["datyp"] = 1

    # X grid
    df = fix_grid(df)

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "file2Comp2.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test de certaines fonctions typiques: abs(TT) + cos(UU) + sqrt(HU) + HR**2 + log10(ES)
    Note: comme test_3 C++ mais sans ceil(vv)
    """

    # open and read source
    source0 = plugin_test_path / "srcFile3.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute
    df = spookipy.Calculator(src_df0, "abs(TT)+cos(UU)+sqrt(HU)+HR**2.0+log10(ES)").compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    # R24
    df["nbits"] = 24
    df["datyp"] = 1

    # X grid
    df = fix_grid(df)

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "file2Comp3.std+20241210python"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un nombre élevé de variables. (Sommation des variables)"""

    # open and read source
    source0 = plugin_test_path / "srcFile4.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute
    df = spookipy.Calculator(src_df0, "TT+UU+VV+HU+HR+ES+TX+UX+VX+XR+XU+EX").compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    # R24
    df["nbits"] = 24
    df["datyp"] = 1

    # X grid
    df = fix_grid(df)

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "file2Comp4.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un outputFieldname différent et une utilisation répétée d'une même variable. ( (TT+UU+VV)/TT )"""

    # open and read source
    source0 = plugin_test_path / "srcFile2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute
    df = spookipy.Calculator(src_df0, "(TT+UU+VV)/TT", nomvar_out="TEST").compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    # R24
    df["nbits"] = 24
    df["datyp"] = 1

    # X grid
    df = fix_grid(df)

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "file2Comp5.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec une seule variable. (TT*7)"""

    # open and read source
    source0 = plugin_test_path / "srcFile2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute
    df = spookipy.Calculator(src_df0, "TT*7", nomvar_out="TT7").compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    # R24
    df["nbits"] = 24
    df["datyp"] = 1

    # X grid
    df = fix_grid(df)

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "file2Comp6.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_7(plugin_test_path):
    """Test #7 : Meme test que test_5, mais echoue parce qu'il manque un PDS
    Note: uu au lieu de UU dans l'expression."""

    # open and read source
    source0 = plugin_test_path / "srcFile2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.CalculatorError):
        _ = spookipy.Calculator(src_df0, "(TT+uu+VV)/TT").compute()


def test_8(plugin_test_path):
    """Test #7 : Meme test que test_5, mais echoue parce qu'il manque une parenthese dans l'expression"""

    # open and read source
    source0 = plugin_test_path / "srcFile2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.CalculatorError):
        _ = spookipy.Calculator(src_df0, "(TT+UU+VV/TT", nomvar_out="TEST", unit="hundredsOfFeet").compute()


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test with two grids"""

    # open and read sources
    source0 = plugin_test_path / "2020061900_024_glbpres"
    src_df0 = fstpy.StandardFileReader(source0, query='nomvar in ["UU", "VV"] & ip1 == 1015').to_pandas()
    source1 = plugin_test_path / "2020061900_024_regeta"
    src_df1 = fstpy.StandardFileReader(source1, query='nomvar in ["UU", "VV"] & ip1 == 12000').to_pandas()
    src_df = pd.safe_concat([src_df0, src_df1])

    # compute
    df = spookipy.Calculator(src_df, "sqrt(UU**2+VV**2)", nomvar_out="UV", unit="knot").compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    # f16
    df.loc[~df.nomvar.isin(["!!", "^^", ">>", "P0", "PT"]), "datyp"] = 134
    df.loc[~df.nomvar.isin(["!!", "^^", ">>", "P0", "PT"]), "nbits"] = 16

    # need to force new style
    df = spookipy.convip(df, style=RmnInterface.CONVIP_ENCODE)

    # write the result
    results_file = test_tmp_path / "test_10.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "file2Comp10.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test with ensemble"""

    # open and read sources
    source0 = plugin_test_path / "ens_2025022100_000_001"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_path / "ens_2025022100_000_002"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.safe_concat([src_df0, src_df1])

    # compute
    df = spookipy.Calculator(src_df, "UU+VV", nomvar_out="UUVV", unit="1").compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    # write the result
    results_file = test_tmp_path / "test_13.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "file2Comp13.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_add_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Additionne des champs 2D."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute
    df = spookipy.Calculator(src_df0, "UU+VV", nomvar_out="ACCU").compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    df["etiket"] = "ADDFIELDS"

    # Pour correspondre a R16
    df["nbits"] = 16
    df["datyp"] = 1

    # write the result
    results_file = test_tmp_path / "test_2d.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "add2d_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_add_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Additionne des champs 3D."""
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute
    df = spookipy.Calculator(src_df0, "TT+UU+VV", nomvar_out="ACCU").compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    df["etiket"] = "ADDFIELDS"

    # Pour correspondre a R16
    df["datyp"] = 1
    df["nbits"] = 16

    # write the result
    results_file = test_tmp_path / "test_3d.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "add3d_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_add_3(plugin_test_path):
    """Utilisation de --outputFieldName avec une valeur > 4 caractères."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.CalculatorError):
        _ = spookipy.Calculator(src_df0, "UU+VV", nomvar_out="TROPLONG").compute()


def test_add_4(plugin_test_path):
    """Essaie d'additionner mais il manque 1 champ"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.CalculatorError):
        _ = spookipy.Calculator(src_df0, "TT+UU+VV", nomvar_out="ACCU").compute()


def test_add_5(plugin_test_path):
    """Essaie d'additionner lorsqu'il y a plusieurs champs mais pas sur la même grille."""
    # open and read source
    source0 = plugin_test_path / "tt_gz_px_2grilles.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.CalculatorError):
        _ = spookipy.Calculator(src_df0, "TT+GZ", nomvar_out="ACCU").compute()


def test_add_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Additionne des champs 2D. Identique au test1 mais avec l'option copy_input"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute
    df = spookipy.Calculator(src_df0, "UU+VV", nomvar_out="ACCU", copy_input=True).compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    df.loc[df["nomvar"] == "ACCU", "etiket"] = "__ADDEPTX"

    # Pour correspondre a R16
    df["nbits"] = 16
    df["datyp"] = 1

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test9_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_add_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """Additionne des champs groupe selon le forecast hour"""
    # Test existant seulement du cote python

    # open and read source
    source0 = plugin_test_path / "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    tt_es_df = fstpy.select_with_meta(src_df0, ["TT", "ES"])

    # compute
    df = spookipy.Calculator(tt_es_df, "TT+ES", nomvar_out="ADEP").compute()

    # exit if profiling
    if test_tmp_path == None:
        return 1

    df.loc[df["nomvar"] == "ADEP", "etiket"] = "__ADDEPTX"

    # write the result
    results_file = test_tmp_path / "test_add_11.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Nouveau fichier de tests, sans zap d'etiket et de typvar.
    # open and read comparison file
    file_to_compare = plugin_test_path / "test11_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def main():
    import sys
    import conftest

    conftest.run_profiling(sys.modules[__name__], "Calculator")


if __name__ == "__main__":
    main()
