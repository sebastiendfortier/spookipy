

# -*- coding: utf-8 -*-
import os
import sys


import unittest
import pytest


prefix = "/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/" % HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/" % (HOST_NUM, USER)


plugin_test_dir = TEST_PATH + "GridMerge/testsFiles/"


class TestGridMerge(unittest.TestCase):

    def test_1(self):
        """Test de fusion de 2 grilles consecutives alignees horizontalement"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridMerge
        df = GridMerge(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([GridCut --startPoint 0,0 --endPoint 50,25] + [GridCut --startPoint 51,0 --endPoint 100,25]) >> [GridMerge] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test1_fileCmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """Test de fusion de 2 grilles consecutives alignees verticalement"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridMerge
        df = GridMerge(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([GridCut --startPoint 0,0 --endPoint 50,25] + [GridCut --startPoint 0,26 --endPoint 50,50]) >> [GridMerge] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test2_fileCmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """Test de fusion de 3 grilles ne formant pas une grille rectangulaire"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridMerge
        df = GridMerge(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([GridCut --startPoint 0,0 --endPoint 50,25] + [GridCut --startPoint 51,0 --endPoint 100,25] + [GridCut --startPoint 0,26 --endPoint 50,50]) >> [GridMerge] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """Test de fusion de grilles consecutives de taille irreguliere"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridMerge
        df = GridMerge(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([GridCut --startPoint 0,0 --endPoint 50,25] + [GridCut --startPoint 51,0 --endPoint 100,25] + [GridCut --startPoint 0,26 --endPoint 100,50]) >> [GridMerge] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test4_fileCmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """Test de fusion de grilles consecutives de taille irreguliere et de point d'origine different de (0,0)"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridMerge
        df = GridMerge(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([GridCut --startPoint 2,15 --endPoint 50,25] + [GridCut --startPoint 51,15 --endPoint 100,25] + [GridCut --startPoint 2,26 --endPoint 100,50]) >> [GridMerge] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test5_fileCmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """Test de fusion de grilles consecutives, retour au fichier original"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridMerge
        df = GridMerge(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([GridCut --startPoint 0,0 --endPoint 498,1027] + [GridCut --startPoint 499,0 --endPoint 995,1027]) >> [GridMerge] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2014031800_024_reghyb_TTGZ.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_7(self):
        """Test de fusion de grilles, retour au fichier original, valeurs manquantes"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridMerge
        df = GridMerge(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([GridCut --startPoint 0,0 --endPoint 498,1026] + [GridCut --startPoint 499,0 --endPoint 994,1026]) >> [GridMerge] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2014031800_024_reghyb_TTGZ_missing_data.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_8(self):
        """Test de fusion de grilles avec overlap"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridMerge
        df = GridMerge(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([GridCut --startPoint 0,0 --endPoint 49,99] + [GridCut --startPoint 45,0 --endPoint 99,99]) >> [GridMerge] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_9(self):
        """Test de fusion de grilles yan yan"""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridMerge
        df = GridMerge(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([GridCut --startPoint 0,0 --endPoint 49,99] + [GridCut --startPoint 50,0 --endPoint 99,99]) >> [GridMerge] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
