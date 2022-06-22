# -*- coding: utf-8 -*-
import datetime
from spookipy.utils import encode_ip2_and_ip3_time
from test import TMP_PATH, TEST_PATH
import pytest
import fstpy
import spookipy
import pandas as pd
from ci_fstcomp import fstcomp
import secrets
import rpnpy.librmn.all as rmn

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/TimeIntervalDifference/testsFiles/'


def test_1(plugin_test_dir):
    """Tester avec un interval=6 sur un range de 12 a 18 et a tous les sauts de 1."""
    # open and read source
    source0 = plugin_test_dir + "18_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "12_fileSrc.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df, nomvar='PR', 
        forecast_hour_range=(datetime.timedelta(hours=12), datetime.timedelta(hours=18)), 
        interval=datetime.timedelta(hours=6), 
        step=datetime.timedelta(hours=1)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [ReaderStd --ignoreExtended --input {sources[1]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 12@18 --interval 6 --step 1] >>
    # [Zap --doNotFlagAsZapped --nbitsForDataStorage R13] >> [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[df.nomvar=='PR', 'nbits'] = 13
    df.loc[df.nomvar=='PR', 'datyp'] = 1
    # df.loc[:,'nbits'] = 32
    # df.loc[:,'datyp'] = 5
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "18_12_diff_file2cmp_noEncoding.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)#, exclude_meta=True, cmp_number_of_fields=False)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Tester avec deux groupes d'interval."""
    # open and read source
    source0 = plugin_test_dir + "18_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "12_fileSrc.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    source2 = plugin_test_dir + "15_fileSrc.std"
    src_df2 = fstpy.StandardFileReader(source2).to_pandas()

    src_df = pd.concat([src_df0, src_df1, src_df2], ignore_index=True)
    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df, nomvar='PR',
                                       forecast_hour_range=[(datetime.timedelta(hours=15), datetime.timedelta(hours=18)),
                                                            (datetime.timedelta(hours=12), datetime.timedelta(hours=18))],
                                       interval=[datetime.timedelta(hours=3), datetime.timedelta(hours=6)],
                                       step=[datetime.timedelta(hours=1), datetime.timedelta(hours=1)]).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [ReaderStd --ignoreExtended --input {sources[1]}] >>
    # [ReaderStd --ignoreExtended --input {sources[2]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 15@18,12@18 --interval 3,6 --step 1,1] >> [WriterStd --output {destination_path} --ignoreExtended ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "18_15_12_diff_file2cmp_noEncoding.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)#, cmp_number_of_fields=False)
    fstpy.delete_file(results_file)
    assert(res)


def test_3(plugin_test_dir):
    """Tester avec un interval=6 sur un range de 6 a 12 et a tous les sauts de 1."""
    # open and read source
    source0 = plugin_test_dir + "PR2009051312_012_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "PR2009051312_006_fileSrc.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df, nomvar='PR',
                                       forecast_hour_range=(datetime.timedelta(hours=6), datetime.timedelta(hours=12)),
                                       interval=datetime.timedelta(hours=6),
                                       step=datetime.timedelta(hours=1)).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [ReaderStd --ignoreExtended --input {sources[1]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 6@12 --interval 6 --step 1] >>
    # [Zap --doNotFlagAsZapped --nbitsForDataStorage R13] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[df.nomvar=='PR', 'nbits'] = 13
    df.loc[df.nomvar=='PR', 'datyp'] = 1

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "12_06_diff_file2cmp_noEncoding.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)#, cmp_number_of_fields=False)
    fstpy.delete_file(results_file)
    assert(res)


def test_4(plugin_test_dir):
    """Tester avec un interval=6 sur un range de 12 a 18 et a tous les sauts de 1."""
    # open and read source
    source0 = plugin_test_dir + "18_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "12_fileSrc.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df, nomvar='PR',
                                       forecast_hour_range=(datetime.timedelta(hours=12), datetime.timedelta(hours=18)),
                                       interval=datetime.timedelta(hours=6),
                                       step=datetime.timedelta(hours=1)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [ReaderStd --ignoreExtended --input {sources[1]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 12@18 --interval 6 --step 1] >>
    # [Zap --doNotFlagAsZapped --nbitsForDataStorage R13] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[df.nomvar=='PR', 'nbits'] = 13
    df.loc[df.nomvar=='PR', 'datyp'] = 1

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "18_12_threshold0.02_diff_file2cmp_noEncoding.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)#, cmp_number_of_fields=False)
    fstpy.delete_file(results_file)
    assert(res)


def test_5(plugin_test_dir):
    """Tester avec un fichier qui vient de regeta."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df0, nomvar='PR',
                                       forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=177)),
                                                            (datetime.timedelta(hours=0), datetime.timedelta(hours=60))],
                                       interval=[datetime.timedelta(hours=12), datetime.timedelta(hours=3)],
                                       step=[datetime.timedelta(hours=24), datetime.timedelta(hours=6)]).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@177,0@60 --interval 12,3 --step 24,6] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "global20121217_file2cmp_noEncoding.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)#, cmp_number_of_fields=False)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir):
    """Test avec une valeur invalide pour interval."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalDifference
    with pytest.raises(spookipy.TimeIntervalDifferenceError):
        _ = spookipy.TimeIntervalDifference(src_df0, nomvar='PR',
                                          forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=177)),
                                                               (datetime.timedelta(hours=0), datetime.timedelta(hours=60))],
                                          interval=[datetime.timedelta(hours=0), datetime.timedelta(hours=3)],
                                          step=[datetime.timedelta(hours=24), datetime.timedelta(hours=6)]).compute()

    # [ReaderStd --input {sources[0]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@177,0@60 --interval 0,3 --step 24,6]


def test_7(plugin_test_dir):
    """Test avec une valeur invalide pour step."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalDifference
    with pytest.raises(spookipy.TimeIntervalDifferenceError):
        _ = spookipy.TimeIntervalDifference(src_df0, nomvar='PR',
                                          forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=177)),
                                                               (datetime.timedelta(hours=0), datetime.timedelta(hours=60))],
                                          interval=[datetime.timedelta(hours=12), datetime.timedelta(hours=3)],
                                          step=[datetime.timedelta(hours=0), datetime.timedelta(hours=6)]).compute()

    # [ReaderStd --input {sources[0]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@177,0@60 --interval 12,3 --step 0,6]


def test_8(plugin_test_dir):
    """Tester avec un fichier qui contient des champs TT et UV mais des UV qui sont a 0 et 20 dans le IP3"""
    # open and read source
    source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df0, nomvar='UV',
                                       forecast_hour_range=[(datetime.timedelta(hours=12), datetime.timedelta(hours=36)),
                                                            (datetime.timedelta(hours=12), datetime.timedelta(hours=36))],
                                       interval=[datetime.timedelta(hours=3), datetime.timedelta(hours=12)],
                                       step=[datetime.timedelta(hours=3), datetime.timedelta(hours=12)]).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [TimeIntervalDifference --fieldName UV --rangeForecastHour 12@36,12@36 --interval 3,12 --step 3,12] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)#, cmp_number_of_fields=False)
    fstpy.delete_file(results_file)
    assert(res)


def test_9(plugin_test_dir):
    """Tester avec un Interval de 0@3 et de 0@9 sur un range de 3@9 avec un interval=de 6 et un saut de 9."""
    # open and read source
    source0 = plugin_test_dir + "PR_Interval_012_0_3_fileSrc_encoded.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "PR_Interval_012_0_9_fileSrc_encoded.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df, nomvar='PR',
                                       forecast_hour_range=(datetime.timedelta(hours=3), datetime.timedelta(hours=9)),
                                       interval=datetime.timedelta(hours=6),
                                       step=datetime.timedelta(hours=9)).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [ReaderStd --ignoreExtended --input {sources[1]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 3@9 --interval 6 --step 9] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "03_09_interval_lb_file2cmp_noEncoding.std"

    # compare results
    res = fstcomp(results_file, file_to_compare) #
    fstpy.delete_file(results_file)
    assert(res)


def test_10(plugin_test_dir):
    """Tester avec un Interval de 0@9 et de 6@9 sur un range de 0@6 avec un interval=de 6 et un saut de 9."""
    # open and read source
    source0 = plugin_test_dir + "PR_Interval_012_6_9_fileSrc_encoded.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "PR_Interval_012_0_9_fileSrc_encoded.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df, nomvar='PR',
                                       forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=6)),
                                       interval=datetime.timedelta(hours=6),
                                       step=datetime.timedelta(hours=9)).compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [ReaderStd --ignoreExtended --input {sources[1]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@6 --interval 6 --step 9] >>
    # [WriterStd --output {destination_path} --ignoreExtended]']

    # df.loc[df.nomvar=='PR', 'nbits'] = 32
    # df.loc[df.nomvar=='PR', 'datyp'] = 5
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "00_06_interval_ub_diff_file2cmp_noEncoding.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/TimeIntervalDifference/result_test_10"
    # compare results
    res = fstcomp(results_file, file_to_compare) #
    fstpy.delete_file(results_file)
    assert(res)


def test_11(plugin_test_dir):
    """Tester avec deux Interval de 0@3 et 9@12 et de 0@9 et 9@18 sur un range de 3@18 avec un interval=de 6 et un saut de 9."""
    # open and read source
    source0 = plugin_test_dir + "PR_Interval_0-3_9-12_fileSrc_encoded.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "PR_Interval_0-9_9-18_fileSrc_encoded.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df, nomvar='PR',
                                       forecast_hour_range=(datetime.timedelta(hours=3), datetime.timedelta(hours=18)),
                                       interval=datetime.timedelta(hours=6),
                                       step=datetime.timedelta(hours=9)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [ReaderStd --ignoreExtended --input {sources[1]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 3@18 --interval 6 --step 9] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "03-09_12-18_intervals_lb_diff_file2cmp_noEncoding.std"

    # compare results
    res = fstcomp(results_file, file_to_compare) #
    fstpy.delete_file(results_file)
    assert(res)


def test_12(plugin_test_dir):
    """Tester avec un Interval de 0@9 et de 6@9 sur un range de 0@6 avec un interval=de 6 et un saut de 9."""
    # open and read source
    source0 = plugin_test_dir + "PR_Interval_0-9_9-18_fileSrc_encoded.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "PR_Interval_6-9_15-18_fileSrc_encoded.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df, nomvar='PR',
                                       forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=15)),
                                       interval=datetime.timedelta(hours=6),
                                       step=datetime.timedelta(hours=9)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [ReaderStd --ignoreExtended --input {sources[1]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@15 --interval 6 --step 9] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    # df.loc[df.nomvar=='PR', 'nbits'] = 32
    # df.loc[df.nomvar=='PR', 'datyp'] = 5
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "00-06_09-15_intervals_ub_diff_file2cmp_noEncoding.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/TimeIntervalDifference/result_test_12"

    # compare results
    res = fstcomp(results_file, file_to_compare) #
    fstpy.delete_file(results_file)
    assert(res)


def test_13(plugin_test_dir):
    """Tester avec un Interval de 0@9 et de 6@9 sur un range de 0@6 avec un interval=de 6 et un saut de 9 en encodant la sortie."""
    # open and read source
    source0 = plugin_test_dir + "PR_Interval_012_6_9_fileSrc_encoded.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "PR_Interval_012_0_9_fileSrc_encoded.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df, nomvar='PR',
                                       forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=6)),
                                       interval=datetime.timedelta(hours=6),
                                       step=datetime.timedelta(hours=9)).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [ReaderStd --ignoreExtended --input {sources[1]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@6 --interval 6 --step 9] >>
    # [WriterStd --output {destination_path} --ignoreExtended --encodeIP2andIP3]
    df = encode_ip2_and_ip3_time(df)
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "00_06_interval_ub_diff_file2cmp_encoded.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/TimeIntervalDifference/result_test_13"

    # compare results
    res = fstcomp(results_file, file_to_compare) #
    fstpy.delete_file(results_file)
    assert(res)


def test_14(plugin_test_dir):
    """Tester avec une valeur invalide pour forecast_hour_range=."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalDifference
    with pytest.raises(spookipy.TimeIntervalDifferenceError):
        _ = spookipy.TimeIntervalDifference(src_df0, nomvar='PR',
                                          forecast_hour_range=(datetime.timedelta(0),
                                                               datetime.timedelta(hours=200)),
                                          interval=datetime.timedelta(hours=3),
                                          step=datetime.timedelta(hours=3)).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@200 --interval 3 --step 3]


def test_15(plugin_test_dir):
    """Tester avec l'intervalle 0@9 manquant dans le fichier source."""
    # open and read source
    source0 = plugin_test_dir + "PR_exclude_interval_0A9_fileSrc_encoded.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalDifference
    with pytest.raises(spookipy.TimeIntervalDifferenceError):
        _ = spookipy.TimeIntervalDifference(src_df0, nomvar='PR',
                                          forecast_hour_range=(datetime.timedelta(hours=0),
                                                               datetime.timedelta(hours=15)),
                                          interval=datetime.timedelta(hours=3),
                                          step=datetime.timedelta(hours=3)).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@15 --interval 3 --step 3]


def test_16(plugin_test_dir):
    """Tester avec un range invalide pour --interval."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalDifference
    with pytest.raises(spookipy.TimeIntervalDifferenceError):
        _ = spookipy.TimeIntervalDifference(src_df0, nomvar='PR',
                                          forecast_hour_range=(datetime.timedelta(hours=3),
                                                               datetime.timedelta(hours=6)),
                                          interval=datetime.timedelta(hours=4),
                                          step=datetime.timedelta(hours=3)).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 3@6 --interval 4 --step 3]


def test_17(plugin_test_dir):
    """Tester avec la valeur du lower bound de --forecastHour plus grand que son upper bound."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalDifference
    with pytest.raises(spookipy.TimeIntervalDifferenceError):
        _ = spookipy.TimeIntervalDifference(src_df0, nomvar='PR',
                                          forecast_hour_range=(datetime.timedelta(hours=9),
                                                               datetime.timedelta(hours=6)),
                                          interval=datetime.timedelta(hours=3),
                                          step=datetime.timedelta(hours=3)).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [TimeIntervalDifference --fieldName PR --rangeForecastHour 9@6 --interval 3 --step 3]


# def test_18(plugin_test_dir):
#     """Tester si single thread fonctionne. Probleme potentiel avec algorithm.hpp => Segmentation fault (core dumped)"""
#     # open and read source
#     source0 = plugin_test_dir + "SN0_SN1.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalDifference
#     df = spookipy.TimeIntervalDifference(src_df0, nomvar='SN',
#                                        forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=1)),
#                                        interval=datetime.timedelta(hours=1),
#                                        step=datetime.timedelta(hours=1)).compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]}] >>
#     # [TimeIntervalDifference --fieldName SN --rangeForecastHour 0@1 --interval 1 --step 1] >>
#     # [WriterStd --output {destination_path} --ignoreExtended]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_18.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "sn0_sn1_diff_file2cmp.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare) #
#     fstpy.delete_file(results_file)
#     assert(res)


def test_19(plugin_test_dir):
    """Tester avec un fichier qui contient des champs TT et UV mais des UV qui sont a 0 et 20 dans le IP3 avec strictlyPositive switch"""
    # open and read source
    source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df0, nomvar='UV',
                                       forecast_hour_range=[(datetime.timedelta(hours=12), datetime.timedelta(hours=36)),
                                                            (datetime.timedelta(hours=12), datetime.timedelta(hours=36))],
                                       interval=[datetime.timedelta(hours=3), datetime.timedelta(hours=12)],
                                       step=[datetime.timedelta(hours=3), datetime.timedelta(hours=12)],
                                       strictly_positive=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [TimeIntervalDifference --fieldName UV --rangeForecastHour 12@36,12@36 --interval 3,12 --step 3,12 --strictlyPositive] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # df.loc[df.nomvar=='UV', 'nbits'] = 32
    # df.loc[df.nomvar=='UV', 'datyp'] = 5
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_19.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_positive_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/TimeIntervalDifference/result_test_19"

    # compare results
    res = fstcomp(results_file, file_to_compare) #
    fstpy.delete_file(results_file)
    assert(res)


def test_20(plugin_test_dir):
    """Tester avec un fichier qui contient des champs TT et UV mais des UV qui sont a 0 et 20 dans le IP3 avec strictlyPositive switch"""
    # open and read source
    source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalDifference
    df = spookipy.TimeIntervalDifference(src_df0, nomvar='UV',  # forecast_hour_range=['12:00:00@36:00:00','12:00:00@36:00:00'] , interval=[3,12] , step=[3,12] , strictlyPositive=True).compute()
                                       forecast_hour_range=[(datetime.timedelta(hours=12), datetime.timedelta(hours=36)),
                                                            (datetime.timedelta(hours=12), datetime.timedelta(hours=36))],
                                       interval=[datetime.timedelta(hours=3), datetime.timedelta(hours=12)],
                                       step=[datetime.timedelta(hours=3), datetime.timedelta(hours=12)],
                                       strictly_positive=True).compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [TimeIntervalDifference --fieldName UV --rangeForecastHour 12:00:00@36:00:00,12:00:00@36:00:00 --interval 3,12 --step 3,12 --strictlyPositive] >>
    # [WriterStd --output {destination_path} --ignoreExtended]']
    # df.loc[df.nomvar=='UV', 'nbits'] = 32
    # df.loc[df.nomvar=='UV', 'datyp'] = 5
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_20.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_positive_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/TimeIntervalDifference/result_test_20"

    # compare results
    res = fstcomp(results_file, file_to_compare) #
    fstpy.delete_file(results_file)
    assert(res)


def test_21(plugin_test_dir):
    """Tester la presence de une des 2 parametres rangeForeCastHour"""
    # open and read source
    source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalDifference
    with pytest.raises(spookipy.TimeIntervalDifferenceError):
        _ = spookipy.TimeIntervalDifference(src_df0, nomvar='UV',
                                          interval=[datetime.timedelta(hours=3), datetime.timedelta(hours=12)],
                                          step=[datetime.timedelta(hours=3), datetime.timedelta(hours=12)]).compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [TimeIntervalDifference --fieldName UV --interval 3,12 --step 3,12 --strictlyPositive] >>
    # [WriterStd --output {destination_path} --ignoreExtended]']


# def test_22(plugin_test_dir):
#     """Test interval patameter"""
#     # open and read source
#     source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #compute TimeIntervalDifference
#     df = spookipy.TimeIntervalDifference(src_df0 , nomvar='UV',
#                                        forecast_hour_range=[(datetime.timedelta(hours=12),datetime.timedelta(hours=36)),
#                                                             (datetime.timedelta(hours=12),datetime.timedelta(hours=36))],
#                                        interval=[datetime.fromisoformat('3:00:00'), datetime.fromisoformat('12:00:00')],
#                                        step=[datetime.timedelta(hours=3), datetime.timedelta(hours=12)]).compute()
#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >>
#     # [TimeIntervalDifference --fieldName UV --rangeForecastHour 12@36,12@36 --interval 3:00:00,12:00:00 --step 3,12 --strictlyPositive] >>
#     # [WriterStd --output {destination_path} --ignoreExtended]']

#     #write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_22.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_positive_file2cmp.std"

#     #compare results
#     res = fstcomp(results_file,file_to_compare) #
#     fstpy.delete_file(results_file)
#     assert(res)


# def test_23(plugin_test_dir):
#     """Test step patameter"""
#     # open and read source
#     source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #compute TimeIntervalDifference
#     df = spookipy.TimeIntervalDifference(src_df0 , nomvar='UV',
#                                        forecast_hour_range=[(datetime.timedelta(hours=12),datetime.timedelta(hours=36)),
#                                                             (datetime.timedelta(hours=12),datetime.timedelta(hours=36))],
#                                        interval=[datetime.timedelta(hours=3), datetime.timedelta(hours=12)],
#                                        step=[datetime.fromisoformat('3:00:00'), datetime.fromisoformat('12:00:00')]).compute()
#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >>
#     # [TimeIntervalDifference --fieldName UV --rangeForecastHour 12@36,12@36 --interval 3,12 --step 3:00:00,12:00:00 --strictlyPositive] >>
#     # [WriterStd --output {destination_path} --ignoreExtended]']

#     #write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_23.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_positive_file2cmp.std"

#     #compare results
#     res = fstcomp(results_file,file_to_compare) #
#     fstpy.delete_file(results_file)
#     assert(res)


# def test_24(plugin_test_dir):
#     """Test allHourMinuteSecond parameters"""
#     # open and read source
#     source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #compute TimeIntervalDifference
#     df = spookipy.TimeIntervalDifference(src_df0 , nomvar='UV',
#                                        forecast_hour_range=[(datetime.fromisoformat('12:00:00'),datetime.fromisoformat('36:00:00')),
#                                                             (datetime.fromisoformat('12:00:00'),datetime.fromisoformat('36:00:00'))],
#                                        interval=[datetime.fromisoformat('3:00:00'), datetime.fromisoformat('12:00:00')],
#                                        step=[datetime.fromisoformat('3:00:00'), datetime.fromisoformat('12:00:00')]).compute()

#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >>
#     # [TimeIntervalDifference --fieldName UV --rangeForecastHour 12:00:00@36:00:00,12:00:00@36:00:00 --interval 3:00:00,12:00:00 --step 3:00:00,12:00:00 --strictlyPositive] >>
#     # [WriterStd --output {destination_path} --ignoreExtended]']

#     #write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_24.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_positive_file2cmp.std"

#     #compare results
#     res = fstcomp(results_file,file_to_compare) #
#     fstpy.delete_file(results_file)
#     assert(res)
