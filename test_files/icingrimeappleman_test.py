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


plugin_test_dir = TEST_PATH + "IcingRimeAppleman/testsFiles/"


class TestIcingRimeAppleman(unittest.TestCase):
    def test_1(self):
        """Test the IcingRimeAppleman function using 3 matrixes (5X4X3)"""
        # open and read source
        source0 = plugin_test_dir + "inputTT_ES_WW.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute IcingRimeAppleman
        df = IcingRimeAppleman(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --nbitsForDataStorage E32 --doNotFlagAsZapped] >> [IcingRimeAppleman] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TT_ES_WW_IcingRimeAppleman_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_3(self):
        """Test the IcingRimeAppleman function using 3 matrixes (5X4X3)"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute IcingRimeAppleman
        df = IcingRimeAppleman(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [IcingRimeAppleman] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "reference_file_test_3.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res
