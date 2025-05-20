# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

from spookipy.utils import VDECODE_IP2_INFO
import pandas as pd
import fstpy
import spookipy
import pytest

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "MinMaxVertically"


def test_1(plugin_test_path):
    """Invalid request -- missing mandatory fields KBAS and KTOP with bounded option"""
    # open and read source
    source0 = plugin_test_path / "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    with pytest.raises(spookipy.MinMaxVerticallyError):
        spookipy.MinMaxVertically(src_df0, nomvar="TT", min=True, bounded=True).compute()


def test_2(plugin_test_path):
    """Invalid request -- missing mandatory fields KBAS and KTOP with bounded option, on the same grid as field UU"""
    # open and read source
    source0 = plugin_test_path / "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_path / "KbasKtop_v2.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df = pd.safe_concat([src_df0, src_df1])

    # compute spookipy.MinMaxVertically
    with pytest.raises(spookipy.MinMaxVerticallyError):
        spookipy.MinMaxVertically(src_df0, nomvar="UU", bounded=True).compute()


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """7 niveaux de UU, recherche min et max"""
    source0 = plugin_test_path / "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute MinMaxVertically
    df = spookipy.MinMaxVertically(
        src_df0, nomvar="UU", max=True, min=True, nomvar_max="UMAX", nomvar_min="UMIN"
    ).compute()

    # Par defaut, les intervalles sont encodes.  On ajoute du code pour decoder
    # le ip2 pour fins de comparaison
    meta_df = df.loc[df.nomvar.isin(["^>", ">>", "^^", "!!", "!!SF"])].copy()
    simple_df = df.loc[~df.nomvar.isin(["^>", ">>", "^^", "!!", "!!SF"])].copy()
    simple_df["ip2"] = VDECODE_IP2_INFO(simple_df["nomvar"], simple_df["ip1"], simple_df["ip2"], simple_df["ip3"])

    res_df = pd.safe_concat([meta_df, simple_df])

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, res_df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "MinMaxVert_file2cmp_test3_20231016.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """3 niveaux de ICGA (sortie du plugin IcingRimeAppleman); BOUNDED, recherche MAX"""
    # open and read source
    source = plugin_test_path / "test_ICGA.std"
    # source90 = plugin_test_path / "minmax_DOWNWARD_bounded_input"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxVertically(src_df, nomvar="ICGA", bounded=True, max=True, nomvar_max="UMAX").compute()

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "MinMaxVert_file2cmp_test4_20231016.std"

    # # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec des fichiers ayant des grilles differentes mais les meme champs; recheche min et max ."""
    # Test relie au test 20 de MinMaxLevelIndex

    # open and read source
    source0 = plugin_test_path / "200906290606_TT_grid1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_path / "200906290606_TT_grid2.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.safe_concat([src_df0, src_df1])
    # compute spookipy.MinMaxLevelIndex
    df = spookipy.MinMaxVertically(src_df, nomvar="TT", nomvar_max="UMAX", nomvar_min="UMIN").compute()

    # Par defaut, les intervalles sont encodes.  On ajoute du code pour decoder
    # le ip2 pour fins de comparaison
    meta_df = df.loc[df.nomvar.isin(["^>", ">>", "^^", "!!", "!!SF"])].copy()
    simple_df = df.loc[~df.nomvar.isin(["^>", ">>", "^^", "!!", "!!SF"])].copy()
    simple_df["ip2"] = VDECODE_IP2_INFO(simple_df["nomvar"], simple_df["ip1"], simple_df["ip2"], simple_df["ip3"])

    res_df = pd.safe_concat([meta_df, simple_df])

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, res_df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "MinMaxVert_file2cmp_test5_20231016.std"

    # # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
