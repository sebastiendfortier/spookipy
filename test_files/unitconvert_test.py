

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"UnitConvert/testsFiles/"

class TestUnitConvert(unittest.TestCase):

    def test_1(self):
        """Test #1 : test a case simple conversion"""
        # open and read source
        source0 = plugin_test_dir + "windModulus_file2cmp.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [UnitConvert --unit kilometer_per_hour] >> [WriterStd --output {destination_path} --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "unitConvertUVInKmhExtended_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Test #2 : test a case with no conversion"""
        # open and read source
        source0 = plugin_test_dir + "windModulus_file2cmp.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [UnitConvert --unit knot] >> [Zap --pdsLabel WINDMODULUS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "windModulus_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Test #3 : test a case with no conversion (with extended info)"""
        # open and read source
        source0 = plugin_test_dir + "windModulus_file2cmp.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [UnitConvert --unit knot] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "windModulusExtended_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Test #4 : test a case with simple conversion and another plugin 2D"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >> [UnitConvert --unit kilometer_per_hour] >> [Zap --fieldName UV* --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "unitConvertUVInKmh_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """Test #5 : test a case with simple conversion and another plugin 3D"""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >> [UnitConvert --unit kilometer_per_hour] >> [Zap --fieldName UV* --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "unitConvertUVInKmh3D_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """Test #6 : test a case with complete roundtrip conversion celcius -> kelvin -> fahrenheit -> celsius"""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> (([Select --fieldName TT] >> [UnitConvert --unit kelvin] >> [UnitConvert --unit fahrenheit] >> [UnitConvert --unit celsius]) + [Select --fieldName TT --exclude]) >> [Zap --pdsLabel R1558V0N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "UUVVTT5x5_fileSrc.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """Test #7 : test a case for output file mode in standard format"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> (((([Select --fieldName TT --pdsLabel R1558V0N] >> [UnitConvert --unit kelvin]) + ([Select --fieldName UU,VV --pdsLabel R1558V0N] >> [UnitConvert --unit kilometer_per_hour]) + ([Select --fieldName GZ --pdsLabel R1558V0N] >> [UnitConvert --unit foot])) >> [UnitConvert --unit STD] >> [Zap --pdsLabel R1558V0N --doNotFlagAsZapped]) + [Select --fieldName TT,UU,VV,GZ --pdsLabel R1558V0N --exclude]) >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "input_big_fileSrc.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """Test #8 : test a case with complete roundtrip conversion celcius -> kelvin -> celsius"""
        # open and read source
        source0 = plugin_test_dir + "TTES_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> (([Select --fieldName TT] >> [UnitConvert --unit kelvin]) + [Select --fieldName ES]) >> [UnitConvert --unit celsius] >> [Zap --pdsLabel TESTGEORGESK --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TTES_fileSrc.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """Test #9 : test a case with complete roundtrip conversion celcius -> kelvin -> fahrenheit -> celsius in GeorgeKIndex context"""
        # open and read source
        source0 = plugin_test_dir + "TTES_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> (([Select --fieldName TT] >> [UnitConvert --unit kelvin]) + ([Select --fieldName ES] >> [UnitConvert --unit fahrenheit])) >> [UnitConvert --unit celsius] >> [Zap --pdsLabel TESTGEORGESK --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TTES_fileSrc.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_10(self):
        """Test #10 : test a case for output file mode in standard format"""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> (((([Select --fieldName TT --pdsLabel R1558V0N] >> [UnitConvert --unit kelvin]) + ([Select --fieldName UU,VV --pdsLabel R1558V0N] >> [UnitConvert --unit kilometer_per_hour]) + ([Select --fieldName GZ --pdsLabel R1558V0N] >> ([UnitConvert --unit foot] + [Zap --fieldName ZGZ --doNotFlagAsZapped]))) >> [UnitConvert --unit STD --ignoreMissing] >> [Zap --pdsLabel R1558V0N --doNotFlagAsZapped]) + [Select --fieldName TT,UU,VV,GZ --pdsLabel R1558V0N --exclude]) >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "input_big_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_11(self):
        """Test #11 : test --ignoremissing"""
        # open and read source
        source0 = plugin_test_dir + "windModulus_file2cmp.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [UnitConvert --unit scoobidoo --ignoreMissing] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "ignoremissing_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_12(self):
        """Test #12 : test bad unit"""
        # open and read source
        source0 = plugin_test_dir + "windModulus_file2cmp.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute UnitConvert
        df = UnitConvert(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [UnitConvert --unit scoobidoobidoo]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
