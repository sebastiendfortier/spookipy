

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


plugin_test_dir = TEST_PATH + "ArcCosine/testsFiles/"


class TestArcCosine(unittest.TestCase):

    def test_1(self):
        """Calcule la valeur arc cosinus de chaque champ."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_point1_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ArcCosine
        df = ArcCosine(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [ArcCosine] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "acos_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
