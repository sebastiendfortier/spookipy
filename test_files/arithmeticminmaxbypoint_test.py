

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"ArithmeticMinMaxByPoint/testsFiles/"

class TestArithmeticMinMaxByPoint(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1: Successfully find both the minimum and the maximum. Default outputFieldName1/2. Small custom file."""
        # open and read source
        source0 = plugin_test_dir + "TTHRHU_3X3X2_SrcFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMinMaxByPoint
        df = ArithmeticMinMaxByPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ArithmeticMinMaxByPoint --minMax BOTH] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TTHRHU_3X3X2_BOTH_File2Cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_2(self):
        """Test #2: Successfully find the minimum, exclusively. Custom outputFieldName1. Small custom file."""
        # open and read source
        source0 = plugin_test_dir + "TTHRHU_3X3X2_SrcFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMinMaxByPoint
        df = ArithmeticMinMaxByPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ArithmeticMinMaxByPoint --minMax MIN --outputFieldName1 MNTH] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TTHRHU_3X3X2_MIN_File2Cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_3(self):
        """"""
        # open and read source
        source0 = plugin_test_dir + "TTHRHU_3X3X2_SrcFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMinMaxByPoint
        df = ArithmeticMinMaxByPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ArithmeticMinMaxByPoint --minMax MAX --outputFieldName1 MNTH] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TTHRHU_3X3X2_MAX_File2Cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_4(self):
        """"""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_regeta_1_petit"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMinMaxByPoint
        df = ArithmeticMinMaxByPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ArithmeticMinMaxByPoint --minMax BOTH --outputFieldName1 MNRE --outputFieldName2 MXRE] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2016031600_024_regeta_1_petit_MINMAX.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_5(self):
        """"""
        # open and read source
        source0 = plugin_test_dir + "TTES2x2x4_MinMax_DifferentForecastHours_SrcFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMinMaxByPoint
        df = ArithmeticMinMaxByPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ArithmeticMinMaxByPoint --minMax BOTH --outputFieldName2 MXFH --groupBy FORECAST_HOUR] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TTES2x2x4_MinMax_DifferentForecastHours_File2Cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6(self):
        """Test avec option --minMax MIN mais sans regrouper les forecast hour."""
        # open and read source
        source0 = plugin_test_dir + "TTES2x2x4_MinMax_DifferentForecastHours_SrcFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMinMaxByPoint
        df = ArithmeticMinMaxByPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ArithmeticMinMaxByPoint --minMax MIN ] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TTES2x2x4_DiffForecastHrs_NoGroupBy_File2Cmp_20200508.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_7(self):
        """Cherche le min lorsqu'il y a seulement 1 champ en entrée."""
        # open and read source
        source0 = plugin_test_dir + "TTES2x2x4_MinMax_DifferentForecastHours_SrcFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMinMaxByPoint
        df = ArithmeticMinMaxByPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> [ArithmeticMinMaxByPoint --minMax MIN --groupBy FORECAST_HOUR] 

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_8(self):
        """Utilisation de --outputFieldName avec une valeur > 4 caractères."""
        # open and read source
        source0 = plugin_test_dir + "TTES2x2x4_MinMax_DifferentForecastHours_SrcFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMinMaxByPoint
        df = ArithmeticMinMaxByPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ArithmeticMinMaxByPoint --minMax MIN --outputFieldName1 TROPLONG] 

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


