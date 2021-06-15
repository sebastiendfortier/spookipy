

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"SweatIndex/testsFiles/"

class TestSweatIndex(unittest.TestCase):

    def test_regtest_sw_algo_1(self):
        """Test #1 : Calcul de l'indice sweat avec TT, UU et VV  à 850 et 500 mb et ES à 850 mb."""
        # open and read source
        source0 = plugin_test_dir + "TTUUVV_850_500_ES_850_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SweatIndex
        df = SweatIndex(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [SweatIndex] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_sw_algo_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Sweat_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_sw_20100823(self):
        """Test #3 : Calcul de l'indice sweat avec ."""
        # open and read source
        source0 = plugin_test_dir + "input_20100823.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SweatIndex
        df = SweatIndex(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [SweatIndex] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_sw_20100823.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "20100823_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


