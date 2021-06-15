

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"WaterVapourMixingRatio/testsFiles/"

class TestWaterVapourMixingRatio(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (HU), option --RPN"""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName HU] >>[WaterVapourMixingRatio --RPN] >>[WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "rpnWaterVapourMixingRatio_HU_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_3(self):
        """Test #3 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (TT et ES), option --RPN"""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName ES --exclude] >> ([Select --fieldName TT] + [DewPointDepression --iceWaterPhase WATER --RPN]) >> [WaterVapourMixingRatio --RPN] >>[WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "rpnWaterVapourMixingRatio_ES_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_4(self):
        """Test #4 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (TT et TD), option --RPN"""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER --RPN]) >>[WaterVapourMixingRatio --RPN] >>[WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "rpnWaterVapourMixingRatio_TD_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_5(self):
        """Test #5 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (HU)"""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName HU] >>[WaterVapourMixingRatio] >>[WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "WaterVapourMixingRatioHU_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6(self):
        """Test #6 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (PX,VPPR from TT,HR)"""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,HR] >>[WaterVapourMixingRatio] >>[WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "WaterVapourMixingRatioPXVPPR_HR_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_7(self):
        """Test #7 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (PX,VPPR from TT,ES)"""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName ES --exclude] >> ([Select --fieldName TT] + [DewPointDepression --iceWaterPhase WATER]) >> [WaterVapourMixingRatio] >>[WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "WaterVapourMixingRatioPXVPPR_ES_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_8(self):
        """Test #8 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride. (PX,VPPR from TT,TD)"""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >> [WaterVapourMixingRatio] >>[WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "WaterVapourMixingRatioPXVPPR_TD_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_9(self):
        """Test #9 :  Calcul du ratio de mélange de la vapeur d'eau; utilisation d'une unité invalide pour --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [WaterVapourMixingRatio --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_10(self):
        """Test #10 :  Calcul du ratio de mélange de la vapeur d'eau; utilisation de valeur invalide ( < borne minimale) pour --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [WaterVapourMixingRatio --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_11(self):
        """Test #11 :  Calcul du ratio de mélange de la vapeur d'eau; utilisation d'une valeur invalide ( > borne maximale) pour --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [WaterVapourMixingRatio --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_12(self):
        """Test #12 :  Calcul du ratio de mélange de la vapeur d'eau; utilisation d'une valeur invalide pour --iceWaterPhase."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [WaterVapourMixingRatio --iceWaterPhase INVALIDE --temperaturePhaseSwitch -40C]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_13(self):
        """Test #13 :  Calcul du ratio de mélange de de la vapeur d'eau à partir d'un fichier hybride 5005. (HU), option --RPN"""
        # open and read source
        source0 = plugin_test_dir + "minimal_HU_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WaterVapourMixingRatio
        df = WaterVapourMixingRatio(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ', '[Select --fieldName HU] >>', '[WaterVapourMixingRatio --RPN] >>', '[WriterStd --output {destination_path} --noMetadata --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_13.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


