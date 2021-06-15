

# -*- coding: utf-8 -*-
import os, sys


import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)

import operator as op

plugin_test_dir=TEST_PATH +"Mask/testsFiles/"

class TestMask(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 : seuils: 0,10,15,20 valeurs: 0,10,15,20 ops: ge,ge,ge,ge"""
        # open and read source
        source0 = plugin_test_dir + "new_input.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        src_df0['ip1'] = 12000
        #compute Mask
        df = Mask(src_df0, thresholds=[0.0,10.0,15.0,20.0], values=[0.0,10.0,15.0,20.0], operators=[op.ge,op.ge,op.ge,op.ge]).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds 0.0,10.0,15.0,20.0 --values 0.0,10.0,15.0,20.0 --operators ge,ge,ge,ge] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_1.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        fstpy.delete_file(results_file)
        assert(res == True)


    def test_regtest_2(self):
        """Test #2 : seuils: -15,-15,-5,10,20 valeurs: -20,-15,-5,10,20 ops: le,ge,ge,ge,ge"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Mask
        df = Mask(src_df0, thresholds=[-15,-15,-5,10,20], values=[-20,-15,-5,10,20], operators=[op.le,op.ge,op.ge,op.ge,op.ge]).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds -15,-15,-5,10,20 --values -20,-15,-5,10,20 --operators le,ge,ge,ge,ge] >> [WriterStd --output {destination_path} --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        fstpy.delete_file(results_file)
        assert(res == True)


    def test_regtest_3(self):
        """Test #3 : seuils: -10,0,10 valeurs: 1,2,3 ops: le,eq,gt"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Mask
        df = Mask(src_df0, thresholds=[-10,0,10], values=[1,2,3], operators=[op.le,eq,op.gt]).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds -10,0,10 --values 1,2,3 --operators le,eq,gt] >> [WriterStd --output {destination_path} --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        fstpy.delete_file(results_file)
        assert(res == True)


    def test_regtest_4(self):
        """Test #4 : ERREUR: pas le meme nombre de valeurs associe a seuils, valeurs, et ops"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        with pytest.raises(MaskError):
            #compute Mask
            df = Mask(src_df0, thresholds=[-10,0,10], values=[1,2], operators=[op.le,eq]).compute()
            #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds -10,0,10 --values 1,2 --operators le,eq] >> [WriterStd --output {destination_path} --noUnitConversion]




    def test_regtest_5(self):
        """Test #5 : ERREUR: valeur invalide associee a operators (TT)"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        with pytest.raises(MaskError):
            #compute Mask
            df = Mask(src_df0, thresholds=[-0,10], values=[0,10], operators=[op.le,'TT']).compute()
            #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds -0,10 --values 0,10 --operators le,'TT'] >> [WriterStd --output {destination_path} --noUnitConversion]


    def test_regtest_6(self):
        """Test #6 :  seuils: -10,0,10 valeurs: 1,2,3 ops: le,eq,gt + outputFieldName=TOTO"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Mask
        df = Mask(src_df0, thresholds = [-10,0,10], values=[1,2,3], operators=[op.le,eq,op.gt], nomvar_out='TOTO').compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds -10,0,10 --values 1,2,3 --operators le,eq,gt --outputFieldName TOTO] >> [WriterStd --output {destination_path} --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_6.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        fstpy.delete_file(results_file)
        assert(res == True)


if __name__ == "__main__":
    unittest.main()