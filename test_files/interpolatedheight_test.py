

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


plugin_test_dir = TEST_PATH + "InterpolatedHeight/testsFiles/"


class TestInterpolatedHeight(unittest.TestCase):

    def test_1(self):
        """ Test  --inputFieldName CLD --threshold 0.6"""
        # open and read source
        source0 = plugin_test_dir + "interHeight_fileSrc.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "interHeightGZ_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute InterpolatedHeight
        df = InterpolatedHeight(src_df0).compute()
        # (([ReaderCsv --input {sources[1]}] >> [Zap --verticalLevelType MILLIBARS]) + ([ReaderCsv --input {sources[0]}] >> [Zap --verticalLevelType MILLIBARS] >> ([BaseTopLevelIndex --comparisonOperator >= --threshold 0.6] + [Zap --fieldName CLD --doNotFlagAsZapped]))) >> [Zap --dateOfOrigin 20080529T133415 --typeOfField FORECAST --nbitsForDataStorage R16 --verticalLevelType MILLIBARS --doNotFlagAsZapped] >> [InterpolatedHeight --inputFieldName CLD --threshold 0.6] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interHeight_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
