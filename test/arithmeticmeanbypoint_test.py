# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "ArithmeticMeanByPoint"

def test_1(plugin_test_path):
    """Test avec un seul champs en entrée; requête invalide."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar == 'UU'].reset_index(drop=True)

    with pytest.raises(spookipy.ArithmeticMeanByPointError):
        # compute ArithmeticMeanByPoint
        df = spookipy.ArithmeticMeanByPoint(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU ] >> [ArithmeticMeanByPoint]


def test_2(plugin_test_path):
    """Utilisation de --outputFieldName avec une valeur > 4 caractères."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.ArithmeticMeanByPointError):
        # compute ArithmeticMeanByPoint
        df = spookipy.ArithmeticMeanByPoint(
            src_df0, nomvar_out='TROPLONG').compute()
        # [ReaderStd --input {sources[0]}] >> [ArithmeticMeanByPoint --outputFieldName TROPLONG]


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Fait la moyenne de champs 2D."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
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
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Mean2d_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Fait la moyenne de champs 3D."""
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5x2_fileSrc.std"
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
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Mean3d_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec plusieurs champs sur des 2 grilles; reusssit a former un groupe."""
    # open and read source
    source0 = plugin_test_path / "tt_gz_px_2grilles.std"

    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ArithmeticMeanByPoint
    df      = spookipy.ArithmeticMeanByPoint(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [ArithmeticMeanByPoint ] >> 
    # [Zap --pdsLabel MEANFIELDS --doNotFlagAsZapped] >>  
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    # Pour respecter le zap du test original et encodage du test original
    df.loc[~df.nomvar.isin(['!!', '^^', '>>']), 'etiket'] = '__MEANFIX'
    df.loc[~df.nomvar.isin(['!!', '^^', '>>']), 'datyp'] = 134
    df.loc[~df.nomvar.isin(['!!', '^^', '>>']), 'nbits'] = 16


    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Mean_test5_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec plusieurs champs, differents forecastHours; calcule les resulats pour chacuns des forecastHours."""
    # open and read source
    source0 = plugin_test_path / "TTES2x2x4_manyForecastHours.std"
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
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Mean_test6_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec plusieurs champs, differents forecastHours; fait la moyenne des champs de tous les forecastHours."""
    # open and read source
    source0 = plugin_test_path / "TTES2x2x4_manyForecastHours.std"
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
    results_file = test_tmp_path / "test_7.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Mean_test7_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec champs pour differents forecastHours; fait la moyenne groupe par champs."""
    # open and read source
    source0 = plugin_test_path / "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ArithmeticMeanByPoint
    df      = spookipy.ArithmeticMeanByPoint(src_df0, 
                                             group_by_nomvar=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [ArithmeticMeanByPoint] >>  
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier de test, sans zap du l'etiket 
    file_to_compare = plugin_test_path / "Mean_test8_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

# Test existant du cote python seulement
def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Moyenne de champs MASK; le resultat est converti en E32 par le plugin lui-meme."""
    # open and read source
    source0   = plugin_test_path / "2021071400_024_masked_fields_reduit.std"
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
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, res_df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Mean_test9_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test de moyenne pour un champ groupé par ensemble member (test eps stat)"

    sources = [
        "eta_2024020800_024_001_tt_fh2_small",
        "eta_2024020800_024_002_tt_fh2_small",
        "eta_2024020800_024_003_tt_fh2_small",
        "eta_2024020800_024_004_tt_fh2_small",
    ]
    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()
    res_df    = spookipy.ArithmeticMeanByPoint(src_df0, 
                                               group_by_forecast_hour=True,
                                               group_by_nomvar=True,
                                            #    group_by_ensemble_member=True,
                                               copy_input=False).compute()

    res_df = res_df.loc[res_df.nomvar == 'TT']
    res_df['etiket'] = "ERMEAN__PALL"
    res_df['ip3'] = 2
    res_df['datyp'] = 6
    res_df['nbits'] = 16
    res_df = fstpy.compute(res_df)

    # write the result
    results_file = test_tmp_path / "test_10.std"
    fstpy.StandardFileWriter(results_file, res_df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "eta_2024020800_ALL_tt_fh2_small_mean2"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)
