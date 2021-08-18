

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"PrecipitableWaterAmount/testsFiles/"

class TestPrecipitableWaterAmount(unittest.TestCase):

    def test_1(self):
        """Test #1 : Test avec un fichier en pression, utilisation de --base SURFACE. Requete invalide."""
        # open and read source
        source0 = plugin_test_dir + "HU_PX_a_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base SURFACE --top HIGHEST]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_2(self):
        """Test #2 : Test avec un fichier simple de 3x3x3, mélange d'unités longueur et pression. Requete invalide."""
        # open and read source
        source0 = plugin_test_dir + "HU_PX_a_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >>[PrecipitableWaterAmount --base 2ft --top 100mb]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_3(self):
        """Test #3 : Test avec un fichier reduit de données, avec --base SURFACE et --top HIGHEST, cas 2-7-9"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >>[PrecipitableWaterAmount --base SURFACE --top HIGHEST] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_3_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_4(self):
        """Test #4 : Test avec un fichier reduit de données, calcul de HU, avec --base SURFACE et --top HIGHEST, cas 2-7-9"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,TD,PX] >>[PrecipitableWaterAmount --base SURFACE --top HIGHEST] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_4_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5(self):
        """Test #5 : Test avec un fichier reduit de données, valeurs en hPa pour base et top, cas 1-5-7-9"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 964.381hPa --top 10hPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_5_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_5a(self):
        """Test #5a : Test avec un fichier reduit de données, valeurs en metres pour base et top, cas 6"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 2m --top 10m] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_5a.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_5a_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_6(self):
        """Test #6 : Test avec un fichier reduit de données, valeurs en hPa pour base et top, cas 5-8"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 965.381hPa --top 954.779hPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_6_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_7(self):
        """Test #7 : Test avec un fichier reduit de données en pression, base et top en hPa, cas 4"""
        # open and read source
        source0 = plugin_test_dir + "regpres_2019100506_012.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 900hPa --top 875hPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_7_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_8(self):
        """Test #8 : Test avec un fichier reduit de données en pression, base et top en mb, cas 1 et 3"""
        # open and read source
        source0 = plugin_test_dir + "regpres_2019100506_012.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 900mb --top 880hPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_8_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_9(self):
        """Test #9 : Test avec un fichier reduit de données en pression, base et top cas 2 et 8"""
        # open and read source
        source0 = plugin_test_dir + "regpres_2019100506_012.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 900hPa --top 860hPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_9_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_10(self):
        """Test #10 : Test avec un fichier reduit de données en pression, cas 5, 7 et 9"""
        # open and read source
        source0 = plugin_test_dir + "regpres_2019100506_012.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 880hPa --top 800hPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_10_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_11(self):
        """Test #11 : Test avec un fichier reduit de données en pression, cas 1 et 10"""
        # open and read source
        source0 = plugin_test_dir + "regpres_2019100506_012.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 885hPa --top 875hPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_11_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_13(self):
        """Test #13 : Test avec un fichier reduit de données, valeurs en hPa pour base et top, cas 5 et 8"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 872.571hPa --top 853.04hPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_13_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_13a(self):
        """Test #13a : Test avec un vrai fichier de données, base et top conversion mb a hPa, cas 5 et 8"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 872.571mb --top 853.04mb] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_13a.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_13_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_14(self):
        """Test #14 : Test avec un vrai fichier de données, base et top conversion Pa a hPa"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 87257.1Pa --top 85304Pa] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_14_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_14a(self):
        """Test #14a : Test avec un vrai fichier de données, base et top conversion kPa a hPa"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 87.2571kPa --top 85.304kPa] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_14a.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_14_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_15(self):
        """Test #15 : Test avec un vrai fichier de données, toute la colonne, parametres explicites"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base SURFACE --top HIGHEST] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_15_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_16(self):
        """Test #16 : Test avec un vrai fichier de données, definition du sommet en pascal"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base SURFACE --top 96906Pa] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_16_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_16a(self):
        """Test #16a : Test avec un vrai fichier de données, definition du sommet en metres"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base SURFACE --top 10m] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_16a.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_16a_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_17(self):
        """Test #17 : Test avec un vrai fichier de données, parametres mixtes, definition de la base"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 969hPa --top HIGHEST] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_17.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_17_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_17a(self):
        """Test #17a : Test avec un vrai fichier de données, definition de la base en metres"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 2m --top HIGHEST] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_17a.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_17a_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_18(self):
        """Test #18 : Test avec un vrai fichier de données, definition du sommet en km"""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_regeta_1"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base SURFACE --top 4km] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_18_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_19(self):
        """Test #19 : Test avec un vrai fichier de données, parametres mixtes, definition de la base en pieds"""
        # open and read source
        source0 = plugin_test_dir + "input_point61-51.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 6.56ft --top HIGHEST] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_19.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_17a_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_20(self):
        """Test #20 : Test avec un vrai fichier de données,  definition du sommet en pieds."""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_regeta_1"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base SURFACE --top 13123.3ft] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_18_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_21(self):
        """Test #21 : Test avec un vrai fichier de données hybrid."""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_reghyb_2pts"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base SURFACE --top HIGHEST] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_21.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_21_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_22(self):
        """Test #22 : Test avec un vrai fichier de données hybrid."""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_reghyb_2pts"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base 900mb --top HIGHEST] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_22_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)


    def test_23(self):
        """Test #23 : Test avec un vrai fichier de données hybrid."""
        # open and read source
        source0 = plugin_test_dir + "2016031600_024_reghyb_2pts"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitableWaterAmount
        df = PrecipitableWaterAmount(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [PrecipitableWaterAmount --base SURFACE --top 4km] >>[WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_23.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EP_test_23_v2.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res)
