

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"TimeIntervalMinMax/testsFiles/"

class TestTimeIntervalMinMax(unittest.TestCase):

    def test_1(self):
        """Tester sans la cle obligatoire FIELDNAME."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --type MAX --rangeForecastHour 0@177 --interval 12 --step 24 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Tester sans la cle obligatoire type."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --rangeForecastHour 0@177 --interval 12 --step 24 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Tester sans la cle obligatoire rangeForecastHour."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --step 24 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Tester avec le type TYPE en majuscule."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --TYPE MIN --interval 12 --step 24 --outputFieldNameMin PRX] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """Tester avec un interval à zero"""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MIN --interval 0 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """Tester avec un step a zero."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --rangeForecastHour 0@177 --step 0 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """Tester avec type max avec une sortie min."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MAX --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """Tester avec step max et une sortie min."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MAX --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """Tester l'option --output avec un path qui n'existe pas!"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MAX --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMax PRX] >>[WriterStd --output /tmp//totonSZBK2/toto.std]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_10(self):
        """Tester avec type MAX et outputfieldNameMIN, c'est pas bon."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MAX --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_11(self):
        """Tester avec type MIN et outputfieldNameMAX c'est pas bon."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMax PRX]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_12(self):
        """Tester avec type MINI, le type mini existe pas."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MINI --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMax PRX]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_13(self):
        """Tester avec un rangeForecastHour invalide"""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MAX --interval 12 --rangeForecastHour -1 --step 24 --outputFieldNameMax PRX]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_14(self):
        """Tester avec deux intervales à la place d'un seul."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MIN --interval 12,10 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_15(self):
        """Tester avec un interval qui depasse le rangeForecastHour."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --rangeForecastHour 0@177,50@58 --step 24 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_16(self):
        """Tester avec deux steps à la place d'un seul."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --rangeForecastHour 0@177 --step 24,15 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_17(self):
        """Tester avec 2 outputfieldNameMin mais un seul fieldName."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type MIN --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX,PRZ]

        #write the result
        results_file = TMP_PATH + "test_17.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_18(self):
        """Tester avec 2 steps  mais un seul fieldName."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type BOTH --interval 12 --rangeForecastHour 0@177 --step 24,15 --outputFieldNameMin PRX]

        #write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_19(self):
        """Tester avec 2 outputFieldNameMax mais 1 seul fieldName."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type BOTH --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX --outputFieldNameMax PRX,PRZ]

        #write the result
        results_file = TMP_PATH + "test_19.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_20(self):
        """Tester avec 1 fieldName PR et 2 outputFieldNameMin PRX,PRZ mais un seul outputFieldNameMax."""
        # open and read source
        source0 = plugin_test_dir + "global20121217_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalMinMax --fieldName PR --type BOTH --interval 12 --rangeForecastHour 0@177 --step 24 --outputFieldNameMin PRX,PRZ --outputFieldNameMax PRX]

        #write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_21(self):
        """ Calcul d'un test min avec un fieldName TT et 2 rangeForecastHours."""
        # open and read source
        source0 = plugin_test_dir + "TT_Interval_3_168_160_150_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type MIN --rangeForecastHour 160@168,150@160 --fieldName TT --interval 3,3 --step 2,2] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_21.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TT_Interval_3_168_160_150_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_22(self):
        """ Calcul d'un test MIN avec 2 fieldNames TT,HU et 2 rangeForecastHours."""
        # open and read source
        source0 = plugin_test_dir + "TT_HU_Interval_3_168_160_24_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type MIN --rangeForecastHour 0@24,160@168 --fieldName TT,HU --interval 3,3 --step 2,2] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TT_HU_Interval_3_168_160_24_0_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_23(self):
        """ Calcul d'un test MAX avec 2 fieldNames TT,GZ et 2 rangeForecastHours."""
        # open and read source
        source0 = plugin_test_dir + "TT_GZ_Interval_3_80_56_20_0_diff_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type MIN --rangeForecastHour 56@80,0@20 --fieldName TT,GZ --interval 3,3 --step 2,2] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_23.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TT_GZ_Interval_3_80_56_20_0_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_24(self):
        """ Calcul d'un test MAX  avec 2 fieldNames HU,GZ et 2 rangeForecastHours."""
        # open and read source
        source0 = plugin_test_dir + "HU_GZ_Interval_4_144_168_20_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type MAX --rangeForecastHour 144@168,0@20 --fieldName HU,GZ --interval 4,4 --step 5,5] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_24.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "HU_GZ_Interval_4_144_168_20_0_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_25(self):
        """ Calcul d'un test MAX avec 1 fieldName TT et 3 rangeForecastHours."""
        # open and read source
        source0 = plugin_test_dir + "TT_Interval_2_3_4_160_150_140_20_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type MAX --rangeForecastHour 0@20,140@150,150@160 --fieldName TT --interval 2,3,4 --step 2,2,2] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_25.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TT_Interval_2_3_4_160_150_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_26(self):
        """ Calcul d'un test MAX avec 3 fieldNames et 1 rangeForecastHour."""
        # open and read source
        source0 = plugin_test_dir + "TT_HU_GZ_Interval_2_30_0_diff_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type MAX --rangeForecastHour 0@30 --fieldName TT,HU,GZ --interval 2 --step 2] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_26.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TT_HU_GZ_Interval_2_30_0_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_27(self):
        """ Calcul d'un test BOTH avec 2 fieldNames , 2 rangeForecastHours."""
        # open and read source
        source0 = plugin_test_dir + "TT_HU_Interval_3_168_160_20_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type BOTH --rangeForecastHour 160@168,0@20 --fieldName TT,HU --interval 3,3 --step 3,3] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_27.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TT_HU_Interval_3_168_160_20_0_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_28(self):
        """ Calcul d'un test BOTH avec 1 fieldNames , 3 rangeForecastHours"""
        # open and read source
        source0 = plugin_test_dir + "TT_168_160_140_20_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type BOTH --rangeForecastHour 160@168,140@160,0@20 --fieldName TT --interval 2,3,4 --step 1,2,3] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_28.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TT_Interval_2_3_4_168_160_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_29(self):
        """ Calcul d'un test BOTH avec 3 fieldNames , 3 rangeForecastHours."""
        # open and read source
        source0 = plugin_test_dir + "TT_HU_GZ_168_160_140_20_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type BOTH --rangeForecastHour 160@168,140@160,0@20 --fieldName TT,HU,GZ --interval 2,3,4 --step 1,2,3] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_29.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TT_HU_GZ_Interval_2_3_4_168_160_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_30(self):
        """ Calcul d'un test MIN avec 1 fieldName sans interval."""
        # open and read source
        source0 = plugin_test_dir + "TT_168_160_140_20_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type MIN --rangeForecastHour 160@168,140@160,0@20 --fieldName TT] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_30.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "min_TT_Interval_not_set_160_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_31(self):
        """ Calcul d'un test MAX avec 1 fieldName sans interval."""
        # open and read source
        source0 = plugin_test_dir + "TT_168_160_140_20_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type MAX --rangeForecastHour 160@168,140@160,0@20 --fieldName TT] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_31.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "max_TT_Interval_not_set_160_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_32(self):
        """ Calcul d'un test BOTH avec 1 fieldName sans interval."""
        # open and read source
        source0 = plugin_test_dir + "TT_168_160_140_20_0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type BOTH --rangeForecastHour 160@168,140@160,0@20 --fieldName TT] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_32.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "both_TT_Interval_not_set_160_140_20_0_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_33(self):
        """ Calcul d'un test MIN avec 3 fieldName avec interval sans step."""
        # open and read source
        source0 = plugin_test_dir + "TT_125_100_75_50_25_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type MIN --rangeForecastHour 0@25,50@75,100@125 --fieldName TT --interval 3,4,5 --outputFieldNameMin TTMN] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_33.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "min_TT_Interval_3_4_5_125_100_75_50_25_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_34(self):
        """ Calcul d'un test MAX avec 3 fieldName avec interval sans step."""
        # open and read source
        source0 = plugin_test_dir + "TT_125_100_75_50_25_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type MAX --rangeForecastHour 0@25,50@75,100@125 --fieldName TT --interval 3,4,5 --outputFieldNameMax TTMX] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_34.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "max_TT_Interval_3_4_5_125_100_75_50_25_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_35(self):
        """ Calcul d'un test BOTH avec 3 fieldName avec interval sans step."""
        # open and read source
        source0 = plugin_test_dir + "TT_125_100_75_50_25_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]} ] >> [TimeIntervalMinMax --type BOTH --rangeForecastHour 0@25,50@75,100@125 --fieldName TT --interval 3,4,5 --outputFieldNameMax TTMX --outputFieldNameMin TTMN ] >> [WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_35.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "both_TT_Interval_3_4_5_125_100_75_50_25_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_36(self):
        """ Calcul d'un test BOTH avec 3 fieldName avec interval sans step. rangeForecastHour"""
        # open and read source
        source0 = plugin_test_dir + "TT_125_100_75_50_25_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]} ] >> ', '[TimeIntervalMinMax --type BOTH --rangeForecastHour 0:00:00@25:00:00,50:00:00@75:00:00,100:00:00@125:00:00 --fieldName TT --interval 3,4,5 --outputFieldNameMax TTMX --outputFieldNameMin TTMN ] >> ', '[WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]']

        #write the result
        results_file = TMP_PATH + "test_36.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "both_TT_Interval_3_4_5_125_100_75_50_25_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_35(self):
        """ Calcul d'un test MAX avec 3 fieldName avec interval sans step."""
        # open and read source
        source0 = plugin_test_dir + "TT_125_100_75_50_25_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]} ] >> ', '[TimeIntervalMinMax --type MAX --rangeForecastHour 0@25,50@75,100@125 --fieldName TT --interval 3:00:00,4:00:00,5:00:00 --outputFieldNameMax TTMX] >> ', '[WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]']

        #write the result
        results_file = TMP_PATH + "test_35.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "max_TT_Interval_3_4_5_125_100_75_50_25_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_36(self):
        """ Calcul d'un test min avec un fieldName TT et 2 rangeForecastHours."""
        # open and read source
        source0 = plugin_test_dir + "TT_Interval_3_168_160_150_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TimeIntervalMinMax
        df = TimeIntervalMinMax(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]} ] >> ', '[TimeIntervalMinMax --type MIN --rangeForecastHour 160@168,150@160 --fieldName TT --interval 3,3 --step 2:00:00,2:00:00] >> ', '[WriterStd --output {destination_path} --noUnitConversion --noMetadata --encodeIP2andIP3 ]']

        #write the result
        results_file = TMP_PATH + "test_36.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TT_Interval_3_168_160_150_diff_file2cmp_encodeIP2andIP3.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
