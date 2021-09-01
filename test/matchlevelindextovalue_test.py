# -*- coding: utf-8 -*-
from spookipy.matchlevelindextovalue.matchlevelindextovalue import MatchLevelIndexToValueError
from fstpy.dataframe_utils import select_with_meta
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import pandas as pd
import spookipy.all as spooki

pytestmark = [pytest.mark.to_skip]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/MatchLevelIndexToValue/testsFiles/'



def test_1(plugin_test_dir):
    """Test match one field1 full computation."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uv_df = spooki.WindModulus(src_df0).compute()

    minmax_df = spooki.MinMaxLevelIndex(uv_df,max=True,nomvar_max='IND').compute()


    #compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(minmax_df, nomvar_out='TEST').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [WindModulus] >>
    # [MinMaxLevelIndex --minMax MAX --direction UPWARD --outputFieldName2 IND] >>
    # [MatchLevelIndexToValue --outputFieldName TEST] >>[WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

    #write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "lou_matchOneField_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Test match one field4 full computation except uv."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_UV_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uv_df = spooki.WindModulus(src_df0).compute()

    minmax_df = spooki.MinMaxLevelIndex(uv_df,max=True,nomvar_max='IND').compute()

    #compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(minmax_df, nomvar_out='TEST').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [WindModulus] >>
    # [MinMaxLevelIndex --minMax MAX --direction UPWARD --outputFieldName2 IND] >>
    # [MatchLevelIndexToValue --outputFieldName TEST] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

    #write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "lou_matchOneField_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_3(plugin_test_dir):
    """Test match one field4 full computation."""
    # open and read source
    source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uv_df = spooki.WindModulus(src_df0).compute()

    minmax_df = spooki.MinMaxLevelIndex(uv_df,max=True,nomvar_max='IND').compute()

    #compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(minmax_df, nomvar_out='T5').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [WindModulus] >>
    # [MinMaxLevelIndex --minMax MAX --direction UPWARD --outputFieldName2 IND] >>
    # [MatchLevelIndexToValue --outputFieldName T5] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

    #write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "lou_matchOneField2_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_4(plugin_test_dir):
    """Tester l'option --outputFieldName avec plus d'un type de champ en entree."""
    # open and read source
    source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = select_with_meta(src_df0,['TT'])

    minmax_df = spooki.MinMaxLevelIndex(src_df0,min=True,nomvar_min='IND').compute()

    uuvv_df = select_with_meta(src_df0,['UU','VV'])

    src_df = pd.concat([tt_df,minmax_df,uuvv_df],ignore_index=True)
    #compute MatchLevelIndexToValue
    with pytest.raises(MatchLevelIndexToValueError):
        _ = spooki.MatchLevelIndexToValue(src_df, nomvar_out='TEST').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # (
    # ( [Select --fieldName TT] >>  [MinMaxLevelIndex --minMax MIN --direction UPWARD --outputFieldName1 IND] ) + [Select --fieldName UU,VV]
    # ) >>
    # [MatchLevelIndexToValue --outputFieldName TEST] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]



def test_5(plugin_test_dir):
    """Test match no fields."""
    # open and read source
    source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uv_df = spooki.WindModulus(src_df0).compute()

    #  ( [SetConstantValue --value -1.0 --bidimensional] >>  [Zap --fieldName IND --doNotFlagAsZapped]  )
    ind_df = spooki.SetConstantValue(uv_df,value=-1.,bi_dimensionnal=True).compute()
    ind_df.loc[:,'nomvar'] = 'IND'

    src_df = pd.concat([uv_df,ind_df],ignore_index=True)

    #compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(src_df, nomvar_out='TEST').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >>
    # (
    # [Copy] +  ( [SetConstantValue --value -1.0 --bidimensional] >>  [Zap --fieldName IND --doNotFlagAsZapped]  )
    # ) >>
    # [MatchLevelIndexToValue --outputFieldName TEST] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

    #write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "lou_matchNoFields_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir):
    """Test match negative index."""
    # open and read source
    source0 = plugin_test_dir + "sortie_cpp_cld_200906290606"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "indneg.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0,src_df1],ignore_index=True)
    #compute MatchLevelIndexToValue
    df = spooki.MatchLevelIndexToValue(src_df, nomvar_out='T7').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} {sources[1]}] >>
    # [MatchLevelIndexToValue --outputFieldName T7] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

    #write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "lou_matchNegativeIndex_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
