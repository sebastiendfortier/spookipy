

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


plugin_test_dir = TEST_PATH + "GridPointDifference/testsFiles/"


class TestGridPointDifference(unittest.TestCase):

    def test_1(self):
        """--axis X,Y --differenceType CENTERED"""
        # open and read source
        source0 = plugin_test_dir + "6x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --unit scalar --doNotFlagAsZapped] >> ([Copy] + [GridPointDifference --axis X,Y --differenceType CENTERED]) >> [ZapSmart --fieldNameFrom FDX --fieldNameTo FFDX] >> [ZapSmart --fieldNameFrom FDY --fieldNameTo FFDY] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "XYCentered_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """test_gridPointDifference_Z_centered"""
        # open and read source
        source0 = plugin_test_dir + "4z2x2y_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> [GridPointDifference --axis Z --differenceType CENTERED] >> [Zap --fieldName FFDZ --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "new_ZCentered_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """test_gridPointDifference_XY_forward"""
        # open and read source
        source0 = plugin_test_dir + "6x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> [GridPointDifference --axis X,Y --differenceType FORWARD] >> [ZapSmart --fieldNameFrom FDX --fieldNameTo FFDX] >> [ZapSmart --fieldNameFrom FDY --fieldNameTo FFDY] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "XYForward_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """test_gridPointDifference_Z_forward"""
        # open and read source
        source0 = plugin_test_dir + "4z2x2y_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> [GridPointDifference --axis Z --differenceType FORWARD] >> [Zap --fieldName FFDZ --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "new_ZForward_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """test_gridPointDifference_XY_backward"""
        # open and read source
        source0 = plugin_test_dir + "6x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> [GridPointDifference --axis X,Y --differenceType BACKWARD] >> [ZapSmart --fieldNameFrom FDX --fieldNameTo FFDX] >> [ZapSmart --fieldNameFrom FDY --fieldNameTo FFDY] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "XYBackward_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """test_gridPointDifference_Z_backward"""
        # open and read source
        source0 = plugin_test_dir + "4z2x2y_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> [GridPointDifference --axis Z --differenceType BACKWARD] >> [Zap --fieldName FFDZ --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "new_ZBackward_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_7(self):
        """test_gridPointDifference_XY_centered2"""
        # open and read source
        source0 = plugin_test_dir + "tape10_UU.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Copy] + [GridPointDifference --axis X,Y --differenceType CENTERED]) >> [ZapSmart --fieldNameFrom FDX --fieldNameTo UUDX] >> [ZapSmart --fieldNameFrom FDY --fieldNameTo UUDY] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "XYCentered2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_8(self):
        """test_gridPointDifference_Z_1level"""
        # open and read source
        source0 = plugin_test_dir + "4z2x2y_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 0] >> [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> [GridPointDifference --axis Z --differenceType CENTERED]

        # write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_9(self):
        """test_gridPointDifference_Xsize1"""
        # open and read source
        source0 = plugin_test_dir + "tictac.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName BB] >> [GridPointDifference --axis X --differenceType CENTERED]

        # write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_10(self):
        """test_gridPointDifference_Ysize1"""
        # open and read source
        source0 = plugin_test_dir + "tictac.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName AA] >> [GridPointDifference --axis Y --differenceType CENTERED]

        # write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_11(self):
        """test_gridPointDifference_moreThan1PDS"""
        # open and read source
        source0 = plugin_test_dir + "tape10.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDifference --axis X,Y --differenceType CENTERED]

        # write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_12(self):
        """Difference centree avec fichier YinYang en entree."""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --verticalLevel 1000] >> [GridPointDifference --axis X,Y --differenceType CENTERED] >> [WriterStd --output {destination_path} --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "XYCentered_YY_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_13(self):
        """Difference vers l'avant (forward) avec fichier YinYang en entree."""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --verticalLevel 1000] >> [GridPointDifference --axis X,Y --differenceType FORWARD] >> [WriterStd --output {destination_path} --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "XYForward_YY_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_14(self):
        """Difference vers l'arriere  avec fichier YinYang en entree."""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GridPointDifference
        df = GridPointDifference(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --verticalLevel 1000] >> [GridPointDifference --axis X,Y --differenceType BACKWARD] >> [WriterStd --output {destination_path} --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "XYBackward_YY_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
