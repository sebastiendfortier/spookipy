

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


plugin_test_dir = TEST_PATH + "BaseTopBoundedLevelIndex/testsFiles/"


class TestBaseTopBoundedLevelIndex(unittest.TestCase):

    def test_base_top_1(self):
        """Calcul les Base et Top d'un phenomene."""
        # open and read source
        source0 = plugin_test_dir + "baseTop_fileSrc.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "baseTopBas_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)

        source2 = plugin_test_dir + "baseTopTop_fileSrc.csv"
        src_df2 = fstpy.StandardFileReader(source2)

        # compute BaseTopBoundedLevelIndex
        df = BaseTopBoundedLevelIndex(src_df0).compute()
        #['[ReaderCsv --input {sources[0]}] >> ', '[ReaderCsv --input {sources[1]}] >> ', '[ReaderCsv --input {sources[2]}] >> ', '[Zap --dateOfOrigin 20080529T133415 --typeOfField FORECAST --nbitsForDataStorage R16 --doNotFlagAsZapped] >> ', '[BaseTopBoundedLevelIndex --comparisonOperator >= --threshold 0.6] >> ', '[ZapSmart --fieldNameFrom KBAS --fieldNameTo BASE] >> ', '[ZapSmart --fieldNameFrom KTOP --fieldNameTo TOP] >> ', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

        # write the result
        results_file = TMP_PATH + "test_base_top_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "bt_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
