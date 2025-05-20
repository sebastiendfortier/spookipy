# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import pytest
import fstpy
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions2]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "TemperatureVirtual"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul avec un fichier hybrid."""
    # open and read source
    source0 = plugin_test_path / "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    input_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    # compute TemperatureVirtual
    df = spookipy.TemperatureVirtual(input_df).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [TemperatureVirtual]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "TemperatureVirtual_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert True


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul avec un fichier hybrid 5005."""
    # open and read source
    source0 = plugin_test_path / "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()

    input_df = fstpy.select_with_meta(src_df0, ["TT", "HR"])

    # compute TemperatureVirtual
    df = spookipy.TemperatureVirtual(input_df).compute()
    # [ReaderStd --input {sources[0]} --group5005] >>
    # [Select --fieldName TT,HR] >>
    # [TemperatureVirtual] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_2.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


# Les tests suivants sont nouveaux (n'existent pas dans Spooki)
# Les fichiers de comparaison ont ete crees avec la version Spooki

# Input pour test 3:
# "[ReaderStd --input   /home/spst900/dataV/saturationVapourPressure/v5.0.x/inputfiles/2014031800_024_regpres] >>
#  [Select --verticalLevel 1000@300] >> [GridCut --startPoint 100,100 --endPoint 200,200] >>
# ([Select -- fieldName TT]+[WaterVapourMixingRatio]) >> [Select --forecastHour 24] >>
# [Zap --nbitsForDataStorage E32] >> [WriterStd --output 2014031800_024_regpres_QV_small.std]"


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de VT a partir de QV precalcule, avec un fichier regpres."""
    # open and read source
    source0 = plugin_test_path / "2014031800_024_regpres_QV_small.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.TemperatureVirtual(src_df0).compute()

    # Modification pour matcher le fichier test cree tel que mentionne plus haut
    df.loc[:, "datyp"] = 5
    df.loc[df.nomvar != "!!", "nbits"] = 32
    df.loc[df.nomvar == "VT", "typvar"] = "PZ"

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2014031800_024_regpres_VT_with_QV_small.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert res


# Input pour tests 4 et 5:
# "[ReaderStd --input   /home/spst900/dataV/saturationVapourPressure/v5.0.x/inputfiles/2014031800_024_regpres] >>
#  [Select --fieldName TT,HU,ES --verticalLevel 1000@300 --forecastHour 24] >>
# [GridCut --startPoint 100,100 --endPoint 200,200] >>
# [Zap --nbitsForDataStorage E32] >> [WriterStd --output 2014031800_024_regpres_TTHUES_small.std]"


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de VT a partir de HU, avec un fichier regpres."""
    # open and read source
    source0 = plugin_test_path / "2014031800_024_regpres_TTHUES_small.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    input_df = fstpy.select_with_meta(src_df0, ["TT", "HU"])

    df = spookipy.TemperatureVirtual(input_df).compute()
    # [ReaderStd --input 2014031800_024_regpres_TTHUES.std] >> [Select --fieldName HU,TT] >>
    # [TemperatureVirtual] >>  [Zap --nbitsForDataStorage E32] >>
    # [WriterStd --output 2014031800_024_regpres_VT_with_HU_small.std]

    # Modification pour matcher le fichier test cree tel que mentionne plus haut
    df.loc[:, "datyp"] = 5
    df.loc[df.nomvar != "!!", "nbits"] = 32
    df.loc[df.nomvar == "VT", "typvar"] = "PZ"

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2014031800_024_regpres_VT_with_HU_small.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de VT a partir de ES, avec un fichier regpres."""
    # open and read source
    source0 = plugin_test_path / "2014031800_024_regpres_TTHUES_small.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    input_df = fstpy.select_with_meta(src_df0, ["TT", "ES"])

    df = spookipy.TemperatureVirtual(input_df).compute()

    # [ReaderStd --input 2014031800_024_regpres_TTHUES.std] >> [Select --fieldName ES,TT] >>
    # [TemperatureVirtual] >>  [Zap --nbitsForDataStorage E32] >>
    # [WriterStd --output 2014031800_024_regpres_VT_with_ES_small.std]

    # Modification pour matcher le fichier test cree tel que mentionne plus haut
    df.loc[:, "datyp"] = 5
    df.loc[df.nomvar != "!!", "nbits"] = 32
    df.loc[df.nomvar == "VT", "typvar"] = "PZ"

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2014031800_024_regpres_VT_with_ES_small.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de VT a partir de ES, resultat deja existant."""
    # open and read source
    source0 = plugin_test_path / "2014031800_024_regpres_VT_with_ES_small.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.TemperatureVirtual(src_df0).compute()

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2014031800_024_regpres_VT_with_ES_small.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
