# -*- coding: utf-8 -*-
import fstpy.all as fstpy
import pytest
import pandas as pd
from test import TMP_PATH,TEST_PATH, convip

import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/HumiditySpecific/testsFiles/'


def test_regtest_a(plugin_test_dir):
    """Test #1 :  Calcul de l'humidité spécifique; utilisation de --iceWaterPhase sans --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute HumiditySpecific
    with pytest.raises(spooki.HumiditySpecificError):
        _ = spooki.HumiditySpecific(src_df0, ice_water_phase='both').compute()
    #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase BOTH]



def test_regtest_2(plugin_test_dir):
    """Test #2 :  Calcul de l'humidité spécifique; utilisation de --temperaturePhaseSwitch sans --iceWaterPhase."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute HumiditySpecific
    with pytest.raises(spooki.HumiditySpecificError):
        _ = spooki.HumiditySpecific(src_df0, temp_phase_switch=-30, temp_phase_switch_unit='celsius').compute()
    #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --temperaturePhaseSwitch -30C]



def test_regtest_c(plugin_test_dir):
    """Test #3 :  Calcul de l'humidité spécifique; utilisation de --iceWaterPhase WATER avec --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute HumiditySpecific
    with pytest.raises(spooki.HumiditySpecificError):
        _ = spooki.HumiditySpecific(src_df0,ice_water_phase='water', temp_phase_switch=-30, temp_phase_switch_unit='celsius').compute()
    #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase WATER --temperaturePhaseSwitch -30C]



def test_regtest_4(plugin_test_dir):
    """Test #4 :  Calcul de l'humidité spécifique; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute HumiditySpecific
    with pytest.raises(spooki.HumiditySpecificError):
        _ = spooki.HumiditySpecific(src_df0, ice_water_phase='both', temp_phase_switch=-30, temp_phase_switch_unit='G').compute()
    #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]



def test_regtest_5(plugin_test_dir):
    """Test #5 :  Calcul de l'humidité spécifique; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute HumiditySpecific
    with pytest.raises(spooki.HumiditySpecificError):
        _ = spooki.HumiditySpecific(src_df0, ice_water_phase='both', temp_phase_switch=-273.76, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]



def test_regtest_6(plugin_test_dir):
    """Test #6 :  Calcul de l'humidité spécifique; utilisation d'une valeur invalide ( > borne maximale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute HumiditySpecific
    with pytest.raises(spooki.HumiditySpecificError):
        _ = spooki.HumiditySpecific(src_df0,ice_water_phase='both', temp_phase_switch=273.17, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]



def test_regtest_7(plugin_test_dir):
    """Test #7 :  Calcul de l'humidité spécifique; utilisation d'une valeur invalide pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute HumiditySpecific
    with pytest.raises(spooki.HumiditySpecificError):
        _ = spooki.HumiditySpecific(src_df0, ice_water_phase='invalide', temp_phase_switch=273.17, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]



def test_regtest_8(plugin_test_dir):
    """Test #8 :  Calcul de l'humidité spécifique (HU) à partir de l'humidité relative (HR)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0,['TT','HR'])

    #compute HumiditySpecific
    df = spooki.HumiditySpecific(tthr_df, ice_water_phase='water').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName TT,HR] >> 
    # [HumiditySpecific --iceWaterPhase WATER] >> 
    # [Zap --pdsLabel R1580V0N --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[:,'etiket'] = 'R1580V0N'
    df = convip(df)
    #write the result
    results_file = TMP_PATH + "test_8.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "regpres_testWithHR_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_10(plugin_test_dir):
    """Test #10 :  Calcul de l'humidité spécifique (HU) à partir de ES et TT."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0,['TT','HU'])

    
    #compute HumiditySpecific
    dpd_d = spooki.DewPointDepression(tthu_df, ice_water_phase='water').compute()
    tt_df = fstpy.select_with_meta(tthu_df,['TT'])
    dpdtt_df = pd.concat([dpd_d,tt_df],ignore_index=True)

    df = spooki.HumiditySpecific(dpdtt_df, ice_water_phase='water').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName TT,HU] >> 
    # ([DewPointDepression --iceWaterPhase WATER] + [Select --fieldName TT]) >> 
    # [HumiditySpecific --iceWaterPhase WATER] >> 
    # [Zap --pdsLabel R1580V0N --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_10.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "regpres_testWithES_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True) 


def test_regtest_11(plugin_test_dir):
    """Test #11 :  Calcul de l'humidité spécifique (HU) à partir de ES et TT, option --RPN."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0,['TT','HU'])
    
    #compute HumiditySpecific
    dpd_df = spooki.DewPointDepression(tthu_df, ice_water_phase='water', rpn=True).compute()
    tt_df = fstpy.select_with_meta(tthu_df,['TT'])
    dpd_df = pd.concat([dpd_df,tt_df],ignore_index=True)

    df = spooki.HumiditySpecific(dpd_df, ice_water_phase='water', rpn=True).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>
    #  [Select --fieldName TT,HU] >> 
    # ([DewPointDepression --iceWaterPhase WATER --RPN] + [Select --fieldName TT]) >>  
    # [HumiditySpecific --iceWaterPhase WATER --RPN] >> 
    # [Zap --pdsLabel R1580V0N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_11.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "regpres_testWithES_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_12(plugin_test_dir):
    """Test #12 :  Calcul de l'humidité spécifique (HU) à partir de la température du point de rosée (TD)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0,['TT','HU'])

    dpd_df = spooki.DewPointDepression(tthu_df, ice_water_phase='water').compute()
    tt_df = fstpy.select_with_meta(tthu_df,['TT'])
    dpd_df = pd.concat([dpd_df,tt_df],ignore_index=True)

    tt_df = fstpy.select_with_meta(dpd_df,['TT'])
    tdp_df = spooki.TemperatureDewPoint(dpd_df, ice_water_phase='water').compute()
    tpd_df = pd.concat([tdp_df,tt_df],ignore_index=True)

    df = spooki.HumiditySpecific(tpd_df, ice_water_phase='water').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName TT,HU] >> 
    # ([DewPointDepression --iceWaterPhase WATER] + [Select --fieldName TT]) >> 
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >> 
    # [HumiditySpecific --iceWaterPhase WATER] >> 
    # [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_12.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_4_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_13(plugin_test_dir):
    """Test #13 :  Calcul de l'humidité spécifique (HU) à partir de la température du point de rosée (TD), option --RPN."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0,['TT','HU'])

    dpd_df = spooki.DewPointDepression(tthu_df, ice_water_phase='water', rpn=True).compute()
    tt_df = fstpy.select_with_meta(tthu_df,['TT'])
    dpd_df = pd.concat([dpd_df,tt_df],ignore_index=True)

    tt_df = fstpy.select_with_meta(dpd_df,['TT'])
    tdp_df = spooki.TemperatureDewPoint(dpd_df, ice_water_phase='water').compute()
    tpd_df = pd.concat([tdp_df,tt_df],ignore_index=True)

    #compute HumiditySpecific
    df = spooki.HumiditySpecific(tpd_df, ice_water_phase='water', rpn=True).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName TT,HU] >> 
    # ([DewPointDepression --iceWaterPhase WATER --RPN] + [Select --fieldName TT]) >> 
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >> 
    # [HumiditySpecific --iceWaterPhase WATER --RPN] >> 
    # [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_13.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_4_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_14(plugin_test_dir):
    """Test #14 :  Calcul de l'humidité spécifique (HU) à partir du rapport de mélange de la vapeur d'eau (QV)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0,['TT','ES'])

    dpd_df = spooki.DewPointDepression(ttes_df, ice_water_phase='water').compute()
    tt_df = fstpy.select_with_meta(ttes_df,['TT'])
    dpd_df = pd.concat([dpd_df,tt_df],ignore_index=True)

    wvmr_df = spooki.WaterVapourMixingRatio(dpd_df)

    #compute HumiditySpecific
    df = spooki.HumiditySpecific(wvmr_df, ice_water_phase='water').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName TT,ES] >> 
    # ([DewPointDepression --iceWaterPhase WATER] + [Select --fieldName TT]) >> 
    # [WaterVapourMixingRatio] >> 
    # [HumiditySpecific --iceWaterPhase WATER] >> 
    # [Zap --pdsLabel R1580V0N --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_14.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "regpres_testWithQV.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


