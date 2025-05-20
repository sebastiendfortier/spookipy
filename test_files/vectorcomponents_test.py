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


plugin_test_dir = TEST_PATH + "VectorComponents/testsFiles/"


class TestVectorComponents(unittest.TestCase):
    def test_1(self):
        """Test l'option --orientationType avec une valeur invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VectorComponents
        df = VectorComponents(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [VectorComponents --orientationType BLABLABLA] >> [WriterStd --output {destination_path}]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_2(self):
        """Test avec un fichier de grille Z."""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VectorComponents
        df = VectorComponents(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [WindModulusAndDirection] >> [VectorComponents --orientationType MATH] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resultGridZ_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_3(self):
        """Test avec un fichier de grille U."""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VectorComponents
        df = VectorComponents(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [WindModulusAndDirection] >> [VectorComponents --orientationType MATH] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resultGridU_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res
