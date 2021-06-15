

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"OperationBase/testsFiles/"

class TestOperationBase(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 :  Test une operation de clonage"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute OperationBase
        df = OperationBase(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --fieldName UU,VV,UV] + [Select --fieldName UU,VV,UV]) >> [Select --fieldName UV] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "windModulus_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_2(self):
        """Test #2 :  Test une autre operation de clonage"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute OperationBase
        df = OperationBase(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU,VV,UV] >> ([Select --fieldName UV] || [Select --fieldName UV]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "windModulus3D_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_3(self):
        """Test #3 :  Test la detection de la meme grille (no deformation fields)."""
        # open and read source
        source0 = plugin_test_dir + "uu.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "vv.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute OperationBase
        df = OperationBase(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} {sources[1]}] >> [PrintIMO] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_B_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_4(self):
        """Test #4 :  Test la detection de la meme grille (no deformation fields), avec operateur."""
        # open and read source
        source0 = plugin_test_dir + "uu.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "vv.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute OperationBase
        df = OperationBase(src_df0).compute()
        #([ReaderStd --ignoreExtended --input {sources[0]}] + [ReaderStd --ignoreExtended --input {sources[1]}]) >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_B_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_5(self):
        """Test #5 :  Test la detection de la meme grille (with deformation fields)."""
        # open and read source
        source0 = plugin_test_dir + "tt.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "qq.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute OperationBase
        df = OperationBase(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} {sources[1]}] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_A_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6(self):
        """Test #6 :  Test la detection de la meme grille (with deformation fields), avec operateur."""
        # open and read source
        source0 = plugin_test_dir + "tt.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "qq.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute OperationBase
        df = OperationBase(src_df0).compute()
        #([ReaderStd --ignoreExtended --input {sources[0]}] + [ReaderStd --ignoreExtended --input {sources[1]}]) >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_A_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


