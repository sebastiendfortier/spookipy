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



def test_1(plugin_test_dir):
    """Calcul de l'humidité relative; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumidityRelative
    with pytest.raises(spooki.HumidityRelativeError):
        _ = spooki.HumidityRelative(src_df0, ice_water_phase='both', temp_phase_switch=-30, temp_phase_switch_unit='G').compute()
    #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]



def test_2(plugin_test_dir):
    """Calcul de l'humidité relative; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    # compute HumidityRelative
    with pytest.raises(spooki.HumidityRelativeError):
        _ = spooki.HumidityRelative(src_df0, ice_water_phase='both', temp_phase_switch=-273.16, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]



def test_3(plugin_test_dir):
    """Calcul de l'humidité relative; utilisation d'une valeur invalide ( > borne maximale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    # compute HumidityRelative
    with pytest.raises(spooki.HumidityRelativeError):
        _ = spooki.HumidityRelative(src_df0, ice_water_phase='both', temp_phase_switch=273.17, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]



def test_4(plugin_test_dir):
    """Calcul de l'humidité relative; utilisation d'une valeur invalide pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    # compute HumidityRelative
    with pytest.raises(spooki.HumidityRelativeError):
        _ = spooki.HumidityRelative(src_df0, ice_water_phase='invalid', temp_phase_switch=273.17, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]



def test_5(plugin_test_dir):
    """Calcul de l'humidité relative (HR) à partir de l'humidité spécifique (HU)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0,['TT','HU'])


    # compute HumidityRelative
    df = spooki.HumidityRelative(src_df0, ice_water_phase='water').compute()

    #[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >> [HumidityRelative --iceWaterPhase WATER] >>
    # [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >>
    # [Select --verticalLevel 1@0.859,0.126@0.103,0.00153@0.125] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[:,'etiket'] = 'G133K80N'

    meta_df = df.loc[df.nomvar.isin(['!!','^^','>>','P0','PT','HY'])]
    ips = [93423264,95366840,95356840,95345840,95332840,95318840,95303840,95287840,95269840,
    95250840,95230840,94497840,94490840,94484840,94479840,94474840,96408416,96362416,
    96313416,96263416,96211416,96158416,96104416,96050416,95996416,95944416,95892416,
    95842416,95795416,95750416,95707416,95667416,95630416,95597416,95566416,95539416,
    97423992,97218992,97045992,96901992,96785992,96692992,96621992]
    df1 = df.loc[df.ip1.isin(ips)]

    df = pd.concat([meta_df,df1],ignore_index=True)

    # df.loc[df.nomvar!='!!','nbits']=32
    # df.loc[:,'datyp']=5

    #write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_5_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/HumidityRelative/result_test_5'

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.01)
    # fstpy.delete_file(results_file)
    assert(res)

def test_6():
    """Pour ajout de test futur"""
    pass

def test_7(plugin_test_dir):
    """Calcul de l'humidité relative (HR) à partir du mélange de la vapeur d'eau (QV)."""
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
    df.loc[:,'etiket'] = 'G133K80N'

    # df.loc[df.nomvar!='!!','nbits']=32
    # df.loc[:,'datyp']=5

    #write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_7_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/HumidityRelative/result_test_7'

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)

def test_8():
    """Pour ajout de test futur"""
    pass



# HumidityRelative - compute
# option 3
# SaturationVapourPressure - compute
# option 1
# VapourPressure - compute
# option 5

def test_9(plugin_test_dir):
    """Calcul de l'humidité relative (HR) à partir de la température du point de rosée (TD)."""
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
    df.loc[:,'etiket'] = 'G133K80N'

    # df.loc[df.nomvar!='!!','nbits']=32
    # df.loc[:,'datyp']=5

    #write the result
    results_file = TMP_PATH + "test_9.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_9_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/HumidityRelative/result_test_9'

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)
