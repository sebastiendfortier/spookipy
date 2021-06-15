

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"VapourPressure/testsFiles/"

class TestVapourPressure(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 :  Calcul de la pression de vapeur; utilisation d'un unité invalide pour --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -30G]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_2(self):
        """Test #2 :  Calcul de la pression de vapeur; utilisation de valeur invalide ( < borne minimale) pour -temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch -273.16K]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_3(self):
        """Test #3 :  Calcul de la pression de vapeur; utilisation d'une valeur invalide ( > borne maximale) pour -temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VapourPressure --iceWaterPhase BOTH --temperaturePhaseSwitch 273.17K]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_4(self):
        """Test #4 :  Calcul de la pression de vapeur; utilisation d'une valeur invalide pour --iceWaterPhase."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VapourPressure --iceWaterPhase INVALIDE --temperaturePhaseSwitch 273.17K]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_5(self):
        """Test #5 : Calcul de la pression de vapeur avec un fichier hybrid (HU)."""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,HU] >> [VapourPressure ] >> [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "VapourPressure_hu_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6(self):
        """Test #6 : Calcul de la pression de vapeur avec un fichier hybrid (HU),  option --RPN."""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,HU] >> [VapourPressure --RPN] >> [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "rpnVapourPressure_hu_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6a(self):
        """Test #6a : Calcul de la pression de vapeur avec un fichier hybrid (HU)"""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,HU] >> [VapourPressure] >> [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_6a.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "rpnVapourPressure_hu_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_7(self):
        """Test #7 : Calcul de la pression de vapeur avec un fichier hybrid (HR)."""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,HR] >> [VapourPressure] >> [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "VapourPressure_hr_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_9(self):
        """Test #9 : Calcul de la pression de vapeur avec un fichier hybrid (ES)."""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,ES] >> [VapourPressure] >> [WriterStd --output {destination_path} --noMetadata --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "VapourPressure_es_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_11(self):
        """Test #11 : Calcul de la pression de vapeur avec un fichier en pression (QV)."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regeta_rdiag_hu"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VapourPressure ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_regeta_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_12(self):
        """Test #12 : Calcul de la pression de vapeur avec un fichier en pression (QV), option --RPN."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regeta_rdiag_hu"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [VapourPressure --RPN] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_regeta_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_13(self):
        """Test #13 : Calcul de la pression de vapeur avec un fichier hybrid 5005 (ES)."""
        # open and read source
        source0 = plugin_test_dir + "minimal_HU_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute VapourPressure
        df = VapourPressure(src_df0).compute()
        #['[ReaderStd --input {sources[0]} ] >> ', '[VapourPressure --RPN] >> ', '[WriterStd --output {destination_path} --noMetadata --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_13.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


