

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"PowerElementsByPoint/testsFiles/"

class TestPowerElementsByPoint(unittest.TestCase):

    def test_1(self):
        """Test #1 :  Test puissance normal - grouped"""
        # open and read source
        source0 = plugin_test_dir + "UUPOW_5x5.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[PowerElementsByPoint --baseFieldName UU --exponentFieldName POW] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_1.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Test #2 :  Test puissance normal, 1 forcastHour and 2 levels - grouped"""
        # open and read source
        source0 = plugin_test_dir + "input_5x5_2fh.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Select --forecastHour 12]>>', '[PowerElementsByPoint --baseFieldName TT --exponentFieldName UU] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Test #3 :  Test puissance normal, 2 forcastHour and 2 levels - grouped"""
        # open and read source
        source0 = plugin_test_dir + "input_5x5_2fh.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[PowerElementsByPoint --baseFieldName TT --exponentFieldName UU] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Test #4 :  Test puissance normal, 1 forcastHour, 2 levels base and 1 level exponent - grouped"""
        # open and read source
        source0 = plugin_test_dir + "input_5x5_2fh.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Select --forecastHour 12]>>([Select --fieldName TT] + [Select --fieldName UU --verticalLevel 1.0])>>', '[PowerElementsByPoint --baseFieldName TT --exponentFieldName UU] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_4.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """Test #5 :  Test puissance normal, 2 forcastHour, 2 levels base and 1 level exponent - grouped"""
        # open and read source
        source0 = plugin_test_dir + "input_5x5_2fh.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '([Select --fieldName TT] + [Select --fieldName UU --verticalLevel 1.0])>>', '[PowerElementsByPoint --baseFieldName TT --exponentFieldName UU] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_5.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """Test #6 :  Test puissance normal, 1 forcastHour, 1 levels base, 2 level exponent - grouped"""
        # open and read source
        source0 = plugin_test_dir + "input_5x5_2fh.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Select --forecastHour 12]>>([Select --fieldName UU] + [Select --fieldName TT --verticalLevel 1.0])>>', '[PowerElementsByPoint --baseFieldName TT --exponentFieldName UU] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_6.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """Test #7 :  Test puissance normal, 2 forcastHour, 1 levels base and 2 level exponent - grouped"""
        # open and read source
        source0 = plugin_test_dir + "input_5x5_2fh.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '([Select --fieldName UU] + [Select --fieldName TT --verticalLevel 1.0])>>', '[PowerElementsByPoint --baseFieldName TT --exponentFieldName UU]>>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_7.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """Test #8 :  Test puissance normal, 2 forcastHour, 1 levels base and 2 level exponent"""
        # open and read source
        source0 = plugin_test_dir + "input_5x5_2fh.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '([Select --fieldName UU] + [Select --fieldName TT --verticalLevel 1.0])>>', '[PowerElementsByPoint --baseFieldName TT --exponentFieldName UU] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_7.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """Test #9 :  Test puissance normal, 2 forcastHour, 1 levels base with one forecastHour and 1 level exponent with different forecastHour"""
        # open and read source
        source0 = plugin_test_dir + "input_5x5_2fh.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '([Select --fieldName UU --forecastHour 12] + [Select --fieldName TT --verticalLevel 1.0 --forecastHour 24])>>', '[PowerElementsByPoint --baseFieldName TT --exponentFieldName UU] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_9.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_10(self):
        """Test #10 :  Test puissance normal, 4 forcastHour, 2 levels base with 2 forecastHour and 2 level exponent with 2 different forecastHour"""
        # open and read source
        source0 = plugin_test_dir + "input_5x5_2fh.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '(([Select --fieldName UU --forecastHour 24] >> [Zap --forecastHour 48]) +([Select --fieldName UU --forecastHour 12] >> [Zap --forecastHour 36])+ [Select --fieldName TT])>>', '[PowerElementsByPoint --baseFieldName TT --exponentFieldName UU] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_10.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_11(self):
        """Test #11 :  Test puissance normal, 1 forcastHour, 2 levels base with 1 forecastHour and 1 level not equal to any of base"""
        # open and read source
        source0 = plugin_test_dir + "input_5x5_2fh.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '(([Select --fieldName UU --forecastHour 12 --verticalLevel 0.995] >> [Zap --verticalLevel 0.871175]) + [Select --fieldName TT --forecastHour 12])>>', '[PowerElementsByPoint --baseFieldName TT --exponentFieldName UU] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_11.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_12(self):
        """Test #12 :  Test puissance normal, 4 forcastHour, 2 levels base with 2 forecastHour and 2 level exponent with 1 different forecastHour"""
        # open and read source
        source0 = plugin_test_dir + "input_5x5_2fh.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PowerElementsByPoint
        df = PowerElementsByPoint(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '(([Select --fieldName UU --forecastHour 24] >> [Zap --forecastHour 48]) + [Select --fieldName UU --forecastHour 12] + [Select --fieldName TT])>>', '[Print --outputType VOIR]>>[PowerElementsByPoint --baseFieldName TT --exponentFieldName UU] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_12.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
