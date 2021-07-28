# -*- coding: utf-8 -*-
import fstpy.all as fstpy
import pytest
import pandas as pd
from test import TMP_PATH,TEST_PATH

import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/HumidityRelative/testsFiles/'



def test_regtest_1(plugin_test_dir):
    """Test #1 :  Calcul de l'humidité relative; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumidityRelative
    with pytest.raises(spooki.HumidityRelativeError):
        _ = spooki.HumidityRelative(src_df0, ice_water_phase='both', temp_phase_switch=-30, temp_phase_switch_unit='G').compute()
    #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]



def test_regtest_2(plugin_test_dir):
    """Test #2 :  Calcul de l'humidité relative; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    # compute HumidityRelative
    with pytest.raises(spooki.HumidityRelativeError):
        _ = spooki.HumidityRelative(src_df0, ice_water_phase='both', temp_phase_switch=-273.16, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]



def test_regtest_3(plugin_test_dir):
    """Test #3 :  Calcul de l'humidité relative; utilisation d'une valeur invalide ( > borne maximale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    # compute HumidityRelative
    with pytest.raises(spooki.HumidityRelativeError):
        _ = spooki.HumidityRelative(src_df0, ice_water_phase='both', temp_phase_switch=273.17, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]



def test_regtest_4(plugin_test_dir):
    """Test #4 :  Calcul de l'humidité relative; utilisation d'une valeur invalide pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    # compute HumidityRelative
    with pytest.raises(spooki.HumidityRelativeError):
        _ = spooki.HumidityRelative(src_df0, ice_water_phase='invalid', temp_phase_switch=273.17, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]



def test_regtest_5(plugin_test_dir):
    """Test #5 :  Calcul de l'humidité relative (HR) à partir de l'humidité spécifique (HU)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0,['TT','HU'])
    
    
    # compute HumidityRelative
    df = spooki.HumidityRelative(src_df0, ice_water_phase='water').compute()

    meta_df = df.loc[df.nomvar.isin(['!!','^^','>>','P0','PT','HY'])]
    levels_df1 = df['level'].between(1.0, 0.859, inclusive=True)
    levels_df2 = df['level'].between(1.0, 0.859, inclusive=True)
    levels_df3 = df['level'].between(1.0, 0.859, inclusive=True)
    df = pd.concat([meta_df,levels_df1,levels_df2,levels_df3],ignore_index=True)
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName TT,HU] >> [HumidityRelative --iceWaterPhase WATER] >> 
    # [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> 
    # [Select --verticalLevel 1@0.859,0.126@0.103,0.00153@0.125] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_5_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_7(plugin_test_dir):
    """Test #7 :  Calcul de l'humidité relative (HR) à partir du mélange de la vapeur d'eau (QV)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb_QV"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0,['TT','QV'])
    # compute HumidityRelative
    df = spooki.HumidityRelative(src_df0, ice_water_phase='water').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName TT,QV] >> 
    # [HumidityRelative --iceWaterPhase WATER] >> 
    # [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]
    # df.loc[:,'etiket'] = 'G133K80N'
    #write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_7_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_9(plugin_test_dir):
    """Test #9 :  Calcul de l'humidité relative (HR) à partir de la température du point de rosée (TD)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb_ES"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0,['TT','TD'])

    # compute HumidityRelative
    df = spooki.HumidityRelative(src_df0, ice_water_phase='water').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName TT,TD] >> 
    # [HumidityRelative --iceWaterPhase WATER] >> 
    # [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_9.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_9_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_10(plugin_test_dir):
    """Test #10 :  Calcul de l'humidité relative (HR) à partir de la température du point de rosée (TD). fichier 5005"""
    # open and read source
    source0 = plugin_test_dir + "minimal_TTTDGZ_5005.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0,['TT','TD'])

    # compute HumidityRelative
    df = spooki.HumidityRelative(src_df0, ice_water_phase='water').compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '
    # [Select --fieldName TT,TD] >> ', '
    # [HumidityRelative --iceWaterPhase WATER] >> ', '
    # [WriterStd --output {destination_path} --ignoreExtended]']

    #write the result
    results_file = TMP_PATH + "test_10.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_10.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


