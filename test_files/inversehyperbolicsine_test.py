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


plugin_test_dir = TEST_PATH + "InverseHyperbolicSine/testsFiles/"


class TestInverseHyperbolicSine(unittest.TestCase):
    def test_1(self):
        """Test InverseHyperbolicSine"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_1_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InverseHyperbolicSine
        df = InverseHyperbolicSine(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [InverseHyperbolicSine] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "asinh_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res
