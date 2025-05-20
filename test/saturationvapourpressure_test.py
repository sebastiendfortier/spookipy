# -*- coding: utf-8 -*-
from test import check_test_ssm_package
from spookipy.utils import VDECODE_IP_INFO

check_test_ssm_package()

import fstpy
import pytest
import spookipy
from spookipy.rmn_interface import RmnInterface

pytestmark = [pytest.mark.regressions, pytest.mark.regressions2, pytest.mark.humidity]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "SaturationVapourPressure"


def test_1(plugin_test_path):
    """Calcul de la pression de vapeur saturante; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SaturationVapourPressure
    with pytest.raises(spookipy.SaturationVapourPressureError):
        _ = spookipy.SaturationVapourPressure(
            src_df0, ice_water_phase="both", temp_phase_switch=-30, temp_phase_switch_unit="G"
        ).compute()
    # [ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]


def test_2(plugin_test_path):
    """Calcul de la pression de vapeur saturante; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SaturationVapourPressure
    with pytest.raises(spookipy.SaturationVapourPressureError):
        _ = spookipy.SaturationVapourPressure(
            src_df0, ice_water_phase="both", temp_phase_switch=-5, temp_phase_switch_unit="kelvin"
        ).compute()


def test_3(plugin_test_path):
    """Calcul de la pression de vapeur saturante; utilisation d'une valeur invalide ( < borne minimale en celsius) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SaturationVapourPressure
    with pytest.raises(spookipy.SaturationVapourPressureError):
        _ = spookipy.SaturationVapourPressure(
            src_df0, ice_water_phase="both", temp_phase_switch=-275, temp_phase_switch_unit="celsius"
        ).compute()


def test_4(plugin_test_path):
    """Calcul de la pression de vapeur saturante; utilisation d'une valeur invalide pour --iceWaterPhase."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SaturationVapourPressure
    with pytest.raises(spookipy.SaturationVapourPressureError):
        _ = spookipy.SaturationVapourPressure(
            src_df0, ice_water_phase="invalid", temp_phase_switch=273.17, temp_phase_switch_unit="kelvin"
        ).compute()
    # [ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]


def test_5(plugin_test_path):
    """Calcul de la pression de vapeur saturante; utilisation de --iceWaterPhase BOTH mais sans --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SaturationVapourPressure
    with pytest.raises(spookipy.SaturationVapourPressureError):
        _ = spookipy.SaturationVapourPressure(src_df0, ice_water_phase="both").compute()
    # [ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase BOTH ]


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur saturante avec un fichier hybrid,  ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SaturationVapourPressure
    df = spookipy.SaturationVapourPressure(src_df0, ice_water_phase="water").compute()
    # [ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase WATER] >>
    #  [WriterStd --output {destination_path} --noMetadata]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SaturationVapourPressure_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.002)
    assert res


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur saturante avec un fichier hybrid 5005,  ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "minimal_4conve_5005.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SaturationVapourPressure
    df = spookipy.SaturationVapourPressure(
        src_df0, ice_water_phase="both", temp_phase_switch=-40, temp_phase_switch_unit="celsius"
    ).compute()

    # ['[ReaderStd --input {sources[0]}] >> ', '[SaturationVapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
    # [WriterStd --output {destination_path} --noMetadata]']

    # write the result
    results_file = test_tmp_path / "test_7.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SaturationVapourPressure_test7_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.002)
    assert res


# Test qui etait en commentaire dans la version Spooki.
#
# Creation du fichier input de la facon suivante:
# /apps/spooki_run  "[ReaderStd --input hyb_prog_2012071312_009_1HY ] >>
# [Select --fieldName WW,WD,UU,VV,UV --exclude] >>
# [GridCut --startPoint 0,0 --endPoint 90,110]
def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur saturante avec un fichier hybrid, option rpn, ice_water_phase = water."""

    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY_reduit"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SaturationVapourPressure
    df = spookipy.SaturationVapourPressure(src_df0, ice_water_phase="water", rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SaturationVapourPressure_test8_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur saturante avec un fichier regeta, option rpn, ice_water_phase = both."""

    # open and read source
    source0 = plugin_test_path / "2011100712_012_regeta"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    tt_df = fstpy.select_with_meta(src_df0, ["TT"])

    # compute SaturationVapourPressure
    df = spookipy.SaturationVapourPressure(
        tt_df, ice_water_phase="both", temp_phase_switch=273, temp_phase_switch_unit="celsius", rpn=True
    ).compute()

    # Equivalent a --IP1EncodingStyle OLDSTYLE
    df = spookipy.convip(df, style=RmnInterface.CONVIP_ENCODE_OLD)

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SaturationVapourPressure_test9_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res
