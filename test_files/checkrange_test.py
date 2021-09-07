

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"CheckRange/testsFiles/"

class TestCheckRange(unittest.TestCase):

    def test_cr_1(self):
        """Tester avec tous les valeurs à l'intérieur du range."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckRange
        df = CheckRange(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [CheckRange --range -30@30] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_cr_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "cr1_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_cr_2(self):
        """Tester avec certaines valeurs à l'extérieur du range"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckRange
        df = CheckRange(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [CheckRange --range -25@28] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_cr_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "cr2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_cr_3(self):
        """Tester avec certaines valeurs sur les limites du range et l'option --strictComparisonOperator"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_int_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckRange
        df = CheckRange(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [CheckRange --range -13@28 --strictComparisonOperator] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_cr_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "cr3_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_cr_4(self):
        """Tester avec certaines valeurs sur les limites du range et sans l'option --strictComparisonOperator"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_int_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CheckRange
        df = CheckRange(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [CheckRange --range -13@28] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_cr_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "cr4_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
