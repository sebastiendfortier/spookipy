# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy
from pathlib import Path

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1, pytest.mark.eps]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "ArithmeticPercentageExceedingVariableThresholdsByPoint"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """"""

    # open and read source
    sources = [
        "eta_2024020800_024_001_tt_fh2_small",
        "eta_2024020800_024_002_tt_fh2_small",
        "eta_2024020800_024_003_tt_fh2_small",
        "eta_2024020800_024_004_tt_fh2_small",
        "eta_2024020800_024_tt_fh2_small_threshold_field",  # this is the variable threshold
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    # compute spookipy.DewPointDepression
    df = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
        src_df0, threshold_operator=">=", threshold_label="_TRHD_"
    ).compute()

    df = df.loc[df.nomvar == "TT"]
    df["ip3"] = 2  # where does ip3 = 2 come from, why aren't the results 0 in epsStat????
    df["nbits"] = 16
    df["etiket"] = df["etiket"].str.replace("^__", "ER", regex=True).str.replace("X", "P", regex=False)

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "eta_2024020800_ALL_tt_fh2_small_threshold_variable"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """members and threshold don't have the same datev with threshold_sensitive_to_date_validity -> fail"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_threshold_UU_1h.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    with pytest.raises(spookipy.ArithmeticPercentageExceedingVariableThresholdsByPointError):
        _ = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
            src_df0, threshold_operator=">=", threshold_label="THRESH", threshold_sensitive_to_date_validity=True
        ).compute()


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """members and threshold don't have the same datev without threshold_sensitive_to_date_validity -> success"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_threshold_UU_1h.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    df = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
        src_df0, threshold_operator=">=", threshold_label="THRESH"
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test_3.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """members and threshold have the same datev with threshold_sensitive_to_date_validity -> success"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_threshold_UU.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    df = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
        src_df0, threshold_operator=">=", threshold_label="THRESH", threshold_sensitive_to_date_validity=True
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()  # ok

    # open and read comparison file
    file_to_compare = plugin_test_path / "test_4.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """members and threshold have the same datev without threshold_sensitive_to_date_validity -> success"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_threshold_UU.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    df = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
        src_df0, threshold_operator=">=", threshold_label="THRESH"
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()  # ok

    # open and read comparison file
    file_to_compare = plugin_test_path / "test_5.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """2 set of members and threshold with different datev with threshold_sensitive_to_date_validity -> success"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_threshold_UU.std",
        "variable_threshold_3x3_4members_UU_1h.std",
        "variable_threshold_3x3_threshold_UU_1h.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    df = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
        src_df0, threshold_operator=">=", threshold_label="THRESH", threshold_sensitive_to_date_validity=True
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test_6.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """2 set of members and threshold with different datev without threshold_sensitive_to_date_validity -> fail"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_threshold_UU.std",
        "variable_threshold_3x3_4members_UU_1h.std",
        "variable_threshold_3x3_threshold_UU_1h.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    with pytest.raises(spookipy.ArithmeticPercentageExceedingVariableThresholdsByPointError):
        _ = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
            src_df0, threshold_operator=">=", threshold_label="THRESH"
        ).compute()


def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """UU and VV members with UU and VV thresholds -> success"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_threshold_UU.std",
        "variable_threshold_3x3_4members_VV.std",
        "variable_threshold_3x3_threshold_VV.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    df = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
        src_df0, threshold_operator=">=", threshold_label="THRESH"
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()  # ok

    # open and read comparison file
    file_to_compare = plugin_test_path / "test_8.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """UU and VV members with only UU thresholds -> success (warning and only UU result)"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_threshold_UU.std",
        "variable_threshold_3x3_4members_VV.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    df = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
        src_df0, threshold_operator=">=", threshold_label="THRESH"
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()  # ok

    # open and read comparison file
    file_to_compare = plugin_test_path / "test_9.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """UU and VV members with only UU thresholds with threshold_nomvar = UU -> success"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_threshold_UU.std",
        "variable_threshold_3x3_4members_VV.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    df = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
        src_df0, threshold_operator=">=", threshold_label="THRESH", threshold_nomvar="UU"
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_10.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()  # ok

    # open and read comparison file
    file_to_compare = plugin_test_path / "test_10.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


###############################################################


def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """UU and VV members and thresholds with 2 different datev without options -> fail"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_4members_VV.std",
        "variable_threshold_3x3_4members_UU_1h.std",
        "variable_threshold_3x3_4members_VV_1h.std",
        "variable_threshold_3x3_threshold_UU.std",
        "variable_threshold_3x3_threshold_VV.std",
        "variable_threshold_3x3_threshold_UU_1h.std",
        "variable_threshold_3x3_threshold_VV_1h.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    with pytest.raises(spookipy.ArithmeticPercentageExceedingVariableThresholdsByPointError):
        _ = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
            src_df0, threshold_operator=">=", threshold_label="THRESH"
        ).compute()


def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
    """UU and VV members and thresholds with 2 different datev with threshold_sensitive_to_date_validity = True -> success"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_4members_VV.std",
        "variable_threshold_3x3_4members_UU_1h.std",
        "variable_threshold_3x3_4members_VV_1h.std",
        "variable_threshold_3x3_threshold_UU.std",
        "variable_threshold_3x3_threshold_VV.std",
        "variable_threshold_3x3_threshold_UU_1h.std",
        "variable_threshold_3x3_threshold_VV_1h.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    df = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
        src_df0, threshold_operator=">=", threshold_label="THRESH", threshold_sensitive_to_date_validity=True
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_12.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()  # ok

    # open and read comparison file
    file_to_compare = plugin_test_path / "test_12.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """UU and VV members and thresholds with 2 different datev with threshold_nomvar = UU -> fail"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_4members_VV.std",
        "variable_threshold_3x3_4members_UU_1h.std",
        "variable_threshold_3x3_4members_VV_1h.std",
        "variable_threshold_3x3_threshold_UU.std",
        "variable_threshold_3x3_threshold_VV.std",
        "variable_threshold_3x3_threshold_UU_1h.std",
        "variable_threshold_3x3_threshold_VV_1h.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    with pytest.raises(spookipy.ArithmeticPercentageExceedingVariableThresholdsByPointError):
        _ = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
            src_df0, threshold_operator=">=", threshold_label="THRESH", threshold_nomvar="UU"
        ).compute()


def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
    """UU and VV members and thresholds with 2 different datev with threshold_sensitive_to_date_validity = True and threshold_nomvar = UU -> success"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_4members_VV.std",
        "variable_threshold_3x3_4members_UU_1h.std",
        "variable_threshold_3x3_4members_VV_1h.std",
        "variable_threshold_3x3_threshold_UU.std",
        "variable_threshold_3x3_threshold_VV.std",
        "variable_threshold_3x3_threshold_UU_1h.std",
        "variable_threshold_3x3_threshold_VV_1h.std",
    ]

    # threshold devrait etre ignorer s'il a le label est identifier comme threshold

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    df = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
        src_df0,
        threshold_operator=">=",
        threshold_label="THRESH",
        threshold_sensitive_to_date_validity=True,
        threshold_nomvar="UU",
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_14.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test_14.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    """UU and VV members and thresholds with 2 different datev with threshold_nomvar = UU -> fail (no threshold found)"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_4members_VV.std",
        "variable_threshold_3x3_4members_UU_1h.std",
        "variable_threshold_3x3_4members_VV_1h.std",
        "variable_threshold_3x3_threshold_UU.std",
        "variable_threshold_3x3_threshold_VV.std",
        "variable_threshold_3x3_threshold_UU_1h.std",
        "variable_threshold_3x3_threshold_VV_1h.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    with pytest.raises(spookipy.ArithmeticPercentageExceedingVariableThresholdsByPointError):
        _ = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
            src_df0, threshold_operator=">=", threshold_label="THRESH", threshold_nomvar="TT"
        ).compute()


def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    """UU and VV members and no thresholds -> fail (no threshold)"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_4members_VV.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    with pytest.raises(spookipy.ArithmeticPercentageExceedingVariableThresholdsByPointError):
        _ = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
            src_df0, threshold_operator=">=", threshold_label="THRESH"
        ).compute()


def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    """UU and VV members and no thresholds -> fail (no result, can't match members to thresholds)"""

    # open and read source
    sources = [
        "variable_threshold_3x3_4members_UU.std",
        "variable_threshold_3x3_threshold_VV.std",
    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    with pytest.raises(spookipy.ArithmeticPercentageExceedingVariableThresholdsByPointError):
        _ = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
            src_df0, threshold_operator=">=", threshold_label="THRESH"
        ).compute()
