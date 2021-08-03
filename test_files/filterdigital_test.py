# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"FilterDigital/testsFiles/"

class TestFilterDigital(unittest.TestCase):

    def test_1(self):
        """Test #1 :  Test 1 répétition avec un filtre standard."""
        # open and read source
        source0 = plugin_test_dir + "UUVVfil5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1 --repetitions 1] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filter1_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_2(self):
        """Test #2 :  Test 3 répétitions avec un filtre standard."""
        # open and read source
        source0 = plugin_test_dir + "UUVVfil5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1 --repetitions 3] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filter2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_3(self):
        """Test #3 :  Test 1 répétition avec un long filtre et un fichier provenant du site de rpn PGSM."""
        # open and read source
        source0 = plugin_test_dir + "UU11x11_1_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1,1,1,1,1,1,1 --repetitions 1] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filter3_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_4(self):
        """Test #4 :  Test 3 répétitions avec un long filtre et un fichier provenant du site de rpn PGSM."""
        # open and read source
        source0 = plugin_test_dir + "UU11x11_1_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1,1,1,1,1,1,1 --repetitions 3] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filter4_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_5(self):
        """Test #5 :  Test 1 répétition avec un filtre à 1 chiffre."""
        # open and read source
        source0 = plugin_test_dir + "UUVVfil5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1 --repetitions 1] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filter5_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_6(self):
        """Test #6 :  Test 1 répétition avec un long filtre et un gros fichier."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1,2,2,1,1,1,1 --repetitions 1] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filter6_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_7(self):
        """Test #7 :  Test 3 répétitions avec un long filtre et un gros fichier."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1,2,2,1,1,1,1 --repetitions 3] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filter7_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_8(self):
        """Test #8 :  Test 3 répétitions avec un long filtre, poids importants et un gros fichier."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1,2,3,2,1,1,1 --repetitions 3] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filter8_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_9(self):
        """Test #9 :  Test de comparaison avec le programme pgsm FILTRE3PTS3X."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel R1558V0N] >> [FilterDigital --filter 2,4,2 --repetitions 3] >> [Zap --userDefinedIndex 303 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filteredByPgsm1_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_10(self):
        """Test #10 :  Test de comparaison avec le programme pgsm FILTRE3PTS1X."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel R1558V0N] >> [FilterDigital --filter 2,4,2 --repetitions 1] >> [Zap --userDefinedIndex 301 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filteredByPgsm2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_11(self):
        """Test #11 :  Test de comparaison avec le programme pgsm FILTRE5PTS2X."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel R1558V0N] >> [FilterDigital --filter 1,2,4,2,1 --repetitions 2] >> [Zap --userDefinedIndex 502 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filteredByPgsm3_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_12(self):
        """Test #12 :  Test de comparaison avec le programme pgsm FILTRE9PTS1X."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel R1558V0N] >> [FilterDigital --filter 1,1,1,1,1,1,1,1,1 --repetitions 1] >> [Zap --userDefinedIndex 901 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filteredByPgsm4_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_13(self):
        """Test #13 :  Test de comparaison."""
        # open and read source
        source0 = plugin_test_dir + "LATLON_L_9x11_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [FilterDigital --filter 1 --repetitions 1] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "LATLON_L_9x11_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_14(self):
        """Test #14 :  Test 1 répétition avec un filtre standard et l'option outputFieldName."""
        # open and read source
        source0 = plugin_test_dir + "UUVVfil5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute FilterDigital
        df = FilterDigital(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU* ] >> [FilterDigital --filter 1,1,1 --repetitions 1 --outputFieldName abcd] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "filter9_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


