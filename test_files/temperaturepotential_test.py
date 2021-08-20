

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"TemperaturePotential/testsFiles/"

class TestTemperaturePotential(unittest.TestCase):

    def test_1(self):
        """ Calcule de la température potentiel à partir d'un fichier standard."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperaturePotential
        df = TemperaturePotential(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [TemperaturePotential] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TemperaturePotential_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """ Calcule de la température potentiel à partir d'un fichier standard."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperaturePotential
        df = TemperaturePotential(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> [UnitConvert --unit kelvin] >> [TemperaturePotential] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TemperaturePotential_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
