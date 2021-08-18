

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"PressureOnConstantPotentialVorticity/testsFiles/"

class TestPressureOnConstantPotentialVorticity(unittest.TestCase):

    def test_1(self):
        """Test #1 : Invalid value for --PVU"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnConstantPotentialVorticity
        df = PressureOnConstantPotentialVorticity(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnConstantPotentialVorticity --PVU 4.0]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Test #2 : Calculate with a small regpres file"""
        # open and read source
        source0 = plugin_test_dir + "regpres_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnConstantPotentialVorticity
        df = PressureOnConstantPotentialVorticity(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnConstantPotentialVorticity --PVU 1.5,2.0] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "regpres_small_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Test #3 : Calculate with a simple test data """
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnConstantPotentialVorticity
        df = PressureOnConstantPotentialVorticity(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnConstantPotentialVorticity --PVU 2.0] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "regpres_file2cmp_test3_20200712.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Test #4 : Same as test 1 but in singlethread"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnConstantPotentialVorticity
        df = PressureOnConstantPotentialVorticity(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnConstantPotentialVorticity --PVU 2.0 -T1] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "regpres_file2cmp_test3_20200712.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """Test #5 : Calculate with more test data with multiple PVU"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnConstantPotentialVorticity
        df = PressureOnConstantPotentialVorticity(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnConstantPotentialVorticity --PVU 1.5,2.0,3.0] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "regpres_file2cmp_test5_20200712.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """Test #6 : Calculate with more test data with multiple PVU but not in order"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PressureOnConstantPotentialVorticity
        df = PressureOnConstantPotentialVorticity(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PressureOnConstantPotentialVorticity --PVU 3.0,2.0,1.5] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "regpres_file2cmp_test5_20200712.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
