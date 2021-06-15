

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"SaturationVapourPressure/testsFiles/"

class TestSaturationVapourPressure(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 :  Calcul de la pression de vapeur saturante; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SaturationVapourPressure
        df = SaturationVapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_2(self):
        """Test #2 :  Calcul de la pression de vapeur saturante; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SaturationVapourPressure
        df = SaturationVapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_3(self):
        """Test #3 :  Calcul de la pression de vapeur saturante; utilisation d'une valeur invalide ( > borne maximale) pour -temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SaturationVapourPressure
        df = SaturationVapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_4(self):
        """Test #4 :  Calcul de la pression de vapeur saturante; utilisation d'une valeur invalide pour --iceWaterPhase."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SaturationVapourPressure
        df = SaturationVapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_5(self):
        """Test #5 :  Calcul de la pression de vapeur saturante; utilisation de --iceWaterPhase BOTH mais sans --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFileSimple.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SaturationVapourPressure
        df = SaturationVapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase BOTH ]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_6(self):
        """Test #6 : Calcul de la pression de vapeur saturante avec un fichier hybrid."""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SaturationVapourPressure
        df = SaturationVapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SaturationVapourPressure --iceWaterPhase WATER] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "SaturationVapourPressure_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_7(self):
        """Test #7 : Calcul de la pression de vapeur saturante avec un fichier hybrid 5005."""
        # open and read source
        source0 = plugin_test_dir + "minimal_4conve_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SaturationVapourPressure
        df = SaturationVapourPressure(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ', '[SaturationVapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_7.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


