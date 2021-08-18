

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"SetUpperBoundary/testsFiles/"

class TestSetUpperBoundary(unittest.TestCase):

    def test_1(self):
        """Test #1 : PLUSIEURS champs en entree SANS l'option --outputFieldName."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_8_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SetUpperBoundary
        df = SetUpperBoundary(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SetUpperBoundary --value 5] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test1_maximum_file2cmp_20201019.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Test #2 : UN seul champ en entree SANS l'option --outputFieldName."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_8_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SetUpperBoundary
        df = SetUpperBoundary(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetUpperBoundary --value 0] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test2_maximum_file2cmp_20201019.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Test #3 : PLUSIEURS champs en entree AVEC l'option --outputFieldName. """
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_8_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SetUpperBoundary
        df = SetUpperBoundary(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SetUpperBoundary --value 0 --outputFieldName TEST]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Test #4 : UN seul champ en entree AVEC l'option --outputFieldName. """
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_8_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SetUpperBoundary
        df = SetUpperBoundary(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetUpperBoundary --value 0 --outputFieldName TEST] >> [WriterStd --output {destination_path} --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test4_maximum_file2cmp_20201019.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
