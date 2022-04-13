

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


plugin_test_dir = TEST_PATH + "CheckNanValue/testsFiles/"


class TestCheckNanValue(unittest.TestCase):

    def test_1(self):
        """Verifie chaque valeur de chaque champ pour savoir s'il y a des nan. Defaut:  msgOnly """
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute CheckNanValue
        df = CheckNanValue(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [CheckNanValue] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion ]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CheckNanValue_file2cmp_test1.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """Verifie chaque valeur de chaque champ pour savoir s'il y a des nan. MsgOnly a False.  Retourne un fichier contenant des 0 où les valeurs ne sont pas des nan """
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute CheckNanValue
        df = CheckNanValue(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [CheckNanValue --msgOnly FALSE] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion ]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CheckNanValue_file2cmp_test2.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """Utilisation de --outputFieldName alors qu'on a plusieurs champs dans le fichier d'entrée."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute CheckNanValue
        df = CheckNanValue(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [CheckNanValue --outputFieldName ABCD]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """Utilisation de --outputFieldName avec une valeur > 4 caractères."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute CheckNanValue
        df = CheckNanValue(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [CheckNanValue --outputFieldName ABCDEF]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
