

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"HighLevelOperation/testsFiles/"

class TestHighLevelOperation(unittest.TestCase):

    def test_1(self):
        """ Test - calculer car les resultats ne sont pas disponibles"""
        # open and read source
        source0 = plugin_test_dir + "UUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HighLevelOperation
        df = HighLevelOperation(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [WindModulusAndDirection --optimizationLevel 1] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UVWD.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """ Test - prendre les resultats deja calcules (no input available)"""
        # open and read source
        source0 = plugin_test_dir + "UVWD.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HighLevelOperation
        df = HighLevelOperation(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulusAndDirection --optimizationLevel 1] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UVWD.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """ Test - Resultats deja calcules"""
        # open and read source
        source0 = plugin_test_dir + "UUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "UVWDWRONG.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute HighLevelOperation
        df = HighLevelOperation(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} {sources[1]}] >> [WindModulusAndDirection --optimizationLevel 1] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UVWDWRONG.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """ Test - Choix de resultats avec plus de niveaux"""
        # open and read source
        source0 = plugin_test_dir + "UUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "UVWDWRONG.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute HighLevelOperation
        df = HighLevelOperation(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 500] + [ReaderStd --ignoreExtended --input {sources[1]}] >> [WindModulusAndDirection --optimizationLevel 1] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UVWDWRONG.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """ Test - Choisit le resultat precalcule meme si il a moins de niveau. C'est le comportement normal de spooki lineaire."""
        # open and read source
        source0 = plugin_test_dir + "UUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "UVWDWRONG.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute HighLevelOperation
        df = HighLevelOperation(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] +([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --verticalLevel 500]) >> [WindModulusAndDirection --optimizationLevel 1] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UVWD500.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
