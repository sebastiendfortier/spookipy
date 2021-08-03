

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"BulletinFBPreparation/testsFiles/"

class TestBulletinFBPreparation(unittest.TestCase):

    def test_1(self):
        """Test #1 : Produit(sans les champs pressions) les informations du bulletin FBCN31_000 à partir d'un fichier eta minimal"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute BulletinFBPreparation
        df = BulletinFBPreparation(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [BulletinFBPreparation] >> [Zap --metadataZappable --dateOfOrigin 20110303T183200 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --noUnitConversion --truncateFieldName --IP1EncodingStyle OLDSTYLE --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "BulletinFBPreparation_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_2(self):
        """Test #2 : Produit les informations du bulletin FBCN31_000 à partir d'un fichier eta complet"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regeta"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute BulletinFBPreparation
        df = BulletinFBPreparation(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [BulletinFBPreparation] >> [Zap --metadataZappable --dateOfOrigin 20110303T183200 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --noUnitConversion --truncateFieldName --IP1EncodingStyle OLDSTYLE --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_regeta_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_3(self):
        """Test #3 : Produit les informations du bulletin FBCN31_000 à partir d'un fichier hybrid complet"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute BulletinFBPreparation
        df = BulletinFBPreparation(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [BulletinFBPreparation] >> [Zap --metadataZappable --dateOfOrigin 20110303T183200 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --noUnitConversion --truncateFieldName --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_reghyb_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_4(self):
        """Test #4 : Produit les informations du bulletin FBCN31_000 à partir d'un fichier hybrid complet et utilise runID et implementation."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute BulletinFBPreparation
        df = BulletinFBPreparation(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [BulletinFBPreparation] >> [Zap --metadataZappable --dateOfOrigin 20110303T183200 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --noUnitConversion --truncateFieldName --makeIP1EncodingWorkWithTests]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_012_reghyb_R9OPERATIONAL_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


