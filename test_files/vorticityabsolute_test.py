

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


plugin_test_dir = TEST_PATH + "VorticityAbsolute/testsFiles/"


class TestVorticityAbsolute(unittest.TestCase):

    def test_regvortab_test_1(self):
        """Calculate with a simple test data """
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VorticityAbsolute
        df = VorticityAbsolute(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --fieldName QQ --exclude] >> [VorticityAbsolute] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = TMP_PATH + "vortab_test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "vortab_file2cmp_test_1_20200618.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_regvortab_test_2(self):
        """Spooki must success when input are in millibars"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VorticityAbsolute
        df = VorticityAbsolute(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >>[VorticityAbsolute]

        # write the result
        results_file = TMP_PATH + "vortab_test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_regvortab_test_3(self):
        """SingleThread. Same as test 1 but in singlethread"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VorticityAbsolute
        df = VorticityAbsolute(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --fieldName QQ --exclude] >> [VorticityAbsolute -T1] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = TMP_PATH + "vortab_test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "vortab_file2cmp_test_3_20200618.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_regvortab_test_4(self):
        """ Test avec une grille globale"""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_glbeta"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VorticityAbsolute
        df = VorticityAbsolute(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VorticityAbsolute] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = TMP_PATH + "vortab_test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "glbeta_file2Cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_regvortab_test_5(self):
        """Calculate with a simple test data - reconnaissance de son resultat """
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VorticityAbsolute
        df = VorticityAbsolute(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VorticityAbsolute] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = TMP_PATH + "vortab_test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "vortab_file2cmp_test_5.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
