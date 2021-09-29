

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


plugin_test_dir = TEST_PATH + "Message/testsFiles/"


class TestMessage(unittest.TestCase):

    def test_1(self):
        """Tester lorsqu'aucune option n'est spécifiée."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Message
        df = Message(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Message]

        # write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """Test avec l'option 'verificationMessage' seulement"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Message
        df = Message(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Copy] + [Message --verificationMessage -------------------------verif_test_message]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """Test avec l'option 'executionMessage' seulement"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Message
        df = Message(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Copy] + [Message --executionMessage -------------------------exec_test_message]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """Test avec l'option 'verificationMessage' et 'severity' a WARNING"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Message
        df = Message(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Copy] + [Message --severity WARNING --verificationMessage -------------------------verif_severity_test_message]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """Test avec l'option 'verificationMessage' et 'severity' a INFO"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Message
        df = Message(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Copy] + [Message --severity INFO --verificationMessage -------------------------verif_severity_test_message]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """Test avec les options 'verificationMessage', 'executionMessage' et 'severity' a ERROR"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Message
        df = Message(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Copy] + [Message --severity ERROR --verificationMessage -------------------------verif_severity_test_message --executionMessage --------------------------exec_test_message]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
