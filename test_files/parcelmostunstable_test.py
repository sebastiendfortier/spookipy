

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


plugin_test_dir = TEST_PATH + "ParcelMostUnstable/testsFiles/"


class TestParcelMostUnstable(unittest.TestCase):

    def test_1(self):
        """Appel a ParcelMostUnstable, unites absentes pour --delta."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ParcelMostUnstable
        df = ParcelMostUnstable(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [ParcelMostUnstable --delta 300 --iceWaterPhase WATER]

        # write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        assert(res)

    def test_2(self):
        """Appel à ParcelMostUnstable, parametre --temperaturePhaseSwitch absent alors que --iceWaterPhase est BOTH."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ParcelMostUnstable
        df = ParcelMostUnstable(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [ParcelMostUnstable --delta 100mb --iceWaterPhase BOTH ]

        # write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        assert(res)

    def test_3(self):
        """Mauvaise utilisation du parametre --temperaturePhaseSwitch alors que --iceWaterPhase est WATER."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ParcelMostUnstable
        df = ParcelMostUnstable(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [ParcelMostUnstable --delta 100mb --iceWaterPhase WATER --temperaturePhaseSwitch 20.0C]

        # write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        assert(res)

    def test_4(self):
        """ Appel a ParcelMostUnstable, donnees manquantes car il n'y a pas de donnees pour interpoler sur les niveaux de fin de la couche."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ParcelMostUnstable
        df = ParcelMostUnstable(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [ParcelMostUnstable --delta 990mb --iceWaterPhase WATER ]

        # write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        assert(res)

    def test_5(self):
        """Appel a ParcelMostUnstable, unites absentes pour --increment."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ParcelMostUnstable
        df = ParcelMostUnstable(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [ParcelMostUnstable --delta 300mb --increment 50 --iceWaterPhase WATER]

        # write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        assert(res)

    def test_6(self):
        """ Calcul de la parcelle Most Unstable à partir d'un fichier pression. Ne peut être calculé à partir d'un fichier pression."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ParcelMostUnstable
        df = ParcelMostUnstable(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [ParcelMostUnstable --delta 300mb --iceWaterPhase WATER ]

        # write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        assert(res)
