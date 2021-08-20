

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"TemperatureWetBulbPotential/testsFiles/"

class TestTemperatureWetBulbPotential(unittest.TestCase):

    def test_1(self):
        """Faire appel a TemperatureAlongPseudoadiabat avec --endLevel 1000mb et --increment 1mb et garderseulement le niveau a 1000mb pour le comparer avec TemperatureWetBulbPotential."""
        # open and read source
        source0 = plugin_test_dir + "2014031006_024_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureWetBulbPotential
        df = TemperatureWetBulbPotential(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 700] >> [TemperatureWetBulbPotential] >> [Select --fieldName TW] >> [Zap --fieldName TTPS] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "TTPS_1000mb_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Calcul TemperatureWetBulbPotential à partir d'un fichier hybrid."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute TemperatureWetBulbPotential
        df = TemperatureWetBulbPotential(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU --verticalLevel 1.0@0.2] >> [TemperatureWetBulbPotential --increment 20mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_reghyb_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
