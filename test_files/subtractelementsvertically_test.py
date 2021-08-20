

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"SubtractElementsVertically/testsFiles/"

class TestSubtractElementsVertically(unittest.TestCase):

    def test_1(self):
        """Utilisation de --outputFieldName avec une valeur > 4 caractères - requete invalide."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SubtractElementsVertically
        df = SubtractElementsVertically(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SubtractElementsVertically --outputFieldName TROPLONG --direction ASCENDING]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Effectue un test avec --outputFieldName mais plusieurs champs en entrée - requete invalide."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SubtractElementsVertically
        df = SubtractElementsVertically(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [SubtractElementsVertically --outputFieldName ABCD --direction ASCENDING]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Test avec 2 champs et 2 niveaux, option --direction ASCENDING"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SubtractElementsVertically
        df = SubtractElementsVertically(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SubtractElementsVertically --direction ASCENDING] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "SubVert_test3_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Test avec un fichier de 2 champs et 2 niveaux, option --direction DESCENDING"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SubtractElementsVertically
        df = SubtractElementsVertically(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SubtractElementsVertically --direction DESCENDING] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "SubVert_test4_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """Test avec un fichier de 2 champs; selection d'un champ et --direction ASCENDING"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SubtractElementsVertically
        df = SubtractElementsVertically(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 500] >> [SubtractElementsVertically --direction ASCENDING] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "SubVert_test5_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """Test sur un fichier dont les champs possèdent des intervalles - requete invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputTest6.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SubtractElementsVertically
        df = SubtractElementsVertically(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [SubtractElementsVertically --direction ASCENDING]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """Test avec 2 champs, plusieurs niveaux, differents forecastHours et --direction ASCENDING"""
        # open and read source
        source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SubtractElementsVertically
        df = SubtractElementsVertically(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SubtractElementsVertically --direction ASCENDING] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "SubVert_test7_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """Test avec 2 champs, plusieurs niveaux, differents forecastHours et --direction DESCENDING"""
        # open and read source
        source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SubtractElementsVertically
        df = SubtractElementsVertically(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SubtractElementsVertically --direction DESCENDING] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "SubVert_test8_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
