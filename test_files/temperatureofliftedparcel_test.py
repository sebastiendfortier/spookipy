

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


plugin_test_dir = TEST_PATH + "TemperatureOfLiftedParcel/testsFiles/"


class TestTemperatureOfLiftedParcel(unittest.TestCase):

    def test_1(self):
        """ Calcul de la temperature d'une parcelle soulevee a partir d'un fichier pression (ascendant)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres_TTPXHR1000.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute TemperatureOfLiftedParcel
        df = TemperatureOfLiftedParcel(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [TemperatureOfLiftedParcel --liftedFrom USER_DEFINED --verticalLevel 1000 --endLevel 100.0hPa --increment 10.0hPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_regpres_asc_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """ Calcul de la temperature d'une parcelle soulevee a partir d'un fichier hybrid (ascendant)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb_TTPXHR1000.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute TemperatureOfLiftedParcel
        df = TemperatureOfLiftedParcel(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [TemperatureOfLiftedParcel --liftedFrom SURFACE --endLevel 100.0hPa --increment 10.0hPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_reghyb_asc_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """ Calcul de la temperature d'une parcelle soulevee a partir d'un fichier contenant le resultat calcule a partir d'un increment different (les niveaux sont totalement differents)."""
        # open and read source
        source0 = plugin_test_dir + \
            "2011100712_012_reghyb_from_SB_and_UD1000_end100_inc2_681.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute TemperatureOfLiftedParcel
        df = TemperatureOfLiftedParcel(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureOfLiftedParcel --endLevel 100mb --increment 5mb --liftedFrom SURFACE,USER_DEFINED --verticalLevel 1000] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """ Calcul de la temperature d'une parcelle soulevee a partir d'un fichier manquant des donnees."""
        # open and read source
        source0 = plugin_test_dir + \
            "2011100712_012_reghyb_from_SB_and_UD1000_end100_inc5_missingUDParcel.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute TemperatureOfLiftedParcel
        df = TemperatureOfLiftedParcel(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureOfLiftedParcel --endLevel 100mb --increment 5mb --liftedFrom SURFACE,USER_DEFINED --verticalLevel 1000] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """ Calcul de la temperature d'une parcelle soulevee a partir d'un fichier contenant le resultat calcule a partir d'un increment different (les niveaux que l'on veut sont deja calcules)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb_from_SB_end100_inc5_file2cmp.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute TemperatureOfLiftedParcel
        df = TemperatureOfLiftedParcel(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureOfLiftedParcel --endLevel 100mb --increment 10mb --liftedFrom SURFACE] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "2011100712_012_reghyb_from_SB_end100_inc10_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """ Calcul de la temperature d'une parcelle soulevée a partir d'un fichier pression et d'un fichier hybrid (ascendant)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres_TTPXHR1000.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute TemperatureOfLiftedParcel
        df = TemperatureOfLiftedParcel(src_df0).compute()
        # ([ReaderStd --input {sources[0]}] + [ReaderStd --input /home/spst900/spooki/spooki_dir_ppp4/pluginsRelatedStuff/TemperatureOfLiftedParcel/testsFiles/2011100712_012_reghyb_TTPXHR1000.std]) >> [TemperatureOfLiftedParcel --liftedFrom SURFACE,USER_DEFINED --verticalLevel 1000 --endLevel 100.0hPa --increment 10.0hPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "2011100712_012_regpres_and_reghyb_asc_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_7(self):
        """ Calcul de la temperature d'une parcelle soulevee MEAN_LAYER a partir d'un fichier hybrid."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute TemperatureOfLiftedParcel
        df = TemperatureOfLiftedParcel(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [TemperatureOfLiftedParcel --liftedFrom MEAN_LAYER --baseMeanLayer SURFACE --deltaMeanLayer 100mb --endLevel 100.0hPa --increment 10.0hPa] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_reghyb_ML_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_8(self):
        """ Calcul de la temperature d'une parcelle soulevee MEAN_LAYER a partir d'un fichier hybrid 5005."""
        # open and read source
        source0 = plugin_test_dir + "minimal_4conve_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute TemperatureOfLiftedParcel
        df = TemperatureOfLiftedParcel(src_df0).compute()
        #['[ReaderStd --input {sources[0]} ] >> ', '[TemperatureOfLiftedParcel --liftedFrom MEAN_LAYER --baseMeanLayer SURFACE --deltaMeanLayer 100mb --endLevel 100.0hPa --increment 10.0hPa] >> ', '[WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]']

        # write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_8.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_9(self):
        """ Calcul de la temperature d'une parcelle soulevee SURFACE a partir d'un fichier hybrid 5005."""
        # open and read source
        source0 = plugin_test_dir + "minimal_TTHR_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute TemperatureOfLiftedParcel
        df = TemperatureOfLiftedParcel(src_df0).compute()
        #['[ReaderStd --input {sources[0]} ] >> ', '([Copy] + [Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField TT]) >> ', '[TemperatureOfLiftedParcel --liftedFrom SURFACE --endLevel 100.0hPa --increment 10.0hPa] >> ', '[WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]']

        # write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_9.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
