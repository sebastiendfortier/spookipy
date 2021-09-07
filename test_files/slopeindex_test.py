

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"SlopeIndex/testsFiles/"

class TestSlopeIndex(unittest.TestCase):

    def test_1(self):
        """Appel a SlopeIndex,valeur invalide pour verticalLevel."""
        # open and read source
        source0 = plugin_test_dir + "minimal_pres.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SlopeIndex
        df = SlopeIndex(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [SlopeIndex --verticalLevel 400 --excludeEdges]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """ Test avec UU, VV fetch 5"""
        # open and read source
        source0 = plugin_test_dir + "minimal_pres.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "minimal_lam_nat.pres.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute SlopeIndex
        df = SlopeIndex(src_df0).compute()
        #['( ([ReaderStd --input {sources[0]}] >> [Select --fieldName ME ]) + ', '([ReaderStd --input {sources[1]}] >> ', '[Select --fieldName UU,VV --verticalLevel 700 --verticalLevelType MILLIBARS]) ) >>', '[SlopeIndex --verticalLevel 700 --fetch 5 --excludeEdges] >> ', '[ReplaceDataIfCondition --condition isnan --value -999.0 --clearMissingDataFlag] >> ', '[Zap --pdsLabel SlopeIndex --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]']

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """without edges default fetch"""
        # open and read source
        source0 = plugin_test_dir + "minimal_pres.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "minimal_lam_nat.pres.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute SlopeIndex
        df = SlopeIndex(src_df0).compute()
        #['( [ReaderStd --input {sources[0]}] >> [Select --fieldName ME ] ) + ', '( [ReaderStd --input {sources[1]}] >> ', '[Select --fieldName UU,VV --verticalLevel 700 --verticalLevelType MILLIBARS] ) >> ', '[SlopeIndex --verticalLevel 700 --excludeEdges] >> ', '[ReplaceDataIfCondition --condition isnan --value -999.0 --clearMissingDataFlag] >> ', '[Zap --pdsLabel SlopeIndex --doNotFlagAsZapped] >>', '[WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]']

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """with edges default fetch"""
        # open and read source
        source0 = plugin_test_dir + "minimal_pres.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "minimal_lam_nat.pres.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute SlopeIndex
        df = SlopeIndex(src_df0).compute()
        #[' ( [ReaderStd --input {sources[0]}] >> [Select --fieldName ME ] ) + ', '( [ReaderStd --input {sources[1]}] >> ', '[Select --fieldName UU,VV --verticalLevel 700 --verticalLevelType MILLIBARS] ) >> ', '[SlopeIndex --verticalLevel 700] >> ', '[WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]']

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_4.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """ Test avec UU, VV fetch 5, verify writer with missing data"""
        # open and read source
        source0 = plugin_test_dir + "minimal_pres.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "minimal_lam_nat.pres.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute SlopeIndex
        df = SlopeIndex(src_df0).compute()
        #['( [ReaderStd --input {sources[0]}] >> [Select --fieldName ME ] ) + ', '( [ReaderStd --input {sources[1]}] >> ', '[Select --fieldName UU,VV --verticalLevel 700 --verticalLevelType MILLIBARS] ) >> ', '[SlopeIndex --verticalLevel 700 --excludeEdges] >> ', '[WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --replaceMissingData]']

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """ Test avec UU, VV fetch 1 - comparer avec exe marc verville"""
        # open and read source
        source0 = plugin_test_dir + "slopeIndex.work"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SlopeIndex
        df = SlopeIndex(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[SlopeIndex --fetch 1] >> ', '[WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_6.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """ segfault test lamarctic - marc verville"""
        # open and read source
        source0 = plugin_test_dir + "lamarctic.eta.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SlopeIndex
        df = SlopeIndex(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[SlopeIndex] >> ', '[WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_7.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """ segfault test ens.regmodel - marc verville"""
        # open and read source
        source0 = plugin_test_dir + "ens.regmodel.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SlopeIndex
        df = SlopeIndex(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[SlopeIndex] >> ', '[WriterStd --output {destination_path} --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_8.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """ segfault test ens.glbmodel - marc verville"""
        # open and read source
        source0 = plugin_test_dir + "ens.glbmodel.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute SlopeIndex
        df = SlopeIndex(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[SlopeIndex] >> ', '[WriterStd --output {destination_path}]']

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_9.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
