

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"CloudFractionDiagnostic/testsFiles/"

class TestCloudFractionDiagnostic(unittest.TestCase):

    def test_cfd_1(self):
        """Test #1 : Test regulier des donnees venant avec la demande de plugin"""
        # open and read source
        source0 = plugin_test_dir + "HR_27_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute CloudFractionDiagnostic
        df = CloudFractionDiagnostic(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [CloudFractionDiagnostic] >> [Zap --pdsLabel CLDFRACTION --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_cfd_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "cfd_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


