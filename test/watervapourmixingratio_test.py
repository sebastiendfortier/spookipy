# -*- coding: utf-8 -*-
from spookipy.temperaturedewpoint.temperaturedewpoint import TemperatureDewPoint
from spookipy.dewpointdepression.dewpointdepression import DewPointDepression
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import pandas as pd
import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/WaterVapourMixingRatio/testsFiles/'



def test_1(plugin_test_dir):
    """Test #1 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (HU), option --RPN"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    hu_df = fstpy.select_with_meta(src_df0,['HU'])
    #compute WaterVapourMixingRatio
    df = spooki.WaterVapourMixingRatio(hu_df,ice_water_phase='both',temp_phase_switch=-40,rpn=True).compute()
    #[ReaderStd --input {sources[0]}] >>
    # [Select --fieldName HU] >>
    # [WaterVapourMixingRatio --RPN] >>
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    df.loc[:,'etiket'] = 'WVMXRT'
    #write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnWaterVapourMixingRatio_HU_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_3(plugin_test_dir):
    """Test #3 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (TT et ES), option --RPN"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar!='ES']

    es_df = DewPointDepression(src_df0,ice_water_phase='water',rpn=True).compute()
    tt_df = fstpy.select_with_meta(src_df0,['TT'])
    df = pd.concat([tt_df,es_df],ignore_index=True)
    #compute WaterVapourMixingRatio
    df = spooki.WaterVapourMixingRatio(df,ice_water_phase='both',temp_phase_switch=-40,rpn=True).compute()
    #[ReaderStd --input {sources[0]}] >>
    # [Select --fieldName ES --exclude] >>
    #  ([Select --fieldName TT] + [DewPointDepression --iceWaterPhase WATER --RPN]) >>
    # [WaterVapourMixingRatio --RPN] >>
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    df.loc[:,'etiket'] = 'WVMXRT'
    #write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnWaterVapourMixingRatio_ES_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_4(plugin_test_dir):
    """Test #4 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (TT et TD), option --RPN"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0,['TT'])
    td_df = TemperatureDewPoint(src_df0,ice_water_phase='water',rpn=True).compute()

    #compute WaterVapourMixingRatio
    df = spooki.WaterVapourMixingRatio(pd.concat([tt_df,td_df],ignore_index=True),ice_water_phase='both',temp_phase_switch=-40,rpn=True).compute()
    #[ReaderStd --input {sources[0]}] >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER --RPN]) >>
    # [WaterVapourMixingRatio --RPN] >>
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]
    df.loc[:,'etiket'] = 'WVMXRT'
    #write the result
    results_file = TMP_PATH + "test_4.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnWaterVapourMixingRatio_TD_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_5(plugin_test_dir):
    """Test #5 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (HU)"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    hu_df = fstpy.select_with_meta(src_df0,['HU'])

    #compute WaterVapourMixingRatio
    df = spooki.WaterVapourMixingRatio(hu_df,ice_water_phase='both',temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >>
    # [Select --fieldName HU] >>
    # [WaterVapourMixingRatio] >>
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatioHU_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_6(plugin_test_dir):
    """Test #6 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (PX,VPPR from TT,HR)"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0,['TT','HR'])
    #compute WaterVapourMixingRatio
    df = spooki.WaterVapourMixingRatio(tthr_df,ice_water_phase='both',temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [WaterVapourMixingRatio] >>
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatioPXVPPR_HR_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_7(plugin_test_dir):
    """Test #7 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (PX,VPPR from TT,ES)"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar!='ES']
    tt_df = fstpy.select_with_meta(src_df0,['TT'])
    es_df = DewPointDepression(src_df0,ice_water_phase='water').compute()
    #compute WaterVapourMixingRatio
    df = spooki.WaterVapourMixingRatio(pd.concat([tt_df,es_df],ignore_index=True),ice_water_phase='both',temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >>
    #  [Select --fieldName ES --exclude] >>
    # ([Select --fieldName TT] + [DewPointDepression --iceWaterPhase WATER]) >>
    # [WaterVapourMixingRatio] >>
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatioPXVPPR_ES_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_8(plugin_test_dir):
    """Test #8 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (PX,VPPR from TT,TD)"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0,['TT'])
    td_df = TemperatureDewPoint(src_df0,ice_water_phase='water').compute()
    #compute WaterVapourMixingRatio
    df = spooki.WaterVapourMixingRatio(pd.concat([tt_df,td_df],ignore_index=True),ice_water_phase='both',temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >>
    # [WaterVapourMixingRatio] >>[WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_8.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "WaterVapourMixingRatioPXVPPR_TD_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_9(plugin_test_dir):
    """Test #9 :  Calcul du ratio de mélange de la vapeur d'eau; utilisation d'une unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute WaterVapourMixingRatio
    with pytest.raises(spooki.WaterVapourMixingRatioError):
        _ = spooki.WaterVapourMixingRatio(src_df0,ice_water_phase='both',temp_phase_switch=-30,temp_phase_switch_unit='G').compute()
    #[ReaderStd --input {sources[0]}] >> [WaterVapourMixingRatio --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]



def test_10(plugin_test_dir):
    """Test #10 :  Calcul du ratio de mélange de la vapeur d'eau; utilisation de valeur invalide ( < borne minimale) pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute WaterVapourMixingRatio
    with pytest.raises(spooki.WaterVapourMixingRatioError):
        _ = spooki.WaterVapourMixingRatio(src_df0,ice_water_phase='both',temp_phase_switch=-273.16,temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [WaterVapourMixingRatio --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]


def test_11(plugin_test_dir):
    """Test #11 :  Calcul du ratio de mélange de la vapeur d'eau; utilisation d'une valeur invalide ( > borne maximale) pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute WaterVapourMixingRatio
    with pytest.raises(spooki.WaterVapourMixingRatioError):
        _ = spooki.WaterVapourMixingRatio(src_df0,ice_water_phase='both',temp_phase_switch=273.17,temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [WaterVapourMixingRatio --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]



def test_12(plugin_test_dir):
    """Test #12 :  Calcul du ratio de mélange de la vapeur d'eau; utilisation d'une valeur invalide pour --iceWaterPhase."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute WaterVapourMixingRatio
    with pytest.raises(spooki.WaterVapourMixingRatioError):
        _ = spooki.WaterVapourMixingRatio(src_df0,ice_water_phase='invalid',temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >>
    # [WaterVapourMixingRatio --iceWaterPhase INVALIDE --temperaturePhaseSwitch -40C]



def test_13(plugin_test_dir):
    """Test #13 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride 5005. (HU), option --RPN"""
    # open and read source
    source0 = plugin_test_dir + "minimal_HU_5005.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    hu_df = fstpy.select_with_meta(src_df0,['HU'])
    #compute WaterVapourMixingRatio
    df = spooki.WaterVapourMixingRatio(src_df0,ice_water_phase='both',temp_phase_switch=-40,rpn=True).compute()
    #['[ReaderStd --input {sources[0]}] >> ', '
    # [Select --fieldName HU] >>', '
    # [WaterVapourMixingRatio --RPN] >>', '[WriterStd --output {destination_path} --noMetadata --ignoreExtended]']

    #write the result
    results_file = TMP_PATH + "test_13.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_13.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)