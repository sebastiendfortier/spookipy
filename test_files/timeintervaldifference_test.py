

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"TimeIntervalDifference/testsFiles/"

class TestTimeIntervalDifference(unittest.TestCase):

    def test_1(self):
        """Test #1 : Tester avec un interval 6 sur un range de 12 a 18 et a tous les sauts de 1."""
        # open and read source
        source0 = plugin_test_dir + "18_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "12_fileSrc.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 12@18 --interval 6 --step 1] >> [Zap --doNotFlagAsZapped --nbitsForDataStorage R13] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "18_12_diff_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_2(self):
        """Test #2 : Tester avec deux groupes d'interval."""
        # open and read source
        source0 = plugin_test_dir + "18_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "12_fileSrc.std"
        src_df1 = fstpy.StandardFileReader(source1)

        source2 = plugin_test_dir + "15_fileSrc.std"
        src_df2 = fstpy.StandardFileReader(source2)


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [ReaderStd --ignoreExtended --input {sources[2]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 15@18,12@18 --interval 3,6 --step 1,1] >> [WriterStd --output {destination_path} --ignoreExtended ]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "18_15_12_diff_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_3(self):
        """Test #3 : Tester avec un interval 6 sur un range de 6 a 12 et a tous les sauts de 1."""
        # open and read source
        source0 = plugin_test_dir + "PR2009051312_012_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "PR2009051312_006_fileSrc.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 6@12 --interval 6 --step 1] >> [Zap --doNotFlagAsZapped --nbitsForDataStorage R13] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "12_06_diff_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_4(self):
        """Test #4 : Tester avec un interval 6 sur un range de 12 a 18 et a tous les sauts de 1."""
        # open and read source
        source0 = plugin_test_dir + "18_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "12_fileSrc.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 12@18 --interval 6 --step 1] >> [Zap --doNotFlagAsZapped --nbitsForDataStorage R13] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "18_12_threshold0.02_diff_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_5(self):
        """Test #5 : Tester avec un fichier qui vient de regeta."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@177,0@60 --interval 12,3 --step 24,6] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "global20121217_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_6(self):
        """Test #6 :   Test avec une valeur invalide pour interval."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@177,0@60 --interval 0,3 --step 24,6] 

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_7(self):
        """Test #7 :   Test avec une valeur invalide pour step."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@177,0@60 --interval 12,3 --step 0,6] 

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_8(self):
        """Test #8 : Tester avec un fichier qui contient des champs TT et UV mais des UV qui sont a 0 et 20 dans le IP3"""
        # open and read source
        source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalDifference --fieldName UV --rangeForecastHour 12@36,12@36 --interval 3,12 --step 3,12] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_9(self):
        """Test #9 : Tester avec un Interval de 0@3 et de 0@9 sur un range de 3@9 avec un interval de 6 et un saut de 9."""
        # open and read source
        source0 = plugin_test_dir + "PR_Interval_012_0_3_fileSrc_encoded.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "PR_Interval_012_0_9_fileSrc_encoded.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 3@9 --interval 6 --step 9] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "03_09_interval_lb_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_10(self):
        """Test #10 : Tester avec un Interval de 0@9 et de 6@9 sur un range de 0@6 avec un interval de 6 et un saut de 9."""
        # open and read source
        source0 = plugin_test_dir + "PR_Interval_012_6_9_fileSrc_encoded.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "PR_Interval_012_0_9_fileSrc_encoded.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[ReaderStd --ignoreExtended --input {sources[1]}] >> ', '[TimeIntervalDifference --fieldName PR --rangeForecastHour 0@6 --interval 6 --step 9] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "00_06_interval_ub_diff_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_11(self):
        """Test #11 : Tester avec deux Interval de 0@3 et 9@12 et de 0@9 et 9@18 sur un range de 3@18 avec un interval de 6 et un saut de 9."""
        # open and read source
        source0 = plugin_test_dir + "PR_Interval_0-3_9-12_fileSrc_encoded.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "PR_Interval_0-9_9-18_fileSrc_encoded.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 3@18 --interval 6 --step 9] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "03-09_12-18_intervals_lb_diff_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_12(self):
        """Test #12 : Tester avec un Interval de 0@9 et de 6@9 sur un range de 0@6 avec un interval de 6 et un saut de 9."""
        # open and read source
        source0 = plugin_test_dir + "PR_Interval_0-9_9-18_fileSrc_encoded.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "PR_Interval_6-9_15-18_fileSrc_encoded.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@15 --interval 6 --step 9] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "00-06_09-15_intervals_ub_diff_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_13(self):
        """Test #13 : Tester avec un Interval de 0@9 et de 6@9 sur un range de 0@6 avec un interval de 6 et un saut de 9 en encodant la sortie."""
        # open and read source
        source0 = plugin_test_dir + "PR_Interval_012_6_9_fileSrc_encoded.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "PR_Interval_012_0_9_fileSrc_encoded.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@6 --interval 6 --step 9] >> [WriterStd --output {destination_path} --ignoreExtended --encodeIP2andIP3]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "00_06_interval_ub_diff_file2cmp_encoded.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_14(self):
        """Test #14 : Tester avec une valeur invalide pour rangeForecastHour."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@200 --interval 3 --step 3] 

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_15(self):
        """Test #15 : Tester avec l'intervalle 0@9 manquant dans le fichier source."""
        # open and read source
        source0 = plugin_test_dir + "PR_exclude_interval_0A9_fileSrc_encoded.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@15 --interval 3 --step 3] 

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_16(self):
        """Test #16 : Tester avec un range invalide pour --interval."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 3@6 --interval 4 --step 3] 

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_17(self):
        """Test #17 : Tester avec la valeur du lower bound de --forecastHour plus grande que son upper bound."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TimeIntervalDifference --fieldName PR --rangeForecastHour 9@6 --interval 3 --step 3] 

        #write the result
        results_file = TMP_PATH + "test_17.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_18(self):
        """Test #18 : Tester si single thread fonctionne. Probleme potentiel avec algorithm.hpp => Segmentation fault (core dumped)"""
        # open and read source
        source0 = plugin_test_dir + "SN0_SN1.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalDifference --fieldName SN --rangeForecastHour 0@1 --interval 1 --step 1] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "sn0_sn1_diff_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_19(self):
        """Test #19 : Tester avec un fichier qui contient des champs TT et UV mais des UV qui sont a 0 et 20 dans le IP3 avec strictlyPositive switch"""
        # open and read source
        source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalDifference --fieldName UV --rangeForecastHour 12@36,12@36 --interval 3,12 --step 3,12 --strictlyPositive] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_19.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_positive_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_20(self):
        """Test #20 : Tester avec un fichier qui contient des champs TT et UV mais des UV qui sont a 0 et 20 dans le IP3 avec strictlyPositive switch"""
        # open and read source
        source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[TimeIntervalDifference --fieldName UV --rangeForecastHour 12:00:00@36:00:00,12:00:00@36:00:00 --interval 3,12 --step 3,12 --strictlyPositive] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_positive_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_21(self):
        """Test #21 : Tester la presence de une des 2 parametres rangeForeCastHour"""
        # open and read source
        source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[TimeIntervalDifference --fieldName UV --interval 3,12 --step 3,12 --strictlyPositive] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_21.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_22(self):
        """Test #22 : Test interval patameter"""
        # open and read source
        source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[TimeIntervalDifference --fieldName UV --rangeForecastHour 12@36,12@36 --interval 3:00:00,12:00:00 --step 3,12 --strictlyPositive] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_positive_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_23(self):
        """Test #23 : Test step patameter"""
        # open and read source
        source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[TimeIntervalDifference --fieldName UV --rangeForecastHour 12@36,12@36 --interval 3,12 --step 3:00:00,12:00:00 --strictlyPositive] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_23.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_positive_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_24(self):
        """Test #24 : Test allHourMinuteSecond parameters"""
        # open and read source
        source0 = plugin_test_dir + "UVTT_3a24hre_delta3_IP3_20_40_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalDifference
        df = TimeIntervalDifference(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[TimeIntervalDifference --fieldName UV --rangeForecastHour 12:00:00@36:00:00,12:00:00@36:00:00 --interval 3:00:00,12:00:00 --step 3:00:00,12:00:00 --strictlyPositive] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_24.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UV_15a36_delta_3et12_positive_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


