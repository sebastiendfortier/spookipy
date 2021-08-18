

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"GridMergeSimilar/testsFiles/"

class TestGridMergeSimilar(unittest.TestCase):

    def test_1(self):
        """Test #1 : Test """
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute GridMergeSimilar
        df = GridMergeSimilar(src_df0).compute()
        #([GetDictionaryInformation --dataBase STATIONS --outputAttribute LAT,LON --advancedRequest SELECT_LATITUDE_AS_LAT,LONGITUDE_AS_LON_FROM_STATIONSFB] + ([ReaderStd --input {sources[0]}] >> [Select --fieldName GZ,UU,VV,TT])) >> [InterpolationHorizontalPoint] >> [InterpolationVertical -m USER_DEFINED --verticalLevel 914.4,1828.8,2743.2,3657.6,5486.4 --verticalLevelType METER_SEA_LEVEL --interpolationType LINEAR --extrapolationType FIXED --valueAbove 999.0 --valueBelow 999.0] >> [GetDictionaryInformation --dataBase STATIONS --outputAttribute StationAlphaId,TerrainElevation,FictiveStationFlag --advancedRequest SELECT_StationAlphaId,COALESCE(TerrainElevation,StationElevation)_AS_TerrainElevation,FictiveStationFlag_FROM_STATIONSFB] >> ([Select --fieldName TT,FictiveStationFlag,StationAlphaId] + ([Select --fieldName TerrainElevation] >> [Zap --unit meter --doNotFlagAsZapped] >> [UnitConvert --unit foot]) + [WindModulusAndDirection]) >> [GridMergeSimilar] >> [Zap --metadataZappable --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --noUnitConversion --truncateFieldName --IP1EncodingStyle OLDSTYLE --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "GridMergeSimilar_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Test #2 : Test"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute GridMergeSimilar
        df = GridMergeSimilar(src_df0).compute()
        #([GetDictionaryInformation --dataBase STATIONS --outputAttribute LAT,LON --advancedRequest SELECT_LATITUDE_AS_LAT,LONGITUDE_AS_LON_FROM_EXTRASSTATIONS] + ([ReaderStd --input {sources[0]}] >> [Select --fieldName GZ,UU,VV,TT])) >> [InterpolationHorizontalPoint] >> [InterpolationVertical -m USER_DEFINED --verticalLevel 914.4,1828.8,2743.2,3657.6,5486.4 --verticalLevelType METER_SEA_LEVEL --interpolationType LINEAR --extrapolationType FIXED --valueAbove 999.0 --valueBelow 999.0] >> [GetDictionaryInformation --dataBase STATIONS --outputAttribute StationAlphaId,TerrainElevation,FictiveStationFlag --advancedRequest SELECT_StationAlphaId,COALESCE(TerrainElevation,StationElevation)_AS_TerrainElevation,FictiveStationFlag_FROM_STATIONSFB] >> ([Select --fieldName TT,FictiveStationFlag,StationAlphaId] + ([Select --fieldName TerrainElevation] >> [Zap --unit meter --doNotFlagAsZapped] >> [UnitConvert --unit foot]) + [WindModulusAndDirection]) >> [GridMergeSimilar]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
