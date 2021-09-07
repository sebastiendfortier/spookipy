

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"ParcelMeanLayer/testsFiles/"

class TestParcelMeanLayer(unittest.TestCase):

    def test_1(self):
        """Appel à ParcelMeanLayer, unites absentes pour --base."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regpres_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ParcelMeanLayer --base 800 --delta 100mb --iceWaterPhase WATER]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Appel à ParcelMeanLayer, unites invalides pour --delta."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regpres_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ParcelMeanLayer --base 800mb --delta 100m --iceWaterPhase WATER]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Appel à ParcelMeanLayer, parametre --temperaturePhaseSwitch absent alors que --iceWaterPhase est BOTH."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regpres_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ParcelMeanLayer --base 900mb --delta 100mb --iceWaterPhase BOTH ]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Mauvaise utilisation du parametre --temperaturePhaseSwitch alors que --iceWaterPhase est WATER."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regpres_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ParcelMeanLayer --base 900mb --delta 100mb --iceWaterPhase WATER --temperaturePhaseSwitch 20.0C]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """Valeurs de parametres invalides, --delta est plus grand que --base."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regpres_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ParcelMeanLayer --base 400mb --delta 1000mb --iceWaterPhase WATER]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """ Calcul de la parcelle Mean Layer, donnees manquantes car il n'y a pas de donnees pour interpoler sur les niveaux de debut et de fin de la couche."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ParcelMeanLayer --base 962mb --delta 100mb --iceWaterPhase WATER]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """ Utilisation du parametre --base SURFACE avec un fichier en pression."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regpres_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ParcelMeanLayer --base SURFACE --delta 100mb --iceWaterPhase WATER]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """ Calcul de la parcelle Mean Layer à partir d'un fichier pression + GZ surface d'un fichier hybrid."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regpres_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_reghyb_small.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #([ReaderStd --input {sources[0]}] + ([ReaderStd --input {sources[1]}] >> [Select --fieldName GZ --verticalLevel SURFACE])) >> [ParcelMeanLayer --base 1000mb --delta 400mb --iceWaterPhase WATER] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test8_newPdsLabel_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """ Appel a ParcelMean Layer avec un fichier pression + GZ surface d'un fichier hybrid, valeurs de debut et de fin de la couche doivent etre interpolees."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regpres_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_reghyb_small.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #([ReaderStd --input {sources[0]}] + ([ReaderStd --input {sources[1]}] >> [Select --fieldName GZ --verticalLevel SURFACE])) >> [ParcelMeanLayer --base 990mb --delta 100mb --iceWaterPhase WATER] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test9_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_10(self):
        """Calcul de la parcelle Mean Layer avec un fichier pression, donnees manquantes car il n'y a pas de donnees pour interpoler sur les niveaux de debut et de fin de la couche."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regpres_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_reghyb_small.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #([ReaderStd --input {sources[0]}] + ([ReaderStd --input {sources[1]}] >> [Select --fieldName GZ --verticalLevel SURFACE])) >> [ParcelMeanLayer --base 1020mb --delta 800mb --iceWaterPhase WATER]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_11(self):
        """ Calcul de la parcelle Mean Layer à partir d'un fichier hybrid, utilisation du parametre --base SURFACE."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ParcelMeanLayer --base SURFACE --delta 200mb --iceWaterPhase WATER] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test11_newPdsLabel_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_12(self):
        """ Calcul de la parcelle Mean Layer à partir d'un fichier hybrid."""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_small.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ParcelMeanLayer --base 820mb --delta 100mb --iceWaterPhase WATER] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "test12_newPdsLabel_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_13(self):
        """ Calcul de la parcelle Mean Layer à partir d'un fichier hybrid, utilisation du parametre --base SURFACE."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ParcelMeanLayer --base SURFACE --delta 100mb --iceWaterPhase WATER] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_reghyb_newPdsLabel_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_14(self):
        """ Calcul de la parcelle Mean Layer à partir d'un fichier hybrid 5005, utilisation du parametre --base 610mb."""
        # open and read source
        source0 = plugin_test_dir + "minimal_4conve_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #['[ReaderStd --input {sources[0]} ] >> ', '[ParcelMeanLayer --base 610mb --delta 100mb --iceWaterPhase WATER] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_14.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_15(self):
        """ Calcul de la parcelle Mean Layer à partir d'un fichier hybrid 5005, utilisation du parametre --base SURFACE."""
        # open and read source
        source0 = plugin_test_dir + "minimal_TTHUGZ_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ParcelMeanLayer
        df = ParcelMeanLayer(src_df0).compute()
        #['[ReaderStd --input {sources[0]} ] >> ', '[ParcelMeanLayer --base SURFACE --delta 100mb --iceWaterPhase WATER] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_15.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
