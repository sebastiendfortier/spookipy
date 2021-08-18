

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"TemperatureWetBulb/testsFiles/"

class TestTemperatureWetBulb(unittest.TestCase):

    def test_1(self):
        """Test #1 :  Calculates wet-bulb temperature from a reghyb file."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureWetBulb
        df = TemperatureWetBulb(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,HU] >> [TemperatureWetBulb] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_reghyb_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Test #2 :  Calculates wet-bulb temperature from a regpres file."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureWetBulb
        df = TemperatureWetBulb(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TemperatureWetBulb] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_regpres_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Test #3 :  Calculates wet-bulb temperature from a glbeta file."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbeta"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureWetBulb
        df = TemperatureWetBulb(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,HU] >> [TemperatureWetBulb] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_glbeta_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Test #4 :  Calculates wet-bulb temperature using neil's files."""
        # open and read source
        source0 = plugin_test_dir + "inputforTW_withQV.fst"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureWetBulb
        df = TemperatureWetBulb(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TemperatureWetBulb] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2014051506_015_TW.fst"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
