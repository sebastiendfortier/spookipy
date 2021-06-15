

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"SpatialWeightedAveraging/testsFiles/"

class TestSpatialWeightedAveraging(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 : SpatialWeightedAveraging --searchRadius 5 --distanceType KM --kernelType UNIFORM"""
        # open and read source
        source0 = plugin_test_dir + "input_nat.eta"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SpatialWeightedAveraging
        df = SpatialWeightedAveraging(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ', '[Select --fieldName TT] >> ', '[SpatialWeightedAveraging --searchRadius 5 --distanceType KM --kernelType UNIFORM --excludeEdges] >> ', '[ReplaceDataIfCondition --condition isnan --value -1.0] >> ', '[Zap --pdsLabel KDEUKM --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_1.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_3(self):
        """Test #3 : SpatialWeightedAveraging --searchRadius 20 --distanceType KM --kernelType GAUSSIAN --smoothingParameter 15"""
        # open and read source
        source0 = plugin_test_dir + "input_nat.eta"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SpatialWeightedAveraging
        df = SpatialWeightedAveraging(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ', '[Select --fieldName TT] >> [SpatialWeightedAveraging --searchRadius 20 --distanceType KM --kernelType GAUSSIAN --smoothingParameter 15 --excludeEdges]>> ', '[ReplaceDataIfCondition --condition isnan --value -1.0] >> ', '[Zap --pdsLabel KDEGKM --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_5(self):
        """Test #5 : SpatialWeightedAveraging --searchRadius 9 --distanceType KM --kernelType GAUSSIAN --smoothingParameter 4         --landFracDiffMax 0.7 """
        # open and read source
        source0 = plugin_test_dir + "input_nat.eta"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SpatialWeightedAveraging
        df = SpatialWeightedAveraging(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ', '[Select --fieldName TT,ME,MG,SLX] >> ', '[SpatialWeightedAveraging --searchRadius 9 --distanceType KM --kernelType GAUSSIAN --smoothingParameter 4 --landFracDiffMax 0.7 --excludeEdges] >> ', '[ReplaceDataIfCondition --condition isnan --value -1.0] >> ', '[Zap --pdsLabel KDEGKM --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_5.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6(self):
        """Test #6 : SpatialWeightedAveraging --searchRadius 15 --distanceType KM --kernelType GAUSSIAN --smoothingParameter 4        --landFracDiffMax 0.7 """
        # open and read source
        source0 = plugin_test_dir + "input_nat.eta"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SpatialWeightedAveraging
        df = SpatialWeightedAveraging(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ', '[SpatialWeightedAveraging --searchRadius 15 --distanceType KM --kernelType GAUSSIAN --smoothingParameter 4 --landFracDiffMax 0.7 --excludeEdges] >> ', '[ReplaceDataIfCondition --condition isnan --value -1.0] >> ', '[Zap --pdsLabel KDEGKM --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_6.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_8(self):
        """Test #8 : test includeEdges with controlled data"""
        # open and read source
        source0 = plugin_test_dir + "gds1_pds1_level.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SpatialWeightedAveraging
        df = SpatialWeightedAveraging(src_df0).compute()
        #['[ReaderCsv --input {sources[0]}] >> ', '[Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> ', '[SpatialWeightedAveraging --searchRadius 2 --distanceType POINTS --kernelType UNIFORM --altDiffMax 500] >> ', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_8.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_9(self):
        """Test #9 : Tester fichier global"""
        # open and read source
        source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SpatialWeightedAveraging
        df = SpatialWeightedAveraging(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [SpatialWeightedAveraging --searchRadius 3 --distanceType POINTS --kernelType UNIFORM] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_9.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_10(self):
        """Test #10 : test includeEdges with controlled data global simulation"""
        # open and read source
        source0 = plugin_test_dir + "gds1_pds1_level.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SpatialWeightedAveraging
        df = SpatialWeightedAveraging(src_df0).compute()
        #['[ReaderCsv --input {sources[0]}] >> ', '[Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> ', '[SpatialWeightedAveraging --searchRadius 3 --distanceType POINTS --kernelType UNIFORM --forceGlobal] >> ', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_10.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_11(self):
        """Test #11 : test excludeEdges with controlled data"""
        # open and read source
        source0 = plugin_test_dir + "input_nat.eta"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SpatialWeightedAveraging
        df = SpatialWeightedAveraging(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ', '[Select --fieldName TT] >> ', '[SpatialWeightedAveraging --searchRadius 5 --distanceType KM --kernelType UNIFORM --excludeEdges] >> ', '[ReplaceDataIfCondition --condition isnan --value -1.0] >> ', '[Zap --pdsLabel KDEUKM --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_1.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_12(self):
        """Test #12 : test excludeEdges with controlled data global simulation, test writer with missing data"""
        # open and read source
        source0 = plugin_test_dir + "gds1_pds1_level.csv"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SpatialWeightedAveraging
        df = SpatialWeightedAveraging(src_df0).compute()
        #['[ReaderCsv --input {sources[0]}] >> ', '[Zap --dateOfOrigin 20100126T211215 --doNotFlagAsZapped] >> ', '[SpatialWeightedAveraging --searchRadius 3 --distanceType POINTS --kernelType UNIFORM --excludeEdges] >> ', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests --flagMissingData --replaceMissingData]']

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_12.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_13(self):
        """Test #13 : issue #120 expected fail with message """
        # open and read source
        source0 = plugin_test_dir + "issue120.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SpatialWeightedAveraging
        df = SpatialWeightedAveraging(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ', '[Select --fieldName PR] >> ', '[SpatialWeightedAveraging --searchRadius 10 --distanceType POINTS --kernelType UNIFORM --excludeEdges] >> ', '[Zap --fieldName V6] >>', '[WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


