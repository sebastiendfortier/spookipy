# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import pandas as pd
import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "SubtractElementsVertically"

def test_1(plugin_test_path):
    """Utilisation de --outputFieldName avec une valeur > 4 caractères - requete invalide."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    with pytest.raises(spookipy.SubtractElementsVerticallyError):
        _ = spookipy.SubtractElementsVertically(src_df0, direction='ascending', nomvar_out='TROPLONG').compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SubtractElementsVertically --outputFieldName TROPLONG --direction ASCENDING]

def test_2(plugin_test_path):
    """Effectue un test avec --outputFieldName mais plusieurs champs en entrée - requete invalide."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    with pytest.raises(spookipy.SubtractElementsVerticallyError):
        _ = spookipy.SubtractElementsVertically(src_df0, direction='ascending', nomvar_out='ABCD').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [SubtractElementsVertically --outputFieldName ABCD --direction ASCENDING]


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec 2 champs et 2 niveaux, option --direction ASCENDING"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    df      = spookipy.SubtractElementsVertically(src_df0, 
                                                  direction='ascending', 
                                                  reduce_df = True).compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SubtractElementsVertically --direction ASCENDING] >> 
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Nouveau fichier de comparaison avec nouvelle etiquette
    file_to_compare = plugin_test_path / "SubVert_test3_file2cmp.std+PY20240208"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier de 2 champs et 2 niveaux, option --direction DESCENDING"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    df      = spookipy.SubtractElementsVertically(src_df0, 
                                                  direction='descending',
                                                  reduce_df = True).compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SubtractElementsVertically --direction DESCENDING] >> 
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Nouveau fichier de comparaison sans --ignoreExtended ----encodeIP2andIP3 du test en CPP
    file_to_compare = plugin_test_path / "SubVert_test4_file2cmp.std+PY20240208"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier de 2 champs; selection d'un champ et --direction ASCENDING"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0,'ip_info')
    meta_df = src_df0.loc[src_df0.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)

    src_df0 = src_df0.loc[src_df0.level==500.]
    src_df  = pd.concat([meta_df,src_df0], ignore_index=True)

    # compute SubtractElementsVertically
    df      = spookipy.SubtractElementsVertically(src_df, 
                                                  direction='ascending', 
                                                  reduce_df=True).compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [Select --verticalLevel 500] >> 
    # [SubtractElementsVertically --direction ASCENDING] >> 
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Nouveau fichier de comparaison sans --ignoreExtended ----encodeIP2andIP3 du test en CPP
    file_to_compare = plugin_test_path / "SubVert_test5_file2cmp.std+PY20240208"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_6(plugin_test_path):
    """Test sur un fichier dont les champs possèdent des intervalles - requete invalide."""
    # open and read source
    source0 = plugin_test_path / "inputTest6.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    with pytest.raises(spookipy.SubtractElementsVerticallyError):
        _ = spookipy.SubtractElementsVertically(src_df0, direction='ascending').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [SubtractElementsVertically --direction ASCENDING]


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec 2 champs, plusieurs niveaux, differents forecastHours et --direction ASCENDING"""
    # open and read source
    source0 = plugin_test_path / "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    df      = spookipy.SubtractElementsVertically(src_df0, 
                                                  direction='ascending',
                                                  reduce_df=True).compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SubtractElementsVertically --direction ASCENDING] >> 
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    # Necessaire pour encodage des metadonnes
    df      = spookipy.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = test_tmp_path / "test_7.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Nouveau fichier sans --ignoreExtended ----encodeIP2andIP3 du test en CPP
    file_to_compare = plugin_test_path / "SubVert_test7_file2cmp.std+PY20240208"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec 2 champs, plusieurs niveaux, differents forecastHours et --direction DESCENDING"""
    # open and read source
    source0 = plugin_test_path / "TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute SubtractElementsVertically
    df      = spookipy.SubtractElementsVertically(src_df0, 
                                                  direction='descending',
                                                  reduce_df=True).compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [SubtractElementsVertically --direction DESCENDING] >> 
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # Nouveau fichier sans metadata et avec nouvelle etiquette
    file_to_compare = plugin_test_path / "SubVert_test8_file2cmp.std+PY20240208"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)
