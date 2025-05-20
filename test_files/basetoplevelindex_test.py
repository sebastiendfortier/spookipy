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


plugin_test_dir = TEST_PATH + "BaseTopLevelIndex/testsFiles/"


class TestBaseTopLevelIndex(unittest.TestCase):
    def test_bt1(self):
        """Lit le champ IFLD et recherche 0.6 dans les colonnes a l'aide de l'opérateur >= et retourne les indices trouvées dans BASE et TOP"""
        # open and read source
        source0 = plugin_test_dir + "baseTop_fileSrc.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute BaseTopLevelIndex
        df = BaseTopLevelIndex(src_df0).compute()
        # [ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20080529T133415 --typeOfField FORECAST --nbitsForDataStorage R16 --verticalLevelType MILLIBARS --doNotFlagAsZapped] >> [BaseTopLevelIndex --comparisonOperator >= --threshold 0.6] >> [ZapSmart --fieldNameFrom KBAS --fieldNameTo BASE] >> [ZapSmart --fieldNameFrom KTOP --fieldNameTo TOP] >> [Zap --pdsLabel BASETOPLVLID --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_bt1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "bt1_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_operatorEqual(self):
        """Lit le champ IFLD et recherche 0.5 dans les colonnes a l'aide de l'opérateur == et retourne les indices trouvées dans BASE et TOP"""
        # open and read source
        source0 = plugin_test_dir + "baseTop_fileSrcEqual.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute BaseTopLevelIndex
        df = BaseTopLevelIndex(src_df0).compute()
        # [ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20090529T133415 --typeOfField FORECAST --nbitsForDataStorage R16 --verticalLevelType MILLIBARS --doNotFlagAsZapped] >> [BaseTopLevelIndex --comparisonOperator == --threshold 0.5] >> [ZapSmart --fieldNameFrom KBAS --fieldNameTo BASE] >> [ZapSmart --fieldNameFrom KTOP --fieldNameTo TOP] >> [Zap --pdsLabel BASETOPLVLID --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_operatorEqual.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Test_OperatorEqual_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_operatorLessEqual(self):
        """Lit le champ IFLD et recherche 0.5 dans les colonnes a l'aide de l'opérateur <= et retourne les indices trouvées dans BASE et TOP"""
        # open and read source
        source0 = plugin_test_dir + "baseTop_fileSrcLessEqual.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute BaseTopLevelIndex
        df = BaseTopLevelIndex(src_df0).compute()
        # [ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20090529T133415 --typeOfField FORECAST --nbitsForDataStorage R16 --verticalLevelType MILLIBARS --doNotFlagAsZapped] >> [BaseTopLevelIndex --comparisonOperator <= --threshold 0.5] >> [ZapSmart --fieldNameFrom KBAS --fieldNameTo BASE] >> [ZapSmart --fieldNameFrom KTOP --fieldNameTo TOP] >> [Zap --pdsLabel BASETOPLVLID --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_operatorLessEqual.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Test_OperatorLessEqual_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_operatorLessThan(self):
        """Lit le champ IFLD et recherche 0.5 dans les colonnes a l'aide de l'opérateur < et retourne les indices trouvées dans BASE et TOP"""
        # open and read source
        source0 = plugin_test_dir + "baseTop_fileSrcLessThan.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute BaseTopLevelIndex
        df = BaseTopLevelIndex(src_df0).compute()
        # [ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20090529T133415 --typeOfField FORECAST --nbitsForDataStorage R16 --verticalLevelType MILLIBARS --doNotFlagAsZapped] >> [BaseTopLevelIndex --comparisonOperator < --threshold 0.5] >> [ZapSmart --fieldNameFrom KBAS --fieldNameTo BASE] >> [ZapSmart --fieldNameFrom KTOP --fieldNameTo TOP] >> [Zap --pdsLabel BASETOPLVLID --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_operatorLessThan.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Test_OperatorLessThan_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_operatorGreaterEqual(self):
        """Lit le champ IFLD et recherche 0.5 dans les colonnes a l'aide de l'opérateur >= et retourne les indices trouvées dans BASE et TOP"""
        # open and read source
        source0 = plugin_test_dir + "baseTop_fileSrcGreaterEqual.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute BaseTopLevelIndex
        df = BaseTopLevelIndex(src_df0).compute()
        # [ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20090529T133415 --typeOfField FORECAST --nbitsForDataStorage R16 --verticalLevelType MILLIBARS --doNotFlagAsZapped] >> [BaseTopLevelIndex --comparisonOperator >= --threshold 0.5] >> [ZapSmart --fieldNameFrom KBAS --fieldNameTo BASE] >> [ZapSmart --fieldNameFrom KTOP --fieldNameTo TOP] >> [Zap --pdsLabel BASETOPLVLID --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_operatorGreaterEqual.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Test_OperatorGreaterEqual_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_operatorGreaterThan(self):
        """Lit le champ IFLD et recherche 0.5 dans les colonnes a l'aide de l'opérateur > et retourne les indices trouvées dans BASE et TOP"""
        # open and read source
        source0 = plugin_test_dir + "baseTop_fileSrcGreaterThan.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute BaseTopLevelIndex
        df = BaseTopLevelIndex(src_df0).compute()
        # [ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20090529T133415 --typeOfField FORECAST --nbitsForDataStorage R16 --verticalLevelType MILLIBARS --doNotFlagAsZapped] >> [BaseTopLevelIndex --comparisonOperator > --threshold 0.5] >> [ZapSmart --fieldNameFrom KBAS --fieldNameTo BASE] >> [ZapSmart --fieldNameFrom KTOP --fieldNameTo TOP] >> [Zap --pdsLabel BASETOPLVLID --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_operatorGreaterThan.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Test_OperatorGreaterThan_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_operatorNotEqual(self):
        """Lit le champ IFLD et recherche 0.5 dans les colonnes a l'aide de l'opérateur != et retourne les indices trouvées dans BASE et TOP"""
        # open and read source
        source0 = plugin_test_dir + "baseTop_fileSrcNotEqual.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute BaseTopLevelIndex
        df = BaseTopLevelIndex(src_df0).compute()
        # [ReaderCsv --input {sources[0]}] >> [Zap --dateOfOrigin 20090529T133415 --typeOfField FORECAST --nbitsForDataStorage R16 --verticalLevelType MILLIBARS --doNotFlagAsZapped] >> [BaseTopLevelIndex --comparisonOperator != --threshold 0.5] >> [ZapSmart --fieldNameFrom KBAS --fieldNameTo BASE] >> [ZapSmart --fieldNameFrom KTOP --fieldNameTo TOP] >> [Zap --pdsLabel BASETOPLVLID --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_operatorNotEqual.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "Test_OperatorNotEqual_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res
