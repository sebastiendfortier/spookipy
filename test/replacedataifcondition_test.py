

# -*- coding: utf-8 -*-
import numpy as np
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets
pd.set_option("display.max_rows", 500, "display.max_columns", 500)

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/ReplaceDataIfCondition/testsFiles/'



def test_1(plugin_test_dir):
    """isnan"""
    # open and read source
    source0 = plugin_test_dir + "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    for i in src_df0.index:
        src_df0.at[i, 'd'] = np.where(src_df0.at[i, 'd']==1,np.NaN,src_df0.at[i, 'd'])
    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0,'isnan',-999).compute()
    #['[ReaderCsv --input {sources[0]}] >>', '[DivideElementBy --value 0] >>', '[ReplaceDataIfCondition --condition isnan --value -999] >>', '[PrintIMO --extended]']

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    # file_to_compare = plugin_test_dir + "resulttest_1"
    file_to_compare = plugin_test_dir + "resulttest_6"

    # # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_2(plugin_test_dir):
    """< 1"""
    # open and read source
    source0 = plugin_test_dir + "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0,"<1",-999).compute()
    #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition <1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_2"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_3(plugin_test_dir):
    """<= 1"""
    # open and read source
    source0 = plugin_test_dir + "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0,"<=1",-999).compute()
    #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition <=1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_3"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_4(plugin_test_dir):
    """> 1"""
    # open and read source
    source0 = plugin_test_dir + "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0,">1",-999).compute()
    #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition >1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_4"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_5(plugin_test_dir):
    """>=1"""
    # open and read source
    source0 = plugin_test_dir + "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0,">=1",-999).compute()
    #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition >=1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_5"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_6(plugin_test_dir):
    """== 1"""
    # open and read source
    source0 = plugin_test_dir + "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    df = spookipy.ReplaceDataIfCondition(src_df0,"==1",-999).compute()
    #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition ==1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_6"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_7(plugin_test_dir):
    """!= 2"""
    # open and read source
    source0 = plugin_test_dir + "simple_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ReplaceDataIfCondition
    with pytest.raises(spookipy.ReplaceDataIfConditionError):
        _ = spookipy.ReplaceDataIfCondition(src_df0,"!=2",-999).compute()
    #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition !=1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

    # # write the result
    # results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    # fstpy.delete_file(results_file)
    # fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    # file_to_compare = plugin_test_dir + "resulttest_7"

    # # compare results
    # res = fstcomp(results_file, file_to_compare)
    # fstpy.delete_file(results_file)
    # assert(res)
