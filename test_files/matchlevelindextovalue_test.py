

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"MatchLevelIndexToValue/testsFiles/"

class TestMatchLevelIndexToValue(unittest.TestCase):

    def test_regtest_match_one_field1_full_computation(self):
        """Test #1 : test_match_one_field1_full_computation."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute MatchLevelIndexToValue
        df = MatchLevelIndexToValue(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >>[MinMaxLevelIndex --minMax MAX --direction UPWARD --outputFieldName2 IND] >>[MatchLevelIndexToValue --outputFieldName TEST] >>[WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_match_one_field1_full_computation.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "lou_matchOneField_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_match_one_field4_full_computation_except_uv(self):
        """Test #4 : test_match_one_field4_full_computation_except_uv."""
        # open and read source
        source0 = plugin_test_dir + "UUVV5x5x2_UV_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute MatchLevelIndexToValue
        df = MatchLevelIndexToValue(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >> [MinMaxLevelIndex --minMax MAX --direction UPWARD --outputFieldName2 IND] >> [MatchLevelIndexToValue --outputFieldName TEST] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_match_one_field4_full_computation_except_uv.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "lou_matchOneField_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_match_one_field4_full_computation(self):
        """Test #5 : test_match_one_field4_full_computation."""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute MatchLevelIndexToValue
        df = MatchLevelIndexToValue(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >> [MinMaxLevelIndex --minMax MAX --direction UPWARD --outputFieldName2 IND] >> [MatchLevelIndexToValue --outputFieldName T5] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_match_one_field4_full_computation.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "lou_matchOneField2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_match_two_fields(self):
        """Test #6 : Tester l'option --outputFieldName avec plus d'un type de champ en entree."""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute MatchLevelIndexToValue
        df = MatchLevelIndexToValue(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ( ( [Select --fieldName TT] >> [MinMaxLevelIndex --minMax MIN --direction UPWARD --outputFieldName1 IND] ) + [Select --fieldName UU,VV] ) >> [MatchLevelIndexToValue --outputFieldName TEST] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_match_two_fields.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_match_no_fields(self):
        """Test #7 : test_match_no_fields."""
        # open and read source
        source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute MatchLevelIndexToValue
        df = MatchLevelIndexToValue(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >> ( [Copy] + ( [SetConstantValue --value -1.0 --bidimensional] >> [Zap --fieldName IND --doNotFlagAsZapped] ) ) >> [MatchLevelIndexToValue --outputFieldName TEST] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_match_no_fields.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "lou_matchNoFields_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_match_negative_index(self):
        """Test #8 : test_match_negative_index."""
        # open and read source
        source0 = plugin_test_dir + "sortie_cpp_cld_200906290606"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "indneg.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute MatchLevelIndexToValue
        df = MatchLevelIndexToValue(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]} {sources[1]}] >> [MatchLevelIndexToValue --outputFieldName T7] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_match_negative_index.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "lou_matchNegativeIndex_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


