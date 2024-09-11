# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy
import warnings

pytestmark = [pytest.mark.regressions, pytest.mark.humidity]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "HumiditySpecific"

def test_1(plugin_test_path):
    """Calcul de l'humidité spécifique; utilisation de --iceWaterPhase sans --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumiditySpecific
    with pytest.raises(spookipy.HumiditySpecificError):
        _ = spookipy.HumiditySpecific(src_df0, ice_water_phase='both').compute()
    # [ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase BOTH]


def test_2(plugin_test_path):
    """Calcul de l'humidité spécifique; utilisation de --temperaturePhaseSwitch sans --iceWaterPhase."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumiditySpecific
    with pytest.raises(spookipy.HumiditySpecificError):
        _ = spookipy.HumiditySpecific(
            src_df0,
            temp_phase_switch=-30,
            temp_phase_switch_unit='celsius').compute()
    # [ReaderStd --input {sources[0]}] >> [HumiditySpecific --temperaturePhaseSwitch -30C]


def test_3(plugin_test_path):
    """Calcul de l'humidité spécifique; utilisation de --iceWaterPhase WATER avec --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumiditySpecific
    with pytest.raises(spookipy.HumiditySpecificError):
        _ = spookipy.HumiditySpecific(
            src_df0,
            ice_water_phase='water',
            temp_phase_switch=-30,
            temp_phase_switch_unit='celsius').compute()
    # [ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase WATER --temperaturePhaseSwitch -30C]


def test_4(plugin_test_path):
    """Calcul de l'humidité spécifique; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumiditySpecific
    with pytest.raises(spookipy.HumiditySpecificError):
        _ = spookipy.HumiditySpecific(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=-30,
            temp_phase_switch_unit='G').compute()
    # [ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]


def test_5(plugin_test_path):
    """Calcul de l'humidité spécifique; utilisation de valeur invalide ( < borne minimale en Celsius) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumiditySpecific
    with pytest.raises(spookipy.HumiditySpecificError):
        _ = spookipy.HumiditySpecific(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=-280,
            temp_phase_switch_unit='celsius').compute()
    # [ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]


def test_6(plugin_test_path):
    """Calcul de l'humidité spécifique; utilisation d'une valeur invalide ( < borne minimale en kelvin) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumiditySpecific
    with pytest.raises(spookipy.HumiditySpecificError):
        _ = spookipy.HumiditySpecific(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=-10,
            temp_phase_switch_unit='kelvin').compute()


def test_7(plugin_test_path):
    """Calcul de l'humidité spécifique; utilisation d'une valeur invalide pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute HumiditySpecific
    with pytest.raises(spookipy.HumiditySpecificError):
        _ = spookipy.HumiditySpecific(
            src_df0,
            ice_water_phase='invalide',
            temp_phase_switch=273.17,
            temp_phase_switch_unit='kelvin').compute()
    # [ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]

def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidité spécifique (HU) à partir de l'humidité relative (HR), ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ['TT', 'HR'])

    # compute HumiditySpecific
    df      = spookipy.HumiditySpecific(tthr_df, 
                                        ice_water_phase='water').compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [HumiditySpecific --iceWaterPhase WATER] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "regpres_testWithHR_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidité spécifique (HU) à partir de l'humidité relative (HR), option rpn, ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ['TT', 'HR'])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute HumiditySpecific
    df      = spookipy.HumiditySpecific(tthr_df, 
                                        ice_water_phase='water',
                                        rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [HumiditySpecific --iceWaterPhase WATER --RPN] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "regpres_testWithHR_RPN_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidité spécifique (HU) à partir de ES et TT, ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ['TT', 'HU'])

    # compute HumiditySpecific
    es_df   = spookipy.DewPointDepression(tthu_df, 
                                          ice_water_phase='water').compute()
    tt_df   = fstpy.select_with_meta(tthu_df, ['TT'])
    dpdtt_df= pd.concat([es_df, tt_df], ignore_index=True)

    df      = spookipy.HumiditySpecific(dpdtt_df, 
                                        ice_water_phase='water').compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # ([DewPointDepression --iceWaterPhase WATER] + [Select --fieldName TT]) >>
    # [HumiditySpecific --iceWaterPhase WATER] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_10.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "regpres_testWithES_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidité spécifique (HU) à partir de ES et TT, option rpn, ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ['TT', 'HU'])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute HumiditySpecific
    es_df   = spookipy.DewPointDepression(tthu_df, 
                                          ice_water_phase='water',
                                          rpn=True).compute()

    tt_df   = fstpy.select_with_meta(tthu_df, ['TT'])

    ttes_df = pd.concat([es_df, tt_df], ignore_index=True)

    df      = spookipy.HumiditySpecific(ttes_df,
                                        ice_water_phase='water',
                                        rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    #  [Select --fieldName TT,HU] >>
    # ([DewPointDepression --iceWaterPhase WATER --RPN] + [Select --fieldName TT]) >>
    # [HumiditySpecific --iceWaterPhase WATER --RPN] >>
    # [Zap --pdsLabel R1580V0N --doNotFlagAsZapped] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_11.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "regpres_testWithES_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidité spécifique (HU) à partir de la température du point de rosée (TD), ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ['TT', 'HU'])
    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])

    es_df   = spookipy.DewPointDepression(tthu_df, 
                                          ice_water_phase='water').compute()
    estt_df = pd.concat([es_df, tt_df], ignore_index=True)

    td_df   = spookipy.TemperatureDewPoint(estt_df, 
                                           ice_water_phase='water').compute()
    tttd_df = pd.concat([td_df, tt_df], ignore_index=True)

    df      = spookipy.HumiditySpecific(tttd_df, 
                                        ice_water_phase='water').compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # ([DewPointDepression --iceWaterPhase WATER] + [Select --fieldName TT]) >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >>
    # [HumiditySpecific --iceWaterPhase WATER] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_12.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_4_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidité spécifique (HU) à partir de la température du point de rosée (TD), option rpn, ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ['TT', 'HU'])
    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    es_df   = spookipy.DewPointDepression(tthu_df, 
                                          ice_water_phase='water', 
                                          rpn=True).compute()
    estt_df = pd.concat([es_df, tt_df], ignore_index=True)

    td_df   = spookipy.TemperatureDewPoint(estt_df, 
                                           ice_water_phase='water').compute()
    tttd_df = pd.concat([td_df, tt_df], ignore_index=True)

    # compute HumiditySpecific
    df      = spookipy.HumiditySpecific(tttd_df,
                                        ice_water_phase='water',
                                        rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # ([DewPointDepression --iceWaterPhase WATER --RPN] + [Select --fieldName TT]) >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >>
    # [HumiditySpecific --iceWaterPhase WATER --RPN] >>
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_13.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_4_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidité spécifique (HU) à partir du rapport de mélange de la vapeur d'eau (QV), ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0, ['TT', 'ES'])
    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])

    es_df   = spookipy.DewPointDepression(ttes_df, 
                                          ice_water_phase='water').compute()
    ttes_df = pd.concat([es_df, tt_df], ignore_index=True)

    qv_df   = spookipy.WaterVapourMixingRatio(ttes_df).compute()
    
    # compute HumiditySpecific
    df      = spookipy.HumiditySpecific(qv_df, 
                                        ice_water_phase='water').compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,ES] >>
    # ([DewPointDepression --iceWaterPhase WATER] + [Select --fieldName TT]) >>
    # [WaterVapourMixingRatio] >>
    # [HumiditySpecific --iceWaterPhase WATER] >>
    # [WriterStd --output {destination_path} ]
    df      = spookipy.convip(df)

    results_file = test_tmp_path / "test_14.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "regpres_testWithQV_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidité spécifique (HU) à partir de la température du point de rosée (TD), ice_water_phase = both."""

    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb_reduit"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ['TT', 'HU'])
    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])

    es_df   = spookipy.DewPointDepression(tthu_df, 
                                        ice_water_phase='both', 
                                        temp_phase_switch=-40, 
                                        temp_phase_switch_unit='celsius').compute()
    estt_df = pd.concat([es_df, tt_df], ignore_index=True)

    td_df   = spookipy.TemperatureDewPoint(estt_df, 
                                         ice_water_phase='both', 
                                         temp_phase_switch=-40, 
                                         temp_phase_switch_unit='celsius').compute()
    tttd_df = pd.concat([td_df, tt_df], ignore_index=True)

    df      = spookipy.HumiditySpecific(tttd_df).compute()

    # Nouveau test; fichier resultat cree a partir de spooki (version C++)
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # ([DewPointDepression  --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] + [Select --fieldName TT]) >>
    # ([Select --fieldName TT] + [TemperatureDewPoint  --iceWaterPhase BOTH --temperaturePhaseSwitch -40C]) >>
    # [HumiditySpecific] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_15.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbhyb_reduit_test15_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_c_cor=0.0001)
    assert(res)

def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidité spécifique (HU) à partir de TD, avec option copy_input."""
    # Existe en python seulement 
    # Idem au test_15, pour tester l'option copy_input

    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb_reduit"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ['TT', 'HU'])
    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])

    es_df   = spookipy.DewPointDepression(tthu_df, 
                                        ice_water_phase='both', 
                                        temp_phase_switch=-40, 
                                        temp_phase_switch_unit='celsius').compute()
    estt_df = pd.concat([es_df, tt_df], ignore_index=True)

    td_df   = spookipy.TemperatureDewPoint(estt_df, 
                                         ice_water_phase='both', 
                                         temp_phase_switch=-40, 
                                         temp_phase_switch_unit='celsius').compute()
    tttd_df = pd.concat([td_df, tt_df], ignore_index=True)

    df      = spookipy.HumiditySpecific(tttd_df, 
                                        copy_input=True).compute()

    # write the result
    results_file = test_tmp_path / "test_16.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbhyb_reduit_test16_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_c_cor=0.0001)
    assert(res)

# Nouveau test - identique au test 8 mais avec option BOTH
def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidité spécifique (HU) à partir de l'humidité relative (HR), ice_water_phase = BOTH."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    meta_df = src_df0.loc[src_df0.nomvar.isin(
        ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

    tthr_df = src_df0.loc[(src_df0.nomvar.isin(["TT", "HR"])) & (src_df0.ip2 == 12)].reset_index(drop=True)

    new_df = pd.concat([meta_df, tthr_df], ignore_index=True)

    # compute HumiditySpecific
    df      = spookipy.HumiditySpecific(new_df, 
                                        ice_water_phase='both', 
                                        temp_phase_switch=273, 
                                        temp_phase_switch_unit='celsius'
                                        ).compute()

    # write the result
    results_file = test_tmp_path / "test_17.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "regpres_testWithHR_test17_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_18(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidité spécifique (HU) à partir du rapport de mélange de la vapeur d'eau (QV), option rpn, ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0, ['TT', 'ES'])
    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    es_df   = spookipy.DewPointDepression(ttes_df, 
                                          ice_water_phase='water',
                                          rpn=True
                                          ).compute()
    ttes_df = pd.concat([es_df, tt_df], ignore_index=True)

    qv_df   = spookipy.WaterVapourMixingRatio(ttes_df, 
                                              rpn=True
                                              ).compute()
    
    # compute HumiditySpecific
    df      = spookipy.HumiditySpecific(qv_df, 
                                        ice_water_phase='water', 
                                        rpn=True
                                        ).compute()

    results_file = test_tmp_path / "test_18.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "regpres_testWithQV_RPN_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_19(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'humidite specifique (HU) avec un fichier regpres (HR), option rpn, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    hr_df   = fstpy.select_with_meta(src_df0, ['HR'])
    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])
    tt_df   = spookipy.SetUpperBoundary(tt_df, 
                                        value=0.0).compute()

    tthr_df = pd.concat([tt_df, hr_df],ignore_index=True)

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute 
    df      = spookipy.HumiditySpecific(tthr_df, 
                                        ice_water_phase='both',
                                        rpn=True).compute()

    results_file = test_tmp_path / "test_19.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "regpres_testWithHR_RPN_test19_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)
