# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions2, pytest.mark.humidity]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "VapourPressure"


def test_1(plugin_test_path):
    """Calcul de la pression de vapeur; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    with pytest.raises(spookipy.VapourPressureError):
        _ = spookipy.VapourPressure(
            src_df0, ice_water_phase="both", temp_phase_switch=-30, temp_phase_switch_unit="G"
        ).compute()
    # [ReaderStd --input {sources[0]}] >> [VapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]


def test_2(plugin_test_path):
    """Calcul de la pression de vapeur; utilisation de valeur invalide ( < borne minimale en kelvin) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    with pytest.raises(spookipy.VapourPressureError):
        _ = spookipy.VapourPressure(
            src_df0, ice_water_phase="both", temp_phase_switch=-5, temp_phase_switch_unit="kelvin"
        ).compute()


def test_3(plugin_test_path):
    """Calcul de la pression de vapeur; utilisation d'une valeur invalide ( < borne minimale en celsius) pour -temperaturePhaseSwitch."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    with pytest.raises(spookipy.VapourPressureError):
        _ = spookipy.VapourPressure(
            src_df0, ice_water_phase="both", temp_phase_switch=-280, temp_phase_switch_unit="celsius"
        ).compute()


def test_4(plugin_test_path):
    """Calcul de la pression de vapeur; utilisation d'une valeur invalide pour --iceWaterPhase."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    with pytest.raises(spookipy.VapourPressureError):
        _ = spookipy.VapourPressure(
            src_df0, ice_water_phase="invalide", temp_phase_switch=273.17, temp_phase_switch_unit="kelvin"
        ).compute()
    # [ReaderStd --input {sources[0]}] >>  [VapourPressure --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier hybrid (HU),  ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    # compute VapourPressure
    df = spookipy.VapourPressure(tthu_df).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # [VapourPressure ] >>
    # [WriterStd --output {destination_path} --noMetadata]

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "VapourPressure_hu_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier hybrid (HU),  option rpn, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    # compute VapourPressure
    df = spookipy.VapourPressure(tthu_df, rpn=True).compute()

    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HU] >>
    # [VapourPressure --RPN] >>
    # [WriterStd --output {destination_path} --noMetadata]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "rpnVapourPressure_hu_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier hybrid (HR)"""
    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    # compute VapourPressure
    df = spookipy.VapourPressure(tthr_df).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [VapourPressure] >>
    # [WriterStd --output {destination_path} --noMetadata]

    # write the result
    results_file = test_tmp_path / "test_7.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "VapourPressure_hr_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier hybrid (HR), option rpn, ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    # compute VapourPressure
    df = spookipy.VapourPressure(tthr_df, ice_water_phase="water", rpn=True).compute()

    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "rpnVapourPressure_hr_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier hybrid (ES), ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0, ["TT", "ES"])

    # compute VapourPressure
    df = spookipy.VapourPressure(ttes_df).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT,ES] >>
    # [VapourPressure] >>
    # [WriterStd --output {destination_path} --noMetadata]

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "VapourPressure_es_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.05)
    assert res


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier hybrid (ES), option rpn, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0, ["TT", "ES"])

    # compute VapourPressure
    df = spookipy.VapourPressure(ttes_df, rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_10.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "rpnVapourPressure_es_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier en pression (QV), ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regeta_rdiag_hu"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    df = spookipy.VapourPressure(src_df0).compute()

    # [ReaderStd --input {sources[0]}] >>
    # [VapourPressure ] >>
    # [Zap --nbitsForDataStorage E32] >>
    #  [WriterStd --output {destination_path}]

    # Pour respecter les zap
    df.loc[df.nomvar == "VPPR", "typvar"] = "PZ"
    df.loc[df.nomvar == "VPPR", "datyp"] = 5  # Correspond a E
    df.loc[df.nomvar == "VPPR", "nbits"] = 32

    # write the result
    results_file = test_tmp_path / "test_11.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_regeta_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier en pression (QV), option rpn, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regeta_rdiag_hu"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    df = spookipy.VapourPressure(src_df0, rpn=True).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [VapourPressure --RPN] >> [Zap --nbitsForDataStorage E32] >>
    # [WriterStd --output {destination_path}]

    # Pour respecter les zap
    df.loc[df.nomvar == "VPPR", "typvar"] = "PZ"
    df.loc[df.nomvar == "VPPR", "datyp"] = 5  # Correspond a E
    df.loc[df.nomvar == "VPPR", "nbits"] = 32

    # write the result
    results_file = test_tmp_path / "test_12.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_regeta_file2cmp_20230426.std"

    # compare results
    # res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier hybrid 5005 (ES), ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "minimal_HU_5005.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute VapourPressure
    df = spookipy.VapourPressure(src_df0, rpn=True).compute()
    # ['[ReaderStd --input {sources[0]} ] >> ', '
    # [VapourPressure --RPN] >> ', '
    # [WriterStd --output {destination_path} --noMetadata]']

    # write the result
    results_file = test_tmp_path / "test_13.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "coord_5005_hu_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier hybrid (HU)"""
    # Identique au test 7, avec un sous-ensemble du fichier d'input, pour tester option copy_input

    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Creation d'un fichier reduit a quelques niveaux
    meta_df = src_df0.loc[src_df0.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(
        drop=True
    )
    tthu_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])
    tthu_reduit = tthu_df.loc[((tthu_df.level <= 1.0) & (tthu_df.level > 0.95))].reset_index(drop=True)
    df_reduit = pd.safe_concat([tthu_reduit, meta_df])

    # compute VapourPressure
    df = spookipy.VapourPressure(df_reduit, copy_input=True).compute()

    # write the result
    results_file = test_tmp_path / "test_14.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "VapourPressure_test14_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier regpres (HR), ice_water_phase=water."""

    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthr_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    df = spookipy.VapourPressure(tthr_df, ice_water_phase="water").compute()

    results_file = test_tmp_path / "test_15.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "VapourPressure_hr_test15_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier regpres (ES), ice_water_phase=water."""

    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0, ["TT", "ES"])

    df = spookipy.VapourPressure(ttes_df, ice_water_phase="water").compute()

    results_file = test_tmp_path / "test_16.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "VapourPressure_es_test16_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.03)
    assert res


def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier regpres (QV), ice_water_phase=both."""

    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0, ["TT"])

    qv_df = spookipy.WaterVapourMixingRatio(src_df0).compute()
    ttqv_df = pd.safe_concat([tt_df, qv_df])

    df = spookipy.VapourPressure(ttqv_df, ice_water_phase="both").compute()

    results_file = test_tmp_path / "test_17.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "VapourPressure_qv_test17_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_18(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier regpres (ES), option rpn, ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    ttes_df = fstpy.select_with_meta(src_df0, ["TT", "ES"])

    # compute VapourPressure
    df = spookipy.VapourPressure(ttes_df, ice_water_phase="water", rpn=True).compute()

    results_file = test_tmp_path / "test_18.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "rpnVapourPressure_es_test18_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_19(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier regpres (HR), option rpn, ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0, ["TT"])
    hr_df = fstpy.select_with_meta(src_df0, ["HR"])

    tt_df = spookipy.SetUpperBoundary(tt_df, value=0.0).compute()
    tthr_df = pd.safe_concat([tt_df, hr_df])

    # compute VapourPressure
    df = spookipy.VapourPressure(
        tthr_df, ice_water_phase="both", temp_phase_switch=273, temp_phase_switch_unit="celsius", rpn=True
    ).compute()

    results_file = test_tmp_path / "test_19.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "rpnVapourPressure_hr_test19_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_20(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier regpres (TD), ice_water_phase = both."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    es_df = fstpy.select_with_meta(src_df0, ["ES"])
    tt_df = fstpy.select_with_meta(src_df0, ["TT"])
    ttes_df = pd.safe_concat([tt_df, es_df])

    td_df = spookipy.TemperatureDewPoint(ttes_df, ice_water_phase="water").compute()

    tttd_df = pd.safe_concat([tt_df, td_df])

    # compute VapourPressure
    df = spookipy.VapourPressure(tttd_df, ice_water_phase="both").compute()

    # write the result
    results_file = test_tmp_path / "test_20.std"
    print(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "VapourPressure_td_test20_file2cmp.std"

    # # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.03)
    assert res


def test_21(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier hybrid (HU),  ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    # compute VapourPressure
    df = spookipy.VapourPressure(tthu_df, ice_water_phase="water").compute()

    # write the result
    results_file = test_tmp_path / "test_21.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "VapourPressure_hu_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_22(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la pression de vapeur avec un fichier hybrid (HU),  option rpn, ice_water_phase = water."""
    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tthu_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    # compute VapourPressure
    df = spookipy.VapourPressure(tthu_df, ice_water_phase="water", rpn=True).compute()

    # write the result
    results_file = test_tmp_path / "test_22.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "rpnVapourPressure_hu_file2cmp_20230426.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


def test_23(plugin_test_path, test_tmp_path, call_fstcomp):
    """2 groupes de TT avec dates d'origine differentes mais dates de validity identiques"""

    source = plugin_test_path / "Regeta_TTHUES_differentDateoSameDatev.std"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    # compute VapourPressure
    df = spookipy.VapourPressure(src_df, ice_water_phase="water").compute()

    # write the result
    results_file = test_tmp_path / "test_23.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    file_to_compare = plugin_test_path / "Regeta_test23_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
