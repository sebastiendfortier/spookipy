# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

from spookipy.watervapourmixingratio.watervapourmixingratio import WaterVapourMixingRatio

import fstpy
import pandas as pd
import pytest
import spookipy
import warnings

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1, pytest.mark.humidity]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "DewPointDepression"


def test_1(plugin_test_path):
    """Calcul du point de rosée; utilisation de --iceWaterPhase BOTH mais sans --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.DewPointDepression
    with pytest.raises(spookipy.DewPointDepressionError):
        _ = spookipy.DewPointDepression(src_df0, ice_water_phase="both").compute()
    # [ReaderStd --input {sources[0]}] >> [DewPointDepression --iceWaterPhase BOTH ]


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité spécifique (HU), option RPN, ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(src_df0, ice_water_phase="water", rpn=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >>
    # [DewPointDepression --iceWaterPhase WATER --RPN ]

    # write the result
    results_file = test_tmp_path / "test_2.std"

    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_hu_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)

    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité spécifique (HU), ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(src_df0, ice_water_phase="water").compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,HU] >>
    # [DewPointDepression --iceWaterPhase WATER ] >> [WriterStd --output {destination_path}]

    # df.loc[df['nomvar'].isin([">>", "^^", "HY", "P0"]), 'etiket'] = "G133K80_N"

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_hu_nonRpn_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité relative (HR), option RPN, ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(src_df0, ice_water_phase="water", rpn=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HR] >>
    # [DewPointDepression --iceWaterPhase WATER ]

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_hr_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité relative (HR), ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(src_df0, ice_water_phase="water").compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,HR] >>
    # [DewPointDepression --iceWaterPhase WATER ] >>
    #  [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_hr_nonRpn_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de la température du point de rosée (TD), option --RPN, ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    tt_df = fstpy.select_with_meta(src_df0, ["TT"])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute spookipy.DewPointDepression
    td_df = spookipy.TemperatureDewPoint(src_df0, ice_water_phase="water").compute()

    src_df1 = pd.safe_concat([tt_df, td_df])

    df = spookipy.DewPointDepression(src_df1, ice_water_phase="water", rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,HU] >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >>
    # [DewPointDepression --iceWaterPhase WATER --RPN] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_td_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de la température du point de rosée (TD), ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    tt_df = fstpy.select_with_meta(src_df0, ["TT"])

    # compute spookipy.DewPointDepression
    tdp_df = spookipy.TemperatureDewPoint(src_df0, ice_water_phase="water").compute()

    src_df1 = pd.safe_concat([tt_df, tdp_df])
    df = spookipy.DewPointDepression(src_df1, ice_water_phase="water").compute()

    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >>
    # [DewPointDepression --iceWaterPhase WATER] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_7.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_td_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir du rapport de mélange de la vapeur d'eau (QV), option RPN, ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb_QV"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(src_df0, ice_water_phase="water", rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [DewPointDepression --iceWaterPhase WATER]

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_qv_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir du rapport de mélange de la vapeur d'eau (QV), ice_water_phase = water ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb_QV"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(src_df0, ice_water_phase="water").compute()
    # [ReaderStd  --input {sources[0]}] >>
    # [DewPointDepression --iceWaterPhase WATER] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_qv_nonRpn_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité relative (HR) avec l'option copy_input."""
    # Existe en python seulement - test vide dans fichier json

    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb_reduit"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(src_df0, ice_water_phase="water", copy_input=True).compute()

    # write the result
    results_file = test_tmp_path / "test_10.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_glbhyb_hr_nonRpn_reduit_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité spécifique (TD), ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0, ["TT", "ES"])
    tt_df = fstpy.select_with_meta(src_df0, ["TT"])

    td_df = spookipy.TemperatureDewPoint(ttes_df, ice_water_phase="water").compute()

    tttd_df = pd.safe_concat([tt_df, td_df])

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(
        tttd_df, ice_water_phase="both", temp_phase_switch=273, temp_phase_switch_unit="celsius"
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_11.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_td_test11_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité spécifique (HR), ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(
        tthr_df, ice_water_phase="both", temp_phase_switch=273, temp_phase_switch_unit="celsius"
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_12.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_hr_test12_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir d'un fichier regpres (QV), ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0, ["TT"])

    qv_df = spookipy.WaterVapourMixingRatio(src_df0).compute()
    ttqv_df = pd.safe_concat([tt_df, qv_df])

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(
        ttqv_df, ice_water_phase="both", temp_phase_switch=273, temp_phase_switch_unit="celsius"
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_13.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_qv_test13_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité spécifique (HU), ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(
        tthu_df, ice_water_phase="both", temp_phase_switch=273, temp_phase_switch_unit="celsius"
    ).compute()

    # write the result
    results_file = test_tmp_path / "test_14.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_hu_test14_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.005)
    assert res


def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité spécifique (HU), option RPN, ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0, ["TT"])
    hu_df = fstpy.select_with_meta(src_df0, ["HU"])

    tt_df = spookipy.SetUpperBoundary(tt_df, value=0.0).compute()
    tthu_df = pd.safe_concat([tt_df, hu_df])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(tthu_df, ice_water_phase="both", rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_15.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_hu_rpn_test15_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.002)
    assert res


def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité spécifique (HR), option RPN, ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0, ["TT"])
    hr_df = fstpy.select_with_meta(src_df0, ["HR"])

    tt_df = spookipy.SetUpperBoundary(tt_df, value=0.0).compute()
    tthr_df = pd.safe_concat([tt_df, hr_df])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(tthr_df, ice_water_phase="both", rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_16.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_hr_rpn_test16_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.002)
    assert res


def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité relative (HR), fichier reduit du global hybrid, option rpn, ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY_4x4.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute DewPointDepression
    df = spookipy.DewPointDepression(tthr_df, ice_water_phase="both", rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_17.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbhyb_reduit_hr_Rpn_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.002)
    assert res


def test_18(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) a partir du melange de vapeur d'eau (QV), option RPN, ice_water_phase = both ."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0, ["TT"])
    tt_df = spookipy.SetUpperBoundary(tt_df, value=0.0).compute()
    qv_df = spookipy.WaterVapourMixingRatio(src_df0).compute()
    ttqv_df = pd.safe_concat([tt_df, qv_df])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(ttqv_df, ice_water_phase="both", rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_18.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_qv_rpn_test18_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.002)
    assert res


def test_19(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'écart du point de rosée (ES) à partir de l'humidité spécifique (TD), option RPN, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    es_df = fstpy.select_with_meta(src_df0, ["ES"])
    tt_df = fstpy.select_with_meta(src_df0, ["TT"])
    ttes_df = pd.safe_concat([tt_df, es_df])

    warnings.filterwarnings("ignore", category=UserWarning, module="spookipy")
    td_df = spookipy.TemperatureDewPoint(ttes_df, ice_water_phase="water").compute()
    tt_df = spookipy.SetUpperBoundary(tt_df, value=0.0).compute()
    tttd_df = pd.safe_concat([tt_df, td_df])

    # compute spookipy.DewPointDepression
    df = spookipy.DewPointDepression(tttd_df, ice_water_phase="both", rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_19.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_td_rpn_test19_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res
