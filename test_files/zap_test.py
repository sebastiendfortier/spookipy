

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


plugin_test_dir = TEST_PATH + "Zap/testsFiles/"


class TestZap(unittest.TestCase):

    def test_1(self):
        """Tester l'option --typeOfField avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --typeOfField BLABLABLA]

        # write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """Tester l'option --run avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --run BLABLABLA]

        # write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """Tester l'option --ensembleMember avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --ensembleMember BLABLABLA]

        # write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """Tester l'option --verticalLevel avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --verticalLevel -1]

        # write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """Tester l'option --verticalLevelType avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --verticalLevelType BLABLABLA]

        # write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_7(self):
        """Tester l'option --forecastHour avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --forecastHour -10]

        # write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_8(self):
        """Tester l'option --forecastHourOnly avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --forecastHourOnly -10]

        # write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_9(self):
        """Tester l'option --userDefinedIndex avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --userDefinedIndex -10]

        # write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_10(self):
        """Tester l'option --nbitsForDataStorage avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --nbitsForDataStorage i65]

        # write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_11(self):
        """Tester l'option --unit avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --unit i65]

        # write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_12(self):
        """Tester l'option --forecastHourOnly avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --forecastHourOnly -10:00:00]

        # write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_13(self):
        """Tester l'option --forecastHourOnly avec une valeur valide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHourOnly 11:00:01] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_13.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_14(self):
        """Tester l'option --forecastHour avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Zap --forecastHour -10:00:00]

        # write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_15(self):
        """Tester l'option --forecastHour avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHour 11:38:00] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_16(self):
        """Tester l'option --forecastHour avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHour 11.633333333] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_17(self):
        """Tester l'option --forecastHourOnly, --timeStepNumber et --lenghtOfTimeStep avec une valeur valide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHourOnly 11.633333333 --lenghtOfTimeStep 1 --timeStepNumber 41880] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_17.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_17.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_18(self):
        """Tester l'option --forecastHour, --timeStepNumber et --lenghtOfTimeStep avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHourOnly 11.6 --lenghtOfTimeStep 1 --timeStepNumber 41880] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_19(self):
        """Tester l'option --forecastHour, --timeStepNumber et --lenghtOfTimeStep avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHourOnly 11.633333333 --lenghtOfTimeStep 2 --timeStepNumber 41880] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_19.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_20(self):
        """Tester l'option --forecastHour, --timeStepNumber et --lenghtOfTimeStep avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHourOnly 11.633333333 --lenghtOfTimeStep 1 --timeStepNumber 41888] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_21(self):
        """Tester l'option --forecastHour et --lenghtOfTimeStep avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHourOnly 11.633333333 --lenghtOfTimeStep 1] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_21.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_22(self):
        """Tester l'option --forecastHour et --timeStepNumber avec une valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHourOnly 11.633333333 --timeStepNumber 41880] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_23(self):
        """Tester l'option --forecastHourOnly, --timeStepNumber et --lenghtOfTimeStep avec une valeur valide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHourOnly 11:31:00 --lenghtOfTimeStep 1 --timeStepNumber 41460] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_23.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_23.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_24(self):
        """Tester l'option --forecastHourOnly, --timeStepNumber et --lenghtOfTimeStep avec une valeur valide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHourOnly 11:31:00 --lenghtOfTimeStep 60 --timeStepNumber 691] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_24.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_24.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_25(self):
        """Tester l'option --forecastHourOnly, --timeStepNumber et --lenghtOfTimeStep avec une valeur valide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --forecastHourOnly 11:31:01 --lenghtOfTimeStep 1 --timeStepNumber 41461] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_25.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_25.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_26(self):
        """Tester l'option --modificationFlag, avec 2 valeurs valide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag ZAPPED=TRUE,BOUNDED=FALSE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_26.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_26.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_27(self):
        """Tester l'option --modificationFlag, avec 1 valeur valide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag ZAPPED=TRUE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_27.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_27.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_28(self):
        """Tester l'option --modificationFlag, avec 1 valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag ZAPPEDS=TRUE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_28.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_29(self):
        """Tester l'option --modificationFlag, avec 1 valeur invalide!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag ZAPPED=TRU] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_29.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_30(self):
        """Tester l'option --modificationFlag, avec FILTERED=TRUE!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag FILTERED=TRUE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_30.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_30.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_31(self):
        """Tester l'option --modificationFlag, avec INTERPOLATED=TRUE!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag INTERPOLATED=TRUE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_31.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_31.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_32(self):
        """Tester l'option --modificationFlag, avec UNITCONVERTED=TRUE!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag UNITCONVERTED=TRUE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_32.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_32.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_33(self):
        """Tester l'option --modificationFlag, avec ALL_FLAGS=TRUE!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag ALL_FLAGS=TRUE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_33.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_33.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_34(self):
        """Tester l'option --modificationFlag, avec ZAPPED!"""
        # open and read source
        source0 = plugin_test_dir + "resulttest_26.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag ZAPPED=FALSE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_34.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_34.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_35(self):
        """Tester l'option --modificationFlag, avec ZAPPED and FILTERED!"""
        # open and read source
        source0 = plugin_test_dir + "resulttest_30.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag ZAPPED=FALSE,FILTERED=FALSE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_35.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_34.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_36(self):
        """Tester l'option --modificationFlag, avec FILTERED!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag FILTERED=FALSE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_36.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_34.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_37(self):
        """Tester l'option --modificationFlag, avec INTERPOLATED!"""
        # open and read source
        source0 = plugin_test_dir + "resulttest_31.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag INTERPOLATED=FALSE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_37.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_34.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_38(self):
        """Tester l'option --modificationFlag, avec UNITCONVERTED!"""
        # open and read source
        source0 = plugin_test_dir + "resulttest_32.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag UNITCONVERTED=FALSE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_38.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_34.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_39(self):
        """Tester l'option --modificationFlag, avec ZAP et FILTERED!"""
        # open and read source
        source0 = plugin_test_dir + "zap_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag ZAPPED=TRUE,FILTERED=TRUE] >>', '[Zap --modificationFlag ZAPPED=FALSE,FILTERED=FALSE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_39.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_34.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_40(self):
        """Tester l'option --modificationFlag, avec ENSEMBLEEXTRAINFO!"""
        # open and read source
        source0 = plugin_test_dir + "resulttest_32.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute Zap
        df = Zap(src_df0).compute()
        #['[ReaderStd --input {sources[0]}] >>', '[Zap --modificationFlag ALL_FLAGS=FALSE] >>', '[Zap --modificationFlag ENSEMBLEEXTRAINFO=TRUE] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

        # write the result
        results_file = TMP_PATH + "test_40.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_40.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
