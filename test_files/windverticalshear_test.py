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


plugin_test_dir = TEST_PATH + "WindVerticalShear/testsFiles/"


class TestWindVerticalShear(unittest.TestCase):
    def test_1(self):
        """Calculate with a simple test data like 3x3x3 matrix for GZ, UU and VV."""
        # open and read source
        source0 = plugin_test_dir + "GZUUVV_144_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute WindVerticalShear
        df = WindVerticalShear(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [WindVerticalShear] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "WindVerticalShear_144_level_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_2(self):
        """Calculate with pressure file."""
        # open and read source
        source0 = plugin_test_dir + "2011051818_000.UUVVTTGZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute WindVerticalShear
        df = WindVerticalShear(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WindVerticalShear] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_regpres_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_3(self):
        """Test the WindVerticalShear calcul with model file."""
        # open and read source
        source0 = plugin_test_dir + "2011070818_054_hyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute WindVerticalShear
        df = WindVerticalShear(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WindVerticalShear] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_hyb_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_4(self):
        """Test the WindVerticalShear plugin extended attributes with a model output file."""
        # open and read source
        source0 = plugin_test_dir + "2011070818_054_hyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute WindVerticalShear
        df = WindVerticalShear(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --doNotFlagAsZapped --metadataZappable --pdsLabel 580V0N] >> [WindVerticalShear] >> [Zap --doNotFlagAsZapped --metadataZappable --implementation EXPERIMENTAL] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NEW/result_hyb2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res
