

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"HumiditySpecific/testsFiles/"

class TestHumiditySpecific(unittest.TestCase):

    def test_regtest_a(self):
        """Test #1 :  Calcul de l'humidité spécifique; utilisation de --iceWaterPhase sans --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase BOTH]

        #write the result
        results_file = TMP_PATH + "test_a.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_2(self):
        """Test #2 :  Calcul de l'humidité spécifique; utilisation de --temperaturePhaseSwitch sans --iceWaterPhase."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --temperaturePhaseSwitch -30C]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_c(self):
        """Test #3 :  Calcul de l'humidité spécifique; utilisation de --iceWaterPhase WATER avec --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase WATER --temperaturePhaseSwitch -30C]

        #write the result
        results_file = TMP_PATH + "test_c.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_4(self):
        """Test #4 :  Calcul de l'humidité spécifique; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_5(self):
        """Test #5 :  Calcul de l'humidité spécifique; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_6(self):
        """Test #6 :  Calcul de l'humidité spécifique; utilisation d'une valeur invalide ( > borne maximale) pour -temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_7(self):
        """Test #7 :  Calcul de l'humidité spécifique; utilisation d'une valeur invalide pour -temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [HumiditySpecific --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_8(self):
        """Test #8 :  Calcul de l'humidité spécifique (HU) à partir de l'humidité relative (HR)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HR] >> [HumiditySpecific --iceWaterPhase WATER] >> [Zap --pdsLabel R1580V0N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "regpres_testWithHR_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_10(self):
        """Test #10 :  Calcul de l'humidité spécifique (HU) à partir de ES et TT."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >> ([DewPointDepression --iceWaterPhase WATER] + [Select --fieldName TT]) >> [HumiditySpecific --iceWaterPhase WATER] >> [Zap --pdsLabel R1580V0N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "regpres_testWithES_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_11(self):
        """Test #11 :  Calcul de l'humidité spécifique (HU) à partir de ES et TT, option --RPN."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >> ([DewPointDepression --iceWaterPhase WATER --RPN] + [Select --fieldName TT]) >> [HumiditySpecific --iceWaterPhase WATER --RPN] >> [Zap --pdsLabel R1580V0N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "regpres_testWithES_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_12(self):
        """Test #12 :  Calcul de l'humidité spécifique (HU) à partir de la température du point de rosée (TD)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >> ([DewPointDepression --iceWaterPhase WATER] + [Select --fieldName TT]) >> ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >> [HumiditySpecific --iceWaterPhase WATER] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_4_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_13(self):
        """Test #13 :  Calcul de l'humidité spécifique (HU) à partir de la température du point de rosée (TD), option --RPN."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >> ([DewPointDepression --iceWaterPhase WATER --RPN] + [Select --fieldName TT]) >> ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >> [HumiditySpecific --iceWaterPhase WATER --RPN] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_4_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_14(self):
        """Test #14 :  Calcul de l'humidité spécifique (HU) à partir du rapport de mélange de la vapeur d'eau (QV)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HumiditySpecific
        df = HumiditySpecific(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,ES] >> ([DewPointDepression --iceWaterPhase WATER] + [Select --fieldName TT]) >> [WaterVapourMixingRatio ] >> [HumiditySpecific --iceWaterPhase WATER] >> [Zap --pdsLabel R1580V0N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "regpres_testWithQV.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


