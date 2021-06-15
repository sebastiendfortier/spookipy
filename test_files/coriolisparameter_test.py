

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"CoriolisParameter/testsFiles/"

class TestCoriolisParameter(unittest.TestCase):

    def test_regcoriop_test_1(self):
        """Test #1 : Calculate with a simple test data """
        # open and read source
        source0 = plugin_test_dir + "UUVVTT_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CoriolisParameter
        df = CoriolisParameter(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [CoriolisParameter] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "coriop_test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "coriop_file2cmp_test_1.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regcoriop_test_2(self):
        """Test #2 : Spooki must success when input are in millibars"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CoriolisParameter
        df = CoriolisParameter(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >>[CoriolisParameter]

        #write the result
        results_file = TMP_PATH + "coriop_test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regcoriop_test_3(self):
        """Test #3 : SingleThread. Same as test 1 but in singlethread"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CoriolisParameter
        df = CoriolisParameter(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [CoriolisParameter] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "coriop_test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "coriop_file2cmp_test_3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


