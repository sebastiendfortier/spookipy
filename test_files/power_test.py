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


plugin_test_dir = TEST_PATH + "Power/testsFiles/"


class TestPower(unittest.TestCase):
    def test_1(self):
        """Utilisation de --outputFieldName avec une valeur > 4 caractères."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Power
        df = Power(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Power --value 2 --outputFieldName ABCDEF]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_2(self):
        """Utilisation de --outputFieldName alors qu'on a plusieurs champs dans le fichier d'entrée."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Power
        df = Power(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Power --value 2 --outputFieldName ABCD]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_3(self):
        """Calcule la valeur exponentielle d'un champ."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Power
        df = Power(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Power --value 2 ] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE --ignoreExtended ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "exponent_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_4(self):
        """Calcule la valeur exponentielle d'un champ et utilise --outputFieldName pour renommer le résultat."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Power
        df = Power(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU*] >> [Power --value 2 --outputFieldName SQRT] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE --ignoreExtended --noUnitConversion]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Power_test4_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res
