# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
from pathlib import Path
import pytest
import spookipy
from spookipy.rmn_interface import RmnInterface

from datetime import datetime, timedelta

pytestmark = [pytest.mark.regressions, pytest.mark.regressions2]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "Zap"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #1 : Tester l'option --typeOfField avec une valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, type_of_field="BLABLABLA").compute()
    # [ReaderStd --input {sources[0]}] >> [Zap --typeOfField BLABLABLA]


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #2 : Tester l'option --run avec une valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, run="BLABLABLA").compute()
    # [ReaderStd --input {sources[0]}] >> [Zap --run BLABLABLA]


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #3 : Tester l'option --ensembleMember avec une valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, ensemble_member="BLABLABLA").compute()
    # [ReaderStd --input {sources[0]}] >> [Zap --ensembleMember BLABLABLA]


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #5 : Tester l'option --verticalLevel avec une valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, vertical_level=-1).compute()
    # [ReaderStd --input {sources[0]}] >> [Zap --verticalLevel -1]


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #6 : Tester l'option --verticalLevelType avec une valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, vertical_level_type="BLABLABLA").compute()
    # [ReaderStd --input {sources[0]}] >> [Zap --verticalLevelType BLABLABLA]


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #7 : Tester l'option --forecastHour avec une valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, forecast_hour=-10).compute()
    # [ReaderStd --input {sources[0]}] >> [Zap --forecastHour -10]


# Removed forecast_hour_only in the Python version
# def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test #8 : Tester l'option --forecastHourOnly avec une valeur invalide!"""
#     source0 = plugin_test_path / "zap_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     with pytest.raises(spookipy.ZapError):
#         _ = spookipy.Zap(src_df0, forecast_hour_only=-10).compute()
#     # [ReaderStd --input {sources[0]}] >> [Zap --forecastHourOnly -10]


def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #9 : Tester l'option --userDefinedIndex avec une valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, user_defined_index=-10).compute()
    # [ReaderStd --input {sources[0]}] >> [Zap --userDefinedIndex -10]


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #10 : Tester l'option --nbitsForDataStorage avec une valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, nbits_for_data_storage="i65").compute()
    # [ReaderStd --input {sources[0]}] >> [Zap --nbitsForDataStorage i65]


def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #11 : Tester l'option --unit avec une valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, unit="i65").compute()
    # [ReaderStd --input {sources[0]}] >> [Zap --unit i65]


# Removed forecast_hour_only in the Python version
# def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test #12 : Tester l'option --forecastHourOnly avec une valeur invalide!"""
#     source0 = plugin_test_path / "zap_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     with pytest.raises(spookipy.ZapError):
#         _ = spookipy.Zap(src_df0, forecast_hour_only=timedelta(hours=-10)).compute()
#     # [ReaderStd --input {sources[0]}] >> [Zap --forecastHourOnly -10:00:00]


# Removed forecast_hour_only in the Python version
# def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test #13 : Tester l'option --forecastHourOnly avec une valeur valide!"""
#     source0 = plugin_test_path / "zap_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     df = spookipy.Zap(src_df0, forecast_hour_only=timedelta(hours=11, seconds=1)).compute()
#     # [ReaderStd --input {sources[0]}] >>
#     # [Zap --forecastHourOnly 11:00:01] >>
#     # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

#     results_file = test_tmp_path / "test_13.std"
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     file_to_compare = plugin_test_path / "resulttest_13.std"

#     res = call_fstcomp(results_file, file_to_compare)
#     assert res


def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #14 : Tester l'option --forecastHour avec une valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, forecast_hour=timedelta(hours=-10)).compute()
    # [ReaderStd --input {sources[0]}] >> [Zap --forecastHour -10:00:00]


def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #15 : Tester l'option --forecastHour avec une valeur incoherente de deet et npas!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, forecast_hour=timedelta(hours=11, minutes=38)).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --forecastHour 11:38:00] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]


def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #16 : Tester l'option --forecastHour avec une valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, forecast_hour=11.633333333).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --forecastHour 11.633333333] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]


def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #17 : Tester l'option --forecastHourOnly, --timeStepNumber et --lenghtOfTimeStep avec une valeur valide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, forecast_hour_only=11.633333333, length_of_time_step=1, time_step_number=41880).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --forecastHourOnly 11.633333333 --lenghtOfTimeStep 1 --timeStepNumber 41880] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_17.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_17.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


# Removed forecast_hour_only in the Python version
# def test_18(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test #18 : Tester l'option --forecastHourOnly, --timeStepNumber et --lenghtOfTimeStep avec une valeur invalide!"""
#     source0 = plugin_test_path / "zap_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     with pytest.raises(spookipy.ZapError):
#         _ = spookipy.Zap(src_df0, forecast_hour_only=11.6, length_of_time_step=1, time_step_number=41880).compute()
#     # [ReaderStd --input {sources[0]}] >>
#     # [Zap --forecastHourOnly 11.6 --lenghtOfTimeStep 1 --timeStepNumber 41880] >>
#     # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]


# Removed forecast_hour_only in the Python version
# def test_19(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test #19 : Tester l'option --forecastHourOnly, --timeStepNumber et --lenghtOfTimeStep avec une valeur invalide!"""
#     source0 = plugin_test_path / "zap_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     with pytest.raises(spookipy.ZapError):
#         _ = spookipy.Zap(
#             src_df0, forecast_hour_only=11.633333333, length_of_time_step=2, time_step_number=41880
#         ).compute()
#     # [ReaderStd --input {sources[0]}] >>
#     # [Zap --forecastHourOnly 11.633333333 --lenghtOfTimeStep 2 --timeStepNumber 41880] >>
#     # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]


# Removed forecast_hour_only in the Python version
# def test_20(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test #20 : Tester l'option --forecastHourOnly, --timeStepNumber et --lenghtOfTimeStep avec une valeur invalide!"""
#     source0 = plugin_test_path / "zap_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     with pytest.raises(spookipy.ZapError):
#         _ = spookipy.Zap(
#             src_df0, forecast_hour_only=11.633333333, length_of_time_step=1, time_step_number=41888
#         ).compute()
#     # [ReaderStd --input {sources[0]}] >>
#     # [Zap --forecastHourOnly 11.633333333 --lenghtOfTimeStep 1 --timeStepNumber 41888] >>
#     # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]


# Removed forecast_hour_only in the Python version
# def test_21(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test #21 : Tester l'option --forecastHourOnly et --lenghtOfTimeStep avec une valeur invalide!"""
#     source0 = plugin_test_path / "zap_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     with pytest.raises(spookipy.ZapError):
#         _ = spookipy.Zap(src_df0, forecast_hour_only=11.633333333, length_of_time_step=1).compute()
#     # [ReaderStd --input {sources[0]}] >>
#     # [Zap --forecastHourOnly 11.633333333 --lenghtOfTimeStep 1] >>
#     # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]


# Removed forecast_hour_only in the Python version
# def test_22(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test #22 : Tester l'option --forecastHourOnly et --timeStepNumber avec une valeur invalide!"""
#     source0 = plugin_test_path / "zap_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     with pytest.raises(spookipy.ZapError):
#         _ = spookipy.Zap(src_df0, forecast_hour_only=11.633333333, time_step_number=41880).compute()
#     # [ReaderStd --input {sources[0]}] >>
#     # [Zap --forecastHourOnly 11.633333333 --timeStepNumber 41880] >>
#     # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]


def test_23(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #23 : Tester l'option --forecastHourOnly, --timeStepNumber et --lenghtOfTimeStep avec une valeur valide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(
        src_df0, forecast_hour_only=timedelta(hours=11, minutes=30), length_of_time_step=1, time_step_number=41400
    ).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --forecastHourOnly 11:30:00 --lenghtOfTimeStep 1 --timeStepNumber 41400] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_23.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_23.std+20250303"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_24(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #24 : Tester l'option --forecastHourOnly, --timeStepNumber et --lenghtOfTimeStep avec une valeur valide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(
        src_df0, forecast_hour_only=timedelta(hours=11, minutes=30), length_of_time_step=60, time_step_number=690
    ).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --forecastHourOnly 11:30:00 --lenghtOfTimeStep 60 --timeStepNumber 690] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_24.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_24.std+20250303"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_25(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #25 : Tester l'option --forecastHourOnly, --timeStepNumber et --lenghtOfTimeStep avec une valeur valide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(
        src_df0,
        forecast_hour_only=timedelta(hours=11, minutes=30, seconds=1),
        length_of_time_step=1,
        time_step_number=41401,
    ).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --forecastHourOnly 11:30:01 --lenghtOfTimeStep 1 --timeStepNumber 41401] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_25.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_25.std+20250303"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_26(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #26 : Tester l'option --modificationFlag, avec 2 valeurs valide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"ZAPPED": True, "BOUNDED": False}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag ZAPPED=TRUE,BOUNDED=FALSE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_26.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_26.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_27(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #27 : Tester l'option --modificationFlag, avec 1 valeur valide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"ZAPPED": True}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag ZAPPED=TRUE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_27.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_27.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_28(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #28 : Tester l'option --modificationFlag, avec 1 valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, modification_flag={"ZAPPEDS": True}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag ZAPPEDS=TRUE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]


def test_29(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #29 : Tester l'option --modificationFlag, avec 1 valeur invalide!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, modification_flag={"ZAPPED": "TRU"}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag ZAPPED=TRU] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]


def test_30(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #30 : Tester l'option --modificationFlag, avec FILTERED=TRUE!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"FILTERED": True}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag FILTERED=TRUE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_30.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_30.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_31(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #31 : Tester l'option --modificationFlag, avec INTERPOLATED=TRUE!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"INTERPOLATED": True}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag INTERPOLATED=TRUE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_31.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_31.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_32(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #32 : Tester l'option --modificationFlag, avec UNITCONVERTED=TRUE!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"UNITCONVERTED": True}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag UNITCONVERTED=TRUE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_32.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_32.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_33(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #33 : Tester l'option --modificationFlag, avec ALL_FLAGS=TRUE!"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"ALL_FLAGS": True}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag ALL_FLAGS=TRUE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_33.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_33.std+20230718"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_34(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #34 : Tester l'option --modificationFlag, avec ZAPPED!"""
    source0 = plugin_test_path / "resulttest_26.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"ZAPPED": False}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag ZAPPED=FALSE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    results_file = test_tmp_path / "test_34.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_34.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_35(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #35 : Tester l'option --modificationFlag, avec ZAPPED and FILTERED!"""
    source0 = plugin_test_path / "resulttest_30.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"ZAPPED": False, "FILTERED": False}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag ZAPPED=FALSE,FILTERED=FALSE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    results_file = test_tmp_path / "test_35.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_34.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_36(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #36 : Tester l'option --modificationFlag, avec FILTERED!"""
    source0 = plugin_test_path / "resulttest_30.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"FILTERED": False}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag FILTERED=FALSE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_36.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_34.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_37(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #37 : Tester l'option --modificationFlag, avec INTERPOLATED!"""
    source0 = plugin_test_path / "resulttest_31.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"INTERPOLATED": False}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag INTERPOLATED=FALSE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    results_file = test_tmp_path / "test_37.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_34.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_38(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #38 : Tester l'option --modificationFlag, avec UNITCONVERTED!"""
    source0 = plugin_test_path / "resulttest_32.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"UNITCONVERTED": False}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag UNITCONVERTED=FALSE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    results_file = test_tmp_path / "test_38.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_34.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


# Impossible en Python puisque le typvar restera PM entre les deux opérations
# def test_39(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test #39 : Tester l'option --modificationFlag, avec ZAP et FILTERED!"""
#     source0 = plugin_test_path / "zap_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     df = spookipy.Zap(src_df0, modification_flag={"ZAPPED": True, "FILTERED": True}).compute()

#     df = spookipy.Zap(df, modification_flag={"ZAPPED": False, "FILTERED": False}).compute()
#     # [ReaderStd --input {sources[0]}] >>
#     # [Zap --modificationFlag ZAPPED=TRUE,FILTERED=TRUE] >>
#     # [Zap --modificationFlag ZAPPED=FALSE,FILTERED=FALSE] >>
#     # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

#     df["etiket"] = "R1558V0_N"
#     results_file = test_tmp_path / "test_39.std"
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     file_to_compare = plugin_test_path / "resulttest_34.std"
#     res = call_fstcomp(results_file, file_to_compare)
#     assert res


def test_40(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #40 : Tester l'option --modificationFlag, avec ENSEMBLEEXTRAINFO!"""
    source0 = plugin_test_path / "resulttest_32.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"ALL_FLAGS": False}).compute()

    df = spookipy.Zap(df, modification_flag={"ENSEMBLEEXTRAINFO": True}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag ALL_FLAGS=FALSE] >>
    # [Zap --modificationFlag ENSEMBLEEXTRAINFO=TRUE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    results_file = test_tmp_path / "test_40.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_40.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_41(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #41 : Tester un Zap qui produit un nouveau PDS a partir de deux PDS qui ont chacun 1 seul niveau et ce niveau est different"""
    source0 = plugin_test_path / "no_sampling_vents"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Select(
        src_df0, nomvar=["UV"], forecast_hour=[timedelta(hours=7)], vertical_level=[1.0, 0.995]
    ).compute()

    df = spookipy.Zap(df, label="WE_2_1").compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName UV --forecastHour 007 --verticalLevel 1.0,0.995] >>
    # [Zap --pdsLabel WE_2_1] >>
    # [WriterStd --output {destination_path}]

    results_file = test_tmp_path / "test_41.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "result_test_41.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_42(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #42 : Tester --ensembleMember"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, ensemble_member="001", do_not_flag_as_zapped=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --ensembleMember 001 --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path}]

    df = spookipy.convip(df, style=RmnInterface.CONVIP_ENCODE)
    results_file = test_tmp_path / "test_42.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "zapensemble_file2cmp.std+20240123"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_43(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #43 : Tester --ensembleMember avec la valeur None pour supprimer le numero de membre"""
    source0 = plugin_test_path / "2013061000_012_004_ens.glbmodel"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = fstpy.select_with_meta(src_df0, ["TT"])

    df = spookipy.Zap(df, ensemble_member="", metadata_zappable=True, do_not_flag_as_zapped=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT] >>
    # [Zap --ensembleMember _NONE_ --metadataZappable --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path}]

    results_file = test_tmp_path / "test_43.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "result_test_43_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


# Removed because -tag has not been reimplemented
# def test_44(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test #44 : Tester --tag. Note: le _tag est seulement visible avec PrintIMO"""
#     source0 = plugin_test_path / "zap_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     df = spookipy.Zap(
#         src_df0,
#         tag='uv'
#     ).compute()
# [ReaderStd --input {sources[0]}] >>
# [Zap --tag uv] >>
# [PrintIMO]

# Removed because -tag has not been reimplemented
# def test_45(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test #45 : Tester --tag avec la valeur _NONE_ pour supprimer le tag. Note: le _tag est seulement visible avec PrintIMO."""
#     source0 = plugin_test_path / "zap_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     df = spookipy.Zap(
#         src_df0,
#         tag='uv'
#     ).compute()

#     df = spookipy.Zap(
#         df,
#         tag='_NONE_'
#     ).compute()
# [ReaderStd --input {sources[0]}] >>
# [Zap --tag uv] >>
# [PrintIMO] >>
# [Zap --tag _NONE_] >>
# [PrintIMO]


def test_46(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #46 : Tester l'option --typeOfField avec FORECAST_MASKED"""

    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, type_of_field="FORECAST_MASKED").compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --typeOfField FORECAST_MASKED] >>
    # [WriterStd --output {destination_path}]

    df["etiket"] = "R1558V0_N"
    df = spookipy.convip(df, style=RmnInterface.CONVIP_ENCODE)
    results_file = test_tmp_path / "test_46.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_46.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_47(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #47 : Tester l'option --modificationFlag, avec ALL_FLAGS=FALSE. Should remove M"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, modification_flag={"ZAPPED": True, "FILTERED": True}).compute()

    df = spookipy.Zap(df, modification_flag={"ALL_FLAGS": False}).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Zap --modificationFlag ZAPPED=TRUE,FILTERED=TRUE] >>
    # [Zap --modificationFlag ZAPPED=FALSE,FILTERED=FALSE] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df["etiket"] = "R1558V0_N"
    results_file = test_tmp_path / "test_47.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_34.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.0005)
    assert res


def test_48(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #48 : Tester toutes les options d'etiket simultanément"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(
        src_df0, ensemble_member="456", etiket_format="2,4,1,3,K", label="BLABLA", run="23", implementation="PARALLEL"
    ).compute()

    results_file = test_tmp_path / "test_48.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_48.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_49(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #49 : Tester etiket_format en tant que seul paramètre"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, etiket_format="0,12,0,0,K").compute()

    results_file = test_tmp_path / "test_49.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_49.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_50(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #50 : Tester etiket_format en tant que seul paramètre avec metadata_zappable"""
    source0 = plugin_test_path / "2013061000_012_004_ens.glbmodel"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = fstpy.select_with_meta(src_df0, ["TT"])

    df = spookipy.Zap(df, etiket_format="0,12,0,0,K", metadata_zappable=True).compute()

    results_file = test_tmp_path / "test_50.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_50.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_51(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #51 : Tester etiket_format avec D (discard) without metadata_zappable"""
    source0 = plugin_test_path / "2013061000_012_004_ens.glbmodel"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = fstpy.select_with_meta(src_df0, ["TT"])

    df["etiket"] = "R1BLABLX5555"
    df = spookipy.Zap(df, etiket_format="2,5,1,4,D").compute()

    results_file = test_tmp_path / "test_51.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_51.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_52(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #52 : Tester date_of_observation valide"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, date_of_observation=datetime.strptime("20250312120000", "%Y%m%d%H%M%S")).compute()

    results_file = test_tmp_path / "test_52.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_52.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_53(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #53 : Tester les options ip1 et ip2 avec metadata_zappable"""
    source0 = plugin_test_path / "2013061000_012_004_ens.glbmodel"
    df = fstpy.StandardFileReader(source0, query="nomvar == 'TT' and ip1 == 93423264").to_pandas()

    df = spookipy.Zap(
        df,
        date_of_observation=datetime.strptime("20250312120000", "%Y%m%d%H%M%S"),
        vertical_level=0.5,
        vertical_level_type="SIGMA",
        forecast_hour=timedelta(hours=11),
        length_of_time_step=60,
        time_step_number=690,
        metadata_zappable=True,
    ).compute()

    # Added a second Zap otherwise the Writer would delete !!
    df = spookipy.Zap(
        df,
        vertical_level_type="HYBRID",
        metadata_zappable=True,
    ).compute()

    results_file = test_tmp_path / "test_53.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_53.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_54(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #54 : Tester nbits_for_data_storage valide"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, nbits_for_data_storage="f32").compute()

    results_file = test_tmp_path / "test_54.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_54.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_55(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #55 : Tester nbits_for_data_storage avec un DATYP non-valide"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, nbits_for_data_storage="Y22").compute()


def test_56(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #56 : Tester unit valide"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Zap(src_df0, unit="2.687e20 m^-2").compute()

    results_file = test_tmp_path / "test_56.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "resulttest_56.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_57(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #57 : Tester unit non-valide"""
    source0 = plugin_test_path / "zap_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ZapError):
        _ = spookipy.Zap(src_df0, unit="bad").compute()
