

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


plugin_test_dir = TEST_PATH + "MatchFieldsByCommonLevels/testsFiles/"


class TestMatchFieldsByCommonLevels(unittest.TestCase):

    def test_1(self):
        """ Sélection du champs avec comme priorité HU,HR,TD."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute MatchFieldsByCommonLevels
        df = MatchFieldsByCommonLevels(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [MatchFieldsByCommonLevels --referenceField TT --matchFields HU,HR,TD] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_HU_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """ Sélection du champs avec comme priorité TD,HR,HU."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute MatchFieldsByCommonLevels
        df = MatchFieldsByCommonLevels(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [MatchFieldsByCommonLevels --referenceField TT --matchFields TD,HR,HU] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_HR_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """ Sélection du champs avec comme priorité HU,HR,TD avec un fichier contenant moins de HU que de HR."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute MatchFieldsByCommonLevels
        df = MatchFieldsByCommonLevels(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --fieldName TT,HR] + [Select --fieldName HU --verticalLevel 0.85@0.3]) >> [MatchFieldsByCommonLevels --referenceField TT --matchFields HU,HR,TD] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_HR_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """ Sélection du champs avec comme priorité HU,HR,TD avec un fichier contenant moins de HU que de HR et moins de HR que de TT."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbhyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute MatchFieldsByCommonLevels
        df = MatchFieldsByCommonLevels(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --fieldName TT] + [Select --fieldName HR --verticalLevel 1.0@0.3] + [Select --fieldName HU --verticalLevel 1.0@0.85]) >> [MatchFieldsByCommonLevels --referenceField TT --matchFields HU,TD,HR] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_HR_partial_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """ Sélection du champs avec comme priorité PX,GX avec un fichier contenant plusieurs product groups de TT,PX,GZ ayant des niveaux differents."""
        # open and read source
        source0 = plugin_test_dir + "input_multiple_groups.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute MatchFieldsByCommonLevels
        df = MatchFieldsByCommonLevels(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [MatchFieldsByCommonLevels --referenceField TT --matchFields PX,GZ] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "input_multiple_groups_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
