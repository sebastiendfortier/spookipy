# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy
from fstpy.dataframe_utils import select_with_meta

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "GeorgeKIndex"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'indice à partir d'une matrice de températures de 5x4x3 et d'écarts de point de rosée de 5x4x2"""
    # open and read source
    source0 = plugin_test_path / "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GeorgeKIndex
    df = spookipy.GeorgeKIndex(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "TTES_GeorgeKIndex_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'indice avec un vrai fichier de données"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GeorgeKIndex
    df = spookipy.GeorgeKIndex(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "GeorgeKIndex_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'indice avec un fichier de données contenant TT et TD mais pas ES"""
    # open and read source
    source0 = plugin_test_path / "inputFileSimpleTD_TT.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GeorgeKIndex
    df = spookipy.GeorgeKIndex(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "TTTD_GeorgeKIndex_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'indice avec un fichier contenant des TT et des ES d'unités différentes"""
    # open and read source
    source0 = plugin_test_path / "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = select_with_meta(src_df0, ["TT"])

    es_df = select_with_meta(src_df0, ["ES"])

    src_df = pd.safe_concat([tt_df, es_df])
    # compute GeorgeKIndex
    df = spookipy.GeorgeKIndex(src_df).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> ( ([Select --fieldName TT] >> [UnitConvert --unit kelvin]) + [Select --fieldName ES] ) >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "TTES_GeorgeKIndex_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


# in python vertsion this works but produces only one result
# def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Calcul avec un fichier ayant plusieurs forecastHour - Ne doit pas fonctionner car des niveaux sont manquants pour un forecastHour"""
#     # open and read source
#     source0 = plugin_test_path / "2016122000_006_NatPres.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     #compute GeorgeKIndex
#     with pytest.raises(spookipy.GeorgeKIndexError):
#         df = spookipy.GeorgeKIndex(src_df0).compute()
#     print(df)
#     assert(False)
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex]


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul avec un fichier ayant plusieurs forecastHour"""
    # open and read source
    source0 = plugin_test_path / "2016122000_006_NatPres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    meta_df = src_df0.loc[src_df0.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(
        drop=True
    )
    fh6_df = src_df0.loc[src_df0.ip2 == 6].reset_index(drop=True)

    src_df = pd.safe_concat([meta_df, fh6_df])

    # compute GeorgeKIndex
    df = spookipy.GeorgeKIndex(src_df).compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]}] >>',
    # '[Select --forecastHour 6] >> [GeorgeKIndex] >> ',
    # '[WriterStd --output {destination_path} --ignoreExtended]']

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "TTES_2016122000_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
