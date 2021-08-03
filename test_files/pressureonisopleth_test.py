

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"PressureOnIsopleth/testsFiles/"

class TestPressureOnIsopleth(unittest.TestCase):

    def test_1(self):
        """Test #1 : Calculate with a simple test data """
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnIsopleth
        df = PressureOnIsopleth(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnIsopleth --fieldName TT --scanDirection DESCENDING --fieldConstant 20 --outputFieldName PXXX] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test1_file2cmp_20200813.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_2(self):
        """Test #2 : Utilisation de --outputFieldName avec une valeur > 4 caractères."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnIsopleth
        df = PressureOnIsopleth(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnIsopleth --fieldName TT --scanDirection DESCENDING --fieldConstant 20 --outputFieldName ABCDEF] 

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_3(self):
        """Test #3 : Utilisation de --fieldName avec une valeur > 4 caractères."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnIsopleth
        df = PressureOnIsopleth(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnIsopleth --fieldName ABCDE --scanDirection DESCENDING --fieldConstant 20 --outputFieldName PXXX] 

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_4(self):
        """Test #4 : Calculate more test data with multiple fieldConstant, DESCENDING scandDirection and cases with larger and smaller values"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnIsopleth
        df = PressureOnIsopleth(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnIsopleth --fieldName TT --scanDirection DESCENDING --fieldConstant 15,20,30 --outputFieldName PXXX] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "prsiso_file2cmp_test_4_20200813.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_5(self):
        """Test #5 :  Calculate more test data with multiple fieldConstant, ASCENDING scandDirection and cases with larger and smaller values"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnIsopleth
        df = PressureOnIsopleth(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnIsopleth --fieldName TT --scanDirection ASCENDING --fieldConstant 15,20,30 --outputFieldName PXXX] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "prsiso_file2cmp_test_5_20200813.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_6(self):
        """Test #6 : Same as test 1 but in singlethread"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnIsopleth
        df = PressureOnIsopleth(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnIsopleth --fieldName TT --scanDirection DESCENDING --fieldConstant 20 --outputFieldName PXXX] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test1_file2cmp_20200813.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


