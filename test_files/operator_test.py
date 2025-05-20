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


plugin_test_dir = TEST_PATH + "Operator/testsFiles/"


class TestOperator(unittest.TestCase):
    def test_1(self):
        """Teste l'operateur logique OU lorsque c'est un succès."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Operator
        df = Operator(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([FalseOperation] || [Select --fieldName TT]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "or_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_2(self):
        """Teste l'operateur logique OU lorsque c'est un échec."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Operator
        df = Operator(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([FalseOperation] || [Select --fieldName FF]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_3(self):
        """Teste l'operateur logique ADD (+)."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Operator
        df = Operator(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --fieldName UU] + [Select --fieldName GZ]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "add_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_4(self):
        """Teste l'operateur logique ADD (+) avec plusieurs readers."""
        # open and read source
        source0 = plugin_test_dir + "addReaderUU_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "addReaderVV_fileSrc.std"
        src_df1 = fstpy.StandardFileReader(source1)

        source2 = plugin_test_dir + "addReaderTT_fileSrc.std"
        src_df2 = fstpy.StandardFileReader(source2)

        source3 = plugin_test_dir + "addReaderGZ_fileSrc.std"
        src_df3 = fstpy.StandardFileReader(source3)

        # compute Operator
        df = Operator(src_df0).compute()
        # ([ReaderStd --ignoreExtended --input {sources[0]}] + [ReaderStd --ignoreExtended --input {sources[1]}] + [ReaderStd --ignoreExtended --input {sources[2]}] + [ReaderStd --ignoreExtended --input {sources[3]}]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "input_big_fileSrc.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_5(self):
        """Teste l'operateur logique AND (&&)."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Operator
        df = Operator(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ( ( [Select --fieldName UU] ) && ( [Select --fieldName VV] ) && ( [Select --fieldName TT] ) && ( [Select --fieldName GZ] ) ) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_6(self):
        """Teste l'utilisation de plusieurs readers."""
        # open and read source
        source0 = plugin_test_dir + "addReaderUU_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "addReaderVV_fileSrc.std"
        src_df1 = fstpy.StandardFileReader(source1)

        source2 = plugin_test_dir + "addReaderTT_fileSrc.std"
        src_df2 = fstpy.StandardFileReader(source2)

        source3 = plugin_test_dir + "addReaderGZ_fileSrc.std"
        src_df3 = fstpy.StandardFileReader(source3)

        # compute Operator
        df = Operator(src_df0).compute()
        # ([ReaderStd --ignoreExtended --input {sources[0]}] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [ReaderStd --ignoreExtended --input {sources[2]}] >> [ReaderStd --ignoreExtended --input {sources[3]}]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "input_big_fileSrc.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_7(self):
        """Teste l'utilisation d'un reader entre d'autres opérations."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "addReaderGZ_fileSrc.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute Operator
        df = Operator(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UV] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "readerMiddle_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_8(self):
        """Teste l'utilisation de plusieurs writers."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Operator
        df = Operator(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_8dEso2T/resultWriter2.std --ignoreExtended --IP1EncodingStyle OLDSTYLE] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_9(self):
        """Teste l'utilisation d'un writer entre 2 opérations."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Operator
        df = Operator(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_9vqeiNX/resultWriterUUVV.std --ignoreExtended --IP1EncodingStyle OLDSTYLE] >> [Select --fieldName UU,VV] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res

    def test_10(self):
        """Teste l'utilisation d'un reader entre d'autres opérations."""
        # open and read source
        source0 = plugin_test_dir + "addcopy.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Operator
        df = Operator(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ( [Copy] + ([Select --fieldName GZ] >> [Zap --fieldName GI --doNotFlagAsZapped]) + ([Select --fieldName TT] >> [Zap --fieldName TI --doNotFlagAsZapped]) ) >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        # write the result
        results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "add_copy_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert res
