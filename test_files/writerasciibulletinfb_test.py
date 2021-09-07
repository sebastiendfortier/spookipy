

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"WriterAsciiBulletinFB/testsFiles/"

class TestWriterAsciiBulletinFB(unittest.TestCase):

    def test_1(self):
        """Tester l'option --outputPath avec un path qui n'existe pas!"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /tmp//totoeUTH4R]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_2(self):
        """Tester l'option --outputPath avec un path qui existe mais qui est un nom de fichier!"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /tmp//totogRD7c2/bidon]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_pathExisteMaisPasLesPermissions(self):
        """Tester l'option --outputPath avec un path existant qui est un répertoire mais dont on n'a pas les permissions!"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2011072100_006_pres_small"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /media]

        #write the result
        results_file = TMP_PATH + "test_pathExisteMaisPasLesPermissions.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_invalidRunHour(self):
        """Tester le plugin avec une heure de run invalide!"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [Zap --dateOfOrigin 20110215163210] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /media]

        #write the result
        results_file = TMP_PATH + "test_invalidRunHour.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_invalidUnitTT(self):
        """Tester le plugin avec TT qui n'a pas les bonnes unités!"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> ([Select --fieldName UV,WD,GZ,TerrainElevation,StationAlphaId,FictiveStationFlag] + ([Select --fieldName TT] >> [UnitConvert --unit kelvin])) >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_invalidUnitTT2aThUd]

        #write the result
        results_file = TMP_PATH + "test_invalidUnitTT.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_invalidUnitUV(self):
        """Tester le plugin avec UV qui n'a pas les bons unités!"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> ([Select --fieldName TT,WD,GZ,TerrainElevation,StationAlphaId,FictiveStationFlag] + ([Select --fieldName UV] >> [UnitConvert --unit kilometer_per_hour])) >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_invalidUnitUVc0rc0i]

        #write the result
        results_file = TMP_PATH + "test_invalidUnitUV.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_invalidUnitGZ(self):
        """Tester le plugin avec GZ qui n'a pas les bons unités!"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> ([Select --fieldName TT,UV,WD,TerrainElevation,StationAlphaId,FictiveStationFlag] + ([Select --fieldName GZ] >> [UnitConvert --unit meter])) >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_invalidUnitGZCC9Nax]

        #write the result
        results_file = TMP_PATH + "test_invalidUnitGZ.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_invalidUnitTerrainElevation(self):
        """Tester le plugin avec TerrainElevation qui n'a pas les bonnes unités!"""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> ([Select --fieldName TT,UV,WD,GZ,StationAlphaId,FictiveStationFlag] + ([Select --fieldName TerrainElevation] >> [UnitConvert --unit kilometer])) >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_invalidUnitTerrainElevationQWZwVU]

        #write the result
        results_file = TMP_PATH + "test_invalidUnitTerrainElevation.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB000061(self):
        """Produit le bulletin FBCN31_000 a comparer avec tely_fd_reg_r100_FDCN01 et ne produit aucun backup (message d'avertissement)."""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB000061cMjYgs]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB000061.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB00012(self):
        """Produit le bulletin FBCN33_000 a comparer avec tely_fd_reg_r100_FDCN02, produit le backup à 6 heure et avertit que le backup 12 n'est pas produit."""
        # open and read source
        source0 = plugin_test_dir + "2011072100_012_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB00012sCXhE8]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB00012.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB00018(self):
        """Donne aucun bulletin (avertir qu'aucun bulletin est produit), produit les backups à 6 et 12 heures. Le backup à 12 sera comparé avec tely_fd_012_backup_FDCN01."""
        # open and read source
        source0 = plugin_test_dir + "2011072100_018_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB00018GoBUe0]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB00018.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB00024(self):
        """Produit le bulletin FBCN35_000 a comparer avec tely_fd_reg_r100_FDCN03, produit le backup 12 qui sera comparé avec tely_fd_012_backup_FDCN01 et avertit que le backup à 6 n'est pas produit."""
        # open and read source
        source0 = plugin_test_dir + "2011072100_024_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2011072100_024_pres_small"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB00024shFkM3]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB00024.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB00030(self):
        """Avertit qu'aucun bulletin n'est produit, produit le backup à 6 et avertit que le backup à 12 n'est pas produit."""
        # open and read source
        source0 = plugin_test_dir + "2011072100_030_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB00030k2Qcin]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB00030.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB00036(self):
        """Avertit qu'aucun bulletin n'est produit, produit le backup à 12 qui sera comparé avec tely_fd_012_backup_FDCN03 et avertit que le backup à 6 n'est pas produit."""
        # open and read source
        source0 = plugin_test_dir + "2011072100_036_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB00036yVsDwS]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB00036.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB00048(self):
        """Avertit qu'aucun bulletin ni backup sont produits."""
        # open and read source
        source0 = plugin_test_dir + "2011072100_048_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB00048y43hiy]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB00048.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB12006(self):
        """"""
        # open and read source
        source0 = plugin_test_dir + "2011072112_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB12006imaQxV]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB12006.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB12012(self):
        """"""
        # open and read source
        source0 = plugin_test_dir + "2011072112_012_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB12012YgcZUW]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB12012.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB12018(self):
        """"""
        # open and read source
        source0 = plugin_test_dir + "2011072112_018_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB12018woJSQ9]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB12018.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB12024(self):
        """"""
        # open and read source
        source0 = plugin_test_dir + "2011072112_024_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB12024yi0cOy]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB12024.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB12030(self):
        """"""
        # open and read source
        source0 = plugin_test_dir + "2011072112_030_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB12030OZ7ZN9]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB12030.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB12036(self):
        """"""
        # open and read source
        source0 = plugin_test_dir + "2011072112_036_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB12036i0hpNW]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB12036.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB12048(self):
        """"""
        # open and read source
        source0 = plugin_test_dir + "2011072112_048_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB12048m0ZlWU]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB12048.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinGlobal(self):
        """À l'aide du dictionnaire FD, produit un bulletin FBCN33_012 et un backup FBCN31_012_backup06 à partir du global eta. Permet de tester la station YJA"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_glbeta"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation --useOriginalFDDictionary] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinGlobal8xjOng]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinGlobal.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFB000061b(self):
        """Produit(sans les champs pressions) le bulletin FBCN31_000 a comparer avec tely_fd_reg_r100_FDCN01 et produit aucun backup (message d'avertissement)."""
        # open and read source
        source0 = plugin_test_dir + "2011072100_006_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --verticalLevel 0.384@1.0] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFB000061bYkCU7F]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFB000061b.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFBDate(self):
        """Test avec une date de fin de mois pour s'assurer que les entetes sont corrects"""
        # open and read source
        source0 = plugin_test_dir + "20150228_018_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFBDateMmwGLh]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFBDate.std"
        StandardFileWriter(results_file, df)()

        assert(res)


    def test_WriterAsciiBulletinFBDate2(self):
        """Test avec une date de fin de mois (annee bisextile) pour s'assurer que les entetes sont corrects"""
        # open and read source
        source0 = plugin_test_dir + "20160228_024_eta_small"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute WriterAsciiBulletinFB
        df = WriterAsciiBulletinFB(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [BulletinFBPreparation] >> [WriterAsciiBulletinFB --backupHour 6,12 --outputPath /home/spst900/spooki/spooki_tmpdir_ppp4/phc001/test_WriterAsciiBulletinFBDate20cpk05]

        #write the result
        results_file = TMP_PATH + "test_WriterAsciiBulletinFBDate2.std"
        StandardFileWriter(results_file, df)()

        assert(res)
