# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy
import pandas as pd
import warnings

pytestmark = [pytest.mark.regressions, pytest.mark.regressions2, pytest.mark.humidity]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "TemperatureDewPoint"


def test_1(plugin_test_path):
    """Calcul du point de rosée; utilisation de --iceWaterPhase both mais sans --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TemperatureDewPoint
    with pytest.raises(spookipy.TemperatureDewPointError):
        _ = spookipy.TemperatureDewPoint(src_df0, ice_water_phase="both").compute()
    # [ReaderStd --input {sources[0]}] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH ]


def test_2(plugin_test_path):
    """Calcul du point de rosée; utilisation de --iceWaterPhase avec une valeur invalide."""
    # open and read source
    source0 = plugin_test_path / "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TemperatureDewPoint
    with pytest.raises(spookipy.TemperatureDewPointError):
        _ = spookipy.TemperatureDewPoint(src_df0, ice_water_phase="ice").compute()
    # [ReaderStd --input {sources[0]}] >>
    # [TemperatureDewPoint --iceWaterPhase ICE ]


def test_3(plugin_test_path):
    """Calcul du point de rosée; unité de --temperaturePhaseSwitch invalide."""
    # open and read source
    source0 = plugin_test_path / "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TemperatureDewPoint
    with pytest.raises(spookipy.TemperatureDewPointError):
        _ = spookipy.TemperatureDewPoint(
            src_df0, ice_water_phase="both", temp_phase_switch=-10, temp_phase_switch_unit="G"
        ).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40G ]


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'une matrice de températures de 5x4x3 et d'écarts de point de rosée de 5x4x2,  ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(
        src_df0, ice_water_phase="both", temp_phase_switch=-40, temp_phase_switch_unit="celsius"
    ).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "TemperatureDewPoint_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier du global hybrid en utilisant TT et ES."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0, ["TT", "ES"])

    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(
        ttes_df, ice_water_phase="both", temp_phase_switch=-40, temp_phase_switch_unit="celsius"
    ).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,ES] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_es_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier du global hybrid en utilisant TT et ES, option --RPN, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0, ["TT", "ES"])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(ttes_df, ice_water_phase="both", rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,ES] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH --RPN] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "rpn2011100712_012_glbhyb_es_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier du global hybrid en utilisant TT et HR, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(
        tthr_df, ice_water_phase="both", temp_phase_switch=-40, temp_phase_switch_unit="celsius"
    ).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_7.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_hr_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier du global hybrid en utilisant TT et HR, option rpn."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(tthr_df, ice_water_phase="both", rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [TemperatureDewPoint --iceWaterPhase BOTH --RPN] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "rpn2011100712_012_glbhyb_hr_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier du global hyb (TT et HU), ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(tthu_df, ice_water_phase="water").compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # [TemperatureDewPoint --iceWaterPhase WATER] >>
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_hu_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier du global hyb (TT et HU), option copy_input, ice_water_phase = water."""
    # Existe en python seulement - test vide dans fichier json

    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb_reduit"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(tthu_df, ice_water_phase="water", copy_input=True).compute()

    # write the result
    results_file = test_tmp_path / "test_10.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_test10_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier du global hybrid (TT et QV)."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb_QV"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(src_df0, ice_water_phase="water").compute()
    # [ReaderStd --input {sources[0]}] >>
    # [TemperatureDewPoint --iceWaterPhase WATER ] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_11.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_qv_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier du global hybrid 5005 (TT et HU) ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(
        tthu_df, ice_water_phase="both", temp_phase_switch=-40, temp_phase_switch_unit="celsius"
    ).compute()
    # ['[ReaderStd --input {sources[0]} ] >> ', '
    # [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >> ', '
    # [WriterStd --output {destination_path}]']

    df = spookipy.convip(df)
    # write the result
    results_file = test_tmp_path / "test_12.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "coord_5005_hu_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier contenant plusieurs forecast hours pour TT et ES."""

    # open and read source
    source0 = plugin_test_path / "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(src_df0, ice_water_phase="water").compute()

    # write the result
    results_file = test_tmp_path / "test_13.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "TemperatureDewPoint_test13_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier du global hybrid (TT et QV), option RPN, ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb_QV"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(src_df0, ice_water_phase="water", rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [TemperatureDewPoint --iceWaterPhase WATER ] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_15.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "rpn2011100712_012_glbhyb_qv_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.003)
    assert res


def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier du global hyb (TT et HU), option RPN, ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(tthu_df, ice_water_phase="water", rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # [TemperatureDewPoint --iceWaterPhase WATER --RPN] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_16.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "rpn2011100712_012_glbhyb_hu_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier regpres (QV), ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0, ["TT"])

    qv_df = spookipy.WaterVapourMixingRatio(src_df0).compute()
    ttqv_df = pd.safe_concat([tt_df, qv_df])

    # compute
    df = spookipy.TemperatureDewPoint(
        ttqv_df, ice_water_phase="both", temp_phase_switch=273, temp_phase_switch_unit="celsius"
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_17.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_qv_test17_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_18(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier regpres (HR), ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    # compute
    df = spookipy.TemperatureDewPoint(tthr_df, ice_water_phase="water").compute()

    # write the result
    results_file = test_tmp_path / "test_18.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_hr_test18_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_19(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier regpres (TT et HR), option RPN, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(tthr_df, ice_water_phase="both", rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_19.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_hr_rpn_test19_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_20(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier regpres (HU), option RPN, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(tthu_df, ice_water_phase="both", rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_20.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_hu_rpn_test20_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_21(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier regpres (QV), option RPN, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0, ["TT"])

    qv_df = spookipy.WaterVapourMixingRatio(src_df0).compute()
    ttqv_df = pd.safe_concat([tt_df, qv_df])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(ttqv_df, ice_water_phase="both", rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_21.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_qv_rpn_test21_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_22(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier regpres (TT et HR), option RPN, ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(tthr_df, ice_water_phase="water", rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_22.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_hr_rpn_test22_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_23(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul du point de rosée à partir d'un fichier du global hybrid en utilisant TT et ES, option --RPN, ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0, ["TT", "ES"])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute TemperatureDewPoint
    df = spookipy.TemperatureDewPoint(ttes_df, ice_water_phase="water", rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,ES] >>
    # [TemperatureDewPoint --iceWaterPhase WATER --RPN]

    # write the result
    results_file = test_tmp_path / "test_23.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_es_rpn_test23_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
