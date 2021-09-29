

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


plugin_test_dir = TEST_PATH + "SupercooledLiquidWaterContent/testsFiles/"


class TestSupercooledLiquidWaterContent(unittest.TestCase):

    def test_1(self):
        """ Test sans la cle optionnel origin."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_M3_MPQC_MPQR_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute SupercooledLiquidWaterContent
        df = SupercooledLiquidWaterContent(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [SupercooledLiquidWaterContent] >> [WriterStd --output {destination_path} --noMetadata]

        # write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_TT_M3_MPQC_MPQR_TOTAL_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """ Test d'une mauvais valeur de la cle origin"""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_M3_MPQC_MPQR_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute SupercooledLiquidWaterContent
        df = SupercooledLiquidWaterContent(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [SupercooledLiquidWaterContent --origin UNDEFINED] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """ Test avec mauvaises donnees pour la cle origin"""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_M3_MPQC_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute SupercooledLiquidWaterContent
        df = SupercooledLiquidWaterContent(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [SupercooledLiquidWaterContent --origin RAIN] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """ Test des resultats pour chaque champs."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_M3_MPQC_MPQR_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute SupercooledLiquidWaterContent
        df = SupercooledLiquidWaterContent(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [SupercooledLiquidWaterContent --origin ALL] >> [WriterStd --output {destination_path} --noMetadata]

        # write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_TT_M3_MPQC_MPQR_ALL_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """ Test TT > 0."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_over_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute SupercooledLiquidWaterContent
        df = SupercooledLiquidWaterContent(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [SupercooledLiquidWaterContent --origin CLOUD] >> [WriterStd --output {destination_path} --noMetadata]

        # write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_TT_over_0_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
