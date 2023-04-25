

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


plugin_test_dir = TEST_PATH + "PrecipitationTypeSignificant/testsFiles/"


class TestPrecipitationTypeSignificant(unittest.TestCase):

    def test_1(self):
        """Tester le plugin avec 2 groupes d'intervalles avec un fichier qui provient de regeta et regdiag."""
        # open and read source
        source0 = plugin_test_dir + "regeta_et_regdiag_2013020400_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute PrecipitationTypeSignificant
        df = PrecipitationTypeSignificant(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [PrecipitationAmount --fieldName RN,SN,FR,PE --rangeForecastHour 0@48,0@48 --interval 12,24 --step 12,24] >> [Select --fieldName RN,SN,FR,PE] >> [FilterDigital --filter 1,2,1 --repetitions 1] >> [PrecipitationTypeSignificant] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NW1_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """Tester le plugin avec 2 groupes d'intervalles avec un fichier qui provient de regeta et regdiag. intervals already calculated"""
        # open and read source
        source0 = plugin_test_dir + "encodedIP2andIP3.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute PrecipitationTypeSignificant
        df = PrecipitationTypeSignificant(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName RN,SN,FR,PE] >> [PrecipitationTypeSignificant] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NW1_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
