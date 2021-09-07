

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"LevelOfCondensationByLifting/testsFiles/"

class TestLevelOfCondensationByLifting(unittest.TestCase):

    def test_1(self):
        """ Calcul du niveau de condensation par ascendance(LCL); utilisation de --outputField avec une valeur invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #[ReaderStd --input {sources[0]} ] >> [LevelOfCondensationByLifting --outputField INVALID_VALUE --liftedFrom SURFACE --iceWaterPhase WATER ]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """ Calcul du niveau de condensation par ascendance(LCL); utilisation de --iceWaterPhase avec une valeur invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [LevelOfCondensationByLifting --outputField TEMPERATURE --liftedFrom SURFACE --iceWaterPhase ICE ]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """ Calcul du niveau de condensation par ascendance(LCL); utilisation de --iceWaterPhase avec une valeur invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [LevelOfCondensationByLifting --outputField TEMPERATURE --liftedFrom INVALID_VALUE --iceWaterPhase WATER ]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """ Calcul du niveau de condensation par ascendance(LCL); utilisation de --iceWaterPhase BOTH mais sans --temperaturePhaseSwitch."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [LevelOfCondensationByLifting --outputField TEMPERATURE --liftedFrom SURFACE --iceWaterPhase BOTH ]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """ Calcul du niveau de condensation par ascendance(LCL); utilisation de --liftedFrom USER_DEFINED mais sans --verticalLevel."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [LevelOfCondensationByLifting --outputField TEMPERATURE --liftedFrom USER_DEFINED --iceWaterPhase WATER ]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """ Calcul du LCL; utilisation de --liftedFrom SURFACE avec un fichier en pression.  Requete invalide car le fichier ne suit pas la topographie."""
        # open and read source
        source0 = plugin_test_dir + "2013022712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [LevelOfCondensationByLifting --outputField HEIGHT --liftedFrom SURFACE --iceWaterPhase WATER ]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """ Calcul du LCL; utilisation d'une mauvaise combinaison de parametres."""
        # open and read source
        source0 = plugin_test_dir + "2013022712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [LevelOfCondensationByLifting --outputField HEIGHT --liftedFrom SURFACE --verticalLevel 0.995 --iceWaterPhase WATER ]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """ Calcul du LCL - 3 champs de sortie (TLCL, PLCL et ZLCL); utilisation de --liftedFrom SURFACE."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [LevelOfCondensationByLifting --outputField TEMPERATURE,PRESSURE,HEIGHT --liftedFrom SURFACE --iceWaterPhase WATER ] >> [Select --fieldName TLCL,PLCL,ZLCL --noMetadata ] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_sfc_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """ Calcul du LCL - 3 champs de sortie (TLCL, PLCL et ZLCL); utilisation de --liftedFrom SURFACE."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [LevelOfCondensationByLifting --outputField TEMPERATURE,PRESSURE,HEIGHT --liftedFrom USER_DEFINED --verticalLevel 0.995 --iceWaterPhase WATER ] >> [Select --fieldName TLCL,PLCL,ZLCL --noMetadata ] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_niv995_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_10(self):
        """ Calcul du LCL - 3 champs de sortie (TLCL, PLCL et ZLCL); utilisation de --liftedFrom MEAN_LAYER."""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [LevelOfCondensationByLifting --outputField TEMPERATURE,PRESSURE,HEIGHT --liftedFrom MEAN_LAYER --baseMeanLayer SURFACE --deltaMeanLayer 200mb --iceWaterPhase WATER ] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011100712_ML_newPdsLabel_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_12(self):
        """ Calcul du LCL - 3 champs de sortie (TLCL, PLCL et ZLCL); utilisation de --liftedFrom USER_DEFINED."""
        # open and read source
        source0 = plugin_test_dir + "2015051400_012_press_gzg_2.fst"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [LevelOfCondensationByLifting -o TEMPERATURE,PRESSURE,HEIGHT --liftedFrom USER_DEFINED --verticalLevel ALL --iceWaterPhase WATER] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2015051400_012_press_gzg_most_unstable_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_13(self):
        """ Calcul du LCL - 3 champs de sortie (TLCL, PLCL et ZLCL); utilisation de --liftedFrom USER_DEFINED. fichier 5005"""
        # open and read source
        source0 = plugin_test_dir + "minimal_TTHUGZ_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute LevelOfCondensationByLifting
        df = LevelOfCondensationByLifting(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[LevelOfCondensationByLifting -o TEMPERATURE,PRESSURE,HEIGHT --liftedFrom USER_DEFINED --verticalLevel ALL --iceWaterPhase WATER] >> ', '[Zap --nbitsForDataStorage E32] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_13.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
