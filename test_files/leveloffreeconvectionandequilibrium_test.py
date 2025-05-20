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


plugin_test_dir = TEST_PATH + "LevelOfFreeConvectionAndEquilibrium/testsFiles/"


class TestLevelOfFreeConvectionAndEquilibrium(unittest.TestCase):
    def test_1(self):
        """Utilisation du parametre --liftedFrom SURFACE avec un fichier en pression. Requete invalide"""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_regpres_1_petit"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute LevelOfFreeConvectionAndEquilibrium
        df = LevelOfFreeConvectionAndEquilibrium(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [LevelOfFreeConvectionAndEquilibrium --liftedFrom SURFACE --outputField LFC_PRESSURE --virtualTemperature BOTH --increment 2.0mb --outputLevels OPTIMAL_VALUE_ONLY]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_2(self):
        """Utilisation du parametre --liftedFrom MEAN_LAYER --baseMeanLayer SURFACE avec un fichier en pression. Requete invalide"""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_regpres_1_petit"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute LevelOfFreeConvectionAndEquilibrium
        df = LevelOfFreeConvectionAndEquilibrium(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [LevelOfFreeConvectionAndEquilibrium --liftedFrom MEAN_LAYER --baseMeanLayer SURFACE --deltaMeanLayer 200mb --outputField LFC_PRESSURE --virtualTemperature NO --increment 2.0mb --outputLevels OPTIMAL_VALUE_ONLY]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_3(self):
        """Utilisation du parametre --liftedFrom MOST_UNSTABLE avec un fichier en pression. Requete invalide"""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_regpres_1_petit"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute LevelOfFreeConvectionAndEquilibrium
        df = LevelOfFreeConvectionAndEquilibrium(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [LevelOfFreeConvectionAndEquilibrium --liftedFrom MOST_UNSTABLE --deltaMostUnstable 200mb --outputField LFC_PRESSURE --virtualTemperature NO --increment 2.0mb --outputLevels OPTIMAL_VALUE_ONLY]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_6(self):
        """Calcul des niveaux de convection a partir d'un fichier hybrid de 2 points, SURFACE."""
        # open and read source
        source0 = plugin_test_dir + "lam_nat_coupe_cas4_TTESHUGZ"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute LevelOfFreeConvectionAndEquilibrium
        df = LevelOfFreeConvectionAndEquilibrium(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [LevelOfFreeConvectionAndEquilibrium --liftedFrom SURFACE --increment 1.0hPa --virtualTemperature NO --outputField EL_PRESSURE,LFC_PRESSURE --outputLevels BOTH] >> [WriterStd --output {destination_path} --ignoreExtended ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "lam_nat_cas4_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_8(self):
        """Calcul des niveaux de convection a partir d'un fichier lam national de 2 points, SURFACE et OPTIMAL_VALUE_ONLY."""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute LevelOfFreeConvectionAndEquilibrium
        df = LevelOfFreeConvectionAndEquilibrium(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [LevelOfFreeConvectionAndEquilibrium --liftedFrom SURFACE --increment 1.0hPa --virtualTemperature NO --outputField EL_PRESSURE,LFC_PRESSURE,EL_HEIGHT,LFC_HEIGHT --outputLevels OPTIMAL_VALUE_ONLY] >> [WriterStd --output {destination_path} --ignoreExtended ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "point61-51_OptimalValue_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_10(self):
        """Calcul des niveaux de convection a partir d'un fichier de 3 points, SURFACE et OPTIMAL_VALUE_ONLY."""
        # open and read source
        source0 = plugin_test_dir + "Fichier3Pts_2017092900.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute LevelOfFreeConvectionAndEquilibrium
        df = LevelOfFreeConvectionAndEquilibrium(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --exclude --fieldName TD] >> [LevelOfFreeConvectionAndEquilibrium --liftedFrom SURFACE --increment 10.0hPa --virtualTemperature NO --outputField EL_PRESSURE,LFC_PRESSURE --outputLevels BOTH] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CroisementCasA_test10_v2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_11(self):
        """Calcul des niveaux de convection a partir d'un fichier de 6 points, SURFACE et OPTIMAL_VALUE_ONLY."""
        # open and read source
        source0 = plugin_test_dir + "2018052906_lam_nat_CroisementsAetB.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute LevelOfFreeConvectionAndEquilibrium
        df = LevelOfFreeConvectionAndEquilibrium(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [LevelOfFreeConvectionAndEquilibrium --liftedFrom SURFACE --increment 2.0hPa --virtualTemperature NO --outputField EL_PRESSURE,LFC_PRESSURE,EL_HEIGHT,LFC_HEIGHT --outputLevels MULTIPLE_VALUES ] >> [WriterStd --output {destination_path} --ignoreExtended ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CroisementsTest11_v2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_12(self):
        """Calcul des niveaux de convection a partir d'un fichier de 6 points, SURFACE et OPTIMAL_VALUE_ONLY."""
        # open and read source
        source0 = plugin_test_dir + "2017092900_000_CroisementCas3.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute LevelOfFreeConvectionAndEquilibrium
        df = LevelOfFreeConvectionAndEquilibrium(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [LevelOfFreeConvectionAndEquilibrium --liftedFrom SURFACE --increment 5.0hPa --virtualTemperature NO --outputField EL_PRESSURE,LFC_PRESSURE,EL_HEIGHT,LFC_HEIGHT --outputLevels MULTIPLE_VALUES ] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CroisementCasB_test12_v2py_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_13(self):
        """Calcul des niveaux de convection a partir d'un fichier de 8 points, avec correction virtuelle,  SURFACE et OPTIMAL_VALUE_ONLY."""
        # open and read source
        source0 = plugin_test_dir + "2018060606_lam_nat_CroisementCas3.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute LevelOfFreeConvectionAndEquilibrium
        df = LevelOfFreeConvectionAndEquilibrium(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [LevelOfFreeConvectionAndEquilibrium --liftedFrom SURFACE --increment 5.0hPa --virtualTemperature YES --outputField EL_PRESSURE,LFC_PRESSURE,EL_HEIGHT,LFC_HEIGHT --outputLevels MULTIPLE_VALUES ] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CroisementCas3_VT_v2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_14(self):
        """Calcul des niveaux de convection a partir d'un fichier de 18 points, SURFACE."""
        # open and read source
        source0 = plugin_test_dir + "input_convection_CroisementCas4.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute LevelOfFreeConvectionAndEquilibrium
        df = LevelOfFreeConvectionAndEquilibrium(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [LevelOfFreeConvectionAndEquilibrium --liftedFrom SURFACE --increment 2.0hPa --virtualTemperature NO --outputField EL_PRESSURE,LFC_PRESSURE,EL_HEIGHT,LFC_HEIGHT --outputLevels BOTH ] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_14.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CroisementCas4_v2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res
