# -*- coding: utf-8 -*-
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
    return TEST_PATH + '/ArithmeticMeanByPoint/testsFiles/'


def test_1(plugin_test_dir):
    """Test avec un seul champs en entrée; requête invalide."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar == 'UU'].reset_index(drop=True)

    with pytest.raises(spookipy.ArithmeticMeanByPointError):
        # compute ArithmeticMeanByPoint
        df = spookipy.ArithmeticMeanByPoint(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU ] >> [ArithmeticMeanByPoint]


def test_2(plugin_test_dir):
    """Utilisation de --outputFieldName avec une valeur > 4 caractères."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ArithmeticMeanByPointError):
        # compute ArithmeticMeanByPoint
        df = spookipy.ArithmeticMeanByPoint(
            src_df0, nomvar_out='TROPLONG').compute()
        # [ReaderStd --input {sources[0]}] >> [ArithmeticMeanByPoint --outputFieldName TROPLONG]


def test_3(plugin_test_dir):
    """Fait la moyenne de champs 2D."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ArithmeticMeanByPoint
    df      = spookipy.ArithmeticMeanByPoint(src_df0, 
                                             nomvar_out='ACCU').compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [ArithmeticMeanByPoint --outputFieldName ACCU] >> 
    # [Zap --pdsLabel MEANFIELDS --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df['etiket'] = 'MEANFIELDS'
    df['nbits']  = 16               # Pour correspondre a R16
    df['datyp']  = 1

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Mean2d_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_4(plugin_test_dir):
    """Fait la moyenne de champs 3D."""
    # open and read source
    source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ArithmeticMeanByPoint
    df      = spookipy.ArithmeticMeanByPoint(src_df0, 
                                             nomvar_out='ACCU').compute()
    # [ReaderStd --input {sources[0]}] >>
    #  [ArithmeticMeanByPoint --outputFieldName ACCU] >> 
    # [Zap --pdsLabel MEANFIELDS --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df['etiket'] = 'MEANFIELDS'
    df['nbits']  = 16               # Pour correspondre a R16
    df['datyp']  = 1

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Mean3d_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_5(plugin_test_dir):
    """Test avec plusieurs champs sur des 2 grilles; reusssit a former un groupe."""
    # open and read source
    source0 = plugin_test_dir + "tt_gz_px_2grilles.std"

    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ArithmeticMeanByPoint
    df      = spookipy.ArithmeticMeanByPoint(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [ArithmeticMeanByPoint ] >> 
    # [Zap --pdsLabel MEANFIELDS --doNotFlagAsZapped] >>  
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    # Pour respecter le zap du test original
    df.loc[~df.nomvar.isin(['!!', '^^', '>>']), 'etiket'] = '__MEANFIX'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Mean_test5_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir):
    """Test avec plusieurs champs, differents forecastHours; calcule les resulats pour chacuns des forecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ArithmeticMeanByPoint
    df      = spookipy.ArithmeticMeanByPoint(src_df0, 
                                             group_by_forecast_hour=True).compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [ArithmeticMeanByPoint --groupBy FORECAST_HOUR] >> 
    # [Zap --pdsLabel MEANFIELDS --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} ]

     # Pour respecter le zap du test original
    df.loc[~df.nomvar.isin(['!!', '^^', '>>', 'P0']), 'etiket'] = '__MEANFIX'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Mean_test6_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_7(plugin_test_dir):
    """Test avec plusieurs champs, differents forecastHours; fait la moyenne des champs de tous les forecastHours."""
    # open and read source
    source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ArithmeticMeanByPoint
    df      = spookipy.ArithmeticMeanByPoint(src_df0).compute()

    # [ReaderStd --input {sources[0]}] >> 
    # [ArithmeticMeanByPoint] >> 
    # [Zap --pdsLabel MEANFIELDS --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} ]

    # Pour respecter le zap du test original
    df.loc[~df.nomvar.isin(['!!', '^^', '>>', 'P0']), 'etiket'] = '__MEANFIX'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Mean_test7_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_8(plugin_test_dir):
    """Test avec champs pour differents forecastHours; fait la moyenne groupe par champs."""
    # open and read source
    source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ArithmeticMeanByPoint
    df      = spookipy.ArithmeticMeanByPoint(src_df0, 
                                             group_by_nomvar=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [ArithmeticMeanByPoint] >>  
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier de test, sans zap du l'etiket 
    file_to_compare = plugin_test_dir + "Mean_test8_file2cmp_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

# Test existant du cote python seulement
def test_9(plugin_test_dir):
    """Moyenne de champs MASK; le resultat est converti en E32 par le plugin lui-meme."""
    # open and read source
    source0   = plugin_test_dir + "2021071400_024_masked_fields_reduit.std"
    src_df    = fstpy.StandardFileReader(source0).to_pandas()
    src_df0   = src_df.loc[(src_df.nomvar.isin(['WHP0', 'WHP1'])) & (src_df.typvar == '@@')]
 
    # # compute AddElementsByPoint
    res_df    = spookipy.ArithmeticMeanByPoint(src_df0, 
                                               nomvar_out="HP01",
                                               copy_input=True).compute()
    # spooki_run.py "[ReaderStd --input 2021071400_024_masked_fields_reduit.std] >> 
    #                ( [Select --typeOfField MASK --fieldName WHP0,WHP1] >> 
    #                  ([Copy] + ([ArithmeticMeanByPoint --outputFieldName HP01] >> [Zap --nbitsForDataStorage E32]))
    #                )  >> 
    #                [WriterStd --output Mean_test9_file2cmp.std  --noMetadata --plugin_language CPP]"

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, res_df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Mean_test9_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
