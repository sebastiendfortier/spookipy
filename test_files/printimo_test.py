

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"PrintIMO/testsFiles/"

class TestPrintIMO(unittest.TestCase):

    def test_1(self):
        """Test #1 : Imprime un IMO vers un fichier, forme courte."""
        # open and read source
        source0 = plugin_test_dir + "UUVV10x10_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrintIMO
        df = PrintIMO(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrintIMO --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_1mUG1lz/shortOutput.txt]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Test #2 : Imprime un IMO vers un fichier, forme longue."""
        # open and read source
        source0 = plugin_test_dir + "UUVV10x10_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrintIMO
        df = PrintIMO(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrintIMO --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_24jpOyc/longOutput.txt --extended]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Test #3 : Imprime un IMO vers un fichier, forme courte json."""
        # open and read source
        source0 = plugin_test_dir + "UUVV10x10_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrintIMO
        df = PrintIMO(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ', '[PrintIMO --output {destination_path} --json]']

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resultetst_3.txt"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
