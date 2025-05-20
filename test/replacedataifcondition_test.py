# -*- coding: utf-8 -*-
import numpy as np
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy

pd.set_option("display.max_rows", 500, "display.max_columns", 500)

pytestmark = [pytest.mark.regressions, pytest.mark.regressions2]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "ReplaceDataIfCondition"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """isnan"""
    # open and read source
    source0 = plugin_test_path / "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    for i in src_df0.index:
        src_df0.at[i, "d"] = np.where(src_df0.at[i, "d"] == 1, np.nan, src_df0.at[i, "d"])
    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0, "isnan", -999).compute()
    # ['[ReaderCsv --input {sources[0]}] >>', '[DivideElementBy --value 0] >>', '[ReplaceDataIfCondition --condition isnan --value -999] >>', '[PrintIMO --extended]']

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    # file_to_compare = plugin_test_path / "resulttest_1"
    file_to_compare = plugin_test_path / "resulttest_6"

    # # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """< 1"""
    # open and read source
    source0 = plugin_test_path / "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0, "<1", -999).compute()
    # ['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition <1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_2"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """<= 1"""
    # open and read source
    source0 = plugin_test_path / "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0, "<=1", -999).compute()
    # ['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition <=1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_3"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """> 1"""
    # open and read source
    source0 = plugin_test_path / "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0, ">1", -999).compute()
    # ['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition >1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_4"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """>=1"""
    # open and read source
    source0 = plugin_test_path / "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0, ">=1", -999).compute()
    # ['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition >=1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_5"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """== 1"""
    # open and read source
    source0 = plugin_test_path / "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0, "==1", -999).compute()
    # ['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition ==1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_6"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_7(plugin_test_path):
    """!= 2"""
    # open and read source
    source0 = plugin_test_path / "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    with pytest.raises(spookipy.ReplaceDataIfConditionError):
        _ = spookipy.ReplaceDataIfCondition(src_df0, "!=2", -999).compute()
    # ['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition !=1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # # write the result
    # results_file = test_tmp_path / "test_7.std"
    # fstpy.delete_file(results_file)
    # fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    # file_to_compare = plugin_test_path / "resulttest_7"

    # # compare results
    # res = call_fstcomp(results_file, file_to_compare)
    # fstpy.delete_file(results_file)
    # assert(res)
