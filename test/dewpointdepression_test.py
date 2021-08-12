# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki
import pandas as pd

pytestmark = [pytest.mark.to_skip]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/DewPointDepression/testsFiles/'

def test_1(plugin_test_dir):
    """Test #1 :  Calcul du point de rosée; utilisation de --iceWaterPhase BOTH mais sans --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute spooki.DewPointDepression
    with pytest.raises(spooki.DewPointDepressionError):
        _ = spooki.DewPointDepression(src_df0,ice_water_phase='both').compute()
    #[ReaderStd --input {sources[0]}] >> [DewPointDepression --iceWaterPhase BOTH ]



def test_3(plugin_test_dir):
    """Test #3 :  Calcul de l'écart du point de rosée (ES) à partir de l'humidité spécifique (HU)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0,['TT','HU'])

    #compute spooki.DewPointDepression
    df = spooki.DewPointDepression(src_df0,ice_water_phase='water').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >>
    # [DewPointDepression --iceWaterPhase WATER ] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

    df.loc[df.nomvar=='ES','etiket'] = 'G133K80N'
    # df.loc[:,'nbits']=32
    # df.loc[:,'datyp']=5
    #write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_hu_nonRpn_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/DewPointDepression/result_test_3'

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)

def test_5(plugin_test_dir):
    """Test #5 :  Calcul de l'écart du point de rosée (ES) à partir de l'humidité relative (HR)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0,['TT','HR'])

    #compute spooki.DewPointDepression
    df = spooki.DewPointDepression(src_df0,ice_water_phase='water').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HR] >>
    # [DewPointDepression --iceWaterPhase WATER ] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

    df.loc[df.nomvar=='ES','etiket'] = 'G133K80N'
    # df.loc[:,'nbits']=32
    # df.loc[:,'datyp']=5
    #write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_hr_nonRpn_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/DewPointDepression/result_test_5'

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_6(plugin_test_dir):
    """Test #6 :  Calcul de l'écart du point de rosée (ES) à partir de la température du point de rosée (TD), option --RPN."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0,['TT','HU'])

    tt_df = fstpy.select_with_meta(src_df0,['TT'])


    #compute spooki.DewPointDepression
    tdp_df = spooki.TemperatureDewPoint(src_df0,ice_water_phase='water').compute()

    src_df1 = pd.concat([tt_df,tdp_df],ignore_index=True)
    df = spooki.DewPointDepression(src_df1,ice_water_phase='water', rpn=True).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER])
    #  >> [DewPointDepression --iceWaterPhase WATER --RPN] >>
    # [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[df.nomvar=='ES','etiket'] = 'G133K80N'
    # df.loc[:,'nbits']=32
    # df.loc[:,'datyp']=5
    #write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_td_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/DewPointDepression/result_test_6'

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_7(plugin_test_dir):
    """Test #7 :  Calcul de l'écart du point de rosée (ES) à partir de la température du point de rosée (TD)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0,['TT','HU'])

    tt_df = fstpy.select_with_meta(src_df0,['TT'])


    #compute spooki.DewPointDepression
    tdp_df = spooki.TemperatureDewPoint(src_df0,ice_water_phase='water').compute()

    src_df1 = pd.concat([tt_df,tdp_df],ignore_index=True)
    df = spooki.DewPointDepression(src_df1,ice_water_phase='water').compute()

    df.loc[:,'etiket'] = 'G133K80N'
    # df.loc[:,'nbits']=32
    # df.loc[:,'datyp']=5
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >>
    # [DewPointDepression --iceWaterPhase WATER] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_td_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/DewPointDepression/result_test_7'

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_9(plugin_test_dir):
    """Test #9 :  Calcul de l'écart du point de rosée (ES) à partir du rapport de mélange de la vapeur d'eau (QV)."""
    # open and read source
    source0 = plugin_test_dir + "2011100712_012_glbhyb_QV"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute spooki.DewPointDepression
    df = spooki.DewPointDepression(src_df0,ice_water_phase='water').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [DewPointDepression --iceWaterPhase WATER] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

    df.loc[:,'etiket'] = 'G133K80N'
    # df.loc[:,'nbits']=32
    # df.loc[:,'datyp']=5
    #write the result
    results_file = TMP_PATH + "test_9.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_qv_nonRpn_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/DewPointDepression/result_test_9'
    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)
