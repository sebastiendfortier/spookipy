

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"VorticityPotential/testsFiles/"

class TestVorticityPotential(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 : Calculate with a simple test data """
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VorticityPotential
        df = VorticityPotential(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VorticityPotential --maxPVU 2.0] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "vortpo_file2cmp_test_1_20200707.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_2(self):
        """Test #2 : Invalid value for --maxPVU"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VorticityPotential
        df = VorticityPotential(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VorticityPotential --maxPVU 4.0]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_3(self):
        """Test #3 : SingleThread. Same as test 1 but in singlethread"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VorticityPotential
        df = VorticityPotential(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VorticityPotential --maxPVU 2.0 -T1] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "vortpo_file2cmp_test_1_20200707.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


