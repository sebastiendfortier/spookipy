

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"TemperatureVirtual/testsFiles/"

class TestTemperatureVirtual(unittest.TestCase):

    def test_1(self):
        """Calcul de la pression de vapeur saturante avec un fichier hybrid."""
        # open and read source
        source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureVirtual
        df = TemperatureVirtual(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,HR] >> [TemperatureVirtual] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TemperatureVirtual_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Calcul de la pression de vapeur saturante avec un fichier hybrid 5005."""
        # open and read source
        source0 = plugin_test_dir + "minimal_TTHR_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureVirtual
        df = TemperatureVirtual(src_df0).compute()
        #['[ReaderStd --input {sources[0]} ] >> ', '[MatchFieldsByCommonLevels --referenceField TT --matchFields HR]>>', '[WriterStd --output {destination_path} ]']

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
