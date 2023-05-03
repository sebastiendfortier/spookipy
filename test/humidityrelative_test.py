# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions, pytest.mark.humidity]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/HumidityRelative/testsFiles/'


def test_1(plugin_test_dir):
    """Calcul de l'humidité relative; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumidityRelative
    with pytest.raises(spookipy.HumidityRelativeError):
        _ = spookipy.HumidityRelative(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=-30,
            temp_phase_switch_unit='G').compute()
    # [ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]


def test_2(plugin_test_dir):
    """Calcul de l'humidité relative; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumidityRelative
    with pytest.raises(spookipy.HumidityRelativeError):
        _ = spookipy.HumidityRelative(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=-273.16,
            temp_phase_switch_unit='kelvin').compute()
    # [ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]


def test_3(plugin_test_dir):
    """Calcul de l'humidité relative; utilisation d'une valeur invalide ( > borne maximale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumidityRelative
    with pytest.raises(spookipy.HumidityRelativeError):
        _ = spookipy.HumidityRelative(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=273.17,
            temp_phase_switch_unit='kelvin').compute()
    # [ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]


def test_4(plugin_test_dir):
    """Calcul de l'humidité relative; utilisation d'une valeur invalide pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumidityRelative
    with pytest.raises(spookipy.HumidityRelativeError):
        _ = spookipy.HumidityRelative(
            src_df0,
            ice_water_phase='invalid',
            temp_phase_switch=273.17,
            temp_phase_switch_unit='kelvin').compute()
    # [ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]


def test_5(plugin_test_dir):
    """Calcul de l'humidité relative (HR) à partir de l'humidité spécifique (HU)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'HU'])

    # compute HumidityRelative
    df      = spookipy.HumidityRelative(src_df0, 
                                        ice_water_phase='water').compute()

    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >> [HumidityRelative --iceWaterPhase WATER] >>
    # [Select --verticalLevel 1@0.859,0.126@0.103,0.00153@0.125] >>
    # [WriterStd --output {destination_path}]
    meta_df = df.loc[df.nomvar.isin(['!!', '^^', '>>', 'P0', 'PT', 'HY'])]
    ips = [
        93423264,
        95366840,
        95356840,
        95345840,
        95332840,
        95318840,
        95303840,
        95287840,
        95269840,
        95250840,
        95230840,
        94497840,
        94490840,
        94484840,
        94479840,
        94474840,
        96408416,
        96362416,
        96313416,
        96263416,
        96211416,
        96158416,
        96104416,
        96050416,
        95996416,
        95944416,
        95892416,
        95842416,
        95795416,
        95750416,
        95707416,
        95667416,
        95630416,
        95597416,
        95566416,
        95539416,
        97423992,
        97218992,
        97045992,
        96901992,
        96785992,
        96692992,
        96621992]
    df1 = df.loc[df.ip1.isin(ips)]

    df = pd.concat([meta_df, df1], ignore_index=True)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_5_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001, columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])
    fstpy.delete_file(results_file)
    assert(res)

def test_6(plugin_test_dir):
    """Calcul de l'humidité relative (HR) à partir de l'humidité spécifique (HU), option RPN."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'HU'])

    # compute HumidityRelative
    df      = spookipy.HumidityRelative(src_df0, 
                                        ice_water_phase='water',
                                        rpn=True).compute()

    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >> [HumidityRelative --iceWaterPhase WATER --RPN] >>
    # [Select --verticalLevel 1@0.859,0.126@0.103,0.00153@0.125] >>
    # [WriterStd --output {destination_path} ]

    meta_df = df.loc[df.nomvar.isin(['!!', '^^', '>>', 'P0', 'PT', 'HY'])]
    ips = [
        93423264,
        95366840,
        95356840,
        95345840,
        95332840,
        95318840,
        95303840,
        95287840,
        95269840,
        95250840,
        95230840,
        94497840,
        94490840,
        94484840,
        94479840,
        94474840,
        96408416,
        96362416,
        96313416,
        96263416,
        96211416,
        96158416,
        96104416,
        96050416,
        95996416,
        95944416,
        95892416,
        95842416,
        95795416,
        95750416,
        95707416,
        95667416,
        95630416,
        95597416,
        95566416,
        95539416,
        97423992,
        97218992,
        97045992,
        96901992,
        96785992,
        96692992,
        96621992]
    df1 = df.loc[df.ip1.isin(ips)]

    df = pd.concat([meta_df, df1], ignore_index=True)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_6_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001, columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])
    fstpy.delete_file(results_file)
    assert(res)


def test_7(plugin_test_dir):
    """Calcul de l'humidité relative (HR) à partir du mélange de la vapeur d'eau (QV)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb_QV"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'QV'])

    # compute HumidityRelative
    df      = spookipy.HumidityRelative(src_df0, 
                                        ice_water_phase='water').compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,QV] >>
    # [HumidityRelative --iceWaterPhase WATER] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_7_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001, columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])
    fstpy.delete_file(results_file)
    assert(res)


def test_8(plugin_test_dir):
    """Calcul de l'humidité relative (HR) à partir du mélange de la vapeur d'eau (QV), option RPN."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb_QV"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'QV'])
    # compute HumidityRelative
    df      = spookipy.HumidityRelative(src_df0, 
                                        ice_water_phase='water',
                                        rpn=True).compute()

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_8_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001, columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])
    fstpy.delete_file(results_file)
    assert(res)

def test_9(plugin_test_dir):
    """Calcul de l'humidité relative (HR) à partir de la température du point de rosée (TD)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb_ES"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'TD'])

    # compute HumidityRelative
    df      = spookipy.HumidityRelative(src_df0,
                                        ice_water_phase='water').compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,TD] >>
    # [HumidityRelative --iceWaterPhase WATER] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_9_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.002, columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])
    fstpy.delete_file(results_file)
    assert(res)

def test_10(plugin_test_dir):
    """Calcul à partir de la température du point de rosée, fichier reduit, copy_input = true."""
    # Test en python seulement.  
    # Fichier input meme que le test 9, cree de cette facon:
    # [ReaderStd --input .../pluginsRelatedStuff/HumidityRelative/testsFiles/2011100712_glbhyb_9_file2cmp.std] 
    #  >>  [GridCut --startPoint 50,50 --endPoint 100,100]
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb_ES_reduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'TD'])

    # compute HumidityRelative
    df      = spookipy.HumidityRelative(src_df0, 
                                        ice_water_phase='water',
                                        copy_input=True).compute()

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_10_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_11(plugin_test_dir):
    """Calcul de l'humidité relative (HR) à partir de la température du point de rosée (TD), option RPN."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb_ES"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'TD'])

    # compute HumidityRelative
    df      = spookipy.HumidityRelative(src_df0,
                                        ice_water_phase='water',
                                        rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,TD] >>
    # [HumidityRelative --iceWaterPhase WATER --RPN] >>
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_glbhyb_11_file2cmp_20230426.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001, columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])
    fstpy.delete_file(results_file)
    assert(res)

def test_12(plugin_test_dir):
    """Calcul de l'humidité relative (HR) avec un fichier regpres (HU), ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df   = fstpy.select_with_meta(src_df0, ['TT','HU'])

    # compute 
    df      = spookipy.HumidityRelative(tthu_df, 
                                        ice_water_phase='both',
                                        temp_phase_switch=273,
                                        temp_phase_switch_unit='celsius').compute()

    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_regpres_test12_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_13(plugin_test_dir):
    """Calcul de l'humidité relative (HR) avec un fichier regpres (HU), option RPN, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    hu_df   = fstpy.select_with_meta(src_df0, ['HU'])
    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])
    tt_df   = spookipy.SetUpperBoundary(tt_df, 
                                        value=0.0).compute()

    tthu_df = pd.concat([tt_df, hu_df],ignore_index=True)

    # compute 
    df      = spookipy.HumidityRelative(tthu_df, 
                                        ice_water_phase='both',
                                        rpn=True).compute()


    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_regpres_rpn_test13_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.002)
    fstpy.delete_file(results_file)
    assert(res)
