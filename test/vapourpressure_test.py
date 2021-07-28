# -*- coding: utf-8 -*-
import fstpy.all as fstpy
import pytest
import pandas as pd
from test import TMP_PATH,TEST_PATH

import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/VapourPressure/testsFiles/'

def test_regtest_1(plugin_test_dir):
    """Test #1 :  Calcul de la pression de vapeur; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute VapourPressure
    with pytest.raises(spooki.VapourPressureError):
        _ = spooki.VapourPressure(src_df0, ice_water_phase='both', temp_phase_switch=-30, temp_phase_switch_unit='G').compute()
    #[ReaderStd --input {sources[0]}] >> [VapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]



def test_regtest_2(plugin_test_dir):
    """Test #2 :  Calcul de la pression de vapeur; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute VapourPressure
    with pytest.raises(spooki.VapourPressureError):
        _ = spooki.VapourPressure(src_df0, ice_water_phase='both', temp_phase_switch=-273.16, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [VapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]



def test_regtest_3(plugin_test_dir):
    """Test #3 :  Calcul de la pression de vapeur; utilisation d'une valeur invalide ( > borne maximale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute VapourPressure
    with pytest.raises(spooki.VapourPressureError):
        _ = spooki.VapourPressure(src_df0, ice_water_phase='both', temp_phase_switch=273.17, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [VapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]



def test_regtest_4(plugin_test_dir):
    """Test #4 :  Calcul de la pression de vapeur; utilisation d'une valeur invalide pour --iceWaterPhase."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute VapourPressure
    with pytest.raises(spooki.VapourPressureError):
        _ = spooki.VapourPressure(src_df0, ice_water_phase='invalide', temp_phase_switch=273.17, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >>  [VapourPressure --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]



def test_regtest_5(plugin_test_dir):
    """Test #5 : Calcul de la pression de vapeur avec un fichier hybrid (HU)."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0,['TT','HU'])
    #compute VapourPressure
    df = spooki.VapourPressure(tthu_df,ice_water_phase='both', temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >> 
    # [Select --fieldName TT,HU] >> 
    # [VapourPressure ] >> 
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]
    df.loc[:,'etiket'] = 'VAPRES'
    #write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "VapourPressure_hu_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_6(plugin_test_dir):
    """Test #6 : Calcul de la pression de vapeur avec un fichier hybrid (HU),  option --RPN."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0,['TT','HU'])

    #compute VapourPressure
    df = spooki.VapourPressure(tthu_df, rpn=True,ice_water_phase='both', temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >> 
    # [Select --fieldName TT,HU] >>
    #  [VapourPressure --RPN] >>
    #  [WriterStd --output {destination_path} --noMetadata --ignoreExtended]
    df.loc[:,'etiket'] = 'VAPRES'
    #write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnVapourPressure_hu_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_6a(plugin_test_dir):
    """Test #6a : Calcul de la pression de vapeur avec un fichier hybrid (HU)"""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0,['TT','HU'])

    #compute VapourPressure
    df = spooki.VapourPressure(tthu_df,ice_water_phase='both', temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >> 
    # [Select --fieldName TT,HU] >> 
    # [VapourPressure] >> 
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]
    df.loc[:,'etiket'] = 'VAPRES'
    #write the result
    results_file = TMP_PATH + "test_6a.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpnVapourPressure_hu_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_7(plugin_test_dir):
    """Test #7 : Calcul de la pression de vapeur avec un fichier hybrid (HR)."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0,['TT','HR'])

    #compute VapourPressure
    df = spooki.VapourPressure(tthr_df,ice_water_phase='both', temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >> 
    # [Select --fieldName TT,HR] >> 
    # [VapourPressure] >> 
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]
    df.loc[:,'etiket'] = 'VAPRES'
    #write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df,no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "VapourPressure_hr_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_9(plugin_test_dir):
    """Test #9 : Calcul de la pression de vapeur avec un fichier hybrid (ES)."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0,['TT','ES'])

    #compute VapourPressure
    df = spooki.VapourPressure(ttes_df,ice_water_phase='both', temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >> 
    # [Select --fieldName TT,ES] >> 
    # [VapourPressure] >> 
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_9.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "VapourPressure_es_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_11(plugin_test_dir):
    """Test #11 : Calcul de la pression de vapeur avec un fichier en pression (QV)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regeta_rdiag_hu"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute VapourPressure
    df = spooki.VapourPressure(src_df0,ice_water_phase='both', temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >> 
    # [VapourPressure ] >> 
    # [Zap --nbitsForDataStorage E32] >>
    #  [WriterStd --output {destination_path} --ignoreExtended]
    df = df.loc[df.nomvar=='VPPR']
    df.loc[:,'etiket'] = 'VAPRES'
    #write the result
    results_file = TMP_PATH + "test_11.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_regeta_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_12(plugin_test_dir):
    """Test #12 : Calcul de la pression de vapeur avec un fichier en pression (QV), option --RPN."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_regeta_rdiag_hu"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute VapourPressure
    df = spooki.VapourPressure(src_df0,rpn=True,ice_water_phase='both', temp_phase_switch=-40).compute()
    #[ReaderStd --input {sources[0]}] >> 
    # [VapourPressure --RPN] >> [Zap --nbitsForDataStorage E32] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]
    df = df.loc[df.nomvar=='VPPR']
    df.loc[:,'etiket'] = 'VAPRES'
    #write the result
    results_file = TMP_PATH + "test_12.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_regeta_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_13(plugin_test_dir):
    """Test #13 : Calcul de la pression de vapeur avec un fichier hybrid 5005 (ES)."""
    # open and read source
    source0 = plugin_test_dir + "minimal_HU_5005.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute VapourPressure
    df = spooki.VapourPressure(src_df0,rpn=True,ice_water_phase='both', temp_phase_switch=-40).compute()
    #['[ReaderStd --input {sources[0]} ] >> ', '
    # [VapourPressure --RPN] >> ', '
    # [WriterStd --output {destination_path} --noMetadata --ignoreExtended]']
    df = df.loc[df.nomvar=='VPPR']
    df.loc[:,'etiket'] = 'VAPRES'
    #write the result
    results_file = TMP_PATH + "test_13.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_13.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


