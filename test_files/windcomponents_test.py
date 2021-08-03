

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"WindComponents/testsFiles/"

class TestWindComponents(unittest.TestCase):

    def test_1(self):
        """Test #1 : Test """
        # open and read source
        source0 = plugin_test_dir + "UUVV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WindComponents
        df = WindComponents(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 0] >> [WindComponents] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "windComponents_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


