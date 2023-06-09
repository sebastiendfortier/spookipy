# -*- coding: utf-8 -*-
import pandas as pd
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/MultiplyElementsByPoint/testsFiles/'


def test_1(plugin_test_dir):
    """Utilisation de --outputFieldName avec une valeur > 4 caractères."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute MultiplyElementsByPoint
    with pytest.raises(spookipy.MultiplyElementsByPointError):
        df = spookipy.MultiplyElementsByPoint(
            src_df0, nomvar_out='TROPLONG').compute()
        # [ReaderStd --input {sources[0]}] >> [MultiplyElementsByPoint --outputFieldName TROPLONG]


def test_2(plugin_test_dir):
    """Essaie de multiplier lorsqu'il y a seulement 1 champ en entrée."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['UU'])
    # src_df0 = src_df0.loc[src_df0.nomvar=='UU'].reset_index(drop=True)
    # compute MultiplyElementsByPoint
    with pytest.raises(spookipy.MultiplyElementsByPointError):
        df = spookipy.MultiplyElementsByPoint(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [MultiplyElementsByPoint]


def test_3(plugin_test_dir):
    """Essaie de multiplier lorsqu'il y a plusieurs champs mais pas sur la même grille."""
    # open and read source
    source0 = plugin_test_dir + "tt_gz_px_2grilles.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'GZ'])

    # compute MultiplyElementsByPoint
    with pytest.raises(spookipy.MultiplyElementsByPointError):
        df = spookipy.MultiplyElementsByPoint(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,GZ ] >> [MultiplyElementsByPoint]


def test_4(plugin_test_dir):
    """Multiplication des champs 2D."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute MultiplyElementsByPoint
    df = spookipy.MultiplyElementsByPoint(src_df0, nomvar_out='UU').compute()
    # [ReaderStd --input {sources[0]}] >> [MultiplyElementsByPoint --outputFieldName UU] >> [Zap --pdsLabel MULTIPLYFIEL --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    df.loc[:, 'etiket'] = 'MULTIPLYFIEL'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Multiply2d_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_5(plugin_test_dir):
    """Multiplication des champs 3D."""
    # open and read source
    source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute MultiplyElementsByPoint
    df = spookipy.MultiplyElementsByPoint(src_df0, nomvar_out='TT').compute()
    # [ReaderStd --input {sources[0]}] >> [MultiplyElementsByPoint --outputFieldName TT] >> [Zap --pdsLabel MULTIPLYFIEL --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    df.loc[:, 'etiket'] = 'MULTIPLYFIEL'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Multiply3d_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir):
    """Test avec plusieurs champs, differents forecastHours; calcule les resulats pour chacuns des forecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute MultiplyElementsByPoint
    df = spookipy.MultiplyElementsByPoint(
        src_df0, group_by_forecast_hour=True).compute()
    # [ReaderStd --input {sources[0]}] >> [MultiplyElementsByPoint --groupBy FORECAST_HOUR] >> [Zap --pdsLabel MULBYPT --doNotFlagAsZapped] >> [WriterStd --output {destination_path} ]

    df.loc[:, 'etiket'] = '__MULBYPX'
    df.loc[df.nomvar.isin(['!!', '^^', '>>', 'P0']), 'etiket'] = 'R1_V700_N'
    df.loc[df.nomvar=='MUEP','typvar'] = 'P'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Multiply_test6_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_7(plugin_test_dir):
    """Test avec plusieurs champs, differents forecastHours; fait la multiplication des champs de tous les forecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute MultiplyElementsByPoint
    df = spookipy.MultiplyElementsByPoint(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [MultiplyElementsByPoint] >> [Zap --pdsLabel MULBYPT --doNotFlagAsZapped] >> [WriterStd --output {destination_path} ]

    df.loc[:, 'etiket'] = '__MULBYPX'
    df.loc[df.nomvar.isin(['!!', '^^', '>>', 'P0']), 'etiket'] = 'R1_V700_N'
    df.loc[df.nomvar=='MUEP','typvar'] = 'P'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Multiply_test7_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_10(plugin_test_dir):
    """Test multiplication avec parametre group_by_nomvar."""
    # open and read source
    source0 = plugin_test_dir + "TTUUVV_12h.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_dir + "TTUUVV_24h.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df = pd.concat([src_df0 , src_df1])

    # compute MultiplyElementsByPoint
    df = spookipy.MultiplyElementsByPoint(src_df, group_by_nomvar=True).compute()

    df.loc[~df.nomvar.isin(['!!', '^^', '>>', 'P0']), 'etiket'] = '__MULBYPX'
    df.loc[~df.nomvar.isin(['!!', '^^', '>>', 'P0']), 'typvar'] = 'P'

    df.sort_values(by=['nomvar', 'level'],ascending=[True, False],inplace=True)
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test10_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
