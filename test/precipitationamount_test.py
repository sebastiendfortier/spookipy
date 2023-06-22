# -*- coding: utf-8 -*-
from json import encoder
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import pandas as pd
import spookipy
from ci_fstcomp import fstcomp
import secrets
import datetime
import numpy as np

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/PrecipitationAmount/testsFiles/'


def test_1(plugin_test_dir):
    """Tester avec une liste de fieldName invalide."""
    # open and read source
    source0 = plugin_test_dir + "18_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "12_fileSrc.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute PrecipitationAmount
    with pytest.raises(spookipy.TimeIntervalDifferenceError):
        _ = spookipy.PrecipitationAmount(src_df, nomvar=['PR','TT'], 
                                        forecast_hour_range=(datetime.timedelta(hours=12), datetime.timedelta(hours=18)), 
                                        interval=datetime.timedelta(hours=6), 
                                        step=datetime.timedelta(hours=1)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [ReaderStd --ignoreExtended --input {sources[1]}] >> 
    # [PrecipitationAmount --fieldName PR,TT --rangeForecastHour 12@18 --interval 6 --step 1] >> 
    # [Zap --pdsLabel R1558V0N] >> [WriterStd --output {destination_path} --ignoreExtended]

def test_2(plugin_test_dir):
    """Tester avec un interval 6 sur un range de 12 a 18 et a tous les sauts de 1."""
    # open and read source
    source0 = plugin_test_dir + "18_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "12_fileSrc.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute PrecipitationAmount
    df = spookipy.PrecipitationAmount(src_df, nomvar='PR', 
                                        forecast_hour_range=(datetime.timedelta(hours=12), datetime.timedelta(hours=18)), 
                                        interval=datetime.timedelta(hours=6), 
                                        step=datetime.timedelta(hours=1)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [ReaderStd --ignoreExtended --input {sources[1]}] >> 
    # [PrecipitationAmount --fieldName PR --rangeForecastHour 12@18 --interval 6 --step 1] >> 
    # [Zap --pdsLabel R1558V0N] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]
    df['etiket'] = 'R1558V0N'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "18_12_diff_file2cmp_noEncoding.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_3(plugin_test_dir):
    """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute PrecipitationAmount
    df = spookipy.PrecipitationAmount(src_df0, nomvar='PR',
                                       forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=18)),
                                                            (datetime.timedelta(hours=0), datetime.timedelta(hours=93))],
                                       interval=[datetime.timedelta(hours=3), datetime.timedelta(hours=39)],
                                       step=[datetime.timedelta(hours=3), datetime.timedelta(hours=18)]).compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
    # [PrecipitationAmount --fieldName PR --rangeForecastHour 0@18,0@93 --interval 3,39 --step 3,18] >> ', '
    # [WriterStd --output {destination_path} --ignoreExtended]']
    df.loc[df.nomvar.isin(['>>','^^']),'etiket'] = 'G133K80_N'
    df.etiket = np.where(df.label.isna(),df.etiket,df.label) #--ignoreExtended

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "global20121217_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

# Nouveau test - identique a test 3 avec encodage des IP selon les standards et moins d'intervalles demandes
def test_4(plugin_test_dir):
    """Tester avec une liste de valeurs pour rangeForecastHour, interval et step et encode selon les standards."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute PrecipitationAmount
    df = spookipy.PrecipitationAmount(src_df0, nomvar='PR',
                                       forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=93))],
                                       interval=[datetime.timedelta(hours=39)],
                                       step=[datetime.timedelta(hours=18)]).compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
    # [PrecipitationAmount --fieldName PR --rangeForecastHour 0@18,0@93 --interval 3,39 --step 3,18] >> ', '
    # [WriterStd --output {destination_path} --ignoreExtended]']
    df.loc[df.nomvar.isin(['>>','^^']),'etiket'] = 'G133K80_N'
    
    _, df['ip2'], df['ip3'] = spookipy.writerstd.vectorized_encode_ip123(df['nomvar'],
                                                                    df['ip1'],df['ip2'],df['ip3'],
                                                                    df['ip1_kind'],df['ip2_kind'],df['ip3_kind'],
                                                                    df['level'],df['ip2_dec'],df['ip3_dec'],
                                                                    df['interval'],False,True)
    df.etiket = np.where(df.label.isna(),df.etiket,df.label) #--ignoreExtended

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_4.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

# identical to 3
# def test_4(plugin_test_dir):
#     """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute PrecipitationAmount
#     df = spookipy.PrecipitationAmount(src_df0).compute()
#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
#     # [PrecipitationAmount --fieldName PR --rangeForecastHour 0:00:00@18:00:00,0:00:00@93:00:00 --interval 3,39 --step 3,18] >> ', '
#     # [WriterStd --output {destination_path} --ignoreExtended]']

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "global20121217_file2cmp.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# identical to 3
# def test_5(plugin_test_dir):
#     """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute PrecipitationAmount
#     df = spookipy.PrecipitationAmount(src_df0).compute()
#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
#     # [PrecipitationAmount --fieldName PR --rangeForecastHour 0@18,0@93 --interval 3:00:00,39:00:00 --step 3,18] >> ', '
#     # [WriterStd --output {destination_path} --ignoreExtended]']

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "global20121217_file2cmp.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# identical to 3
# def test_6(plugin_test_dir):
#     """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute PrecipitationAmount
#     df = spookipy.PrecipitationAmount(src_df0).compute()
#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
#     # [PrecipitationAmount --fieldName PR --rangeForecastHour 0@18,0@93 --interval 3,39 --step 3:00:00,18:00:00] >> ', '
#     # [WriterStd --output {destination_path} --ignoreExtended]']

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "global20121217_file2cmp.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# identical to 3
# def test_7(plugin_test_dir):
#     """Test HourMinuteSecond parameters"""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute PrecipitationAmount
#     df = spookipy.PrecipitationAmount(src_df0).compute()
#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
#     # [PrecipitationAmount --fieldName PR --rangeForecastHour 0:00:00@18:00:00,0:00:00@93:00:00 --interval 3:00:00,39:00:00 --step 3:00:00,18:00:00] >> ', '
#     # [WriterStd --output {destination_path} --ignoreExtended]']

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "global20121217_file2cmp.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

def test_8(plugin_test_dir):
    """Test HourMinuteSecond parameters step test"""
    # open and read source
    source0 = plugin_test_dir + "2020102212_023_lamwest_minimal.pres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute PrecipitationAmount
    df = spookipy.PrecipitationAmount(src_df0, nomvar='PR',
                                    forecast_hour_range=(datetime.timedelta(hours=22, minutes=30), datetime.timedelta(hours=23)),
                                       interval=datetime.timedelta(minutes=30),
                                       step=datetime.timedelta(minutes=30)).compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
    # [PrecipitationAmount --fieldName PR --rangeForecastHour 22:30:00@23:00:00 --interval 0:30:00 --step 0:30:00] >> ', '
    # [WriterStd --output {destination_path} --ignoreExtended]']
    df.etiket = np.where(df.label.isna(),df.etiket,df.label) #--ignoreExtended
    
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_8.std+20210517"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_9(plugin_test_dir):
    """Test HourMinuteSecond  - avec encodage des ip"""
    # open and read source
    source0 = plugin_test_dir + "2020102212_023_lamwest_minimal.pres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute PrecipitationAmount
    df = spookipy.PrecipitationAmount(src_df0, nomvar='PR',
                                       forecast_hour_range=(datetime.timedelta(hours=22, minutes=30), datetime.timedelta(hours=23)),
                                       interval=datetime.timedelta(minutes=30),
                                       step=datetime.timedelta(minutes=30)).compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
    # [PrecipitationAmount --fieldName PR --rangeForecastHour 22:30:00@23:00:00 --interval 0:30:00 --step 0:30:00] >> ', '
    # [WriterStd --output {destination_path} --ignoreExtended]']
    
    _, df['ip2'], df['ip3'] = spookipy.writerstd.vectorized_encode_ip123(df['nomvar'],
                                                                    df['ip1'],df['ip2'],df['ip3'],
                                                                    df['ip1_kind'],df['ip2_kind'],df['ip3_kind'],
                                                                    df['level'],df['ip2_dec'],df['ip3_dec'],
                                                                    df['interval'],False,True)
    df.etiket = np.where(df.label.isna(),df.etiket,df.label) #--ignoreExtended

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_9.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
