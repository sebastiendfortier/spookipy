# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy
from ci_fstcomp import fstcomp
from pathlib import Path

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1, pytest.mark.eps]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "ArithmeticPercentileByPoint"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """"""

    # open and read source
    sources = [
        "eta_2024020800_024_001_tt_fh2",
        "eta_2024020800_024_002_tt_fh2",
        "eta_2024020800_024_003_tt_fh2",
        "eta_2024020800_024_004_tt_fh2",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()
    # no_meta_df0 = src_df0.loc[src_df0.nomvar == 'TT']
    # meta_df0 = src_df0.loc[~(src_df0.nomvar == 'TT')]
    # no_meta_df0 = no_meta_df0.loc[(no_meta_df0.ip1 == 26314400)]
    # src_df0 = pd.safe_concat([meta_df0,no_meta_df0])

    src_df0 = src_df0.loc[src_df0.nomvar == "TT"]
    src_df0 = src_df0.loc[(src_df0.ip1 == 26314400)]

    # compute spookipy.DewPointDepression
    df = spookipy.ArithmeticPercentileByPoint(src_df0, [0, 10, 25, 50, 75, 90, 100]).compute()

    df["ip3"] = 2  # where does ip3 = 2 come from, why aren't the rusults 0 in epsStat????
    df["nbits"] = 16
    df["etiket"] = df["etiket"].str.replace("^__", "ER", regex=True).str.replace("X", "P", regex=False)

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "eta_2024020800_ALL_tt_fh2_percent2"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """"""

    # open and read source
    sources = [
        "2024020800_024_001",
        "2024020800_024_002",
        "2024020800_024_003",
        "2024020800_024_004",
        "2024020800_024_005",
        "2024020800_024_006",
        "2024020800_024_007",
        "2024020800_024_008",
        "2024020800_024_009",
        "2024020800_024_010",
        "2024020800_024_011",
        "2024020800_024_012",
        "2024020800_024_013",
        "2024020800_024_014",
        "2024020800_024_015",
        "2024020800_024_016",
        "2024020800_024_017",
        "2024020800_024_018",
        "2024020800_024_019",
        "2024020800_024_020",
    ]
    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ["TT"])

    no_meta_df0 = src_df0.loc[src_df0.nomvar == "TT"]
    meta_df0 = src_df0.loc[src_df0.nomvar.isin(["^^", ">>"])]  # P0 et PT are weird, why aren't they cleaned?
    no_meta_df0 = no_meta_df0.loc[(no_meta_df0.ip1 == 12000) & (no_meta_df0.ip2 == 24)]

    src_df0 = pd.safe_concat([meta_df0, no_meta_df0])

    # compute spookipy.DewPointDepression
    df = spookipy.ArithmeticPercentileByPoint(src_df0, [0, 10, 25, 32.5, 50, 75, 90]).compute()
    df.loc[df.nomvar == "TT", "nbits"] = 16
    df["etiket"] = df["etiket"].str.replace("^__", "ER", regex=True).str.replace("X", "P", regex=False)

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "ensemble_percentile_test_2_modified_v3.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.002)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """"""

    # open and read source
    sources = [
        "eta_2024020800_024_001_tt_fh2_small",
        "eta_2024020800_024_002_tt_fh2_small",
        "eta_2024020800_024_003_tt_fh2_small",
        "eta_2024020800_024_004_tt_fh2_small",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    # compute spookipy.DewPointDepression
    df = spookipy.ArithmeticPercentileByPoint(src_df0, [0, 10, 25, 50, 67.5, 100]).compute()
    df = df.loc[df.nomvar == "TT"]
    df["ip3"] = 2  # where does ip3 = 2 come from, why aren't the rusults 0 in epsStat????
    df["nbits"] = 16
    df["etiket"] = df["etiket"].str.replace("^__", "ER", regex=True).str.replace("X", "P", regex=False)

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "eta_2024020800_ALL_tt_fh2_small_percent"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_4(plugin_test_path):
    """"""

    # open and read source
    sources = [
        "eta_2024020800_024_001_tt_fh2_small",
        "eta_2024020800_024_002_tt_fh2_small",
        "eta_2024020800_024_003_tt_fh2_small",
        "eta_2024020800_024_004_tt_fh2_small",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    with pytest.raises(spookipy.ArithmeticPercentileByPointError):
        _ = spookipy.ArithmeticPercentileByPoint(src_df0, [0, 10, 25, 50, 67.5, 110]).compute()


def test_5(plugin_test_path):
    """"""

    # open and read source
    sources = [
        "eta_2024020800_024_001_tt_fh2_small",
        "eta_2024020800_024_002_tt_fh2_small",
        "eta_2024020800_024_003_tt_fh2_small",
        "eta_2024020800_024_004_tt_fh2_small",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    with pytest.raises(spookipy.ArithmeticPercentileByPointError):
        _ = spookipy.ArithmeticPercentileByPoint(src_df0, [0, -10, 25, 50, 67.5, 100]).compute()


if __name__ == "__main__":
    test_3("/home/ron000/site6/epsStat/in/eta/")
