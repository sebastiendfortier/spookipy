# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/MinMaxLevelIndex/testsFiles/'


def test_1(plugin_test_dir):
    """--minMax MIN --direction UPWARD --outputFieldName1 IND"""
    # open and read source
    source0 = plugin_test_dir + "UUOrdered2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        min=True,
        ascending=True,
        nomvar_min='IND').compute()
    # [ReaderStd --input {sources[0]}] >> [spooki.MinMaxLevelIndex --minMax MIN --direction UPWARD --outputFieldName1 IND] >>
    # [Zap --verticalLevelType ARBITRARY_CODE --doNotFlagAsZapped] >>[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    # print(df)
    # df = fstpy.zap(df, pkind='_')

    # write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "minIndice_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)


def test_2(plugin_test_dir):
    """--minMax MIN --direction UPWARD --outputFieldName1 IND"""
    # open and read source
    source0 = plugin_test_dir + "UUDoubled2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        min=True,
        ascending=True,
        nomvar_min='IND').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.MinMaxLevelIndex --minMax MIN --direction UPWARD --outputFieldName1 IND] >> [Zap --verticalLevelType ARBITRARY_CODE --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "minIndiceForward_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)


def test_3(plugin_test_dir):
    """--minMax MIN --direction DOWNWARD --outputFieldName1 IND"""
    # open and read source
    source0 = plugin_test_dir + "UUOrdered2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        min=True,
        ascending=False,
        nomvar_min='IND').compute()
    # [ReaderStd --input {sources[0]}] >> [spooki.MinMaxLevelIndex --minMax MIN --direction DOWNWARD --outputFieldName1 IND] >> [Zap --verticalLevelType ARBITRARY_CODE --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "minIndice_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)


def test_4(plugin_test_dir):
    """--minMax MIN --direction DOWNWARD --outputFieldName1 IND"""
    # open and read source
    source0 = plugin_test_dir + "UUDoubled2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        min=True,
        ascending=False,
        nomvar_min='IND').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.MinMaxLevelIndex --minMax MIN --direction DOWNWARD --outputFieldName1 IND] >> [Zap --verticalLevelType ARBITRARY_CODE --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_4.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "minIndiceReverse_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)


def test_5(plugin_test_dir):
    """-minMax MAX --outputFieldName2 IND"""
    # open and read source
    source0 = plugin_test_dir + "UUOrdered2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(src_df0, max=True, nomvar_max='IND').compute()
    # [ReaderStd --input {sources[0]}] >> [spooki.MinMaxLevelIndex --minMax MAX --outputFieldName2 IND] >> [Zap --verticalLevelType ARBITRARY_CODE --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "maxIndice_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)


def test_6(plugin_test_dir):
    """--minMax MAX --direction UPWARD --outputFieldName2 IND"""
    # open and read source
    source0 = plugin_test_dir + "UUDoubled2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        max=True,
        ascending=True,
        nomvar_max='IND').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.MinMaxLevelIndex --minMax MAX --direction UPWARD --outputFieldName2 IND] >> [Zap --verticalLevelType ARBITRARY_CODE --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "maxIndiceForward_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)


def test_7(plugin_test_dir):
    """--minMax MAX --direction DOWNWARD --outputFieldName2 IND"""
    # open and read source
    source0 = plugin_test_dir + "UUOrdered2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        max=True,
        ascending=False,
        nomvar_max='IND').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.MinMaxLevelIndex --minMax MAX --direction DOWNWARD --outputFieldName2 IND] >> [Zap --verticalLevelType ARBITRARY_CODE --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "maxIndice_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)


def test_8(plugin_test_dir):
    """--minMax MAX --direction DOWNWARD --outputFieldName2 IND"""
    # open and read source
    source0 = plugin_test_dir + "UUDoubled2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        max=True,
        ascending=False,
        nomvar_max='IND').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.MinMaxLevelIndex --minMax MAX --direction DOWNWARD --outputFieldName2 IND] >> [Zap --verticalLevelType ARBITRARY_CODE --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = TMP_PATH + "test_8.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "maxIndiceReverse_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)


def test_9(plugin_test_dir):
    """--bounded --minMax MAX --outputFieldName2 IND"""
    # open and read source
    source0 = plugin_test_dir + "test_ICGA.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(
        src_df0,
        max=True,
        bounded=True,
        nomvar_max='IND').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [spooki.MinMaxLevelIndex --bounded --minMax MAX --outputFieldName2 IND] >>
    # [Zap --pdsLabel MinMaxBoundedIndexLevel --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]
    df['etiket'] = 'MINMAXBOUNDE'

    # write the result
    results_file = TMP_PATH + "test_9.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test_ICGA_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_10(plugin_test_dir):
    """--bounded --minMax BOTH"""
    # open and read source
    source0 = plugin_test_dir + "TT_bounded_minmax.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxLevelIndex(src_df0, bounded=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.MinMaxLevelIndex --bounded --minMax BOTH] >> [Select --fieldName KBAS,KTOP --exclude] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    df['ip2'] = 24
    # write the result
    results_file = TMP_PATH + "test_10.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "TT_bounded_minmax_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
