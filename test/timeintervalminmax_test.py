# -*- coding: utf-8 -*-
import datetime
from spookipy.timeintervalminmax.timeintervalminmax import TimeIntervalMinMaxError
from spookipy.utils import adjust_ip3_time_interval, encode_ip2_and_ip3_time
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
    return TEST_PATH + '/TimeIntervalMinMax/testsFiles/'


def test_1(plugin_test_dir):
    """Tester sans la cle obligatoire FIELDNAME."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    with pytest.raises(TimeIntervalMinMaxError):
        df = spookipy.TimeIntervalMinMax(src_df0, max=True,
            forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=177)), 
            interval=datetime.timedelta(hours=12), 
            step=datetime.timedelta(hours=24),
            nomvar_min='PRX').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TimeIntervalMinMax --type MAX --rangeForecastHour 0@177 --interval 12 --step 24 --outputFieldNameMin PRX]


# not tested, has defaults for min and max
# def test_2(plugin_test_dir):
#     """Tester sans la cle obligatoire type."""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalMinMax
#     df = spookipy.TimeIntervalMinMax(src_df0,
#         forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=177)), 
#         interval=datetime.timedelta(hours=12), 
#         step=datetime.timedelta(hours=24),
#         nomvar_min='PRX').compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
#     # [TimeIntervalMinMax --fieldName PR --rangeForecastHour 0@177 --interval 12 --step 24 --outputFieldNameMin PRX]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "nan"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

def test_3(plugin_test_dir):
    """Tester sans la cle obligatoire rangeForecastHour."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    with pytest.raises(TimeIntervalMinMaxError):
        df = spookipy.TimeIntervalMinMax(src_df0,
            interval=datetime.timedelta(hours=12), 
            step=datetime.timedelta(hours=24),
            nomvar_min='PRX').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --step 24 --outputFieldNameMin PRX]



# not tested, has defaults for seting min and max to True
# def test_4(plugin_test_dir):
#     """Tester avec le type TYPE en majuscule."""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalMinMax
#     df = spookipy.TimeIntervalMinMax(src_df0,
#         forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=177)), 
#         interval=datetime.timedelta(hours=12), 
#         step=datetime.timedelta(hours=24),
#         nomvar_min='PRX').compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
#     # [TimeIntervalMinMax --fieldName PR --TYPE MIN --interval 12 --step 24 --outputFieldNameMin PRX] >> 
#     # [WriterStd --output {destination_path} --ignoreExtended]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "nan"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

def test_5(plugin_test_dir):
    """Tester avec un interval à zero"""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    with pytest.raises(TimeIntervalMinMaxError):
        df = spookipy.TimeIntervalMinMax(src_df0, 
            nomvar='PR', 
            min=True,
            forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=177)), 
            interval=datetime.timedelta(hours=0), 
            step=datetime.timedelta(hours=24),
            nomvar_min='PRX').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TimeIntervalMinMax --fieldName PR --type MIN --interval 0 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX]


def test_6(plugin_test_dir):
    """Tester avec un step a zero."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    with pytest.raises(TimeIntervalMinMaxError):
        df = spookipy.TimeIntervalMinMax(src_df0,
            nomvar='PR',
            min=True,
            forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=177)), 
            interval=datetime.timedelta(hours=12), 
            step=datetime.timedelta(hours=0),
            nomvar_min='PRX').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --rangeForecastHour 0@177 --step 0 --outputFieldNameMin PRX]


# not tested , has a default for out nomvars
# def test_7(plugin_test_dir):
#     """Tester avec type max avec une sortie min."""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalMinMax
#     df = spookipy.TimeIntervalMinMax(src_df0,
#         nomvar='PR',
#         max=True,
#         forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=177)), 
#         interval=datetime.timedelta(hours=12), 
#         step=datetime.timedelta(hours=24),
#         nomvar_min='PRX').compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
#     # [TimeIntervalMinMax --fieldName PR --type MAX --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "nan"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# not tested, has defaults
# def test_8(plugin_test_dir):
#     """Tester avec step max et une sortie min."""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalMinMax
#     df = spookipy.TimeIntervalMinMax(src_df0,
#         nomvar='PR',
#         max=True,
#         ).compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
#     # [TimeIntervalMinMax --fieldName PR --type MAX --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "nan"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# should not test writer here
# def test_9(plugin_test_dir):
#     """Tester l'option --output avec un path qui n'existe pas!"""
#     # open and read source
#     source0 = plugin_test_dir + "inputFile.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalMinMax
#     df = spookipy.TimeIntervalMinMax(src_df0).compute()
#     # [ReaderStd --input {sources[0]}] >> 
#     # [TimeIntervalMinMax --fieldName PR --type MAX --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMax PRX] >>
#     # [WriterStd --output /tmp//totonSZBK2/toto.std]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "nan"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# not tested , has defaults
# def test_10(plugin_test_dir):
#     """Tester avec type MAX et outputfieldNameMIN, c'est pas bon."""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalMinMax
#     df = spookipy.TimeIntervalMinMax(src_df0).compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
#     # [TimeIntervalMinMax --fieldName PR --type MAX --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "nan"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# not tested, has defaults
# def test_11(plugin_test_dir):
#     """Tester avec type MIN et outputfieldNameMAX c'est pas bon."""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalMinMax
#     df = spookipy.TimeIntervalMinMax(src_df0).compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
#     # [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMax PRX]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "nan"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# not tested, invalid param automatically rejected
# def test_12(plugin_test_dir):
#     """Tester avec type MINI, le type mini existe pas."""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalMinMax
#     df = spookipy.TimeIntervalMinMax(src_df0).compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
#     # [TimeIntervalMinMax --fieldName PR --type MINI --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMax PRX]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "nan"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

def test_13(plugin_test_dir):
    """Tester avec un rangeForecastHour invalide"""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    with pytest.raises(TimeIntervalMinMaxError):
        df = spookipy.TimeIntervalMinMax(src_df0,
            nomvar='PR',
            max=True,
            forecast_hour_range=(datetime.timedelta(hours=-1)), 
            interval=datetime.timedelta(hours=12), 
            step=datetime.timedelta(hours=0),
            nomvar_max='PRX').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TimeIntervalMinMax --fieldName PR --type MAX --interval 12 --rangeForecastHour -1 --step 24 --outputFieldNameMax PRX]


def test_14(plugin_test_dir):
    """Tester avec deux intervales à la place d'un seul."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    with pytest.raises(TimeIntervalMinMaxError):
        df = spookipy.TimeIntervalMinMax(src_df0,
            nomvar='PR',
            min=True,
            forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=177)), 
            interval=[datetime.timedelta(hours=12),datetime.timedelta(hours=10)], 
            step=datetime.timedelta(hours=0),
            nomvar_min='PRX').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TimeIntervalMinMax --fieldName PR --type MIN --interval 12,10 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX]


def test_15(plugin_test_dir):
    """Tester avec un interval qui depasse le rangeForecastHour."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    with pytest.raises(TimeIntervalMinMaxError):
        df = spookipy.TimeIntervalMinMax(src_df0,
            nomvar='PR',
            min=True,
            forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=177)),(datetime.timedelta(hours=50), datetime.timedelta(hours=58))], 
            interval=datetime.timedelta(hours=12), 
            step=datetime.timedelta(hours=24),
            nomvar_min='PRX').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --rangeForecastHour 0@177,50@58 --step 24 --outputFieldNameMin PRX]


def test_16(plugin_test_dir):
    """Tester avec deux steps à la place d'un seul."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    with pytest.raises(TimeIntervalMinMaxError):
        df = spookipy.TimeIntervalMinMax(src_df0,
            nomvar='PR',
            min=True,
            forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=177)), 
            interval=datetime.timedelta(hours=12), 
            step=[datetime.timedelta(hours=24),datetime.timedelta(hours=15)],
            nomvar_min='PRX').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --rangeForecastHour 0@177 --step 24,15 --outputFieldNameMin PRX]



def test_17(plugin_test_dir):
    """Tester avec 2 outputfieldNameMin mais un seul fieldName."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    with pytest.raises(TimeIntervalMinMaxError):
        df = spookipy.TimeIntervalMinMax(src_df0,
            nomvar='PR',
            min=True,
            forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=177)), 
            interval=datetime.timedelta(hours=12), 
            step=datetime.timedelta(hours=24),
            nomvar_min=['PRX','PRZ']).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX,PRZ]


def test_18(plugin_test_dir):
    """Tester avec 2 steps  mais un seul fieldName."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    with pytest.raises(TimeIntervalMinMaxError):
        df = spookipy.TimeIntervalMinMax(src_df0,
            nomvar='PR',
            min=True,
            forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=177)), 
            interval=datetime.timedelta(hours=12), 
            step=[datetime.timedelta(hours=24),datetime.timedelta(hours=15)],
            nomvar_min='PRX').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TimeIntervalMinMax --fieldName PR --type BOTH --interval 12 --rangeForecastHour 0@177 --step 24,15 --outputFieldNameMin PRX]


def test_19(plugin_test_dir):
    """Tester avec 2 outputFieldNameMax mais 1 seul fieldName."""
    # open and read source
    source0 = plugin_test_dir + "global20121217_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    with pytest.raises(TimeIntervalMinMaxError):
        df = spookipy.TimeIntervalMinMax(src_df0,
            nomvar='PR',
            min=True,
            max=True,
            forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=177)), 
            interval=datetime.timedelta(hours=12), 
            step=datetime.timedelta(hours=24),
            nomvar_min='PRX',
            nomvar_max=['PRX','PRZ']).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TimeIntervalMinMax --fieldName PR --type BOTH --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX --outputFieldNameMax PRX,PRZ]

# same as test_19
# def test_20(plugin_test_dir):
#     """Tester avec 1 fieldName PR et 2 outputFieldNameMin PRX,PRZ mais un seul outputFieldNameMax."""
#     # open and read source
#     source0 = plugin_test_dir + "global20121217_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalMinMax
#     df = spookipy.TimeIntervalMinMax(src_df0).compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
#     # [TimeIntervalMinMax --fieldName PR --type BOTH --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX,PRZ --outputFieldNameMax PRX]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_20.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "nan"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

def test_21(plugin_test_dir):
    """ Calcul d'un test min avec un fieldName TT et 2 rangeForecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TT_Interval_3_168_160_150_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar='TT',
        min=True,
        forecast_hour_range=[(datetime.timedelta(hours=160), datetime.timedelta(hours=168)),(datetime.timedelta(hours=150), datetime.timedelta(hours=160))], 
        interval=[datetime.timedelta(hours=3),datetime.timedelta(hours=3)], 
        step=[datetime.timedelta(hours=2),datetime.timedelta(hours=2)]).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type MIN --rangeForecastHour 160@168,150@160 --fieldName TT --interval 3,3 --step 2,2] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('V[0-9]+M.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)
    # print(df)
    
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_21.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "TT_Interval_3_168_160_150_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_22(plugin_test_dir):
    """ Calcul d'un test MIN avec 2 fieldNames TT,HU et 2 rangeForecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TT_HU_Interval_3_168_160_24_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar=['TT','HU'],
        min=True,
        forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=24)),(datetime.timedelta(hours=160), datetime.timedelta(hours=168))], 
        interval=[datetime.timedelta(hours=3),datetime.timedelta(hours=3)], 
        step=[datetime.timedelta(hours=2),datetime.timedelta(hours=2)]).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type MIN --rangeForecastHour 0@24,160@168 --fieldName TT,HU --interval 3,3 --step 2,2] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('V[0-9]+M.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_22.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "TT_HU_Interval_3_168_160_24_0_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_23(plugin_test_dir):
    """ Calcul d'un test MAX avec 2 fieldNames TT,GZ et 2 rangeForecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TT_GZ_Interval_3_80_56_20_0_diff_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar=['TT','GZ'],
        min=True,
        forecast_hour_range=[(datetime.timedelta(hours=56), datetime.timedelta(hours=80)),(datetime.timedelta(hours=0), datetime.timedelta(hours=20))], 
        interval=[datetime.timedelta(hours=3),datetime.timedelta(hours=3)], 
        step=[datetime.timedelta(hours=2),datetime.timedelta(hours=2)]).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type MIN --rangeForecastHour 56@80,0@20 --fieldName TT,GZ --interval 3,3 --step 2,2] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('V[0-9]+M.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)
    
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_23.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "TT_GZ_Interval_3_80_56_20_0_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_24(plugin_test_dir):
    """ Calcul d'un test MAX  avec 2 fieldNames HU,GZ et 2 rangeForecastHours."""
    # open and read source
    source0 = plugin_test_dir + "HU_GZ_Interval_4_144_168_20_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar=['HU','GZ'],
        max=True,
        forecast_hour_range=[(datetime.timedelta(hours=144), datetime.timedelta(hours=168)),(datetime.timedelta(hours=0), datetime.timedelta(hours=20))], 
        interval=[datetime.timedelta(hours=4),datetime.timedelta(hours=4)], 
        step=[datetime.timedelta(hours=5),datetime.timedelta(hours=5)]).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type MAX --rangeForecastHour 144@168,0@20 --fieldName HU,GZ --interval 4,4 --step 5,5] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('V[0-9]+M.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)


    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_24.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "HU_GZ_Interval_4_144_168_20_0_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_25(plugin_test_dir):
    """ Calcul d'un test MAX avec 1 fieldName TT et 3 rangeForecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TT_Interval_2_3_4_160_150_140_20_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar='TT',
        max=True,
        forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=20)),(datetime.timedelta(hours=140), datetime.timedelta(hours=150)),(datetime.timedelta(hours=150), datetime.timedelta(hours=160))], 
        interval=[datetime.timedelta(hours=2),datetime.timedelta(hours=3),datetime.timedelta(hours=4)], 
        step=[datetime.timedelta(hours=2),datetime.timedelta(hours=2),datetime.timedelta(hours=2)]).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type MAX --rangeForecastHour 0@20,140@150,150@160 --fieldName TT --interval 2,3,4 --step 2,2,2] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('V[0-9]+M.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_25.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "TT_Interval_2_3_4_160_150_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_26(plugin_test_dir):
    """ Calcul d'un test MAX avec 3 fieldNames et 1 rangeForecastHour."""
    # open and read source
    source0 = plugin_test_dir + "TT_HU_GZ_Interval_2_30_0_diff_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar=['TT','HU','GZ'],
        max=True,
        forecast_hour_range=(datetime.timedelta(hours=0), datetime.timedelta(hours=30)), 
        interval=datetime.timedelta(hours=2), 
        step=datetime.timedelta(hours=2)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type MAX --rangeForecastHour 0@30 --fieldName TT,HU,GZ --interval 2 --step 2] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]
    df.loc[df.nomvar.str.match('V[0-9]+M.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_26.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "TT_HU_GZ_Interval_2_30_0_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_27(plugin_test_dir):
    """ Calcul d'un test BOTH avec 2 fieldNames , 2 rangeForecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TT_HU_Interval_3_168_160_20_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar=['TT','HU'],
        min=True,
        max=True,
        forecast_hour_range=[(datetime.timedelta(hours=160), datetime.timedelta(hours=168)),(datetime.timedelta(hours=0), datetime.timedelta(hours=20))], 
        interval=[datetime.timedelta(hours=3),datetime.timedelta(hours=3)], 
        step=[datetime.timedelta(hours=3),datetime.timedelta(hours=3)]).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type BOTH --rangeForecastHour 160@168,0@20 --fieldName TT,HU --interval 3,3 --step 3,3] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('V[0-9]+M.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)
    

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_27.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "TT_HU_Interval_3_168_160_20_0_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_28(plugin_test_dir):
    """ Calcul d'un test BOTH avec 1 fieldNames , 3 rangeForecastHours"""
    # open and read source
    source0 = plugin_test_dir + "TT_168_160_140_20_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar='TT',
        min=True,
        max=True,
        forecast_hour_range=[(datetime.timedelta(hours=160), datetime.timedelta(hours=168)),(datetime.timedelta(hours=140), datetime.timedelta(hours=160)),(datetime.timedelta(hours=0), datetime.timedelta(hours=20))], 
        interval=[datetime.timedelta(hours=2),datetime.timedelta(hours=3),datetime.timedelta(hours=4)], 
        step=[datetime.timedelta(hours=1),datetime.timedelta(hours=2),datetime.timedelta(hours=3)]).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type BOTH --rangeForecastHour 160@168,140@160,0@20 --fieldName TT --interval 2,3,4 --step 1,2,3] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('V[0-9]+M.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_28.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "TT_Interval_2_3_4_168_160_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_29(plugin_test_dir):
    """ Calcul d'un test BOTH avec 3 fieldNames , 3 rangeForecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TT_HU_GZ_168_160_140_20_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar=['TT','HU','GZ'],
        min=True,
        max=True,
        forecast_hour_range=[(datetime.timedelta(hours=160), datetime.timedelta(hours=168)),(datetime.timedelta(hours=140), datetime.timedelta(hours=160)),(datetime.timedelta(hours=0), datetime.timedelta(hours=20))], 
        interval=[datetime.timedelta(hours=2),datetime.timedelta(hours=3),datetime.timedelta(hours=4)], 
        step=[datetime.timedelta(hours=1),datetime.timedelta(hours=2),datetime.timedelta(hours=3)]).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type BOTH --rangeForecastHour 160@168,140@160,0@20 --fieldName TT,HU,GZ --interval 2,3,4 --step 1,2,3] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('V[0-9]+M.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_29.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "TT_HU_GZ_Interval_2_3_4_168_160_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_30(plugin_test_dir):
    """ Calcul d'un test MIN avec 1 fieldName sans interval."""
    # open and read source
    source0 = plugin_test_dir + "TT_168_160_140_20_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar='TT',
        min=True,
        forecast_hour_range=[
            (datetime.timedelta(hours=160), datetime.timedelta(hours=168)),
            (datetime.timedelta(hours=140), datetime.timedelta(hours=160)),
            (datetime.timedelta(hours=0), datetime.timedelta(hours=20))], 
        ).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type MIN --rangeForecastHour 160@168,140@160,0@20 --fieldName TT] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('V[0-9]+M.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_30.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "min_TT_Interval_not_set_160_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

# same as test_30
# def test_31(plugin_test_dir):
#     """ Calcul d'un test MAX avec 1 fieldName sans interval."""
#     # open and read source
#     source0 = plugin_test_dir + "TT_168_160_140_20_0_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalMinMax
#     df = spookipy.TimeIntervalMinMax(src_df0).compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
#     # [TimeIntervalMinMax --type MAX --rangeForecastHour 160@168,140@160,0@20 --fieldName TT] >> 
#     # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_31.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + \
#         "max_TT_Interval_not_set_160_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

# same as test_30
# def test_32(plugin_test_dir):
#     """ Calcul d'un test BOTH avec 1 fieldName sans interval."""
#     # open and read source
#     source0 = plugin_test_dir + "TT_168_160_140_20_0_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # compute TimeIntervalMinMax
#     df = spookipy.TimeIntervalMinMax(src_df0).compute()
#     # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
#     # [TimeIntervalMinMax --type BOTH --rangeForecastHour 160@168,140@160,0@20 --fieldName TT] >> 
#     # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_32.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + \
#         "both_TT_Interval_not_set_160_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)

def test_33(plugin_test_dir):
    """ Calcul d'un test MIN avec 3 fieldName avec interval sans step."""
    # open and read source
    source0 = plugin_test_dir + "TT_125_100_75_50_25_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar='TT',
        min=True,
        forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=25)),(datetime.timedelta(hours=50), datetime.timedelta(hours=75)),(datetime.timedelta(hours=100), datetime.timedelta(hours=125))], 
        interval=[datetime.timedelta(hours=3), datetime.timedelta(hours=4), datetime.timedelta(hours=5)],
        nomvar_min='TTMN').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type MIN --rangeForecastHour 0@25,50@75,100@125 --fieldName TT --interval 3,4,5 --outputFieldNameMin TTMN] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('TTM.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_33.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "min_TT_Interval_3_4_5_125_100_75_50_25_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_34(plugin_test_dir):
    """ Calcul d'un test MAX avec 3 fieldName avec interval sans step."""
    # open and read source
    source0 = plugin_test_dir + "TT_125_100_75_50_25_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar='TT',
        max=True,
        forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=25)),(datetime.timedelta(hours=50), datetime.timedelta(hours=75)),(datetime.timedelta(hours=100), datetime.timedelta(hours=125))], 
        interval=[datetime.timedelta(hours=3),datetime.timedelta(hours=4),datetime.timedelta(hours=5)],
        nomvar_max='TTMX').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type MAX --rangeForecastHour 0@25,50@75,100@125 --fieldName TT --interval 3,4,5 --outputFieldNameMax TTMX] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('TTM.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_34.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "max_TT_Interval_3_4_5_125_100_75_50_25_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_35(plugin_test_dir):
    """ Calcul d'un test BOTH avec 3 fieldName avec interval sans step."""
    # open and read source
    source0 = plugin_test_dir + "TT_125_100_75_50_25_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar='TT',
        min=True,
        max=True,
        forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=25)),(datetime.timedelta(hours=50), datetime.timedelta(hours=75)),(datetime.timedelta(hours=100), datetime.timedelta(hours=125))], 
        interval=[datetime.timedelta(hours=3),datetime.timedelta(hours=4),datetime.timedelta(hours=5)],
        nomvar_min='TTMN',
        nomvar_max='TTMX').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} ] >> 
    # [TimeIntervalMinMax --type BOTH --rangeForecastHour 0@25,50@75,100@125 --fieldName TT --interval 3,4,5 --outputFieldNameMax TTMX --outputFieldNameMin TTMN ] >> 
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

    df.loc[df.nomvar.str.match('TTM.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_35.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "both_TT_Interval_3_4_5_125_100_75_50_25_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_36(plugin_test_dir):
    """ Calcul d'un test BOTH avec 1 fieldName avec interval sans step. rangeForecastHour"""
    # open and read source
    source0 = plugin_test_dir + "TT_125_100_75_50_25_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar='TT',
        min=True,
        max=True,
        forecast_hour_range=[(datetime.timedelta(hours=0,minutes=0,seconds=0), datetime.timedelta(hours=25,minutes=0,seconds=0)),(datetime.timedelta(hours=50,minutes=0,seconds=0), datetime.timedelta(hours=75,minutes=0,seconds=0)),(datetime.timedelta(hours=100,minutes=0,seconds=0), datetime.timedelta(hours=125,minutes=0,seconds=0))], 
        interval=[datetime.timedelta(hours=3),datetime.timedelta(hours=4),datetime.timedelta(hours=5)],
        nomvar_min='TTMN',
        nomvar_max='TTMX').compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]} ] >> ', '
    # [TimeIntervalMinMax --type BOTH --rangeForecastHour 0:00:00@25:00:00,50:00:00@75:00:00,100:00:00@125:00:00 --fieldName TT --interval 3,4,5 --outputFieldNameMax TTMX --outputFieldNameMin TTMN ] >> ', '
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]']
    df.loc[df.nomvar.str.match('TTM.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_36.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "both_TT_Interval_3_4_5_125_100_75_50_25_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_37(plugin_test_dir):
    """ Calcul d'un test MAX avec 1 fieldName avec interval sans step."""
    # open and read source
    source0 = plugin_test_dir + "TT_125_100_75_50_25_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar='TT',
        max=True,
        forecast_hour_range=[(datetime.timedelta(hours=0), datetime.timedelta(hours=25)),(datetime.timedelta(hours=50), datetime.timedelta(hours=75)),(datetime.timedelta(hours=100), datetime.timedelta(hours=125))], 
        interval=[datetime.timedelta(hours=3,minutes=0,seconds=0),datetime.timedelta(hours=4,minutes=0,seconds=0),datetime.timedelta(hours=5,minutes=0,seconds=0)],
        nomvar_max='TTMX').compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]} ] >> ', '
    # [TimeIntervalMinMax --type MAX --rangeForecastHour 0@25,50@75,100@125 --fieldName TT --interval 3:00:00,4:00:00,5:00:00 --outputFieldNameMax TTMX] >> ', '
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]']

    df.loc[df.nomvar.str.match('TTM.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_35.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "max_TT_Interval_3_4_5_125_100_75_50_25_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_38(plugin_test_dir):
    """ Calcul d'un test min avec un fieldName TT et 2 rangeForecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TT_Interval_3_168_160_150_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TimeIntervalMinMax
    df = spookipy.TimeIntervalMinMax(src_df0,
        nomvar='TT',
        min=True,
        forecast_hour_range=[(datetime.timedelta(hours=160), datetime.timedelta(hours=168)),(datetime.timedelta(hours=150), datetime.timedelta(hours=160))], 
        interval=[datetime.timedelta(hours=3),datetime.timedelta(hours=3)],
        step=[datetime.timedelta(hours=2,minutes=0,seconds=0),datetime.timedelta(hours=2,minutes=0,seconds=0)]).compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]} ] >> ', '
    # [TimeIntervalMinMax --type MIN --rangeForecastHour 160@168,150@160 --fieldName TT --interval 3,3 --step 2:00:00,2:00:00] >> ', '
    # [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]']

    df.loc[df.nomvar.str.match('V[0-9]+M.'),'etiket'] = '__TIMNMXX'
    df['ig1'] = 0
    df['ig2'] = 0
    df['grtyp'] = 'X'
    # print(df)
    df = encode_ip2_and_ip3_time(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_36.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "TT_Interval_3_168_160_150_diff_file2cmp_encodeIP2andIP3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_39(plugin_test_dir):
    """Teste HourMinuteSecond - objet interval - sans encodage des IPs"""
    # open and read source
    source0 = plugin_test_dir + "2020102212_023_lamwest_minimal.pres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute PrecipitationAmount
    df = spookipy.TimeIntervalMinMax(src_df0, nomvar='PR', min=True,
                                        forecast_hour_range=(datetime.timedelta(hours=22, minutes=30), datetime.timedelta(hours=23)),
                                        interval=datetime.timedelta(minutes=30), nomvar_min='TTMN',
                                        step=datetime.timedelta(minutes=30)).compute()
    
    df.loc[df.nomvar!='PR', 'etiket'] = 'WE_1_2_0N'

    # IPs non encodes, on convertit la valeur du ip3 en delta (ip2-ip3)
    # Temporaire, en attendant que ce soit fait dans le writer
    # df = adjust_ip3_time_interval(df)
    df_encode = encode_ip2_and_ip3_time(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_39.std"])
    fstpy.delete_file(results_file)
    # fstpy.StandardFileWriter(results_file, df).to_fst()
    fstpy.StandardFileWriter(results_file, df_encode).to_fst()
    # open and read comparison file
    file_to_compare = plugin_test_dir + "Test39_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

