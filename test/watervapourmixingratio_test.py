# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy
from ci_fstcomp import fstcomp
import rpnpy.librmn.all as rmn
import secrets

pytestmark = [pytest.mark.regressions, pytest.mark.humidity]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/WaterVapourMixingRatio/testsFiles/'


def test_1(plugin_test_dir):
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (HU), option rpn,  ice_water_phase = both"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    hu_df   = fstpy.select_with_meta(src_df0, ['HU'])
    # compute WaterVapourMixingRatio
    df      = spookipy.WaterVapourMixingRatio(hu_df,
                                              ice_water_phase='both',
                                              temp_phase_switch=-40,
                                              rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName HU] >>
    # [WaterVapourMixingRatio --RPN] >>
    # [WriterStd --output {destination_path} --noMetadata]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnWaterVapourMixingRatio_HU_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_2(plugin_test_dir):  
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (TT et HR), option rpn,  ice_water_phase = both"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df   = fstpy.select_with_meta(src_df0, ['TT', 'HR'])

    # compute WaterVapourMixingRatio
    df      = spookipy.WaterVapourMixingRatio(tt_df,
                                              rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [WaterVapourMixingRatio --RPN] >>
    # [WriterStd --output {destination_path} --noMetadata ]
    
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnWaterVapourMixingRatio_HR_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_3(plugin_test_dir):  # option 1 rpn
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (TT et ES), option rpn,  ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar != 'ES']

    es_df   = spookipy.DewPointDepression(src_df0,
                                          ice_water_phase='water',
                                          rpn=True).compute()

    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])
    df      = pd.concat([tt_df, es_df], ignore_index=True)

    # compute WaterVapourMixingRatio
    df      = spookipy.WaterVapourMixingRatio(df,
                                              ice_water_phase='both',
                                              temp_phase_switch=-40,
                                              rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName ES --exclude] >>
    #  ([Select --fieldName TT] + [DewPointDepression --iceWaterPhase WATER --RPN]) >>
    # [WaterVapourMixingRatio --RPN] >>
    # [WriterStd --output {destination_path} --noMetadata]
    
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnWaterVapourMixingRatio_ES_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_4(plugin_test_dir):  # option 1 rpn
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (TT et TD), option rpn,  ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])
    td_df   = spookipy.TemperatureDewPoint(src_df0,
                                           ice_water_phase='water',
                                           rpn=True).compute()

    # compute WaterVapourMixingRatio
    df      = spookipy.WaterVapourMixingRatio(pd.concat([tt_df, td_df], ignore_index=True),
                                              ice_water_phase='both',
                                              temp_phase_switch=-40,
                                              rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER --RPN]) >>
    # [WaterVapourMixingRatio --RPN] >>
    # [WriterStd --output {destination_path} --noMetadata]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnWaterVapourMixingRatio_TD_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.003)
    fstpy.delete_file(results_file)
    assert(res)

def test_5(plugin_test_dir):
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (HU), ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WaterVapourMixingRatio
    df      = spookipy.WaterVapourMixingRatio(src_df0,
                                              ice_water_phase='both',
                                              temp_phase_switch=-40).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName HU] >>
    # [WaterVapourMixingRatio] >>
    # [WriterStd --output {destination_path} --noMetadata]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatioHU_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_6(plugin_test_dir):
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (PX,VPPR from TT,HR), ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ['TT', 'HR'])

    # compute WaterVapourMixingRatio
    df      = spookipy.WaterVapourMixingRatio(tthr_df,
                                              ice_water_phase='both',
                                              temp_phase_switch=-40).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [WaterVapourMixingRatio] >>
    # [WriterStd --output {destination_path} --noMetadata]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatioPXVPPR_HR_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_7(plugin_test_dir):
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (PX,VPPR from TT,ES), ice_water_phase = both"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar != 'ES']

    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])
    es_df   = spookipy.DewPointDepression(src_df0, 
                                          ice_water_phase='water').compute()

    # compute WaterVapourMixingRatio
    df = spookipy.WaterVapourMixingRatio(pd.concat(
        [tt_df, es_df], ignore_index=True), 
        ice_water_phase='both', 
        temp_phase_switch=-40).compute()
    # [ReaderStd --input {sources[0]}] >>
    #  [Select --fieldName ES --exclude] >>
    # ([Select --fieldName TT] + [DewPointDepression --iceWaterPhase WATER]) >>
    # [WaterVapourMixingRatio] 
  
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatioPXVPPR_ES_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.02)
    # fstpy.delete_file(results_file)
    assert(res)

def test_8(plugin_test_dir):
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (PX,VPPR from TT,TD), ice_water_phase = both ."""
    # Appel a WaterVapourMixingRatio sans parametres, utilisation des valeurs par defaut
    
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])
    td_df   = spookipy.TemperatureDewPoint(src_df0, 
                                           ice_water_phase='water').compute()

    # compute WaterVapourMixingRatio
    df      = spookipy.WaterVapourMixingRatio(pd.concat([tt_df, td_df],
                                              ignore_index=True)).compute()
    # [ReaderStd --input {sources[0]}] >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >>
    # [WaterVapourMixingRatio] >>[WriterStd --output {destination_path} --noMetadata]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatioPXVPPR_TD_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.02)
    fstpy.delete_file(results_file)
    assert(res)

def test_9(plugin_test_dir):
    """Calcul du ratio de mélange de la vapeur d'eau; utilisation d'une unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WaterVapourMixingRatio
    with pytest.raises(spookipy.WaterVapourMixingRatioError):
        _ = spookipy.WaterVapourMixingRatio(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=-30,
            temp_phase_switch_unit='G').compute()
    # [ReaderStd --input {sources[0]}] >> [WaterVapourMixingRatio --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]

def test_10(plugin_test_dir):
    """Calcul du ratio de mélange de la vapeur d'eau; utilisation de valeur invalide ( < borne minimale en kelvin) pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WaterVapourMixingRatio
    with pytest.raises(spookipy.WaterVapourMixingRatioError):
        _ = spookipy.WaterVapourMixingRatio(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=-5,
            temp_phase_switch_unit='kelvin').compute()

def test_11(plugin_test_dir):
    """Calcul du ratio de mélange de la vapeur d'eau; utilisation d'une valeur invalide ( < borne minimale en celsius) pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WaterVapourMixingRatio
    with pytest.raises(spookipy.WaterVapourMixingRatioError):
        _ = spookipy.WaterVapourMixingRatio(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=-275,
            temp_phase_switch_unit='celsius').compute()

def test_12(plugin_test_dir):
    """Calcul du ratio de mélange de la vapeur d'eau; utilisation d'une valeur invalide pour --iceWaterPhase."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WaterVapourMixingRatio
    with pytest.raises(spookipy.WaterVapourMixingRatioError):
        _ = spookipy.WaterVapourMixingRatio(
            src_df0,
            ice_water_phase='invalid',
            temp_phase_switch=-
            40).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [WaterVapourMixingRatio --iceWaterPhase INVALIDE --temperaturePhaseSwitch -40C]

def test_13(plugin_test_dir):
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride 5005. (HU), option rpn, ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_dir + "minimal_HU_5005.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    hu_df = fstpy.select_with_meta(src_df0, ['HU'])
    # compute WaterVapourMixingRatio
    df = spookipy.WaterVapourMixingRatio(
        hu_df,
        ice_water_phase='both',
        temp_phase_switch=-40,
        rpn=True).compute()
    # ['[ReaderStd --input {sources[0]}] >> ', '
    # [Select --fieldName HU] >>', '
    # [WaterVapourMixingRatio --RPN] >>', '[WriterStd --output {destination_path} --noMetadata]']

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatio_HU_test13_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_14(plugin_test_dir):
    """Calcul du ratio de mélange de la vapeur d'eau à partir d'un fichier hybride, option copy_input. (PX,VPPR from TT,HR)"""
    # Identique au test 6, avec un sous-ensemble du fichier d'input, pour tester option copy_input
    
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Creation d'un fichier reduit a quelques niveaux 
    meta_df         = src_df0.loc[src_df0.nomvar.isin(
                                    ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)
    tthr_df         = fstpy.select_with_meta(src_df0, ['TT', 'HR'])
    tthr_df_reduit  = tthr_df.loc[((tthr_df.level <= 1.0) & (tthr_df.level > 0.95))].reset_index(drop=True)
    df_reduit       = pd.concat([tthr_df_reduit, meta_df],ignore_index=True)

    # compute WaterVapourMixingRatio
    df = spookipy.WaterVapourMixingRatio(df_reduit,
                                         ice_water_phase='both',
                                         temp_phase_switch=-40, 
                                         copy_input=True).compute()

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_14.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatioPXVPPR_test14_file2cmp_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_15(plugin_test_dir):
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (HR), ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regeta"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ['TT', 'HR'])

    # compute WaterVapourMixingRatio
    df      = spookipy.WaterVapourMixingRatio(tthr_df,
                                              ice_water_phase='water').compute()
    
    # Equivalent a --IP1EncodingStyle OLDSTYLE
    df = spookipy.convip(df, style=rmn.CONVIP_ENCODE_OLD)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_15.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatio_HR_test15_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_16(plugin_test_dir):
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (HU), option rpn,  ice_water_phase = water"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    hu_df   = fstpy.select_with_meta(src_df0, ['HU'])
    # compute WaterVapourMixingRatio
    df      = spookipy.WaterVapourMixingRatio(hu_df,
                                              ice_water_phase='water',
                                              rpn=True).compute()

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_16.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnWaterVapourMixingRatio_HU_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_17(plugin_test_dir):
    """Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (HU), ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WaterVapourMixingRatio
    df      = spookipy.WaterVapourMixingRatio(src_df0,
                                              ice_water_phase='water').compute()

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_17.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatioHU_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)
