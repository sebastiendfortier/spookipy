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
    return TEST_PATH + '/VapourPressure/testsFiles/'


def test_1(plugin_test_dir):
    """Calcul de la pression de vapeur; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    with pytest.raises(spookipy.VapourPressureError):
        _ = spookipy.VapourPressure(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=-30,
            temp_phase_switch_unit='G').compute()
    # [ReaderStd --input {sources[0]}] >> [VapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]


def test_2(plugin_test_dir):
    """Calcul de la pression de vapeur; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    with pytest.raises(spookipy.VapourPressureError):
        _ = spookipy.VapourPressure(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=-273.16,
            temp_phase_switch_unit='kelvin').compute()
    # [ReaderStd --input {sources[0]}] >> [VapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]


def test_3(plugin_test_dir):
    """Calcul de la pression de vapeur; utilisation d'une valeur invalide ( > borne maximale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    with pytest.raises(spookipy.VapourPressureError):
        _ = spookipy.VapourPressure(
            src_df0,
            ice_water_phase='both',
            temp_phase_switch=273.17,
            temp_phase_switch_unit='kelvin').compute()
    # [ReaderStd --input {sources[0]}] >> [VapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]


def test_4(plugin_test_dir):
    """Calcul de la pression de vapeur; utilisation d'une valeur invalide pour --iceWaterPhase."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    with pytest.raises(spookipy.VapourPressureError):
        _ = spookipy.VapourPressure(
            src_df0,
            ice_water_phase='invalide',
            temp_phase_switch=273.17,
            temp_phase_switch_unit='kelvin').compute()
    # [ReaderStd --input {sources[0]}] >>  [VapourPressure --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]


def test_5(plugin_test_dir):
    """Calcul de la pression de vapeur avec un fichier hybrid (HU)."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ['TT', 'HU'])

    # compute VapourPressure
    df = spookipy.VapourPressure(
        tthu_df,
        ice_water_phase='both',
        temp_phase_switch=-40).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # [VapourPressure ] >>
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    # df['datyp']=5
    # df.loc[df.nomvar!='!!','nbits']=32
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "VapourPressure_hu_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir):
    """Calcul de la pression de vapeur avec un fichier hybrid (HU),  option --RPN."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ['TT', 'HU'])

    # compute VapourPressure
    df = spookipy.VapourPressure(
        tthu_df,
        rpn=True,
        ice_water_phase='both',
        temp_phase_switch=-
        40).compute()

    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    #  [VapourPressure --RPN] >>
    #  [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    # df['datyp']=5
    # df.loc[df.nomvar!='!!','nbits']=32
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnVapourPressure_hu_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_7(plugin_test_dir):
    """Calcul de la pression de vapeur avec un fichier hybrid (HU)"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ['TT', 'HU'])

    # compute VapourPressure
    df = spookipy.VapourPressure(
        tthu_df,
        ice_water_phase='both',
        temp_phase_switch=-
        40).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # [VapourPressure] >>
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    # df['datyp']=5
    # df.loc[df.nomvar!='!!','nbits']=32
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnVapourPressure_hu_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_8(plugin_test_dir):
    """Calcul de la pression de vapeur avec un fichier hybrid (HR)."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ['TT', 'HR'])

    # compute VapourPressure
    df = spookipy.VapourPressure(
        tthr_df,
        ice_water_phase='both',
        temp_phase_switch=-
        40).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [VapourPressure] >>
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    # write the result
    # df['datyp']=5
    # df.loc[df.nomvar!='!!','nbits']=32
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "VapourPressure_hr_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_9(plugin_test_dir):
    """Calcul de la pression de vapeur avec un fichier hybrid (ES)."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0, ['TT', 'ES'])

    # compute VapourPressure
    df = spookipy.VapourPressure(
        ttes_df,
        ice_water_phase='both',
        temp_phase_switch=-
        40).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,ES] >>
    # [VapourPressure] >>
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    # df['datyp']=5
    # df.loc[df.nomvar!='!!','nbits']=32
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "VapourPressure_es_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_11(plugin_test_dir):
    """Calcul de la pression de vapeur avec un fichier en pression (QV)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regeta_rdiag_hu"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # px_df = spookipy.Pressure(src_df0,reference_field='QV')
    # print(px_df)
    # print(src_df0[['grid','nomvar','forecast_hour']].to_string())
    # compute VapourPressure
    df = spookipy.VapourPressure(
        src_df0,
        ice_water_phase='both',
        temp_phase_switch=-40).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [VapourPressure ] >>
    # [Zap --nbitsForDataStorage E32] >>
    #  [WriterStd --output {destination_path} --ignoreExtended]

    df.loc[df.nomvar.isin(['>>', '^^', 'P0']), 'etiket'] = '580V0'
    df.loc[df.nomvar=='VPPR', 'typvar'] = 'P'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_regeta_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_12(plugin_test_dir):
    """Calcul de la pression de vapeur avec un fichier en pression (QV), option --RPN."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regeta_rdiag_hu"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    df = spookipy.VapourPressure(
        src_df0,
        rpn=True,
        ice_water_phase='both',
        temp_phase_switch=-
        40).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [VapourPressure --RPN] >> [Zap --nbitsForDataStorage E32] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    # df = df.loc[df.nomvar=='VPPR']

    df.loc[df.nomvar.isin(['>>', '^^', 'P0']), 'etiket'] = '580V0'
    df.loc[df.nomvar=='VPPR', 'typvar'] = 'P'
    # df['datyp']=5
    # df.loc[df.nomvar!='!!','nbits']=32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_regeta_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_13(plugin_test_dir):
    """Calcul de la pression de vapeur avec un fichier hybrid 5005 (ES)."""
    # open and read source
    source0 = plugin_test_dir + "minimal_HU_5005.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    df = spookipy.VapourPressure(
        src_df0,
        rpn=True,
        ice_water_phase='both',
        temp_phase_switch=-40).compute()
    # ['[ReaderStd --input {sources[0]} ] >> ', '
    # [VapourPressure --RPN] >> ', '
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]']

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_13.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_14(plugin_test_dir):
    """Calcul de la pression de vapeur avec un fichier hybrid (HU)"""
     # Identique au test 7, avec un sous-ensemble du fichier d'input, pour tester option copy_input
    
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Creation d'un fichier reduit a quelques niveaux 
    meta_df = src_df0.loc[src_df0.nomvar.isin(
            ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)
    tthu_df = fstpy.select_with_meta(src_df0, ['TT', 'HU'])
    tthu_df_reduit = tthu_df.loc[((tthu_df.level <= 1.0) & (tthu_df.level > 0.95))].reset_index(drop=True)
    df_reduit = pd.concat([tthu_df_reduit, meta_df],ignore_index=True)

    # compute VapourPressure
    df = spookipy.VapourPressure(
        df_reduit,
        ice_water_phase='both',
        temp_phase_switch=-40, 
        copy_input=True).compute()

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_14.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "VapourPressure_test14_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
