

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


plugin_test_dir = TEST_PATH + "HumidityRelativeWeightedMean/testsFiles/"


class TestHumidityRelativeWeightedMean(unittest.TestCase):

    def test_1(self):
        """Test avec un petit fichier contenant des valeurs verifiees a la main."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute HumidityRelativeWeightedMean
        df = HumidityRelativeWeightedMean(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [HumidityRelativeWeightedMean] >> [WriterStd --output {destination_path} --encodeIP2andIP3]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Test1_file2Cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """Test avec une sortie de modele."""
        # open and read source
        source0 = plugin_test_dir + "2020030412_024"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute HumidityRelativeWeightedMean
        df = HumidityRelativeWeightedMean(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [HumidityRelativeWeightedMean] >> [WriterStd --output {destination_path}]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2020030412_file2Cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """Test avec une sortie de modele, avec clé --capped."""
        # open and read source
        source0 = plugin_test_dir + "2020030412_024"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute HumidityRelativeWeightedMean
        df = HumidityRelativeWeightedMean(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [HumidityRelativeWeightedMean --capped 1.0] >> [WriterStd --output {destination_path}]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2020030412_test3_file2Cmp_20200904.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
