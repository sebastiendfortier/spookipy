# -*- coding: utf-8 -*-
import fstpy.all as fstpy
import pytest
from test import TMP_PATH,TEST_PATH

import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/SaturationVapourPressure/testsFiles/'


def test_regtest_1(plugin_test_dir):
    """Test #1 :  Calcul de la pression de vapeur saturante; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute SaturationVapourPressure
    with pytest.raises(spooki.SaturationVapourPressureError):
        _ = spooki.SaturationVapourPressure(src_df0,ice_water_phase='both', temp_phase_switch=-30, temp_phase_switch_unit='G').compute()
    #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]



def test_regtest_2(plugin_test_dir):
    """Test #2 :  Calcul de la pression de vapeur saturante; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute SaturationVapourPressure
    with pytest.raises(spooki.SaturationVapourPressureError):
        _ = spooki.SaturationVapourPressure(src_df0,ice_water_phase='both', temp_phase_switch=-273.16, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]


def test_regtest_3(plugin_test_dir):
    """Test #3 :  Calcul de la pression de vapeur saturante; utilisation d'une valeur invalide ( > borne maximale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute SaturationVapourPressure
    with pytest.raises(spooki.SaturationVapourPressureError):
        _ = spooki.SaturationVapourPressure(src_df0,ice_water_phase='both', temp_phase_switch=273.17, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]



def test_regtest_4(plugin_test_dir):
    """Test #4 :  Calcul de la pression de vapeur saturante; utilisation d'une valeur invalide pour --iceWaterPhase."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute SaturationVapourPressure
    with pytest.raises(spooki.SaturationVapourPressureError):
        _ = spooki.SaturationVapourPressure(src_df0,ice_water_phase='invalid', temp_phase_switch=273.17, temp_phase_switch_unit='kelvin').compute()
    #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]



def test_regtest_5(plugin_test_dir):
    """Test #5 :  Calcul de la pression de vapeur saturante; utilisation de --iceWaterPhase BOTH mais sans --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_dir + "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute SaturationVapourPressure
    with pytest.raises(spooki.SaturationVapourPressureError):
        _ = spooki.SaturationVapourPressure(src_df0,ice_water_phase='both').compute()
    #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase BOTH ]


def test_regtest_6(plugin_test_dir):
    """Test #6 : Calcul de la pression de vapeur saturante avec un fichier hybrid."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute SaturationVapourPressure
    df = spooki.SaturationVapourPressure(src_df0,ice_water_phase='water').compute()
    #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase WATER] >> [WriterStd --output {destination_path} --ignoreExtended]

    df.loc[df.nomvar=='SVP','etiket']='SVPRES'
    df.loc[df.nomvar.isin(['HY','P0']),'etiket']='580V0'

    #write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "SaturationVapourPressure_file2cmp.std"
    # file_to_compare = '/fs/site4/eccc/cmd/w/sbf000/testFiles/SaturationVapourPressure/res_test_6.std'

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.01,e_moy=0.001)#,e_max=0.01,e_moy=0.01
    fstpy.delete_file(results_file)
    assert(res == True)


def test_regtest_7(plugin_test_dir):
    """Test #7 : Calcul de la pression de vapeur saturante avec un fichier hybrid 5005."""
    # open and read source
    source0 = plugin_test_dir + "minimal_4conve_5005.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute SaturationVapourPressure
    df = spooki.SaturationVapourPressure(src_df0,ice_water_phase='both', temp_phase_switch=-40, temp_phase_switch_unit='celsius').compute()
    #['[ReaderStd --input {sources[0]}] >> ', '[SaturationVapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]']

    df.loc[df.nomvar=='SVP','etiket']='SVPRES'
    df.loc[df.nomvar.isin(['!!','^^','>>','HY','P0']),'etiket']='_V710_'

    # df.loc[:,'nbits'] = 32
    # df.loc[:,'datyp'] = 5
    #write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_7.std"
    # file_to_compare = '/fs/site4/eccc/cmd/w/sbf000/testFiles/SaturationVapourPressure/res_test_7.std'

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res == True)


