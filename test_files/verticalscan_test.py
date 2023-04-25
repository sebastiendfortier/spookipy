

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


plugin_test_dir = TEST_PATH + "VerticalScan/testsFiles/"


class TestVerticalScan(unittest.TestCase):

    def test_1(self):
        """Test with GEOPOTENTIAL vertical representation, consecutiveEvents = INF."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.1e-05] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan1_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """  Test with GEOPOTENTIAL vertical representation, consecutiveEvents = SUP."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.1e-05] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """  Test with GEOPOTENTIAL vertical representation, limited occurrences (same as input)."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 7 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.1e-05] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan_limitOcceq_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """  Test with GEOPOTENTIAL vertical representation, limited occurrences (less than input)."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 6 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.1e-05] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan_limitOccless_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """  Test with GEOPOTENTIAL vertical representation, limited occurrences (one only)."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 1 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.1e-05] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "verticalScan_limitOccone_file2cmp_20200831.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """  Test with PRESSURE vertical representation, consecutiveEvents = INF."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation PRESSURE --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScanPXinf_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_7(self):
        """  Test with PRESSURE vertical representation, consecutiveEvents = SUP."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation PRESSURE --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScanPXsup_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_8(self):
        """  Test with BOTH vertical representations, consecutiveEvents = INF."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan3inf_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_9(self):
        """  Test with BOTH vertical representations, consecutiveEvents = SUP."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan3sup_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_10(self):
        """  Test with BOTH vertical representations, with outputFieldName1, outputFieldName2, outputFieldName3, outputFieldName4 and consecutiveEvents = SUP."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputFieldName1 AG1 --outputFieldName2 AP2 --outputFieldName3 BO3 --outputFieldName4 NB4 --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ( ([Select --fieldName AP2] >> [Zap --fieldName APX ]) + ([Select --fieldName AG1] >> [Zap --fieldName AGZ ]) + ([Select --fieldName BO3] >> [Zap --fieldName BOVS ])+ ([Select --fieldName NB4] >> [Zap --fieldName NBVS ]) ) >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan3sup_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_11(self):
        """  Test with maxNbOccurrence = -1, it should stop because of invalid value."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan  --direction ASCENDING --maxNbOccurrence -1 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation BOTH --epsilon 0.1e-05]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_12(self):
        """  Test with epsilon = -1, it should stop because of invalid value."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 1 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation BOTH --epsilon -1.0]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_13(self):
        """  Test with BOTH vertical representations, consecutiveEvents = INF, type VARIABLEVALUE."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT --verticalLevel 1000] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonType VARIABLEVALUE --comparisonValueOrField CF --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan3inf_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_14(self):
        """  Test with BOTH vertical representations, crossover, consecutiveEvents = INF, type VARIABLEVALUE."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT --verticalLevel 1000] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan  --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonType VARIABLEVALUE --comparisonValueOrField CF --crossover --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_14.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan3infCrossTrue_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_15(self):
        """ Test with direction = INVALID, it should stop because of invalid value."""
        # open and read source
        source0 = plugin_test_dir + "tests_15_16_source.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan --direction INVALID --maxNbOccurrence 2 --consecutiveEvents SUP --referenceField D1 --comparisonValueOrField D2 --comparisonType INTERSECTIONS --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.001] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_15.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_16(self):
        """  Test with comparisonType INTERSECTIONS, consecutiveEvents = SUP."""
        # open and read source
        source0 = plugin_test_dir + "tests_15_16_source.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan --direction ASCENDING --maxNbOccurrence 2 --consecutiveEvents SUP --referenceField D1 --comparisonValueOrField D2 --comparisonType INTERSECTIONS --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.001] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_16.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test15_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_17(self):
        """  Test with comparisonField, consecutiveEvents = INF."""
        # open and read source
        source0 = plugin_test_dir + "tests_15_16_source.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan --direction ASCENDING --maxNbOccurrence 2 --consecutiveEvents INF --referenceField D1 --comparisonValueOrField D2 --comparisonType INTERSECTIONS --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.001] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_17.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test16_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_19(self):
        """  Test with a file that contains only 1 level for TT."""
        # open and read source
        source0 = plugin_test_dir + "verticalScan_1niveau.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --doNotFlagAsZapped]) + ([Select --fieldName TT] >> [Pressure --coordinateType AUTODETECT --referenceField TT]) ) >> [VerticalScan --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonValueOrField 0 --comparisonType CONSTANTVALUE --outputVerticalRepresentation PRESSURE --epsilon 0.00001] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_19.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "reference_file_test_19.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_20(self):
        """  Test with a file that contains many occurences."""
        # open and read source
        source0 = plugin_test_dir + "verticalScanHighOccurence.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan -d ASCENDING -r TTLP -t INTERSECTIONS -c TT -o BOTH -e INF -m 30 --epsilon 0.00001 --valueToIgnore -300] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_20.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScanHighOccurence_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_21(self):
        """  Test with a file that contains a first point with equalities, but no crossing and a second point with close crossing."""
        # open and read source
        source0 = plugin_test_dir + "equalitiesWithoutCrossingAndCloseOccurences.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan -d ASCENDING -r TT -t INTERSECTIONS -c TTLP -o PRESSURE -e INF -m 10 --epsilon 0.00001 --valueToIgnore -300] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_21.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "equalitiesWithoutCrossingAndCloseOccurences_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_22(self):
        """  Test with BOTH vertical representations, crossover, consecutiveEvents = SUP, type VARIABLEVALUE."""
        # open and read source
        source0 = plugin_test_dir + "testcases2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT --verticalLevel 1000] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType VARIABLEVALUE --comparisonValueOrField CF --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_22.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "testcases2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_23(self):
        """  Test with BOTH vertical representations, crossover, consecutiveEvents = SUP, type VARIABLEVALUE."""
        # open and read source
        source0 = plugin_test_dir + "testcases2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT --verticalLevel 1000] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType VARIABLEVALUE --comparisonValueOrField CF --crossover --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_23.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "testcases2_crossover_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_24(self):
        """  Test with BOTH vertical representations, crossover, consecutiveEvents = SUP, type VARIABLEVALUE."""
        # open and read source
        source0 = plugin_test_dir + "testcases2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --crossover --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_24.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "testcases2_crossover_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_25(self):
        """  Test with BOTH vertical representations, crossover, consecutiveEvents = SUP, type INTERSECTIONS."""
        # open and read source
        source0 = plugin_test_dir + "testcases2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT ] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan --direction ASCENDING --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType INTERSECTIONS --comparisonValueOrField CF --crossover --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_25.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "testcases2_crossover_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_26(self):
        """Test with GEOPOTENTIAL vertical representation, direction DESCENDING, comparisonType = CONSTANTVALUE, consecutiveEvents = INF."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan --direction DESCENDING --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.1e-05] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_26.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan26_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_27(self):
        """  Test with GEOPOTENTIAL vertical representation, direction DESCENDING, comparisonType = CONSTANTVALUE,consecutiveEvents = SUP."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan --direction DESCENDING --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.1e-05] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_27.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan27_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_28(self):
        """  Test with PRESSURE vertical representation,  direction = DESCENDING, comparisonType = CONSTANTVALUE,consecutiveEvents = INF."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan --direction DESCENDING --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation PRESSURE --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_28.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan28_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_29(self):
        """  Test with PRESSURE vertical representation, direction = DESCENDING, comparisonType = CONSTANTVALUE, consecutiveEvents = SUP."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan --direction DESCENDING --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation PRESSURE --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_29.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan29_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_30(self):
        """  Test with BOTH vertical representations, crossover, direction = DESCENDING, consecutiveEvents = INF, type VARIABLEVALUE."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT --verticalLevel 1000] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan --direction DESCENDING --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonType VARIABLEVALUE --comparisonValueOrField CF --crossover --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_30.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan30_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_31(self):
        """  Test with BOTH vertical representations, descending, crossover, consecutiveEvents = SUP, type INTERSECTIONS."""
        # open and read source
        source0 = plugin_test_dir + "testcases2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT ] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [VerticalScan --direction DESCENDING --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType INTERSECTIONS --comparisonValueOrField CF --crossover --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_31.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan31_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_32(self):
        """Test with GEOPOTENTIAL vertical representation, checkForEquality, consecutiveEvents = INF."""
        # open and read source
        source0 = plugin_test_dir + "testcases_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan --direction ASCENDING --checkForEquality --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.1e-05] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_32.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan32_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_33(self):
        """Test with PRESSURE vertical representation, checkForEquality, direction DESCENDING, consecutiveEvents = INF, outputFieldName5 = ABCD ."""
        # open and read source
        source0 = plugin_test_dir + "testcases2_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan --direction DESCENDING --checkForEquality --maxNbOccurrence 5 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation PRESSURE --epsilon 0.1e-05 --outputFieldName5 ABCD] >> ([Select --fieldName ABCD --exclude] + ([Select --fieldName ABCD] >> [Zap --fieldName BOEQ ])) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_33.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan33_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_34(self):
        """Test with GEOPOTENTIAL vertical representation, checkForEquality, consecutiveEvents = INF."""
        # open and read source
        source0 = plugin_test_dir + "testcases3_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [VerticalScan --direction DESCENDING --checkForEquality --maxNbOccurrence 1 --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation GEOPOTENTIAL --epsilon 0.1e-05] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_34.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalScan34_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_35(self):
        """  Test with BOTH vertical representations, crossover, consecutiveEvents = SUP, type VARIABLEVALUE. HYBRID_5005"""
        # open and read source
        source0 = plugin_test_dir + "minimal_TT_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute VerticalScan
        df = VerticalScan(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >> ', '(', '[Copy] + ([Select --fieldName TT ] >> [SetConstantValue --value 0] >> ', '[Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> ', '[VerticalScan --maxNbOccurrence 10 --consecutiveEvents SUP --referenceField TT --comparisonType INTERSECTIONS --comparisonValueOrField CF --crossover --outputVerticalRepresentation BOTH --epsilon 0.1e-05] >> ', '([Select --fieldName APX --exclude] + ([Select --fieldName APX ] >> [Zap --nbitsForDataStorage R16])', ') >> ', '[WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]']

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_35.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_26.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
