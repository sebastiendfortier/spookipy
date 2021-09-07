

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"ConvectiveEnergies/testsFiles/"

class TestConvectiveEnergies(unittest.TestCase):

    def test_1(self):
        """ Utilisation du parametre --liftedFrom SURFACE avec un fichier en pression. Requete invalide"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --virtualTemperature NO --increment 2.0mb ]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """ Utilisation du parametre --liftedFrom MEAN_LAYER --baseMeanLayer SURFACE avec un fichier en pression. Requete invalide"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom MEAN_LAYER --baseMeanLayer SURFACE --deltaMeanLayer 200mb --virtualTemperature NO --increment 2.0mb]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """ Utilisation du parametre --liftedFrom MOST_UNSTABLE avec un fichier en pression. Requete invalide"""
        # open and read source
        source0 = plugin_test_dir + "2011100712_012_regpres"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom MOST_UNSTABLE --deltaMostUnstable 200mb --virtualTemperature NO --increment 2.0mb]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """ Calcul des niveaux de convection a partir d'un fichier lam national de 2 points, SURFACE."""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 1.0hPa --virtualTemperature NO ] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion ]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "point61-51_v2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """ Calcul a partir d'un fichier de 2 points, liftedFrom SURFACE et outputConvectiveLevels."""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 1.0hPa --virtualTemperature NO --outputConvectiveLevels LFC_PRESSURE,LFC_HEIGHT,EL_PRESSURE,EL_HEIGHT ] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "point61-51_optLevels_v2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """ Calcul a partir d'un fichier de 2 points, liftedFrom MEAN_LAYER et outputConvectiveLevels."""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom MEAN_LAYER --baseMeanLayer 800mb --deltaMeanLayer 500mb --increment 1.0hPa --virtualTemperature NO --outputConvectiveLevels LFC_PRESSURE,LFC_HEIGHT,EL_PRESSURE,EL_HEIGHT ] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "point61-51_optLevelsML_v2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """ Calcul a partir d'un fichier de 2 points, liftedFrom MOST_UNSTABLE et outputConvectiveLevels."""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom MOST_UNSTABLE --deltaMostUnstable 500mb --increment 1.0hPa --virtualTemperature YES --outputConvectiveLevels LFC_PRESSURE,EL_PRESSURE ] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "point61-51_optLevelsMU2_v2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_10(self):
        """ Calcul a partir d'un fichier de 3 points, SURFACE et OPTIMAL_VALUE_ONLY."""
        # open and read source
        source0 = plugin_test_dir + "Fichier3Pts_2017092900.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 10.0hPa --virtualTemperature NO ] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CroisementCasA_test10_v2py_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_11(self):
        """ Calcul des niveaux de convection a partir d'un fichier de 6 points, SURFACE et OPTIMAL_VALUE_ONLY."""
        # open and read source
        source0 = plugin_test_dir + "2018052906_lam_nat_CroisementCas2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 2.0hPa --virtualTemperature NO ] >> [WriterStd --output {destination_path} --ignoreExtended ]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CroisementsTest11_v2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_12(self):
        """ Calcul a partir d'un fichier de 6 points, SURFACE et OPTIMAL_VALUE_ONLY."""
        # open and read source
        source0 = plugin_test_dir + "2017092900_000_CroisementCas3.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 5.0hPa --virtualTemperature NO ] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CroisementCas3_v2py_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_13(self):
        """ Calcul a partir d'un fichier de 6 points, SURFACE et OPTIMAL_VALUE_ONLY, avec correction de temperature."""
        # open and read source
        source0 = plugin_test_dir + "2018060606_lam_nat_CroisementCas3.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 5.0hPa --virtualTemperature YES --outputConvectiveLevels LFC_PRESSURE,LFC_HEIGHT,EL_PRESSURE,EL_HEIGHT ] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CroisementCas3_VT_v2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_14(self):
        """ Calcul a partir d'un fichier de 18 points, SURFACE."""
        # open and read source
        source0 = plugin_test_dir + "input_convection_CroisementCas4.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 2.0hPa --virtualTemperature NO --outputConvectiveLevels LFC_PRESSURE,LFC_HEIGHT,EL_PRESSURE,EL_HEIGHT ] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CroisementCas4_v2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_15(self):
        """ Utilisation du parametre --capeType UNBOUNDED avec des bornes. Requete invalide"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --virtualTemperature NO --increment 10.0mb --capeType UNBOUNDED --lowerBoundary 0km --upperBoundary 10km ]

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_16(self):
        """ Calcul a partir d'un fichier de 2 points, liftedFrom SURFACE et outputConvectiveLevels."""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 1.0hPa --virtualTemperature NO --outputConvectiveLevels LFC_PRESSURE,LFC_HEIGHT,EL_PRESSURE,EL_HEIGHT --capeType UNBOUNDED ] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "point61-51_optLevels_v2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_17(self):
        """ Test avec cle pour tenir compte du LCL et calcul de l'energie bornee (Cas A,B,C,D et F)."""
        # open and read source
        source0 = plugin_test_dir + "2017092900_000_reduit_pourCasABCDF.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 10.0hPa --virtualTemperature NO --capeType BOTH --lowerBoundary 20dam --upperBoundary 35dam ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_17.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CasMultiples_test17_v2py_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_18(self):
        """ Test avec cle pour tenir compte du LCL et calcul de l'energie bornee (Cas A,B,C,D et F)."""
        # open and read source
        source0 = plugin_test_dir + "2017092900_000_nrj"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 10.0hPa --virtualTemperature NO --capeType BOUNDED --lowerBoundary -60C --upperBoundary -152C ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CasMultiples_test18_v2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_19(self):
        """ Calcul de l'energie bornee avec l'option  --liftedFrom MEAN_LAYER; la borne inferieure est sous le niveau de depart de la parcelle, donc CAPE indefini."""
        # open and read source
        source0 = plugin_test_dir + "2018092112_008_reduit"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom MEAN_LAYER --baseMeanLayer 800mb --deltaMeanLayer 500mb --increment 2.0hPa --virtualTemperature NO --capeType BOTH --lowerBoundary 400dam --upperBoundary 800dam ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_19.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CE_test19_v3_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_20(self):
        """ Calcul de l'energie bornee avec l'option  --liftedFrom MEAN_LAYER."""
        # open and read source
        source0 = plugin_test_dir + "2018092112_008_reduit"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom MEAN_LAYER --baseMeanLayer 800mb --deltaMeanLayer 500mb --increment 2.0hPa --virtualTemperature NO --capeType BOTH --lowerBoundary 560dam --upperBoundary 800dam ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CE_test20_v3_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_21(self):
        """ Calcul de l'energie bornee avec l'option  --liftedFrom MOST_UNSTABLE; la borne inferieure est sous le niveau de depart de la parcelle, donc CAPE indefini."""
        # open and read source
        source0 = plugin_test_dir + "2018092112_008_reduit"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom MOST_UNSTABLE --deltaMostUnstable 500mb --increment 2.0hPa --virtualTemperature NO --capeType BOTH --lowerBoundary 50dam --upperBoundary 800dam ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_21.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CE_test21_v3_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_22(self):
        """ Calcul de l'energie bornee avec l'option  --liftedFrom MOST_UNSTABLE."""
        # open and read source
        source0 = plugin_test_dir + "2018092112_008_reduit"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom MOST_UNSTABLE --deltaMostUnstable 500mb --increment 2.0hPa --virtualTemperature NO --capeType BOTH --lowerBoundary 100dam --upperBoundary 800dam ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CE_test22_v3_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_23(self):
        """ Calcul de l'energie bornee avec l'option  --liftedFrom SURFACE; la borne inferieure est au-dessus de la valeur de la 1er temperature."""
        # open and read source
        source0 = plugin_test_dir + "2017092900_000_nrj_reduit"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 10.0hPa --virtualTemperature NO --capeType BOTH --lowerBoundary 6C --upperBoundary -152C ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_23.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CE_test23_v2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_24(self):
        """ Calcul de l'energie bornee avec l'option  --liftedFrom SURFACE; les bornes sont trouvees au milieu des temperatures."""
        # open and read source
        source0 = plugin_test_dir + "2017092900_000_nrj_reduit"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 10.0hPa --virtualTemperature NO --capeType BOUNDED --lowerBoundary -10C --upperBoundary -21C ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_24.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CE_test24_v2_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_25(self):
        """ Calcul de l'energie bornee avec l'option  --liftedFrom SURFACE; on ne trouve pas de valeurs pour la borne inferieure, CAPE indefini."""
        # open and read source
        source0 = plugin_test_dir + "2017092900_000_nrj_reduit2"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 10.0hPa --virtualTemperature NO --capeType BOUNDED --lowerBoundary 15C --upperBoundary -152C ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_25.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CE_test25_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_26(self):
        """ Calcul de l'energie bornee avec l'option  --liftedFrom SURFACE;on frole la valeur de borne inferieure sans jamais l'atteindre, donc CAPE indefini."""
        # open and read source
        source0 = plugin_test_dir + "2017092900_000_nrj_reduit2"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [ConvectiveEnergies --liftedFrom SURFACE --increment 10.0hPa --virtualTemperature NO --capeType BOUNDED --lowerBoundary -28C --upperBoundary -152C ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 ]

        #write the result
        results_file = TMP_PATH + "test_26.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "CE_test26_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_27(self):
        """ Calcul des niveaux de convection a partir d'un fichier 5005, SURFACE et OPTIMAL_VALUE_ONLY."""
        # open and read source
        source0 = plugin_test_dir + "minimal_4conve_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute ConvectiveEnergies
        df = ConvectiveEnergies(src_df0).compute()
        #['[ReaderStd --input {sources[0]} ] >> ', '[ConvectiveEnergies --liftedFrom SURFACE --increment 2.0hPa --virtualTemperature NO] >> ', '[WriterStd --output {destination_path} --ignoreExtended ]']

        #write the result
        results_file = TMP_PATH + "test_27.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_27.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
