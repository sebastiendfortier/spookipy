

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"WindDeformation/testsFiles/"

class TestWindDeformation(unittest.TestCase):

    def test_1(self):
        """Test #1 : test_wind_deformation_tape10"""
        # open and read source
        source0 = plugin_test_dir + "tape10.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WindDeformation
        df = WindDeformation(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU,VV --verticalLevel 400,300,250,200] >> [UnitConvert --unit meter_per_second] >> [WindDeformation] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "tape10_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Test #2 : test_wind_deformation_tape10_100km"""
        # open and read source
        source0 = plugin_test_dir + "tape10.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WindDeformation
        df = WindDeformation(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU,VV --verticalLevel 400,300,250,200] >> [UnitConvert --unit meter_per_second] >> [WindDeformation] >> [MultiplyElementBy --value 100000] >> [Zap --fieldName DEF --pdsLabel WINDDEF --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "tape10_100km_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
