

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"PrecipitationTypeDominant/testsFiles/"

class TestPrecipitationTypeDominant(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 : Tester le plugin avec un epsilon invalide """
        # open and read source
        source0 = plugin_test_dir + "PetitFichier.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [PrecipitationTypeDominant --microphysics BOURGOUIN --epsilon -10.0] 

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_2(self):
        """Test #2 : Tester le plugin avec un precipThreshold invalide """
        # open and read source
        source0 = plugin_test_dir + "PetitFichier.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [PrecipitationTypeDominant --microphysics BOURGOUIN --precipThreshold -9.0] 

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_3(self):
        """Test #3 : Tester le plugin avec le cas de base BOURGOUIN"""
        # open and read source
        source0 = plugin_test_dir + "accums.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalDifference --fieldName RN,SN,FR,PE --rangeForecastHour 0@48,0@48 --interval 12,24 --step 12,24 --strictlyPositive] >> [PrecipitationTypeDominant --microphysics BOURGOUIN --epsilon 0.0] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_BOURGOUIN_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_4(self):
        """Test #4 : Tester le plugin avec le cas de base MY2"""
        # open and read source
        source0 = plugin_test_dir + "accums.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalDifference --fieldName RN,SN,FR,PE,RN1,FR1,SN1,SN3 --rangeForecastHour 0@48,0@48 --interval 12,24 --step 12,24 --strictlyPositive] >> [PrecipitationTypeDominant --microphysics MY2 --epsilon 0.0] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_MY2P3_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_5(self):
        """Test #5 : Tester le plugin avec le cas de base P3"""
        # open and read source
        source0 = plugin_test_dir + "accums.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalDifference --fieldName RN,SN,FR,PE,RN1,FR1,SN1,SN3 --rangeForecastHour 0@48,0@48 --interval 12,24 --step 12,24 --strictlyPositive] >> [PrecipitationTypeDominant --microphysics P3 --epsilon 0.0] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_MY2P3_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_6(self):
        """Test #6 : Tester le plugin avec le cas de base CUSTOM"""
        # open and read source
        source0 = plugin_test_dir + "customAccums.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[TimeIntervalDifference --fieldName RN2,RN1,FR2,FR1,PE1,SN3,SG,SN1,SN2,PE2 --rangeForecastHour 0@48,0@48 --interval 12,24 --step 12,24 --strictlyPositive] >> ', '[PrecipitationTypeDominant --microphysics CUSTOM --rain RN2 --drizzle RN1 --freezingRain FR2 --freezingDrizzle FR1 --icePellets PE1 --graupel SN3 --snowGrain SG --iceCrystals SN1 --snow SN2 --hail PE2 --epsilon 0.0] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_6.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_7(self):
        """Test #7 : Tester le plugin avec le cas 3 champs CUSTOM"""
        # open and read source
        source0 = plugin_test_dir + "customAccums.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[TimeIntervalDifference --fieldName RN2,FR2,FR1 --rangeForecastHour 0@48,0@48 --interval 12,24 --step 12,24 --strictlyPositive] >> ', '[PrecipitationTypeDominant --microphysics CUSTOM --rain RN2 --freezingRain FR2 --freezingDrizzle FR1 --epsilon 0.0] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_custom_RN2FR2FR1_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_8(self):
        """Test #8 : Tester le plugin avec le cas de base BOURGOUIN precipAmountPreCalcule"""
        # open and read source
        source0 = plugin_test_dir + "accumIntervals.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [PrecipitationTypeDominant --microphysics BOURGOUIN --epsilon 0.0] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_BOURGOUIN_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_9(self):
        """Test #9 : Tester le plugin avec le cas 4 champs CUSTOM"""
        # open and read source
        source0 = plugin_test_dir + "accums.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalDifference --fieldName RN1,FR,FR1,SN --rangeForecastHour 0@48,0@48 --interval 12,24 --step 12,24 --strictlyPositive] >> [PrecipitationTypeDominant --microphysics CUSTOM --rain RN1 --freezingRain FR --freezingDrizzle FR1 --snow SN] >> [Zap --nbitsForDataStorage E32] >>[WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_9_14_07_2020.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_10(self):
        """Test #10 : Tester le plugin avec le cas 4 champs CUSTOM et option de nbits npak E32"""
        # open and read source
        source0 = plugin_test_dir + "accumsNbits.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalDifference --fieldName RN1,FR,FR1,SN --rangeForecastHour 0@48,0@48 --interval 12,24 --step 12,24 --strictlyPositive] >> [PrecipitationTypeDominant --microphysics CUSTOM --rain RN1 --freezingRain FR --freezingDrizzle FR1 --snow SN] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_custom_RN1FRFR1SNE32_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_11(self):
        """Test #11 : Tester le plugin avec le cas 4 champs CUSTOM et option de nbits npak e32"""
        # open and read source
        source0 = plugin_test_dir + "accumsNbits2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [TimeIntervalDifference --fieldName RN1,FR,FR1,SN --rangeForecastHour 0@48,0@48 --interval 12,24 --step 12,24 --strictlyPositive] >> [PrecipitationTypeDominant --microphysics CUSTOM --rain RN1 --freezingRain FR --freezingDrizzle FR1 --snow SN] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "result_custom_RN1FRFR1SNe32_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_12(self):
        """Test #12: Tester le plugin avec champs CUSTOM egalite des champs RN==RN1, ordre"""
        # open and read source
        source0 = plugin_test_dir + "intervals_cp.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[PrecipitationTypeDominant --microphysics CUSTOM --epsilon 1e-12 --precipThreshold 1e-7 --snow RN1 --graupel RN] >> ', '[WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --noMetadata]']

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_12.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_13(self):
        """Test #13: Tester le plugin avec champs MY2 egalite des champs RN=RN1, ordre"""
        # open and read source
        source0 = plugin_test_dir + "intervals_cp2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[PrecipitationTypeDominant --microphysics MY2 --epsilon 1e-12 --precipThreshold 1e-7] >> ', '[WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --noMetadata]']

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_13.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_14(self):
        """Test #14: Tester le plugin avec champs CUSTOM egalite des champs RN=RN1, ordre"""
        # open and read source
        source0 = plugin_test_dir + "intervals_cp3.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[PrecipitationTypeDominant --microphysics CUSTOM --epsilon 1e-12 --precipThreshold 1e-7 --rain RN --drizzle RN1] >> ', '[WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --noMetadata]']

        #write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_14.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_15(self):
        """Test #15: Tester le plugin avec champs CUSTOM egalite des champs, difference en un point"""
        # open and read source
        source0 = plugin_test_dir + "intervals_cp4.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >>', '[PrecipitationTypeDominant --microphysics CUSTOM --epsilon 1e-12 --precipThreshold 1e-7 --rain RN --freezingRain FR --icePellets PE --snow SN --freezingDrizzle FR1 --drizzle RN1 --iceCrystals SN1 --graupel SN3] >> ', '[WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --noMetadata]']

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_15.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_16(self):
        """Test #16: Tester le plugin avec champs CUSTOM egalite des champs, difference en un point"""
        # open and read source
        source0 = plugin_test_dir + "intervals_cp5.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >>', '[PrecipitationTypeDominant --microphysics CUSTOM --epsilon 1e-12 --precipThreshold 1e-7 --rain PE --freezingRain SN --icePellets FR --snow RN1 --freezingDrizzle SN1 --drizzle FR1 --iceCrystals SN3 --graupel RN] >> ', '[WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --noMetadata]']

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_16.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_17(self):
        """Test #17: Tester le plugin avec champs CUSTOM egalite des champs, difference en un point"""
        # open and read source
        source0 = plugin_test_dir + "intervals_cp6.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >>', '[PrecipitationTypeDominant --microphysics CUSTOM --epsilon 1e-12 --precipThreshold 1e-7 --rain SN3 --freezingRain PE --icePellets RN --snow FR --freezingDrizzle RN1 --drizzle SN --iceCrystals FR1 --graupel SN1] >> ', '[WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --noMetadata]']

        #write the result
        results_file = TMP_PATH + "test_17.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_17.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_18(self):
        """Test #18: Tester le plugin avec champs BOURGOUIN egalite des champs, difference en un point"""
        # open and read source
        source0 = plugin_test_dir + "intervals_cp7.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute PrecipitationTypeDominant
        df = PrecipitationTypeDominant(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >>', '[PrecipitationTypeDominant --microphysics BOURGOUIN --epsilon 1e-12 --precipThreshold 1e-7] >> ', '[WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --noMetadata]']

        #write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_18.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


