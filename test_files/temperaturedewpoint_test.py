

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"TemperatureDewPoint/testsFiles/"

class TestTemperatureDewPoint(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 :  Calcul du point de rosée; utilisation de --iceWaterPhase BOTH mais sans --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFileSimple.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureDewPoint
        df = TemperatureDewPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TemperatureDewPoint --iceWaterPhase BOTH ]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_2(self):
        """Test #2 :  Calcul du point de rosée; utilisation de --iceWaterPhase avec une valeur invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFileSimple.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureDewPoint
        df = TemperatureDewPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TemperatureDewPoint --iceWaterPhase ICE ]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_3(self):
        """Test #3 :  Calcul du point de rosée; unité de --temperaturePhaseSwitch invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFileSimple.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureDewPoint
        df = TemperatureDewPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40G ]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_4(self):
        """Test #4 :  Calcul du point de rosée à partir d'une matrice de températures de 5x4x3 et d'écarts de point de rosée de 5x4x2"""
        # open and read source
        source0 = plugin_test_dir + "inputFileSimple.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureDewPoint
        df = TemperatureDewPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TemperatureDewPoint_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_5(self):
        """Test #5 :  Calcul du point de rosée à partir d'un fichier du global hybrid en utilisant TT et ES."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureDewPoint
        df = TemperatureDewPoint(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,ES] >>[TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_es_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6(self):
        """Test #6 :  Calcul du point de rosée à partir d'un fichier du global hybrid en utilisant TT et ES, option --RPN."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureDewPoint
        df = TemperatureDewPoint(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,ES] >>[TemperatureDewPoint --iceWaterPhase BOTH --RPN] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "rpn2011100712_012_glbhyb_es_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_7(self):
        """Test #7 :  Calcul du point de rosée à partir d'un fichier du global hybrid en utilisant TT et HR."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureDewPoint
        df = TemperatureDewPoint(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HR] >> [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_hr_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_9(self):
        """Test #9 :  Calcul du point de rosée à partir d'un fichier du global hyb (TT et HU)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureDewPoint
        df = TemperatureDewPoint(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >> [TemperatureDewPoint --iceWaterPhase WATER] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_hu_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_11(self):
        """Test #11 :  Calcul du point de rosée à partir d'un fichier du global hybrid (TT et QV)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb_QV"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureDewPoint
        df = TemperatureDewPoint(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureDewPoint --iceWaterPhase WATER ] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_qv_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_12(self):
        """Test #12 :  Calcul du point de rosée à partir d'un fichier du global hybrid 5005 (TT et HU)."""
        # open and read source
        source0 = plugin_test_dir + "minimal_TTHUGZ_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureDewPoint
        df = TemperatureDewPoint(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]} ] >> ', '[TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_12.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


