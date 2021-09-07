

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"PrecipitationAmount/testsFiles/"

class TestPrecipitationAmount(unittest.TestCase):

    def test_1(self):
        """Tester avec une liste de fieldName invalide."""
        # open and read source
        source0 = plugin_test_dir + "18_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "12_fileSrc.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute PrecipitationAmount
        df = PrecipitationAmount(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [PrecipitationAmount --fieldName PR,TT --rangeForecastHour 12@18 --interval 6 --step 1] >> [Zap --pdsLabel R1558V0N] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Tester avec un interval 6 sur un range de 12 a 18 et a tous les sauts de 1."""
        # open and read source
        source0 = plugin_test_dir + "18_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "12_fileSrc.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute PrecipitationAmount
        df = PrecipitationAmount(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [PrecipitationAmount --fieldName PR --rangeForecastHour 12@18 --interval 6 --step 1] >> [Zap --pdsLabel R1558V0N] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "18_12_diff_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationAmount
        df = PrecipitationAmount(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[PrecipitationAmount --fieldName PR --rangeForecastHour 0@18,0@93 --interval 3,39 --step 3,18] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "global20121217_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationAmount
        df = PrecipitationAmount(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[PrecipitationAmount --fieldName PR --rangeForecastHour 0:00:00@18:00:00,0:00:00@93:00:00 --interval 3,39 --step 3,18] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "global20121217_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationAmount
        df = PrecipitationAmount(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[PrecipitationAmount --fieldName PR --rangeForecastHour 0@18,0@93 --interval 3:00:00,39:00:00 --step 3,18] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "global20121217_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """Tester avec une liste de valeurs pour rangeForecastHour, interval et step."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationAmount
        df = PrecipitationAmount(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[PrecipitationAmount --fieldName PR --rangeForecastHour 0@18,0@93 --interval 3,39 --step 3:00:00,18:00:00] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "global20121217_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """Test HourMinuteSecond parameters"""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationAmount
        df = PrecipitationAmount(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[PrecipitationAmount --fieldName PR --rangeForecastHour 0:00:00@18:00:00,0:00:00@93:00:00 --interval 3:00:00,39:00:00 --step 3:00:00,18:00:00] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "global20121217_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """Test HourMinuteSecond parameters step test"""
        # open and read source
        source0 = plugin_test_dir + "2020102212_023_lamwest_minimal.pres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationAmount
        df = PrecipitationAmount(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[PrecipitationAmount --fieldName PR --rangeForecastHour 22:30:00@23:00:00 --interval 0:30:00 --step 0:30:00] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_8.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
