# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pandas as pd
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp
from fstpy.dataframe_utils import select_with_meta
from spookipy.matchlevelindextovalue.matchlevelindextovalue import \
    MatchLevelIndexToValueError

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/MatchLevelIndexToValue/testsFiles/'

def test_1(plugin_test_dir):
    """Test match one field - full computation."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uv_df = spooki.WindModulus(src_df0).compute()

    minmax_df = spooki.MinMaxLevelIndex(
        uv_df, nomvar="UV", max=True, nomvar_max_idx='IND').compute()

    # compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(minmax_df, nomvar_out='TEST').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [WindModulus] >>
    # [MinMaxLevelIndex --minMax MAX --direction UPWARD --outputFieldName2 IND] >>
    # [MatchLevelIndexToValue --outputFieldName TEST] >>[WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "lou_matchOneField_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_2(plugin_test_dir):
    """Tester l'option --outputFieldName avec plus d'un type de champ en entree."""
    # open and read source
    source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = select_with_meta(src_df0, ['TT'])

    minmax_df = spooki.MinMaxLevelIndex(
        src_df0, nomvar="TT", min=True, nomvar_min_idx='IND').compute()

    uuvv_df = select_with_meta(src_df0, ['UU', 'VV'])

    src_df = pd.concat([tt_df, minmax_df, uuvv_df], ignore_index=True)
    # compute MatchLevelIndexToValue
    with pytest.raises(MatchLevelIndexToValueError):
        _ = spooki.MatchLevelIndexToValue(src_df, nomvar_out='TEST').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # (
    # ( [Select --fieldName TT] >>  [MinMaxLevelIndex --minMax MIN --direction UPWARD --outputFieldName1 IND] ) + [Select --fieldName UU,VV]
    # ) >>
    # [MatchLevelIndexToValue --outputFieldName TEST] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

def test_4(plugin_test_dir):
    """Test match one field - full computation except uv."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_UV_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uv_df = spooki.WindModulus(src_df0).compute()

    minmax_df = spooki.MinMaxLevelIndex(
        uv_df, nomvar="UV", max=True, nomvar_max_idx='IND').compute()

    # compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(minmax_df, nomvar_out='TEST').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [WindModulus] >>
    # [MinMaxLevelIndex --minMax MAX --direction UPWARD --outputFieldName2 IND] >>
    # [MatchLevelIndexToValue --outputFieldName TEST] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "lou_matchOneField_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_5(plugin_test_dir):
    """Test match one field - full computation."""
    # open and read source
    source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uv_df = spooki.WindModulus(src_df0).compute()

    minmax_df = spooki.MinMaxLevelIndex(
        uv_df, nomvar="UV", max=True, nomvar_max_idx='IND').compute()

    # compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(minmax_df, nomvar_out='T5').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [WindModulus] >>
    # [MinMaxLevelIndex --minMax MAX --direction UPWARD --outputFieldName2 IND] >>
    # [MatchLevelIndexToValue --outputFieldName T5] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "lou_matchOneField2_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_7(plugin_test_dir):
    """Test match no fields."""
    # open and read source
    source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uv_df = spooki.WindModulus(src_df0).compute()

    #  ( [SetConstantValue --value -1.0 --bidimensional] >>  [Zap --fieldName IND --doNotFlagAsZapped]  )
    ind_df = spooki.SetConstantValue(
        uv_df, value=-1., bi_dimensionnal=True).compute()
    ind_df.loc[:, 'nomvar'] = 'IND'

    src_df = pd.concat([uv_df, ind_df], ignore_index=True)

    # compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(src_df, nomvar_out='TEST').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >>
    # (
    # [Copy] +  ( [SetConstantValue --value -1.0 --bidimensional] >>  [Zap --fieldName IND --doNotFlagAsZapped]  )
    # ) >>
    # [MatchLevelIndexToValue --outputFieldName TEST] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "lou_matchNoFields_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_8(plugin_test_dir):
    """Test match negative index - partial match."""
    # open and read source
    source0 = plugin_test_dir + "sortie_cpp_cld_200906290606"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "indneg.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(src_df, nomvar_out='T7').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} {sources[1]}] >>
    # [MatchLevelIndexToValue --outputFieldName T7] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_8.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "lou_matchNegativeIndex_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

# nouveaux tests   
def test_9(plugin_test_dir):
    """Identique au test 1 mais avec utilisation de l'objet interval."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uv_df = spooki.WindModulus(src_df0).compute()

    minmax_df = spooki.MinMaxLevelIndex(
        uv_df, 
        nomvar="UV", 
        max=True, 
        nomvar_max_idx='IND').compute()

    # compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(
        minmax_df, 
        nomvar_out='TEST',
        use_interval=True).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [WindModulus] >>
    # [MinMaxLevelIndex --minMax MAX --direction UPWARD --outputFieldName2 IND] >>
    # [MatchLevelIndexToValue --useIntervalObject --outputFieldName TEST] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --encodeIP2andIP3]

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = TMP_PATH + "test_9.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MatchLevel_file2cmp_test9.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_10(plugin_test_dir):
    """Identique au test 8 - avec objet interval."""
    # open and read source
    source0 = plugin_test_dir + "sortie_cpp_cld_200906290606"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "indneg.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(
        src_df, 
        nomvar_out='T7',
        use_interval=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} {sources[1]}] >>
    # [MatchLevelIndexToValue --useIntervalObject --outputFieldName T7] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --encodeIP2andIP3]

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = TMP_PATH + "test_10.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MatchLevel_file2cmp_test10.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_11(plugin_test_dir):
    """Test avec des fichiers ayant des grilles differentes mais les meme champs."""
    # open and read source
    source0 = plugin_test_dir + "200906290606_CLD_grid1.std"
    source1 = plugin_test_dir + "200906290606_TT_grid1.std"
    source2 = plugin_test_dir + "200906290606_IND_grid1.std"
    source3 = plugin_test_dir + "200906290606_CLD_grid2.std"
    source4 = plugin_test_dir + "200906290606_TT_grid2.std"
    source5 = plugin_test_dir + "200906290606_IND_grid2.std"

    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df2 = fstpy.StandardFileReader(source2).to_pandas()
    src_df3 = fstpy.StandardFileReader(source3).to_pandas()
    src_df4 = fstpy.StandardFileReader(source4).to_pandas()
    src_df5 = fstpy.StandardFileReader(source5).to_pandas()

    src_df = pd.concat([src_df0, src_df1, src_df2, src_df3, src_df4, src_df5], ignore_index=True)

    # compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(
        src_df, 
        use_interval=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} {sources[1]} {sources[2]} {sources[3]} {sources[4]} {sources[5]}] >>
    # [MatchLevelIndexToValue --useIntervalObject] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --encodeIP2andIP3]

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = TMP_PATH + "test_11.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MatchLevel_file2cmp_test11.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_12(plugin_test_dir):
    """Test avec des fichiers ayant des grilles differentes et un nombre de niveaux differents pour les meme champs."""
    # open and read source
    source0 = plugin_test_dir + "200906290606_CLD_grid1.std"
    source1 = plugin_test_dir + "200906290606_TT_grid1_lessLevels.std"
    source2 = plugin_test_dir + "200906290606_IND_grid1.std"
    source3 = plugin_test_dir + "200906290606_CLD_grid2.std"
    source4 = plugin_test_dir + "200906290606_TT_grid2.std"
    source5 = plugin_test_dir + "200906290606_IND_grid2.std"

    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df2 = fstpy.StandardFileReader(source2).to_pandas()
    src_df3 = fstpy.StandardFileReader(source3).to_pandas()
    src_df4 = fstpy.StandardFileReader(source4).to_pandas()
    src_df5 = fstpy.StandardFileReader(source5).to_pandas()

    src_df = pd.concat([src_df0, src_df1, src_df2, src_df3, src_df4, src_df5], ignore_index=True)

    # compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(
        src_df, 
        use_interval=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} {sources[1]} {sources[2]} {sources[3]} {sources[4]} {sources[5]}] >>
    # [MatchLevelIndexToValue --useIntervalObject] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --encodeIP2andIP3]

    # Encodage des ip2
    df = spooki.encode_ip2_and_ip3_height(df)

    # write the result
    results_file = TMP_PATH + "test_12.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MatchLevel_file2cmp_test12.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    # fstpy.delete_file(results_file)
    assert(res)