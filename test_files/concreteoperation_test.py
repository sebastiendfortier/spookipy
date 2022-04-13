

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


plugin_test_dir = TEST_PATH + "ConcreteOperation/testsFiles/"


class TestConcreteOperation(unittest.TestCase):

    def test_1(self):
        """ Test - manque 1 niveau pour UU et 2 niveaux pour VV"""
        # open and read source
        source0 = plugin_test_dir + "GZUUVV_144_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ConcreteOperation
        df = ConcreteOperation(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --fieldName UU --verticalLevel 1,2] + [Select --fieldName VV --verticalLevel 1] + [Select --fieldName GZ]) >> [AddElementsByPoint --outputFieldName ACCU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "miss_one_level_for_UU_and_two_for_VV_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """ Test - seulement niveau 2 pour GZ"""
        # open and read source
        source0 = plugin_test_dir + "GZUUVV_144_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ConcreteOperation
        df = ConcreteOperation(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --fieldName UU ] + [Select --fieldName VV] + [Select --fieldName GZ --verticalLevel 2]) >> [AddElementsByPoint --outputFieldName ACCU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "only_level_2_for_GZ_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """ Test - seulement niveau 0 pour UU"""
        # open and read source
        source0 = plugin_test_dir + "GZUUVV_144_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ConcreteOperation
        df = ConcreteOperation(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --fieldName UU --verticalLevel 0] + [Select --fieldName VV] + [Select --fieldName GZ ]) >> [AddElementsByPoint --outputFieldName ACCU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "only_level_0_for_UU_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """Verifier si ca fonctionne meme s'il manque un niveau dans le milieu."""
        # open and read source
        source0 = plugin_test_dir + "GZUUVV_144_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ConcreteOperation
        df = ConcreteOperation(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --fieldName UU] + [Select --fieldName VV --verticalLevel 0,2] + [Select --fieldName GZ ]) >> [AddElementsByPoint --outputFieldName ACCU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "miss_level_1_for_VV_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """Verifier si ca fonctionne lorsque 2 calculs ont besoin des mêmes données."""
        # open and read source
        source0 = plugin_test_dir + "GZUUVV_144_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ConcreteOperation
        df = ConcreteOperation(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --fieldName UU] + [Select --fieldName VV --verticalLevel 0,2] + [Select --fieldName GZ ]) >> [SetConstantValue --value 5] >> [AddElementsByPoint --outputFieldName ACCU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "two_calcul_need_same_data_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """Test avec pressure."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ConcreteOperation
        df = ConcreteOperation(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "reference_file_test_6.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_7(self):
        """Test avec des données manquantes."""
        # open and read source
        source0 = plugin_test_dir + "notSameMatrixShape.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute ConcreteOperation
        df = ConcreteOperation(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [AddElementsByPoint --outputFieldName ACCU]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
