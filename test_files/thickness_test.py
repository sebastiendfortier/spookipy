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


plugin_test_dir = TEST_PATH + "Thickness/testsFiles/"


class TestThickness(unittest.TestCase):
    def test_1(self):
        """Test avec un fichier de coordonnées Sigma."""
        # open and read source
        source0 = plugin_test_dir + "GZ_12000_10346_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Thickness
        df = Thickness(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 1.0 --top 0.8346 --coordinateType SIGMA_COORDINATE] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Thick_test1-2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_2(self):
        """Test avec un fichier de coordonnées Sigma avec valeur de base plus haute dans l'atmosphère que valeur de top."""
        # open and read source
        source0 = plugin_test_dir + "GZ_12000_10346_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Thickness
        df = Thickness(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 0.8346 --top 1.0 --coordinateType SIGMA_COORDINATE] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Thick_test1-2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_3(self):
        """Test avec un fichier en pression."""
        # open and read source
        source0 = plugin_test_dir + "GZ_1000_500_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Thickness
        df = Thickness(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 1000 --top 500 --coordinateType PRESSURE_COORDINATE] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Thick_test3-4_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_4(self):
        """Test avec un fichier en pression avec valeur de base plus haute dans l'atmosphère que valeur de top."""
        # open and read source
        source0 = plugin_test_dir + "GZ_1000_500_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Thickness
        df = Thickness(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 500 --top 1000 --coordinateType PRESSURE_COORDINATE] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Thick_test3-4_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_5(self):
        """Test en utilisant le même niveau pour base et top; requête invalide."""
        # open and read source
        source0 = plugin_test_dir + "GZ_1000_500_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Thickness
        df = Thickness(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 1000 --top 1000 --coordinateType PRESSURE_COORDINATE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_6(self):
        """Test avec un fichier hybride."""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Thickness
        df = Thickness(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 1 --top 0.607 --coordinateType HYBRID_COORDINATE] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Thick_test6_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res
