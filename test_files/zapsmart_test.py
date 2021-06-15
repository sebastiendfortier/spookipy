

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"ZapSmart/testsFiles/"

class TestZapSmart(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 : test_zapsmart"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ZapSmart
        df = ZapSmart(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ZapSmart --fieldNameFrom UV --fieldNameTo TT --pdsLabelFrom WINDMODULUS --pdsLabelTo R1558V0N] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "zapSmart5x5x2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_2(self):
        """Test #2 : test_zapsmart_vertical_level1"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ZapSmart
        df = ZapSmart(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ZapSmart --verticalLevelFrom 500 --verticalLevelTo 333] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "zapSmartVerticalLevel1_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_3(self):
        """Test #3 : test_zapsmart_vertical_level2"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ZapSmart
        df = ZapSmart(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ZapSmart --verticalLevelFrom 500 --verticalLevelTo 750] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "zapSmartVerticalLevel2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_4(self):
        """Test #4 : test_zapsmart_vertical_level3"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ZapSmart
        df = ZapSmart(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ZapSmart --fieldNameFrom TT --fieldNameTo TT --verticalLevelFrom 500 --verticalLevelTo 1000] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "zapSmartVerticalLevel3_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_5(self):
        """Test #5 : test_zapsmart_typeOfField"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ZapSmart
        df = ZapSmart(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ZapSmart --typeOfFieldFrom FORECAST --typeOfFieldTo CLIMATOLOGY] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "zapsmart_typeOfField_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6(self):
        """Test #6 : test_zapsmart_dateOfOrigin"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ZapSmart
        df = ZapSmart(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ZapSmart --dateOfOriginFrom 20061116000000 --dateOfOriginTo 20120120120000] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "zapsmart_dateOfOrigin_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_7(self):
        """Test #7 : test_zapsmart_forecastHour"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ZapSmart
        df = ZapSmart(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ZapSmart --forecastHourFrom 0 --forecastHourTo 23] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "zapsmart_forecastHour_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_8(self):
        """Test #8 : test_zapsmart_userDefinedIndex"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ZapSmart
        df = ZapSmart(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[ZapSmart --userDefinedIndexFrom 0 --userDefinedIndexTo 99] >> ', '[WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]']

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "zapsmart_userDefinedIndex_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_9(self):
        """Test #9 : test_zapsmart_forecastHour"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ZapSmart
        df = ZapSmart(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[ZapSmart --forecastHourFrom 0:00:00 --forecastHourTo 23:00:00] >> ', '[WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]']

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "zapsmart_forecastHour_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


