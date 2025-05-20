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


plugin_test_dir = TEST_PATH + "AirDensity/testsFiles/"


class TestAirDensity(unittest.TestCase):
    def test_1(self):
        """Calcul de la densite de l'air avec un fichier d'entree normal qui a des TT,HU et PX."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_HU_PX_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute AirDensity
        df = AirDensity(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [AirDensity --virtualTemperature ACTUAL] >> [WriterStd --output {destination_path} --noMetadata]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_TT_HU_PX_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_2(self):
        """Calcul de la densite de l'air avec un fichier d'entree VT et PX."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_VT_PX_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute AirDensity
        df = AirDensity(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [AirDensity --virtualTemperature ACTUAL] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_VT_PX_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_3(self):
        """Calcul de la densite de l'air avec un fichier d'entree TT,ES et PX."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_ES_PX_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute AirDensity
        df = AirDensity(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [AirDensity --virtualTemperature ACTUAL] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_TT_ES_PX_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_4(self):
        """Calcul de la densite de l'air avec un fichier d'entree TT,QV et PX."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_QV_PX_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute AirDensity
        df = AirDensity(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [AirDensity --virtualTemperature ACTUAL] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_TT_QV_PX_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_5(self):
        """Calcul de la densite de l'air avec un fichier d'entree TT,TD et PX."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_TD_PX_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute AirDensity
        df = AirDensity(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [AirDensity --virtualTemperature ACTUAL] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_TT_TD_PX_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_6(self):
        """Calcul de la densite de l'air avec un fichier d'entree TT,HR et PX."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_HR_PX_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute AirDensity
        df = AirDensity(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [AirDensity --virtualTemperature ACTUAL] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_TT_HR_PX_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_7(self):
        """Test d'une mauvais valeur de la cle virtualTemperature"""
        # open and read source
        source0 = plugin_test_dir + "inputFile_VT_PX_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute AirDensity
        df = AirDensity(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [AirDensity --virtualTemperature UNDEFINED] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_8(self):
        """Test de la valeur par défaut de virtualTemperature"""
        # open and read source
        source0 = plugin_test_dir + "inputFile_VT_PX_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute AirDensity
        df = AirDensity(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [AirDensity] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_VT_PX_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_9(self):
        """Calcul de la densite de l'air sec avec un fichier d'entree TT et PX."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_PX_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute AirDensity
        df = AirDensity(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [PrintIMO] >> [AirDensity --virtualTemperature DRY] >> [PrintIMO] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_TT_PX_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_10(self):
        """Calcul de la densite de l'air sec avec un fichier d'entree VT et PX."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_VT_PX_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute AirDensity
        df = AirDensity(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [AirDensity --virtualTemperature DRY] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_11(self):
        """Calcul de la densite de l'air reelle et sec."""
        # open and read source
        source0 = plugin_test_dir + "inputFile_TT_HU_PX_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute AirDensity
        df = AirDensity(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} ] >> [AirDensity --virtualTemperature BOTH] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "inputFile_TT_HU_PX_BOTH_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res
