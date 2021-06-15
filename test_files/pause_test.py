

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"Pause/testsFiles/"

class TestPause(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 : """
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pause
        df = Pause(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Pause --time MUFFIN] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test1_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_2(self):
        """Test #2 : """
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pause
        df = Pause(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Pause --time CAFE] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


