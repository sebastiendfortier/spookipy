

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


plugin_test_dir = TEST_PATH + "GridPointDistance/testsFiles/"


class TestGridPointDistance(unittest.TestCase):

    def test_1(self):
        """test_gridPointDistance_X_centered"""
        # open and read source
        source0 = plugin_test_dir + "ps5x4_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDistance
        df = GridPointDistance(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis X --differenceType CENTERED] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "XCentered_file2cmp_rmn19.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """test_gridPointDistance_Y_centered"""
        # open and read source
        source0 = plugin_test_dir + "ps5x4_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDistance
        df = GridPointDistance(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis Y --differenceType CENTERED] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "YCentered_file2cmp_rmn19.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """test_gridPointDistance_X_forward"""
        # open and read source
        source0 = plugin_test_dir + "ps5x4_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDistance
        df = GridPointDistance(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis X --differenceType FORWARD] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "XForward_file2cmp_rmn12.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """test_gridPointDistance_Y_forward"""
        # open and read source
        source0 = plugin_test_dir + "ps5x4_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDistance
        df = GridPointDistance(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis Y --differenceType FORWARD] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "YForward_file2cmp_rmn12.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """test_gridPointDistance_X_backward"""
        # open and read source
        source0 = plugin_test_dir + "ps5x4_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDistance
        df = GridPointDistance(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis X --differenceType BACKWARD] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "XBackward_file2cmp_rmn12.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """test_gridPointDistance_Y_backward"""
        # open and read source
        source0 = plugin_test_dir + "ps5x4_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDistance
        df = GridPointDistance(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis Y --differenceType BACKWARD] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "YBackward_file2cmp_rmn12.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_7(self):
        """test_gridPointDistance_XY_centered"""
        # open and read source
        source0 = plugin_test_dir + "ps5x4_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDistance
        df = GridPointDistance(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDistance --axis X,Y --differenceType CENTERED] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "XYCentered_file2cmp_rmn19.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
