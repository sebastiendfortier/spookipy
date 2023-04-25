

# -*- coding: utf-8 -*-
import os
import sys


import unittest
import pytest


prefix = "/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/" % HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/" % (HOST_NUM, USER)


plugin_test_dir = TEST_PATH + "ReplaceDataIfCondition/testsFiles/"


class TestReplaceDataIfCondition(unittest.TestCase):

    def test_1(self):
        """isnan"""
        # open and read source
        source0 = plugin_test_dir + "simple_input.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ReplaceDataIfCondition
        df = ReplaceDataIfCondition(src_df0).compute()
        #['[ReaderCsv --input {sources[0]}] >>', '[DivideElementBy --value 0] >>', '[ReplaceDataIfCondition --condition isnan --value -999] >>', '[PrintIMO --extended]']

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_1"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """< 1"""
        # open and read source
        source0 = plugin_test_dir + "simple_input.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ReplaceDataIfCondition
        df = ReplaceDataIfCondition(src_df0).compute()
        #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition <1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_2"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """<= 1"""
        # open and read source
        source0 = plugin_test_dir + "simple_input.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ReplaceDataIfCondition
        df = ReplaceDataIfCondition(src_df0).compute()
        #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition <=1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_3"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """> 1"""
        # open and read source
        source0 = plugin_test_dir + "simple_input.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ReplaceDataIfCondition
        df = ReplaceDataIfCondition(src_df0).compute()
        #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition >1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_4"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """>=1"""
        # open and read source
        source0 = plugin_test_dir + "simple_input.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ReplaceDataIfCondition
        df = ReplaceDataIfCondition(src_df0).compute()
        #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition >=1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_5"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """== 2"""
        # open and read source
        source0 = plugin_test_dir + "simple_input.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ReplaceDataIfCondition
        df = ReplaceDataIfCondition(src_df0).compute()
        #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition ==1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_6"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_7(self):
        """!= 2"""
        # open and read source
        source0 = plugin_test_dir + "simple_input.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ReplaceDataIfCondition
        df = ReplaceDataIfCondition(src_df0).compute()
        #['[ReaderCsv --input {sources[0]}] >>', '[Zap --dateOfOrigin 20080529T133415 --doNotFlagAsZapped] >> ', '[ReplaceDataIfCondition --condition !=1 --value -999] >>', '[Zap --pdsLabel REPLACEONCON --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_7"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
