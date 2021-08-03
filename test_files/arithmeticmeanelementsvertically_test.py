

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"ArithmeticMeanElementsVertically/testsFiles/"

class TestArithmeticMeanElementsVertically(unittest.TestCase):

    def test_1(self):
        """Test #1 : Calcul des moyennes verticales de chaque champ."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMeanElementsVertically
        df = ArithmeticMeanElementsVertically(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ArithmeticMeanElementsVertically] >> [Zap --pdsLabel MEANCOLUMNS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "mean_columns_Forward_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_2(self):
        """Test #2 : Calcul des moyennes verticales avec un niveau seulement."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMeanElementsVertically
        df = ArithmeticMeanElementsVertically(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 500] >> [ArithmeticMeanElementsVertically] >> [Zap --pdsLabel MEANCOLUMNS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "mean_oneInputOnly_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_3(self):
        """Test #3 : Calcul des moyennes verticales avec un seul champ et utilisation de --outputFieldName."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMeanElementsVertically
        df = ArithmeticMeanElementsVertically(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [ArithmeticMeanElementsVertically --outputFieldName ABCD] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "arithMean_test3_file2cmp_noEncoding.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_5(self):
        """Test #5 : Calcul des moyennes verticales des champs TT, UU et VV entre 0.0102@à0.0374 et 0.0625@1 à partir d'un fichier de regeta­ pour différent intervalle de hauteurs."""
        # open and read source
        source0 = plugin_test_dir + "2013102212_024_UUVVTTSNPRGZRNPE.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMeanElementsVertically
        df = ArithmeticMeanElementsVertically(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '(', '([Select --fieldName TT --verticalLevel 0.0102@0.0374] >> [ArithmeticMeanElementsVertically]) + ', '([Select --fieldName TT --verticalLevel 0.0625@1] >> [ArithmeticMeanElementsVertically]) + ', '([Select --fieldName UU --verticalLevel 0.0102@0.0374] >> [ArithmeticMeanElementsVertically]) + ', '([Select --fieldName UU --verticalLevel 0.0625@1] >> [ArithmeticMeanElementsVertically]) + ', '([Select --fieldName VV --verticalLevel 0.0102@0.0374] >> [ArithmeticMeanElementsVertically]) + ', '([Select --fieldName VV --verticalLevel 0.0625@1] >> [ArithmeticMeanElementsVertically])', ')', ' >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2013102212_024_UUVVTT_TwoIntervalPerField_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_6(self):
        """Test #6 : Calcul des moyennes verticales des champs TT, UU et VV entre 0@1 à partir d'un fichier de regeta­ pour différent intervalle de hauteurs."""
        # open and read source
        source0 = plugin_test_dir + "2013102212_024_UUVVTTSNPRGZRNPE.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMeanElementsVertically
        df = ArithmeticMeanElementsVertically(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> ( ([Select --fieldName TT --verticalLevel 0@1] >> [ArithmeticMeanElementsVertically]) + ([Select --fieldName UU --verticalLevel 0@1] >> [ArithmeticMeanElementsVertically]) + ([Select --fieldName VV --verticalLevel 0@1] >> [ArithmeticMeanElementsVertically]) ) >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2013102212_024_UUVVTT_OneIntervalPerField_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_7(self):
        """Test #7 : Calcul des moyennes verticales des champs TT, UU et VV entre 0@1 à partir d'un fichier de regeta­ pour différent intervalle de hauteurs qui contient deja des champs calcules."""
        # open and read source
        source0 = plugin_test_dir + "2013102212_024_UUVVTT_plusOneIntervalPerField_file2cmp.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMeanElementsVertically
        df = ArithmeticMeanElementsVertically(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,UU,VV --verticalLevel 0@1] >> [ArithmeticMeanElementsVertically] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2013102212_024_UUVVTT_OneIntervalPerField_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_8(self):
        """Test #8 : Effectue un test sur un fichier qui possède seulement des intervalles."""
        # open and read source
        source0 = plugin_test_dir + "2013102212_024_UUVVTT_OneIntervalPerField_file2cmp.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMeanElementsVertically
        df = ArithmeticMeanElementsVertically(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[ArithmeticMeanElementsVertically] >> ', '[WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_9(self):
        """Test #9 : Effectue un test avec --outputFieldName mais plusieurs champs en entree."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMeanElementsVertically
        df = ArithmeticMeanElementsVertically(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [ArithmeticMeanElementsVertically --outputFieldName ABCD] 

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_10(self):
        """Test #10 : Utilisation de --outputFieldName avec une valeur > 4 caractères."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ArithmeticMeanElementsVertically
        df = ArithmeticMeanElementsVertically(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ArithmeticMeanElementsVertically --outputFieldName ABCDEF] 

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


