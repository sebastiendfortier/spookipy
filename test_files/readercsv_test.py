

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"ReaderCsv/testsFiles/"

class TestReaderCsv(unittest.TestCase):

    def test_1(self):
        """test_read_csv_pds1_level2"""
        # open and read source
        source0 = plugin_test_dir + "pds1_level2.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "pds1_level2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """test_read_csv_gds1_pds1_level2"""
        # open and read source
        source0 = plugin_test_dir + "gds1_pds1_level2.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}] >> [PrintIMO] >> [Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "gds1_pds1_level2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """test_read_csv_missing_eol_at_last_line_of_data"""
        # open and read source
        source0 = plugin_test_dir + "missing_eol_at_last_line_of_data.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "pds1_level2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """test_read_csv_pds1_level2_inversed_level_order"""
        # open and read source
        source0 = plugin_test_dir + "pds1_level2_inversed_level_order.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "pds1_level2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """test_read_csv_withSpace"""
        # open and read source
        source0 = plugin_test_dir + "with_space.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "pds1_level2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """test_read_csv_withComments"""
        # open and read source
        source0 = plugin_test_dir + "with_comments.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "pds1_level2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """test_read_csv_pds2"""
        # open and read source
        source0 = plugin_test_dir + "pds2.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "pds2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """test_read_csv_not_all_same_number_of_lines_in_a_pds"""
        # open and read source
        source0 = plugin_test_dir + "not_all_same_number_of_lines_in_a_pds.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """test_read_csv_not_all_same_number_of_items_in_lines_of_a_pds"""
        # open and read source
        source0 = plugin_test_dir + "not_all_same_number_of_items_in_lines_of_a_pds.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_10(self):
        """test_read_csv_only_1_line_per_level"""
        # open and read source
        source0 = plugin_test_dir + "only_1_line_per_level.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "only_1_line_per_level_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_11(self):
        """test_read_csv_only_1_item_per_line"""
        # open and read source
        source0 = plugin_test_dir + "only_1_item_per_line.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "only_1_item_per_line_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_12(self):
        """test missing value when one data by line"""
        # open and read source
        source0 = plugin_test_dir + "missingvalue.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_13(self):
        """test missing value when multiple data on a line separated by comma"""
        # open and read source
        source0 = plugin_test_dir + "missingvalue2.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ReaderCsv
        df = ReaderCsv(src_df0).compute()
        #[ReaderCsv --input {sources[0]}]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
