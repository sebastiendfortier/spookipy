# -*- coding: utf-8 -*-
from test import check_test_ssm_package
from spookipy.utils import VDECODE_IP_INFO

check_test_ssm_package()

import fstpy
import pytest
import pandas as pd
import spookipy
import datetime

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "PrecipitationAmount"


def test_1(plugin_test_path):
    """Tester avec une liste de fieldName invalide."""
    # open and read source
    source0 = plugin_test_path / "18_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_path / "12_fileSrc.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.safe_concat([src_df0, src_df1])
    # compute PrecipitationAmount
    with pytest.raises(spookipy.TimeIntervalDifferenceError):
        _ = spookipy.PrecipitationAmount(
            src_df,
            nomvar=["PR", "TT"],
            forecast_hour_range=(datetime.timedelta(hours=12), datetime.timedelta(hours=18)),
            interval=datetime.timedelta(hours=6),
            step=datetime.timedelta(hours=1),
        ).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [ReaderStd --ignoreExtended --input {sources[1]}] >>
    # [PrecipitationAmount --fieldName PR,TT --rangeForecastHour 12@18 --interval 6 --step 1] >>
    # [Zap --pdsLabel R1558V0N] >> [WriterStd --output {destination_path} --ignoreExtended]


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester avec un interval 6 sur un range de 12 a 18 et a tous les sauts de 1."""
    # open and read source
    source0 = plugin_test_path / "18_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_path / "12_fileSrc.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.safe_concat([src_df0, src_df1])
    # compute PrecipitationAmount
    df = spookipy.PrecipitationAmount(
        src_df,
        nomvar="PR",
        forecast_hour_range=(datetime.timedelta(hours=12), datetime.timedelta(hours=18)),
        interval=datetime.timedelta(hours=6),
        step=datetime.timedelta(hours=1),
    ).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [ReaderStd --ignoreExtended --input {sources[1]}] >>
    # [PrecipitationAmount --fieldName PR --rangeForecastHour 12@18 --interval 6 --step 1] >>
    # [Zap --pdsLabel R1558V0N] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # Par defaut, les intervalles sont encodes.  On ajoute du code pour les decoder
    # pour fins de comparaison
    meta_df = df.loc[df.nomvar.isin(["^>", ">>", "^^", "!!", "!!SF"])].copy()
    simple_df = df.loc[~df.nomvar.isin(["^>", ">>", "^^", "!!", "!!SF"])].copy()
    _, simple_df["ip2"], simple_df["ip3"] = VDECODE_IP_INFO(
        simple_df["nomvar"], simple_df["ip1"], simple_df["ip2"], simple_df["ip3"]
    )

    res_df = pd.safe_concat([meta_df, simple_df])

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, res_df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "18_12_diff_file2cmp_noEncoding_20231016.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
    # open and read source
    source0 = plugin_test_path / "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute PrecipitationAmount
    df = spookipy.PrecipitationAmount(
        src_df0,
        nomvar="PR",
        forecast_hour_range=[
            (datetime.timedelta(hours=0), datetime.timedelta(hours=18)),
            (datetime.timedelta(hours=0), datetime.timedelta(hours=93)),
        ],
        interval=[datetime.timedelta(hours=3), datetime.timedelta(hours=39)],
        step=[datetime.timedelta(hours=3), datetime.timedelta(hours=18)],
    ).compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [PrecipitationAmount --fieldName PR --rangeForecastHour 0@18,0@93 --interval 3,39 --step 3,18] >>

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "global20121217_file2cmp_20231016.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


# Nouveau test - identique a test 3 avec encodage des IP selon les standards et moins d'intervalles demandes
def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester avec une liste de valeurs pour rangeForecastHour, interval et step et encode selon les standards."""
    # open and read source
    source0 = plugin_test_path / "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute PrecipitationAmount
    df = spookipy.PrecipitationAmount(
        src_df0,
        nomvar="PR",
        forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=93))],
        interval=[datetime.timedelta(hours=39)],
        step=[datetime.timedelta(hours=18)],
    ).compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
    # [PrecipitationAmount --fieldName PR --rangeForecastHour 0@18,0@93 --interval 3,39 --step 3,18] >> ', '

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest4_20231016.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


# identical to 3
# def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
#     # open and read source
#     source0 = plugin_test_path / "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute PrecipitationAmount
#     df = spookipy.PrecipitationAmount(src_df0).compute()
#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
#     # [PrecipitationAmount --fieldName PR --rangeForecastHour 0:00:00@18:00:00,0:00:00@93:00:00 --interval 3,39 --step 3,18] >> ', '
#     # [WriterStd --output {destination_path} --ignoreExtended]']

#     # write the result
#     results_file = test_tmp_path / "test_4.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_path / "global20121217_file2cmp.std"

#     # compare results
#     res = call_fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# identical to 3
# def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
#     # open and read source
#     source0 = plugin_test_path / "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute PrecipitationAmount
#     df = spookipy.PrecipitationAmount(src_df0).compute()
#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
#     # [PrecipitationAmount --fieldName PR --rangeForecastHour 0@18,0@93 --interval 3:00:00,39:00:00 --step 3,18] >> ', '
#     # [WriterStd --output {destination_path} --ignoreExtended]']

#     # write the result
#     results_file = test_tmp_path / "test_5.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_path / "global20121217_file2cmp.std"

#     # compare results
#     res = call_fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# identical to 3
# def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
#     # open and read source
#     source0 = plugin_test_path / "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute PrecipitationAmount
#     df = spookipy.PrecipitationAmount(src_df0).compute()
#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
#     # [PrecipitationAmount --fieldName PR --rangeForecastHour 0@18,0@93 --interval 3,39 --step 3:00:00,18:00:00] >> ', '
#     # [WriterStd --output {destination_path} --ignoreExtended]']

#     # write the result
#     results_file = test_tmp_path / "test_6.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_path / "global20121217_file2cmp.std"

#     # compare results
#     res = call_fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# identical to 3
# def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Test HourMinuteSecond parameters"""
#     # open and read source
#     source0 = plugin_test_path / "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute PrecipitationAmount
#     df = spookipy.PrecipitationAmount(src_df0).compute()
#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
#     # [PrecipitationAmount --fieldName PR --rangeForecastHour 0:00:00@18:00:00,0:00:00@93:00:00 --interval 3:00:00,39:00:00 --step 3:00:00,18:00:00] >> ', '
#     # [WriterStd --output {destination_path} --ignoreExtended]']

#     # write the result
#     results_file = test_tmp_path / "test_7.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_path / "global20121217_file2cmp.std"

#     # compare results
#     res = call_fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)


def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test HourMinuteSecond parameters step test"""
    # open and read source
    source0 = plugin_test_path / "2020102212_023_lamwest_minimal.pres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute PrecipitationAmount
    df = spookipy.PrecipitationAmount(
        src_df0,
        nomvar="PR",
        forecast_hour_range=(datetime.timedelta(hours=22, minutes=30), datetime.timedelta(hours=23)),
        interval=datetime.timedelta(minutes=30),
        step=datetime.timedelta(minutes=30),
    ).compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
    # [PrecipitationAmount --fieldName PR --rangeForecastHour 22:30:00@23:00:00 --interval 0:30:00 --step 0:30:00] >> ', '
    # [WriterStd --output {destination_path} --ignoreExtended]']

    # Par defaut, les intervalles sont encodes.  On ajoute du code pour les decoder
    # pour fins de comparaison
    meta_df = df.loc[df.nomvar.isin(["^>", ">>", "^^", "!!", "!!SF"])].copy()
    simple_df = df.loc[~df.nomvar.isin(["^>", ">>", "^^", "!!", "!!SF"])].copy()
    _, simple_df["ip2"], simple_df["ip3"] = VDECODE_IP_INFO(
        simple_df["nomvar"], simple_df["ip1"], simple_df["ip2"], simple_df["ip3"]
    )

    res_df = pd.safe_concat([meta_df, simple_df])

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, res_df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest8_20231016.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test HourMinuteSecond  - avec encodage des ip"""
    # open and read source
    source0 = plugin_test_path / "2020102212_023_lamwest_minimal.pres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute PrecipitationAmount
    df = spookipy.PrecipitationAmount(
        src_df0,
        nomvar="PR",
        forecast_hour_range=(datetime.timedelta(hours=22, minutes=30), datetime.timedelta(hours=23)),
        interval=datetime.timedelta(minutes=30),
        step=datetime.timedelta(minutes=30),
    ).compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
    # [PrecipitationAmount --fieldName PR --rangeForecastHour 22:30:00@23:00:00 --interval 0:30:00 --step 0:30:00] >> ', '
    # [WriterStd --output {destination_path} --ignoreExtended]']

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest9_20231016.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
