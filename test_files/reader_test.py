

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


plugin_test_dir = TEST_PATH + "Reader/testsFiles/"


class TestReader(unittest.TestCase):

    def test_1(self):
        """test reading 2 files STD and CSV"""
        # open and read source
        source0 = plugin_test_dir + "UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "3x2_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute Reader
        df = Reader(src_df0).compute()
        # [Reader --input {sources[0]} {sources[1]}] >> [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "stdPlusCsv_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
