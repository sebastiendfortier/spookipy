

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


plugin_test_dir = TEST_PATH + "GetDictionaryInformation/testsFiles/"


class TestGetDictionaryInformation(unittest.TestCase):

    def test_1(self):
        """Get every column of table DATATYPE."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STDVAR --table DATATYPE --outputAttribute * ] >> [Zap --metadataZappable --dateOfOrigin 20110303T183200 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --truncateFieldName --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "datatype_STDVAR_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """Get station type only from FDSTATIONS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute TYPE --table CANSTAT] >> [Zap --metadataZappable --dateOfOrigin 20110303T183200 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_type_CANSTAT_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """Get station lat only from CANSTAT."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Latitude --table CANSTAT] >> [Zap --metadataZappable --dateOfOrigin 20110303T183200 --fieldName LAT --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_lat_CANSTAT_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """Get station lon only from CANSTAT."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Longitude --table CANSTAT] >> [Zap --metadataZappable --dateOfOrigin 20110303T183200 --fieldName LON --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_lon_CANSTAT_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """Get station elevation only from CANSTAT."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute ELEVATION --table CANSTAT] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --truncateFieldName --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_elevation_CANSTAT_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """Get all except id from CANSTAT."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute TYPE,Latitude,Longitude,ELEVATION --table CANSTAT] >> [ZapSmart --fieldNameFrom Latitude --fieldNameTo LAT] >> [ZapSmart --fieldNameFrom Longitude --fieldNameTo LON] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --truncateFieldName --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_all_except_ids_CANSTAT_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_7(self):
        """Get station type only from FDSTATIONS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Unknown1 --table FDSTATIONS] >> [ZapSmart --fieldNameFrom Unknown1 --fieldNameTo TYPE] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_type_FDSTNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_8(self):
        """Get station lat only from FDSTATIONS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Latitude --table FDSTATIONS] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --fieldName LAT --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_lat_FDSTNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_9(self):
        """Get station lon only from FDSTATIONS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Longitude --table FDSTATIONSRAW] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --fieldName LON --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_lon_FDSTNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_10(self):
        """Get station elevation only from FDSTATIONS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute TerrainElevation --table FDSTATIONS] >> [ZapSmart --fieldNameFrom TerrainElevation --fieldNameTo ELEV] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --truncateFieldName --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_elevation_FDSTNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_11(self):
        """Get many fields from FDSTATIONS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Unknown1,Latitude,Longitude,TerrainElevation --table FDSTATIONS] >> [ZapSmart --fieldNameFrom Latitude --fieldNameTo LAT] >> [ZapSmart --fieldNameFrom Longitude --fieldNameTo LON] >> [ZapSmart --fieldNameFrom Unknown1 --fieldNameTo TYPE] >> [ZapSmart --fieldNameFrom TerrainElevation --fieldNameTo ELEV] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --truncateFieldName --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_all_except_ids_FDSTNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_12(self):
        """Get station type only from FUSTNS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute TYPE --table FUSTNS] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_type_FUSTNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_13(self):
        """Get station lat only from FUSTNS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Latitude --table FUSTNS] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --fieldName LAT --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_lat_FUSTNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_14(self):
        """Get station lon only from FUSTNS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Longitude --table FUSTNS] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --fieldName LON --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_14.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_lon_FUSTNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_15(self):
        """Get station elevation only from FUSTNS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute ELEVATION --table FUSTNS] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --truncateFieldName --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_15.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_elevation_FUSTNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_16(self):
        """Get all except ids from FUSTNS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute TYPE,Latitude,Longitude,ELEVATION --table FUSTNS] >> [ZapSmart --fieldNameFrom Latitude --fieldNameTo LAT] >> [ZapSmart --fieldNameFrom Longitude --fieldNameTo LON] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --truncateFieldName --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_16.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_all_except_ids_FUSTNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_17(self):
        """Get station type only from FX6STNS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute TYPE --table FX6STNS] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_17.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_type_FX6STNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_18(self):
        """Get station lat only from FX6STNS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Latitude --table FX6STNS] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --fieldName LAT --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_18.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_lat_FX6STNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_19(self):
        """Get station lon only from FX6STNS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Longitude --table FX6STNS] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --fieldName LON --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_19.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_lon_FX6STNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_20(self):
        """Get station elevation only from FX6STNS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute ELEVATION --table FX6STNS] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --truncateFieldName --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_20.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_elevation_FX6STNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_21(self):
        """Get all except ids from FX6STNS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute TYPE,Latitude,Longitude,ELEVATION --table FX6STNS] >> [ZapSmart --fieldNameFrom Latitude --fieldNameTo LAT] >> [ZapSmart --fieldNameFrom Longitude --fieldNameTo LON] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --truncateFieldName --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_21.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_all_except_ids_FX6STNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_22(self):
        """Get all except ids from FX6STNS."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute TYPE,Latitude,Longitude,ELEVATION --advancedRequest SELECT_TYPE,Latitude,Longitude,ELEVATION_FROM_FX6STNS;] >> [ZapSmart --fieldNameFrom Latitude --fieldNameTo LAT] >> [ZapSmart --fieldNameFrom Longitude --fieldNameTo LON] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --truncateFieldName --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_22.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "station_all_except_ids_FX6STNS_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_23(self):
        """Test advancedRequest 2 : get all FB station."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Latitude,Longitude --advancedRequest SELECT_Latitude,Longitude_FROM_MDICP4D_JOIN_PRODUCTS_ON_PRODUCTS.SpookiStationKey=MDICP4D.SpookiStationKey_WHERE_PRODUCTS.ProductName_LIKE_'%FB%'] >> [ZapSmart --fieldNameFrom Latitude --fieldNameTo LAT] >> [ZapSmart --fieldNameFrom Longitude --fieldNameTo LON] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_23.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "advancedRequest2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_24(self):
        """Test advancedRequest 3 : get all FB station from view."""
        # open and read source
        source0 = plugin_test_dir + "bidon_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [GetDictionaryInformation --dataBase STATIONS --outputAttribute Latitude,Longitude --advancedRequest SELECT_Latitude,Longitude_FROM_STATIONSFB] >> [ZapSmart --fieldNameFrom Latitude --fieldNameTo LAT] >> [ZapSmart --fieldNameFrom Longitude --fieldNameTo LON] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_24.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "advancedRequest2_fromview_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_25(self):
        """Get all except ids from FX6STNS and interpolate with interpolationHorizontalLatLon."""
        # open and read source
        source0 = plugin_test_dir + "input_big_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute GetDictionaryInformation
        df = GetDictionaryInformation(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT --pdsLabel 928V4 --verticalLevel 700,500] >> [GetDictionaryInformation --dataBase STATIONS --outputAttribute LATITUDE,LONGITUDE --table FX6STNS] >> [ZapSmart --fieldNameFrom LATITUDE --fieldNameTo LAT] >> [ZapSmart --fieldNameFrom LONGITUDE --fieldNameTo LON] >> [InterpolationHorizontalPoint] >> [GetDictionaryInformation --dataBase STATIONS --outputAttribute TYPE,ELEVATION --table FX6STNS] >> [Zap --metadataZappable --dateOfOrigin 20110303T183205 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --truncateFieldName --IP1EncodingStyle OLDSTYLE --makeIP1EncodingWorkWithTests ]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_25.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "createInterpolatedOutput_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
