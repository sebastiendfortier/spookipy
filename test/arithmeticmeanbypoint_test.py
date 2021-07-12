# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/ArithmeticMeanByPoint/testsFiles/'

def test_regtest_1(plugin_test_dir):
    """Test #1 : Test avec un seul champs en entrée; requête invalide."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.query( 'nomvar == "UU"').reset_index(drop=True)

    with pytest.raises(spooki.ArithmeticMeanByPointError):
        #compute ArithmeticMeanByPoint
        df = spooki.ArithmeticMeanByPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU ] >> [ArithmeticMeanByPoint]

    

def test_regtest_2(plugin_test_dir):
    """Test #2 : Utilisation de --outputFieldName avec une valeur > 4 caractères."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    with pytest.raises(spooki.ArithmeticMeanByPointError):
        #compute ArithmeticMeanByPoint
        df = spooki.ArithmeticMeanByPoint(src_df0, nomvar_out='TROPLONG').compute()
        #[ReaderStd --input {sources[0]}] >> [ArithmeticMeanByPoint --outputFieldName TROPLONG] 




def test_regtest_3(plugin_test_dir):
    """Test #3 : Fait la moyenne de champs 2D."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute ArithmeticMeanByPoint
    df = spooki.ArithmeticMeanByPoint(src_df0, nomvar_out='ACCU').compute()
    #[ReaderStd --input {sources[0]}] >> [ArithmeticMeanByPoint --outputFieldName ACCU] >> [Zap --pdsLabel MEANFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df['etiket']='MEANFIELDS'
    #write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Mean2d_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_4(plugin_test_dir):
    """Test #4 : Fait la moyenne de champs 3D."""
    # open and read source
    source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute ArithmeticMeanByPoint
    df = spooki.ArithmeticMeanByPoint(src_df0, nomvar_out='ACCU').compute()
    #[ReaderStd --input {sources[0]}] >> [ArithmeticMeanByPoint --outputFieldName ACCU] >> [Zap --pdsLabel MEANFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df['etiket']='MEANFIELDS'
    #write the result
    results_file = TMP_PATH + "test_4.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Mean3d_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_5(plugin_test_dir):
    """Test #5 : Test avec plusieurs champs sur des 2 grilles; reusssit a former un groupe."""
    # open and read source
    source0 = plugin_test_dir + "tt_gz_px_2grilles.std"

    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute ArithmeticMeanByPoint
    df = spooki.ArithmeticMeanByPoint(src_df0).compute()
    #[ReaderStd --input {sources[0]}] >> [ArithmeticMeanByPoint ] >> [Zap --pdsLabel MEANFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]
    df['etiket']='__MEANFIX'
    # df['ip1']=500
    # df['etiket']='MEANFIELDS'
    
    #write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Mean_test5_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_6(plugin_test_dir):
    """Test #6 : Test avec plusieurs champs, differents forecastHours; calcule les resulats pour chacuns des forecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute ArithmeticMeanByPoint
    df = spooki.ArithmeticMeanByPoint(src_df0, group_by_forecast_hour=True).compute()
    #[ReaderStd --input {sources[0]}] >> [ArithmeticMeanByPoint --groupBy FORECAST_HOUR] >> [Zap --pdsLabel MEANFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} ]
    df['etiket']='__MEANFIX'
    # df['etiket']='MEANFIELDS'

    #write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Mean_test6_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_7(plugin_test_dir):
    """Test #7 : Test avec plusieurs champs, differents forecastHours; fait la moyenne des champs de tous les forecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute ArithmeticMeanByPoint
    df = spooki.ArithmeticMeanByPoint(src_df0).compute()
    #[ReaderStd --input {sources[0]}] >> [ArithmeticMeanByPoint] >> [Zap --pdsLabel MEANFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} ]
    df['etiket']='__MEANFIX'
    # df['typvar']='P'
    # df['ip2']=30
    # df['deet']=300
    # df['npas']=360

    # df['etiket']='MEANFIELDS'

    #write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    
    # open and read comparison file
    file_to_compare = plugin_test_dir + "Mean_test7_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)
