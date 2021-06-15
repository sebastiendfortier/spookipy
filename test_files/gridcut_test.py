

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"GridCut/testsFiles/"

class TestGridCut(unittest.TestCase):

    def test_reggc_test_1(self):
        """Test #1 : Tester sur une zone de 3x4 depuis une extremite de la matrice."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute GridCut
        df = GridCut(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --startPoint 0,0 --endPoint 2,3] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "gc_test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "gc_test_1.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_reggc_test_2(self):
        """Test #2 : Tester sur une zone de 3x4 depuis un point quelconque de la matrice"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute GridCut
        df = GridCut(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --startPoint 2,1 --endPoint 4,4] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "gc_test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "gc_test_2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_reggc_test_3(self):
        """Test #3 : Test selection de toute la matrice"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute GridCut
        df = GridCut(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --startPoint 0,0 --endPoint 4,4] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "gc_test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UUVV5x5x2_fileSrc.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_reggc_test_4(self):
        """Test #4 : Tester sur une zone plus grande que la matrice d'origine"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute GridCut
        df = GridCut(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --startPoint 0,0 --endPoint 4,5]

        #write the result
        results_file = TMP_PATH + "gc_test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_reggc_test_5(self):
        """Test #5 : Tester sur une zone de 25x25 avec meta products et depuis un point quelconque de la matrice"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TT.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute GridCut
        df = GridCut(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --startPoint 4,6 --endPoint 28,30] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "gc_test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "gc_test_5.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_reggc_test_6(self):
        """Test #6 : Tester coupure en 2 avec !! 64 bits"""
        # open and read source
        source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute GridCut
        df = GridCut(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --startPoint 0,0 --endPoint 511,399] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "gc_test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "gc_test_6.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_14(self):
        """Test #14 : Interpolation Verticale 1/16 pieces 649x672 664Mo"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2011100712_012_reghyb"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute GridCut
        df = GridCut(src_df0).compute()
        #[ReaderStd --input {sources[0]}] + ([ReaderStd --input {sources[1]}] >> ([Select --fieldName GZ --verticalLevel SURFACE] + [Select --metadataFieldName P0] )) >> [Select --xAxisMatrixSize 649 --yAxisMatrixSize 672] >> (([GridCut --startPoint 0,0 --endPoint 648,42] >> [InterpolationVertical -m FIELD_DEFINED --outputField INCLUDE_ALL_FIELDS --extrapolationType FIXED --valueAbove -300 --valueBelow -300 --referenceFieldName TT]) +([GridCut --startPoint 0,43 --endPoint 648,84] >> [InterpolationVertical -m FIELD_DEFINED --outputField INCLUDE_ALL_FIELDS --extrapolationType FIXED --valueAbove -300 --valueBelow -300 --referenceFieldName TT]) ) >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_regpres_ud850_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_reggc_test_15(self):
        """Test #15 : Tester SingleThread. Comme le test 1 mais en singlethread"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute GridCut
        df = GridCut(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut -T 1 --startPoint 0,0 --endPoint 2,3] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "gc_test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "gc_test_1.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


