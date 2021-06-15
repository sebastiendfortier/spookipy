

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"TemperatureAlongPseudoadiabat/testsFiles/"

class TestTemperatureAlongPseudoadiabat(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 : Comparaison des resultats entre un fichiers produits par Spooki et un obtenu par Sandrine des jobs operationnel."""
        # open and read source
        source0 = plugin_test_dir + "2014031006_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 1000] >> [TemperatureAlongPseudoadiabat --endLevel 10mb --increment 1mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TTPS_1000mb_to_10mb_inc_1mb_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_2(self):
        """Test #2 : Comparaison entre Spooki et les donnees calculees par Neil. de 829mb a 100mb, increment de 1mb."""
        # open and read source
        source0 = plugin_test_dir + "2x2_TT_829mb_2014040212_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 100mb --increment 1mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2x2_TTPS_829mb_to_100mb_inc_1mb_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_3(self):
        """Test #3 : Comparaison entre Spooki et les donnees calculees par Neil. de 789mb a 100mb, increment de 1mb."""
        # open and read source
        source0 = plugin_test_dir + "2x2_TT_789mb_2014040212_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 100mb --increment 1mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2x2_TTPS_789mb_to_100mb_inc_1mb_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_4(self):
        """Test #4 : Comparaison entre Spooki et les donnees calculees par Neil. de 24mb a 1000mb, increment de 1mb."""
        # open and read source
        source0 = plugin_test_dir + "2x2_TT_24mb_2014040212_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 1000mb --increment 1mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2x2_TTPS_24mb_to_1000mb_inc_1mb_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_5(self):
        """Test #5 : On essaie le plugin avec un fichier qui contient des TT de 100, 200, 300, 400, 500 et 600mb."""
        # open and read source
        source0 = plugin_test_dir + "TT_regpres_100a600mb_2014040212_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 1000mb --increment 1mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_6(self):
        """Test #6 : On essaie de calculer les temperatures pour deux champs TT a 600mb, un a 6hre et l'autre a 12hre."""
        # open and read source
        source0 = plugin_test_dir + "TT_regpres_600mb_forecastHour6et12_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 1000mb --increment 50mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_7(self):
        """Test #7 : Calcul de temperature avec TT et PX deja calcules."""
        # open and read source
        source0 = plugin_test_dir + "3x3_TTPX_regeta_2014041506_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 950mb --increment 50mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "3x3_TTPS_1100mb_to_1mb_inc_50mb_2014041506_024_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_8(self):
        """Test #8 : Calcul de temperature avec TT, P0 et PT sur grille de regeta."""
        # open and read source
        source0 = plugin_test_dir + "3x3_TTP0PT_regeta_2014041506_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 950mb --increment 50mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "3x3_P0_PT_TTPS_1100mb_to_1mb_inc_50mb_2014041506_024_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_9(self):
        """Test #9 : Calcul de temperature avec TT a 0.6034sg, P0 et PT sur grille de regeta et --endLevel SURFACE."""
        # open and read source
        source0 = plugin_test_dir + "3x3_TTPX_regeta_0.6034sg_2014041506_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel SURFACE --increment 50mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "3x3_TTPS_P0_PT_1100mb_to_1mb_inc_50mb_0.6034sg_2014041506_024_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_10(self):
        """Test #10 : On essaie le plugin avec un fichier en pression et en demandant de calculer la parcelle en mouvement ascendant."""
        # open and read source
        source0 = plugin_test_dir + "2x2_TT_789mb_2014040212_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 800mb --increment 10mb --direction ASCENDING] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_11(self):
        """Test #11 : On calcule la temperature avec un fichier en pression et en demandant de calculer la parcelle en mouvement descendant."""
        # open and read source
        source0 = plugin_test_dir + "2x2_TT_789mb_2014040212_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 800mb --increment 10mb --direction DESCENDING] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2x2_TTPS_789mb_to_800mb_inc_10mb_Descending_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_12(self):
        """Test #12 : On essaie le plugin avec un fichier en pression et en demandant de calculer la parcelle en mouvement descendant."""
        # open and read source
        source0 = plugin_test_dir + "2x2_TT_789mb_2014040212_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 600mb --increment 10mb --direction DESCENDING] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_13(self):
        """Test #13 : On calcule la temperature avec un fichier en pression et en demandant de calculer la parcelle en mouvement descendant."""
        # open and read source
        source0 = plugin_test_dir + "2x2_TT_789mb_2014040212_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 600mb --increment 10mb --direction ASCENDING] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2x2_TTPS_789mb_to_600mb_inc_10mb_Ascending_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_14(self):
        """Test #14 : Calcul de temperature avec TT a 0.6034sg, P0 et PT sur grille de regeta et --endLevel SURFACE et --direction DESCENDING."""
        # open and read source
        source0 = plugin_test_dir + "3x3_TTPX_regeta_0.6034sg_2014041506_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel SURFACE --increment 50mb --direction DESCENDING] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "3x3_TTPS_P0_PT_1100mb_to_1mb_inc_50mb_0.6034sg_2014041506_024_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_15(self):
        """Test #15 : Calcul de temperature avec TT a 0.6034sg, P0 et PT sur grille de regeta et --endLevel 550mb et --direction ASCENDING."""
        # open and read source
        source0 = plugin_test_dir + "3x3_TTPX_regeta_0.6034sg_2014041506_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 550mb --increment 50mb --direction ASCENDING] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "3x3_TTPS_P0_PT_1100mb_to_1mb_inc_50mb_0.6034sg_2014041506_024_withAscending_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_16(self):
        """Test #16 : Calcul de temperature avec TT a 0.6034sg, P0 et PT sur grille de regeta et --endLevel 600mb et --direction DESCENDING."""
        # open and read source
        source0 = plugin_test_dir + "3x3_TTPX_regeta_0.6034sg_2014041506_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureAlongPseudoadiabat
        df = TemperatureAlongPseudoadiabat(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TemperatureAlongPseudoadiabat --endLevel 600mb --increment 50mb --direction DESCENDING] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "3x3_TTPS_P0_PT_1100mb_to_1mb_inc_50mb_0.6034sg_2014041506_024_withDescending_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


