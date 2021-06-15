

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"HeightIndexAboveSurfaceLevel/testsFiles/"

class TestHeightIndexAboveSurfaceLevel(unittest.TestCase):

    def test_regtest_basic(self):
        """Test #1 : test numero 1"""
        # open and read source
        source0 = plugin_test_dir + "GZ_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HeightIndexAboveSurfaceLevel
        df = HeightIndexAboveSurfaceLevel(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [HeightIndexAboveSurfaceLevel --unit decameter --height 300] >> [Zap --pdsLabel HEIGHTIDXABO --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_basic.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "heightIndexAboveSurfaceLevel_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_basic_km(self):
        """Test #2 : test numero 2"""
        # open and read source
        source0 = plugin_test_dir + "GZ_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HeightIndexAboveSurfaceLevel
        df = HeightIndexAboveSurfaceLevel(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [HeightIndexAboveSurfaceLevel --unit kilometer --height 3] >> [Zap --pdsLabel HEIGHTIDXABO --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_basic_km.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "heightIndexAboveSurfaceLevel_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_base(self):
        """Test #3 : test numero 3"""
        # open and read source
        source0 = plugin_test_dir + "GZ_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute HeightIndexAboveSurfaceLevel
        df = HeightIndexAboveSurfaceLevel(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [HeightIndexAboveSurfaceLevel --unit decameter --height 0] >> [HeightIndexFromLevel --unit decameter --height 300] >> [Zap --pdsLabel HEIGHTIDXABO --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_base.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "heightIndexAboveSurfaceLevel_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


