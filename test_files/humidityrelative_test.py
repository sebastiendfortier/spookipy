

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"HumidityRelative/testsFiles/"

class TestHumidityRelative(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 :  Calcul de l'humidité relative; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumidityRelative
        df = HumidityRelative(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_2(self):
        """Test #2 :  Calcul de l'humidité relative; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumidityRelative
        df = HumidityRelative(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_3(self):
        """Test #3 :  Calcul de l'humidité relative; utilisation d'une valeur invalide ( > borne maximale) pour -temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumidityRelative
        df = HumidityRelative(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_4(self):
        """Test #4 :  Calcul de l'humidité relative; utilisation d'une valeur invalide pour -temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumidityRelative
        df = HumidityRelative(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [HumidityRelative --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_5(self):
        """Test #5 :  Calcul de l'humidité relative (HR) à partir de l'humidité spécifique (HU)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumidityRelative
        df = HumidityRelative(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >> [HumidityRelative --iceWaterPhase WATER] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [Select --verticalLevel 1@0.859,0.126@0.103,0.00153@0.125] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_glbhyb_5_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_7(self):
        """Test #7 :  Calcul de l'humidité relative (HR) à partir du mélange de la vapeur d'eau (QV)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb_QV"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumidityRelative
        df = HumidityRelative(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,QV] >> [HumidityRelative --iceWaterPhase WATER] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_glbhyb_7_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_9(self):
        """Test #9 :  Calcul de l'humidité relative (HR) à partir de la température du point de rosée (TD)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb_ES"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumidityRelative
        df = HumidityRelative(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,TD] >> [HumidityRelative --iceWaterPhase WATER] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_glbhyb_9_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_10(self):
        """Test #10 :  Calcul de l'humidité relative (HR) à partir de la température du point de rosée (TD). fichier 5005"""
        # open and read source
        source0 = plugin_test_dir + "minimal_TTTDGZ_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumidityRelative
        df = HumidityRelative(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[Select --fieldName TT,TD] >> ', '[HumidityRelative --iceWaterPhase WATER] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_10.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


