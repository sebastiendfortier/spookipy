

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"SetLowerBoundary/testsFiles/"

class TestSetLowerBoundary(unittest.TestCase):

    def test_1(self):
        """PLUSIEURS champs en entree SANS l'option --outputFieldName."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SetLowerBoundary
        df = SetLowerBoundary(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SetLowerBoundary --value 0] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test1_minimum_file2cmp_20201019.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """UN seul champ en entree SANS l'option --outputFieldName."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SetLowerBoundary
        df = SetLowerBoundary(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetLowerBoundary --value 0] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test2_minimum_file2cmp_20201019.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """PLUSIEURS champs en entree AVEC l'option --outputFieldName. """
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SetLowerBoundary
        df = SetLowerBoundary(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SetLowerBoundary --value 0 --outputFieldName TEST]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """UN seul champ en entree AVEC l'option --outputFieldName. """
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SetLowerBoundary
        df = SetLowerBoundary(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetLowerBoundary --value 0 --outputFieldName TEST] >> [WriterStd --output {destination_path} --noUnitConversion ]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test4_minimum_file2cmp_20201019.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """Valeur trop longue pour --outputFieldName. """
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SetLowerBoundary
        df = SetLowerBoundary(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetLowerBoundary --value 0 --outputFieldName TROPLONG]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """Valeur trop courte pour --outputFieldName. """
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SetLowerBoundary
        df = SetLowerBoundary(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetLowerBoundary --value 0 --outputFieldName T]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
