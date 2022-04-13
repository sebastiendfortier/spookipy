

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


plugin_test_dir = TEST_PATH + "PrecipitationTypeInstantaneousBourgouin/testsFiles/"


class TestPrecipitationTypeInstantaneousBourgouin(unittest.TestCase):

    def test_1(self):
        """  Test avec une valeur invalide pour precipitationRate."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute PrecipitationTypeInstantaneousBourgouin
        df = PrecipitationTypeInstantaneousBourgouin(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [PrecipitationTypeInstantaneousBourgouin --precipitationRate -0.2]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """  Test avec un fichier contenant les niveaux de congelation (FRP et NBFL)"""
        # open and read source
        source0 = plugin_test_dir + "input_2010032500_012"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute PrecipitationTypeInstantaneousBourgouin
        df = PrecipitationTypeInstantaneousBourgouin(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [PrecipitationTypeInstantaneousBourgouin --precipitationRate 0.2] >> [Select --fieldName T6 --noMetadata] >> [Zap --fieldName NW] >> [WriterStd --output {destination_path} --ignoreExtended ]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "PrecipBourgouin_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """  Test avec un fichier dont on doit calculer au prealable les niveaux de congelation"""
        # open and read source
        source0 = plugin_test_dir + "input_2013041212_024"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute PrecipitationTypeInstantaneousBourgouin
        df = PrecipitationTypeInstantaneousBourgouin(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [PrecipitationTypeInstantaneousBourgouin --precipitationRate 0.2] >> [Select --fieldName T6 --noMetadata] >> [Zap --fieldName NW] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "PrecipBourgouin2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
