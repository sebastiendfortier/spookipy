# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

from spookipy.watervapourmixingratio.watervapourmixingratio import WaterVapourMixingRatio

import fstpy
import pandas as pd
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions, pytest.mark.humidity]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/DewPointDepression/testsFiles/'


def test_1(plugin_test_dir):
    """Calcul du point de rosée; utilisation de --iceWaterPhase BOTH mais sans --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.DewPointDepression
    with pytest.raises(spookipy.DewPointDepressionError):
        _ = spookipy.DewPointDepression(
            src_df0, ice_water_phase='both').compute()
    # [ReaderStd --input {sources[0]}] >> [DewPointDepression --iceWaterPhase BOTH ]


def test_3(plugin_test_dir):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité spécifique (HU)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'HU'])

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(src_df0, ice_water_phase='water').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >>
    # [DewPointDepression --iceWaterPhase WATER ] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

    df.loc[df.nomvar == 'ES', 'etiket'] = 'G133K80N'
    # df.loc[:,'nbits']=32
    # df.loc[:,'datyp']=5
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_hu_nonRpn_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_5(plugin_test_dir):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité relative (HR)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'HR'])

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(src_df0, ice_water_phase='water').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HR] >>
    # [DewPointDepression --iceWaterPhase WATER ] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

    df.loc[df.nomvar == 'ES', 'etiket'] = 'G133K80N'
    # df.loc[:,'nbits']=32
    # df.loc[:,'datyp']=5
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_hr_nonRpn_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir):
    """Calcul de l'écart du point de rosée (ES) à partir de la température du point de rosée (TD), option --RPN."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'HU'])

    tt_df = fstpy.select_with_meta(src_df0, ['TT'])

    # compute spookipy.DewPointDepression
    td_df = spookipy.TemperatureDewPoint(
        src_df0, ice_water_phase='water').compute()

    src_df1 = pd.concat([tt_df, td_df], ignore_index=True)
    df = spookipy.DewPointDepression(
        src_df1,
        ice_water_phase='water',
        rpn=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER])
    #  >> [DewPointDepression --iceWaterPhase WATER --RPN] >>
    # [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[df.nomvar == 'ES', 'etiket'] = 'G133K80N'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_td_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_7(plugin_test_dir):
    """Calcul de l'écart du point de rosée (ES) à partir de la température du point de rosée (TD)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'HU'])

    tt_df = fstpy.select_with_meta(src_df0, ['TT'])

    # compute spookipy.DewPointDepression
    tdp_df = spookipy.TemperatureDewPoint(
        src_df0, ice_water_phase='water').compute()

    src_df1 = pd.concat([tt_df, tdp_df], ignore_index=True)
    df = spookipy.DewPointDepression(src_df1, ice_water_phase='water').compute()

    df.loc[:, 'etiket'] = 'G133K80N'
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >>
    # [DewPointDepression --iceWaterPhase WATER] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_td_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_9(plugin_test_dir):
    """Calcul de l'écart du point de rosée (ES) à partir du rapport de mélange de la vapeur d'eau (QV)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb_QV"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(src_df0, ice_water_phase='water').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [DewPointDepression --iceWaterPhase WATER] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

    df.loc[:, 'etiket'] = 'G133K80N'
    # df.loc[:,'nbits']=32
    # df.loc[:,'datyp']=5
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_qv_nonRpn_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)  # ,e_max=)
    fstpy.delete_file(results_file)
    assert(res)

