# -*- coding: utf-8 -*-
import fstpy.all as fstpy
import pytest
import pandas as pd
from test import TMP_PATH,TEST_PATH, convip

import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/TemperatureDewPoint/testsFiles/'


def test_1(plugin_test_dir):
    """Test #1 :  Calcul du point de rosée; utilisation de --iceWaterPhase BOTH mais sans --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute TemperatureDewPoint
    with pytest.raises(spooki.TemperatureDewPointError):
        _ = spooki.TemperatureDewPoint(src_df0, ice_water_phase='both').compute()
    #[ReaderStd --input {sources[0]}] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH ]


def test_2(plugin_test_dir):
    """Test #2 :  Calcul du point de rosée; utilisation de --iceWaterPhase avec une valeur invalide."""
    # open and read source
    source0 = plugin_test_dir + "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute TemperatureDewPoint
    with pytest.raises(spooki.TemperatureDewPointError):
        _ = spooki.TemperatureDewPoint(src_df0, ice_water_phase='ice').compute()
    #[ReaderStd --input {sources[0]}] >>
    # [TemperatureDewPoint --iceWaterPhase ICE ]


def test_3(plugin_test_dir):
    """Test #3 :  Calcul du point de rosée; unité de --temperaturePhaseSwitch invalide."""
    # open and read source
    source0 = plugin_test_dir + "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute TemperatureDewPoint
    with pytest.raises(spooki.TemperatureDewPointError):
        _ = spooki.TemperatureDewPoint(src_df0, ice_water_phase='both', temp_phase_switch=-10, temp_phase_switch_unit='G').compute()
    #[ReaderStd --input {sources[0]}] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40G ]



def test_4(plugin_test_dir):
    """Test #4 :  Calcul du point de rosée à partir d'une matrice de températures de 5x4x3 et d'écarts de point de rosée de 5x4x2"""
    # open and read source
    source0 = plugin_test_dir + "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute TemperatureDewPoint
    df = spooki.TemperatureDewPoint(src_df0, ice_water_phase='both', temp_phase_switch=-40, temp_phase_switch_unit='celsius').compute()
    #[ReaderStd --input {sources[0]}] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df.loc[:,'etiket'] = 'DEWPTT'
    df.loc[:,'datyp'] = 5
    df.loc[:,'nbits'] = 32
    #write the result
    results_file = TMP_PATH + "test_4.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "TemperatureDewPoint_file2cmp.std"
    file_to_compare = "/home/sbf000/data/testFiles/TemperatureDewPoint/result_test_4"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_5(plugin_test_dir):
    """Test #5 :  Calcul du point de rosée à partir d'un fichier du global hybrid en utilisant TT et ES."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0,['TT','ES'])

    #compute TemperatureDewPoint
    df = spooki.TemperatureDewPoint(ttes_df, ice_water_phase='both', temp_phase_switch=-40, temp_phase_switch_unit='celsius').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT,ES] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[df.nomvar=='TD','etiket'] = 'DEWPTT'
    df.loc[:,'datyp'] = 5
    df.loc[:,'nbits'] = 32
    #write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_es_file2cmp.std"
    file_to_compare = "/home/sbf000/data/testFiles/TemperatureDewPoint/result_test_5"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_6(plugin_test_dir):
    """Test #6 :  Calcul du point de rosée à partir d'un fichier du global hybrid en utilisant TT et ES, option --RPN."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0,['TT','ES'])

    #compute TemperatureDewPoint
    df = spooki.TemperatureDewPoint(ttes_df, ice_water_phase='both', temp_phase_switch=-40, rpn=True).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT,ES] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH --RPN] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[df.nomvar=='TD','etiket'] = 'DEWPTT'
    df.loc[:,'datyp'] = 5
    df.loc[:,'nbits'] = 32
    #write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "rpn2011100712_012_glbhyb_es_file2cmp.std"
    file_to_compare = "/home/sbf000/data/testFiles/TemperatureDewPoint/result_test_6"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_7(plugin_test_dir):
    """Test #7 :  Calcul du point de rosée à partir d'un fichier du global hybrid en utilisant TT et HR."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0,['TT','HR'])

    #compute TemperatureDewPoint
    df = spooki.TemperatureDewPoint(tthr_df, ice_water_phase='both', temp_phase_switch=-40, temp_phase_switch_unit='celsius').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[df.nomvar=='TD','etiket'] = 'DEWPTT'
    df.loc[:,'datyp'] = 5
    df.loc[:,'nbits'] = 32
    #write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_hr_file2cmp.std"
    file_to_compare = "/home/sbf000/data/testFiles/TemperatureDewPoint/result_test_7"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_9(plugin_test_dir):
    """Test #9 :  Calcul du point de rosée à partir d'un fichier du global hyb (TT et HU)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0,['TT','HU'])

    #compute TemperatureDewPoint
    df = spooki.TemperatureDewPoint(tthu_df, ice_water_phase='water').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # [TemperatureDewPoint --iceWaterPhase WATER] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[df.nomvar=='TD','etiket'] = 'DEWPTT'
    df.loc[:,'datyp'] = 5
    df.loc[:,'nbits'] = 32

    #write the result
    results_file = TMP_PATH + "test_9.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_hu_file2cmp.std"
    file_to_compare = "/home/sbf000/data/testFiles/TemperatureDewPoint/result_test_9"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_11(plugin_test_dir):
    """Test #11 :  Calcul du point de rosée à partir d'un fichier du global hybrid (TT et QV)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb_QV"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute TemperatureDewPoint
    df = spooki.TemperatureDewPoint(src_df0, ice_water_phase='water').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [TemperatureDewPoint --iceWaterPhase WATER ] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[df.nomvar=='TD','etiket'] = 'DEWPTT'
    df.loc[:,'datyp'] = 5
    df.loc[:,'nbits'] = 32

    #write the result
    results_file = TMP_PATH + "test_11.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_qv_file2cmp.std"
    file_to_compare = "/home/sbf000/data/testFiles/TemperatureDewPoint/result_test_11"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_12(plugin_test_dir):
    """Test #12 :  Calcul du point de rosée à partir d'un fichier du global hybrid 5005 (TT et HU)."""
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0,['TT','HU'])

    #compute TemperatureDewPoint
    df = spooki.TemperatureDewPoint(tthu_df, ice_water_phase='both', temp_phase_switch=-40, temp_phase_switch_unit='celsius').compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]} ] >> ', '
    # [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >> ', '
    # [WriterStd --output {destination_path} --ignoreExtended]']
    df.loc[df.nomvar=='TD','etiket'] = 'DEWPTT'
    # df.loc[df.nomvar=='TD','dateo']= 443004200
    df.loc[:,'datyp'] = 5
    df.loc[:,'nbits'] = 32
    df = convip(df,'TD,')
    #write the result
    results_file = TMP_PATH + "test_12.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_12.std"
    file_to_compare = "/home/sbf000/data/testFiles/TemperatureDewPoint/result_test_12"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    # fstpy.delete_file(results_file)
    assert(res == True)
