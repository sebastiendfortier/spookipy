

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"Calculator/testsFiles/"

class TestCalculator(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 : Multiplication de deux valeurs d'un fichier volumineux."""
        # open and read source
        source0 = plugin_test_dir + "srcFile1.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Calculator
        df = Calculator(src_df0).compute()
        #['[ReaderStd --input {sources[0]}]  >> (([Select --fieldName ZZ ] >> [Zap --tag zz]) + ([Select --fieldName TT ] >> [Zap --tag tt])) >> [Calculator --expression @zz*@tt --unit hundredsOfFeet --outputFieldName RSLT] >> [WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "file2Comp1.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_2(self):
        """Test #2 : 6 variables impliquant plusieurs opérateurs simples (HU+HR+ES)/(VV-(TT*UU))."""
        # open and read source
        source0 = plugin_test_dir + "srcFile2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Calculator
        df = Calculator(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> (([Select --fieldName TT ] >> [Zap --tag tt]) + ([Select --fieldName UU ] >> [Zap --tag uu ]) + ([Select --fieldName VV ] >> [Zap --tag vv ]) + ([Select --fieldName HU ] >> [Zap --tag hu ])+ ([Select --fieldName HR ] >> [Zap --tag hr ]) + ([Select --fieldName ES ] >> [Zap --tag es ])) >> [Calculator --expression (@hu+@hr+@es)/(@vv-(@tt*@uu)) --unit hundredsOfFeet --outputFieldName RSLT] >> [WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "file2Comp2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_3(self):
        """Test #3 : Test de certaines fonctions typiques: abs(tt) + cos(uu) + ceil(vv) + sqrt(hu) + pow(hr,2) + log10(es)"""
        # open and read source
        source0 = plugin_test_dir + "srcFile3.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Calculator
        df = Calculator(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> (([Select --fieldName TT ] >> [Zap --tag tt]) + ([Select --fieldName UU ] >> [Zap --tag uu ]) + ([Select --fieldName VV ] >> [Zap --tag vv ]) + ([Select --fieldName HU ] >> [Zap --tag hu ])+ ([Select --fieldName HR ] >> [Zap --tag hr ]) + ([Select --fieldName ES ] >> [Zap --tag es ])) >> [Calculator --expression abs(@tt)+cos(@uu)+ceil(@vv)+sqrt(@hu)+pow(@hr,2.0)+log10(@es) --unit hundredsOfFeet --outputFieldName RSLT] >> [WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "file2Comp3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_4(self):
        """Test #4 : Test avec un nombre élevé de variables. (Sommation des variables)"""
        # open and read source
        source0 = plugin_test_dir + "srcFile4.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Calculator
        df = Calculator(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ( ([Select --fieldName TT ] >> [Zap --tag tt]) + ([Select --fieldName UU ] >> [Zap --tag uu ]) + ([Select --fieldName VV ] >> [Zap --tag vv ]) + ([Select --fieldName HU ] >> [Zap --tag hu ])+ ([Select --fieldName HR ] >> [Zap --tag hr ]) + ([Select --fieldName ES ] >> [Zap --tag es ])+ ([Select --fieldName TX ] >> [Zap --tag tx ]) + ([Select --fieldName UX ] >> [Zap --tag ux]) + ([Select --fieldName VX] >> [Zap --tag vx ]) + ([Select --fieldName XR ] >> [Zap --tag xr ]) + ([Select --fieldName XU ] >> [Zap --tag xu ]) + ([Select --fieldName EX ] >> [Zap --tag ex ])) >> [Calculator --expression @tt+@uu+@vv+@hu+@hr+@es+@tx+@ux+@vx+@xr+@xu+@ex --unit hundredsOfFeet --outputFieldName RSLT] >> [WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "file2Comp4.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_5(self):
        """Test #5 : Test avec un outputFieldname différent et une utilisation répétée d'une même variable. ( (TT+UU+VV)/TT )"""
        # open and read source
        source0 = plugin_test_dir + "srcFile2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Calculator
        df = Calculator(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> (([Select --fieldName TT ] >> [Zap --tag tt]) + ([Select --fieldName UU] >> [Zap --tag uu ]) + ([Select --fieldName VV ] >> [Zap --tag vv ])) >> [Calculator --outputFieldName TEST --expression (@tt+@uu+@vv)/@tt]>> [WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "file2Comp5.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6(self):
        """Test #6 : Test avec une seule variable. (TT*7)"""
        # open and read source
        source0 = plugin_test_dir + "srcFile2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Calculator
        df = Calculator(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ([Select --fieldName TT ] >> [Zap --tag TT]) >> [Calculator --outputFieldName TT7 --expression @TT*7]>> [WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "file2Comp6.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_7(self):
        """Test #7 : Même test que test_5, mais échoue parce qu'il y n'y a pas le même nombre de variables que de PDS avec tag."""
        # open and read source
        source0 = plugin_test_dir + "srcFile2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Calculator
        df = Calculator(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> (([Select --fieldName TT ] >> [Zap --tag tt]) + ([Select --fieldName UU]) + ([Select --fieldName VV ] >> [Zap --tag vv ])) >> [Calculator --outputFieldName TEST --expression (@tt+@uu+@vv)/@tt]>> [WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "file2Comp5.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


