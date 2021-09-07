

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"InterpolationHorizontalPoint/testsFiles/"

class TestInterpolationHorizontalPoint(unittest.TestCase):

    def test_1(self):
        """test_onlyscalarR1Operational"""
        # open and read source
        source0 = plugin_test_dir + "4panneaux_input4_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlon_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resultOnlyScalarR1Operational_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """test_onlyscalar"""
        # open and read source
        source0 = plugin_test_dir + "4panneaux_input4_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlon_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resultOnlyScalar_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """test_scalarvectorial"""
        # open and read source
        source0 = plugin_test_dir + "tape10.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlon_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resultScalarVectorial_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """test_scalarvectorial2"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlon_fileSrc2.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resultScalarVectorial2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """test_nearest"""
        # open and read source
        source0 = plugin_test_dir + "tape10.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlon_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint --interpolationType NEAREST] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resultNearest_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """test_linear"""
        # open and read source
        source0 = plugin_test_dir + "tape10.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlon_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint --interpolationType BI-LINEAR] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resultLinear_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """test_withGridInCsv"""
        # open and read source
        source0 = plugin_test_dir + "tape10.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlonWithGrid_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint --interpolationType NEAREST] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_withGridInCsv_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """test_extrapolationValue"""
        # open and read source
        source0 = plugin_test_dir + "tape10.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlonExtrapolation_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType VALUE=999.9] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_extrapolValue_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """test_negativeValue"""
        # open and read source
        source0 = plugin_test_dir + "tape10.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlonExtrapolation_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType VALUE=-99.9] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_negativeValue_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_10(self):
        """test_extrapolationMax"""
        # open and read source
        source0 = plugin_test_dir + "tape10.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlonExtrapolation_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType MAXIMUM] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_extrapolMax_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_11(self):
        """test_extrapolationMin"""
        # open and read source
        source0 = plugin_test_dir + "tape10.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlonExtrapolation_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType MINIMUM] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_extrapolMin_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_12(self):
        """test_stations"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName GZ,UU,VV,TT] >> [GetDictionaryInformation --dataBase STATIONS --outputAttribute LAT,LON --advancedRequest SELECT_Latitude,Longitude_FROM_STATIONSFB] >> [InterpolationHorizontalPoint] >> [Zap --metadataZappable --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_stations_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_13(self):
        """test with 2 grids and 3 fields on each grid"""
        # open and read source
        source0 = plugin_test_dir + "2011110112_045_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2011110112_048_small"
        src_df1 = fstpy.StandardFileReader(source1)

        source2 = plugin_test_dir + "latlon_fileSrc.csv"
        src_df2 = fstpy.StandardFileReader(source2)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ReaderStd --input {sources[1]}] >> [ReaderCsv --input {sources[2]}] >> [InterpolationHorizontalPoint] >> [Zap --metadataZappable --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_2grids_3fields_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_14(self):
        """test_DanielPoints"""
        # open and read source
        source0 = plugin_test_dir + "2012022712_012_glbdiag"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlong_stn_ALL.fst"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName 2Z] >> [ReaderStd --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType VALUE=999.9] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_DanielPoints_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_15(self):
        """test_northPole_southPole"""
        # open and read source
        source0 = plugin_test_dir + "2012022712_012_glbdiag"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlong_stn_ALL.fst"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName SN] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType VALUE=999.9] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "northSouthPole_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_16(self):
        """Test avec un fichier YinYang"""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "inputFile.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20150805T094230 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint --interpolationType BI-LINEAR --extrapolationType VALUE=99.9] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "InterpGridUtoGridY_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_17(self):
        """Test avec un fichier YinYang en entree et des lat-lon sur les grilles Yin et Yang."""
        # open and read source
        source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "latlonYY_fileSrc.csv"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationHorizontalPoint
        df = InterpolationHorizontalPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20150805T094230 --doNotFlagAsZapped] >> [InterpolationHorizontalPoint --interpolationType BI-LINEAR --extrapolationType VALUE=99.9] >> [WriterStd --output {destination_path}]

        #write the result
        results_file = TMP_PATH + "test_17.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "InterpGridU_manyPts_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
