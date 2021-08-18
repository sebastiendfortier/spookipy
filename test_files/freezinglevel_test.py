

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"FreezingLevel/testsFiles/"

class TestFreezingLevel(unittest.TestCase):

    def test_1(self):
        """Test #1 :  Test avec un fichier maison de 10 cas différents où la courbe de température croise le 0 deg C (matrice 10x1), avec l'option --outputVerticalRepresentation BOTH."""
        # open and read source
        source0 = plugin_test_dir + "inputFileMillibar.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation BOTH --forcedForTestsOnly] >> [Select --fieldName FRH,BOVS,NBFL] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Test #2 :  Test avec un fichier maison de 10 cas différents où la courbe de température croise le 0 deg C (matrice 10x1), avec l'option -maxNbFzLvl 1 et --outputVerticalRepresentation BOTH."""
        # open and read source
        source0 = plugin_test_dir + "inputFileMillibar.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation BOTH --maxNbFzLvl 1 --forcedForTestsOnly] >> [Select --fieldName FRH,BOVS,NBFL] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Test #3 :  Test avec un fichier maison de 10 cas différents où la courbe de température croise le 0 deg C (matrice 10x1), avec l'option -maxNbFzLvl 1 et --outputVerticalRepresentation GEOPOTENTIAL."""
        # open and read source
        source0 = plugin_test_dir + "inputFileMillibar.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation GEOPOTENTIAL --forcedForTestsOnly] >> [Select --fieldName FRH,BOVS,NBFL] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Test #4 :  Test avec un fichier maison de 10 cas différents où la courbe de température croise le 0 deg C (matrice 10x1), avec l'option -maxNbFzLvl 3 et --outputVerticalRepresentation BOTH."""
        # open and read source
        source0 = plugin_test_dir + "inputFileMillibar.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation BOTH --maxNbFzLvl 3 --forcedForTestsOnly] >> [Select --fieldName FRH,BOVS,NBFL] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """Test #5 :  Test avec un fichier maison de 10 cas différents où la courbe de température croise le 0 deg C (matrice 10x1), avec l'option -maxNbFzLvl 3 et --outputVerticalRepresentation GEOPOTENTIAL."""
        # open and read source
        source0 = plugin_test_dir + "inputFileMillibar.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation GEOPOTENTIAL --maxNbFzLvl 3 --forcedForTestsOnly] >> [Select --fieldName FRH,BOVS,NBFL] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """Test #6 :  Test avec un fichier sortie de modele eta, avec l'option --outputVerticalRepresentation PRESSURE."""
        # open and read source
        source0 = plugin_test_dir + "inputFile2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation PRESSURE --maxNbFzLvl 5] >> [Select --fieldName FRP,BOVS,NBFL] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test6.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """Test #7 :  Test avec un fichier sortie de modele sigma, avec l'option --outputVerticalRepresentation GEOPOTENTIAL."""
        # open and read source
        source0 = plugin_test_dir + "inputFile2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation GEOPOTENTIAL --maxNbFzLvl 5 ] >> [Select --fieldName FRH,BOVS,NBFL] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test7.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """Test #8 :  Test avec un fichier sortie de modele sigma, avec l'option --outputVerticalRepresentation BOTH."""
        # open and read source
        source0 = plugin_test_dir + "inputFile2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [FreezingLevel  --outputVerticalRepresentation BOTH --maxNbFzLvl 5] >> [Select --fieldName FRH,BOVS,NBFL] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test7.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """Test #9 :  Test avec un fichier contenant a la fois des niveaux pressions et des niveaux sigma"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation GEOPOTENTIAL --maxNbFzLvl 5] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_with_sigma_level_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_10(self):
        """Test #10 :  Test de l'option --highestFreezingLevel (outputVerticalRepresentation == BOTH et highestFreezingLevel == BOTH)"""
        # open and read source
        source0 = plugin_test_dir + "inputFile2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation BOTH --maxNbFzLvl 5 --highestFreezingLevel BOTH] >> [WriterStd --output {destination_path} --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test10_20201021.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_15(self):
        """Test #15 :  Test de l'option --highestFreezingLevel (outputVerticalRepresentation == BOTH et highestFreezingLevel == YES)"""
        # open and read source
        source0 = plugin_test_dir + "inputFile2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation BOTH --maxNbFzLvl 5 --highestFreezingLevel YES] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test15_20201021.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_16(self):
        """Test #16 :  Test de l'option --highestFreezingLevel (outputVerticalRepresentation == PRESSURE et highestFreezingLevel == YES)"""
        # open and read source
        source0 = plugin_test_dir + "testcases2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation PRESSURE --maxNbFzLvl 5 --highestFreezingLevel YES --forcedForTestsOnly ]

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_18(self):
        """Test #18 :  Test de l'option --highestFreezingLevel (outputVerticalRepresentation == PRESSURE et highestFreezingLevel == YES)"""
        # open and read source
        source0 = plugin_test_dir + "testcases2-2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation PRESSURE --maxNbFzLvl 5 --highestFreezingLevel YES --forcedForTestsOnly ] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test18_20201021.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_19(self):
        """Test #19 :  Test de l'option --highestFreezingLevel (outputVerticalRepresentation == GEOPOTENTIAL et highestFreezingLevel == YES)"""
        # open and read source
        source0 = plugin_test_dir + "testcases3-2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation GEOPOTENTIAL --maxNbFzLvl 5 --highestFreezingLevel YES --forcedForTestsOnly] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_19.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test19_20201021.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_20(self):
        """Test #20 :  Test de l'option --highestFreezingLevel (outputVerticalRepresentation == GEOPOTENTIAL et highestFreezingLevel == YES)"""
        # open and read source
        source0 = plugin_test_dir + "testcases4-2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation GEOPOTENTIAL --maxNbFzLvl 5 --highestFreezingLevel YES --forcedForTestsOnly] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test20_20201021.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_21(self):
        """Test #21 :  Test de l'option --highestFreezingLevel (outputVerticalRepresentation == BOTH et highestFreezingLevel == YES)"""
        # open and read source
        source0 = plugin_test_dir + "testcases3-2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FreezingLevel --outputVerticalRepresentation BOTH --maxNbFzLvl 5 --highestFreezingLevel YES --forcedForTestsOnly] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_21.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "FreezingLevel_file2cmp_test21_20201021.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_22(self):
        """Test #22 :  Test avec un fichier 5005, avec les options --outputVerticalRepresentation BOTH --highestFreezingLevel BOTH et --maxNbFzLvl 2."""
        # open and read source
        source0 = plugin_test_dir + "minimal_TTHUGZ_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FreezingLevel
        df = FreezingLevel(src_df0).compute()
        #['[ReaderStd --input {sources[0]} ] >> ', '[FreezingLevel --outputVerticalRepresentation BOTH --highestFreezingLevel BOTH --maxNbFzLvl 2 --forcedForTestsOnly] >> ', '[WriterStd --output {destination_path} ]']

        #write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_22.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
