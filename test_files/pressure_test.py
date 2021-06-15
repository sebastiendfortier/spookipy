

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"Pressure/testsFiles/"

class TestPressure(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 : Test sur un fichier sortie de modele eta avec l'option --coordinateType ETA_COORDINATE. VCODE 1002"""
        # open and read source
        source0 = plugin_test_dir + "tt_eta_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >>[Pressure --coordinateType ETA_COORDINATE --referenceField TT] >>[Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_eta_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_2(self):
        """Test #2 : Test sur un fichier sortie de modele eta avec les options --coordinateType ETA_COORDINATE --standardAtmosphere."""
        # open and read source
        source0 = plugin_test_dir + "tt_eta_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_eta_std_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_3(self):
        """Test #3 : Test sur un fichier sortie de modele eta avec l'option --coordinateType AUTODETECT."""
        # open and read source
        source0 = plugin_test_dir + "tt_eta_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField TT] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_eta_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_4(self):
        """Test #4 : Test sur un fichier sortie de modele eta avec les options --coordinateType AUTODETECT --standardAtmosphere."""
        # open and read source
        source0 = plugin_test_dir + "tt_eta_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT ] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_eta_std_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_5(self):
        """Test #5 : Test sur un fichier sortie de modele Sigma, avec l'option --coordinateType SIGMA_COORDINATE. VCODE 1001"""
        # open and read source
        source0 = plugin_test_dir + "hu_sig_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType SIGMA_COORDINATE --referenceField HU ] >>[Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_sig_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6(self):
        """Test #6 : Test sur un fichier sortie de modele Sigma, avec les options --coordinateType SIGMA_COORDINATE --standardAtmosphere."""
        # open and read source
        source0 = plugin_test_dir + "hu_sig_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField HU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_sig_std_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_7(self):
        """Test #7 : Test sur un fichier sortie de modele Sigma, avec l'option --coordinateType AUTODETECT."""
        # open and read source
        source0 = plugin_test_dir + "hu_sig_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField HU] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_sig_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_8(self):
        """Test #8 : Test sur un fichier sortie de modele Sigma, avec les options --coordinateType AUTODETECT --standardAtmosphere."""
        # open and read source
        source0 = plugin_test_dir + "hu_sig_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField HU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_sig_std_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_9(self):
        """Test #9 : Test sur un fichier sortie de modele hybrid, avec l'option --coordinateType HYBRID_COORDINATE."""
        # open and read source
        source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[Pressure --coordinateType HYBRID_COORDINATE --referenceField TT] >>', '[Zap --pdsLabel R1580V0N] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_hyb_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_10(self):
        """Test #10 : Test sur un fichier sortie de modele Hybrid avec les options --coordinateType HYBRID_COORDINATE --standardAtmosphere."""
        # open and read source
        source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_hyb_std_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_11(self):
        """Test #11 : Test sur un fichier sortie de modele Hybrid, avec l'option --coordinateType AUTODETECT."""
        # open and read source
        source0 = plugin_test_dir + "input_hyb_2011100712_012.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_hyb2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_12(self):
        """Test #12 : Test sur un fichier sortie de modele Hybrid avec les options --coordinateType AUTODETECT --standardAtmosphere."""
        # open and read source
        source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_hyb_std_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_13(self):
        """Test #13 : Test sur un fichier sortie de modele Hybrid staggered, avec l'option --coordinateType HYBRID_STAGGERED_COORDINATE."""
        # open and read source
        source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --referenceField UU] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_hyb_stg_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_14(self):
        """Test #14 : Test sur un fichier sortie de modele Hybrid staggered, avec les options --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere."""
        # open and read source
        source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField UU] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_hyb_stg_std_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_15(self):
        """Test #15 : Test sur un fichier sortie de modele hybrid staggered, avec l'option --coordinateType AUTODETECT."""
        # open and read source
        source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField UU] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_hyb_stg_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_16(self):
        """Test #16 : Test sur un fichier sortie de modele Hybrid staggered, avec les options --coordinateType AUTODETECT --standardAtmosphere."""
        # open and read source
        source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField UU] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_hyb_stg_std_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_17(self):
        """Test #17 : Test sur un fichier sortie de modele en pression, avec l'option --coordinateType PRESSURE_COORDINATE."""
        # open and read source
        source0 = plugin_test_dir + "tt_pres_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType PRESSURE_COORDINATE --referenceField TT] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_17.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_pres_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_18(self):
        """Test #18 : Test sur un fichier sortie de modele en pression avec les options --coordinateType PRESSURE_COORDINATE --standardAtmosphere."""
        # open and read source
        source0 = plugin_test_dir + "tt_pres_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType PRESSURE_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_pres_std_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_19(self):
        """Test #19 : Test sur un fichier sortie de modele en pression l'option --coordinateType AUTODETECT."""
        # open and read source
        source0 = plugin_test_dir + "tt_pres_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --referenceField TT] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_19.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_pres_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_20(self):
        """Test #20 : Test sur un fichier sortie de modele en pression avec les options --coordinateType AUTODETECT --standardAtmosphere."""
        # open and read source
        source0 = plugin_test_dir + "tt_pres_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "px_pres_std_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_21(self):
        """Test #21 : Test avec -- coordinateType ETA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees ETA - Kind invalide."""
        # open and read source
        source0 = plugin_test_dir + "tt_pres_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_21.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_22(self):
        """Test #22 : Test avec l'option -- coordinateType ETA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees ETA - Champs PT et P0 sont absents."""
        # open and read source
        source0 = plugin_test_dir + "input_eta_2008061012_000_model_noPTnoP0.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_23(self):
        """Test #23 : Test avec -- coordinateType SIGMA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees SIGMA - Kind invalide."""
        # open and read source
        source0 = plugin_test_dir + "tt_pres_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_23.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_24(self):
        """Test #24 : Test avec l'option -- coordinateType SIGMA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees SIGMA - Champ P0 est absent."""
        # open and read source
        source0 = plugin_test_dir + "hu_sig_noP0_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField HU] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_24.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_25(self):
        """Test #25 : Test avec l'option -- coordinateType HYBRID_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID - Kind invalide."""
        # open and read source
        source0 = plugin_test_dir + "tt_pres_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_25.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_26(self):
        """Test #26 : Test avec l'option -- coordinateType HYBRID_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID - Champs P0 et HY sont absents."""
        # open and read source
        source0 = plugin_test_dir + "tt_hyb_noP0noHYnoBB_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_26.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_27(self):
        """Test #27 : Test avec l'option -- coordinateType HYBRID_STAGGERED_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID STAGGERED - Kind invalide."""
        # open and read source
        source0 = plugin_test_dir + "tt_pres_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_27.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_28(self):
        """Test #28 : Test avec l'option -- coordinateType HYBRID_STAGGERED_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID STAGGERED- Champs P0 et HY sont absents."""
        # open and read source
        source0 = plugin_test_dir + "tt_hyb_noP0noHYnoBB_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_28.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_29(self):
        """Test #29 : Test avec l'option -- coordinateType PRESSURE_COORDINATE alors que le fichier d'entree n'est pas en pression."""
        # open and read source
        source0 = plugin_test_dir + "tt_eta_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType PRESSURE_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_29.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_30(self):
        """Test #30 : Test avec un fichier contenant differentes heures de prevision."""
        # open and read source
        source0 = plugin_test_dir + "input_vrpcp24_00_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noMetadata]

        #write the result
        results_file = TMP_PATH + "test_30.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "input_vrpcp24_00_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_31(self):
        """Test #31 : Test avec un fichier contenant differentes heures de prevision."""
        # open and read source
        source0 = plugin_test_dir + "input_test_31.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[Select --exclude --fieldName PX] >> ', '[Pressure --coordinateType AUTODETECT --referenceField TT] >>', '[Zap --pdsLabel EH02558_X --metadataZappable --doNotFlagAsZapped]>>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended ]']

        #write the result
        results_file = TMP_PATH + "test_31.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_31_TT.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_32(self):
        """Test #32 : Test avec un fichier glbpres avec l'option --coordinateType HYBRID_STAGGERED_COORDINATE"""
        # open and read source
        source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --referenceField TT] >>[WriterStd --output {destination_path} --ignoreExtended ]

        #write the result
        results_file = TMP_PATH + "test_32.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "glbpres_hybrid_staggered_coordinate_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_33(self):
        """Test #33 : Test avec un fichier glbpres avec l'option --coordinateType PRESSURE_COORDINATE"""
        # open and read source
        source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType PRESSURE_COORDINATE --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended ]

        #write the result
        results_file = TMP_PATH + "test_33.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "glbpres_pressure_coordinate_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_34(self):
        """Test #34 : Test avec un fichier qui genere des artefacts dans les cartes"""
        # open and read source
        source0 = plugin_test_dir + "2019091000_000_input.orig"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType ETA_COORDINATE --referenceField TT] >> [Zap --pdsLabel G1_7_0_0N --nbitsForDataStorage e32]>>[WriterStd --output {destination_path} --ignoreExtended --noMetadata --IP1EncodingStyle OLDSTYLE]

        #write the result
        results_file = TMP_PATH + "test_34.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "d.compute_pressure_varicelle_rslt.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_35(self):
        """Test #35 : Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE thermodynamic"""
        # open and read source
        source0 = plugin_test_dir + "coord_5005_big.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]} ]>> ', '[Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField TT] >>', '[Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_35.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_35_TT.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_36(self):
        """Test #36 : Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE momentum"""
        # open and read source
        source0 = plugin_test_dir + "coord_5005_big.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]} ]>> ', '[Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField UU] >> ', '[Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_36.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_36_UU.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_37(self):
        """Test #37 : Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE thermo sub grid - attendu fail"""
        # open and read source
        source0 = plugin_test_dir + "coord_5005_big.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute Pressure
        df = Pressure(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]} ]>> ', '[Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField CK] >> ', '[Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_37.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


