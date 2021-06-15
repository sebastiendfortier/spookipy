

# -*- coding: utf-8 -*-
import os, sys



import unittest, pytest


prefix="/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)


plugin_test_dir=TEST_PATH +"InterpolationVertical/testsFiles/"

class TestInterpolationVertical(unittest.TestCase):

    def test_regtest_1(self):
        """Test #1 : Tester l'option --outputGridDefinitionMethod avec une valeur invalide _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical --outputGridDefinitionMethod DEFINED_SOMEHOW --interpolationType LINEAR --extrapolationType NEAREST ]

        #write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_2(self):
        """Test #2 : Tester l'option --interpolationType avec une valeur invalide _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GRID --interpolationType INTERPOLATE_SOMEHOW --extrapolationType NEAREST ]

        #write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_3(self):
        """Test #3 : Tester l'option --extrapolationType avec une valeur invalide _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GRID --interpolationType LINEAR --extrapolationType EXTRAPOLATE_SOMEHOW ]

        #write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_4(self):
        """Test #4 : Tester l'option --outputGridDefinitionMethod FIELD_DEFINED sans l'option --referenceFieldName _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --interpolationType LINEAR --extrapolationType NEAREST ]

        #write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_5(self):
        """Test #5 : Tester l'option --outputGridDefinitionMethod USER_DEFINED sans l'option --verticalLevel _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ]

        #write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_6(self):
        """Test #6 : Tester l'option --verticalLevel avec des valeurs invalides _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 50,-20,100,A,200 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ]

        #write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_7(self):
        """Test #7 : Tester l'option --verticalLevel avec un intervalle sans --verticalLevelRangeIncrement. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100@200,300 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ]

        #write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_8(self):
        """Test #8 : Tester l'option --outputGridDefinitionMethod USER_DEFINED sans l'option --verticalLevelType _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100,200,300 --interpolationType LINEAR --extrapolationType NEAREST ]

        #write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_9(self):
        """Test #9 : Tester l'option --verticalLevelType avec une valeur invalide _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevelType SOME_VERTICALLEVELTYPE --verticalLevel 100,200,300 --interpolationType LINEAR --extrapolationType NEAREST ]

        #write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_10(self):
        """Test #10 : Tester l'option --referenceFieldName avec un champ qui n'est pas dans le fichier d'input. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GRID --interpolationType LINEAR --extrapolationType NEAREST ]

        #write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_11(self):
        """Test #11 : Tester l'option --referenceFieldName avec un champ sur plusieurs grilles. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_reghyb_pres_TTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT]) ) >> [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName TT --interpolationType LINEAR --extrapolationType NEAREST ]

        #write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_12(self):
        """Test #12 :  Interpolation vertical hybrid (reg) to millibars. _BETTER_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regpres_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) ) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2014031800_024_regpres_hy_shortTTGZUUVV_NEXT_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_13(self):
        """Test #13 :  Interpolation vertical millibars (reg) to hybrid. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regpres_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_reghyb_pres_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) ) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2014031800_024_reghyb_pres_shortTTGZUUVV_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_15(self):
        """Test #15 :  Interpolation vertical hybrid staggered (glb) to millibars. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbhyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical --verticalLevel 950,700,350,100,20 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST -m USER_DEFINED] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2014031800_024_glbpres_hystag_shortTTGZUUVV_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_16(self):
        """Test #16 :  Interpolation vertical eta (glb) to hybrid staggered. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_glbhyb_eta_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> (([Select --fieldName TT] >> [Zap --fieldName GRID]) +([Select --fieldName UU] >> [Zap --fieldName GRDU]))) ) >> (([Select --fieldName TT,GZ,GRID] >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY]) + ([Select --fieldName UU,VV,GRDU] >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRDU -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY])) >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2014031800_024_glbhyb_eta_shortTTGZUUVV_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_18(self):
        """Test #18 :  Interpolation vertical millibars (glb) to hybrid staggered. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbpres_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_glbhyb_pres_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #(([ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --noMetadata]) + ([ReaderStd --ignoreExtended --input {sources[1]}] >> (([Select --fieldName TT] >> [Zap --fieldName GRID]) +([Select --fieldName UU] >> [Zap --fieldName GRDU]))) ) >> (([Select --fieldName TT,GZ,GRID] >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY]) + ([Select --fieldName UU,VV,GRDU] >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRDU -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY])) >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2014031800_024_glbhyb_pres_shortTTGZUUVV_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_20(self):
        """Test #20 :  Interpolation vertical hybrid (reg) to eta. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) ) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_22(self):
        """Test #22 :  Interpolation vertical eta (reg) to millibars. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical --verticalLevel 950,700,350,100,20 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST -m USER_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2014031800_024_regpres_eta_shortTTGZUUVV_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_24(self):
        """Test #24 :  Interpolation vertical millibars to meter sea level. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2011051818_000.UUVVTTGZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,GZ] >> [InterpolationVertical --verticalLevel 1000,2000,3000,4000,6000 --verticalLevelType METER_SEA_LEVEL --interpolationType LINEAR --extrapolationType NEAREST -m USER_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_24.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interpolationvertical_meter_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_25(self):
        """Test #25 :  Interpolation vertical hybrid to meter sea level. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2011070818_054_hyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName GZ,TT] >> [InterpolationVertical --verticalLevel 1000,2000,3000,4000,6000 --verticalLevelType METER_SEA_LEVEL --interpolationType LINEAR --extrapolationType FIXED --valueAbove 999.0 --valueBelow 999.0 -m USER_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_25.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "from_hybrid_to_meter_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_26(self):
        """Test #26 :  Teste l'option --verticalLevelType MILLIBARS_ABOVE_LEVEL sans l'option --referenceLevel. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical -m USER_DEFINED --verticalLevel 100 --verticalLevelType MILLIBARS_ABOVE_LEVEL ]

        #write the result
        results_file = TMP_PATH + "test_26.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_27(self):
        """Test #27 :  Teste l'option --verticalLevelType MILLIBARS_ABOVE_LEVEL sans l'option --referenceLevel. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical -m USER_DEFINED --verticalLevel 100 --verticalLevelType MILLIBARS_ABOVE_LEVEL ]

        #write the result
        results_file = TMP_PATH + "test_27.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_28(self):
        """Test #28 :  Interpolation vertical eta (glb) to millibars above ground. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> ([Pressure --referenceField TT --coordinateType AUTODETECT] + [Select --fieldName GZ,TT,UU,VV]) >> [InterpolationVertical -m USER_DEFINED --verticalLevel 100 --verticalLevelType MILLIBARS_ABOVE_LEVEL --referenceLevel SURFACE ] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_28.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "from_to_eta_millibars_above_ground.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_29(self):
        """Test #29 :  Interpolation vertical with extrapolationType ABORT _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2011070818_054_hyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --fieldName GZ,TT] + [Pressure --referenceField TT --coordinateType AUTODETECT]) >> [InterpolationVertical -T 1 --verticalLevel 900,500,300,200,100 --verticalLevelType METER_SEA_LEVEL --interpolationType LINEAR --extrapolationType ABORT --valueAbove 999.0 --valueBelow 999.0 -m USER_DEFINED ]

        #write the result
        results_file = TMP_PATH + "test_29.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_30(self):
        """Test #30 :  Interpolation vertical with interpolationType NEAREST _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbhyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical -m USER_DEFINED --verticalLevel 1000,3000,6000 --verticalLevelType METER_GROUND_LEVEL --interpolationType NEAREST --extrapolationType NEAREST] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_30.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interpolationType_nearest_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_31(self):
        """Test #31 :  Interpolation vertical with interpolationLevelType METER_GROUND_LEVEL _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbhyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical -m USER_DEFINED --verticalLevel 1000,3000,6000 --verticalLevelType METER_GROUND_LEVEL --interpolationType LINEAR --extrapolationType NEAREST] >> [WriterStd --output {destination_path} --ignoreExtended]

        #write the result
        results_file = TMP_PATH + "test_31.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "verticalLevelType_meterGroundLevel_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_32(self):
        """Test #32 : Tester l'option --outputField avec une valeur invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GZ --outputField INCLUDE_SOMETHING --interpolationType LINEAR --extrapolationType NEAREST]

        #write the result
        results_file = TMP_PATH + "test_32.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_33(self):
        """Test #33 :  Interpolation vertical hybrid (reg) to eta --outputField INCLUDE_REFERENCE_FIELD. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID])) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --outputField INCLUDE_REFERENCE_FIELD --referenceFieldName GRID -m FIELD_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_33.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "includeReferenceField_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_34(self):
        """Test #34 : Interpolation vertical hybrid (reg) to eta --outputField INCLUDE_ALL_FIELDS. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName GZ] >> [Zap --fieldName OUT])) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --outputField INCLUDE_ALL_FIELDS --referenceFieldName GRID -m FIELD_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_34.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "includeAllFields_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_35(self):
        """Test #35 : Interpolation vertical hybrid (reg) to eta --outputField INTERPOLATED_FIELD_ONLY _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName GZ] >> [Zap --fieldName OUT])) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --outputField INTERPOLATED_FIELD_ONLY --referenceFieldName GRID -m FIELD_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_35.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interpolatedFieldsOnly_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_36(self):
        """Test #36 : Interpolation vertical hybrid (reg) to eta avec le parametre --outputField INTERPOLATED_FIELD_ONLY _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName GZ] >> [Zap --fieldName OUT])) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_36.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interpolatedFieldsOnly_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_37(self):
        """Test #37 : Tester l'option --outputField INTERPOLATED_FIELD_ONLY avec pas de champs a interpole. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_pres_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >>[Select --fieldName TT,UU] >> [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName TT --interpolationType LINEAR --extrapolationType NEAREST --outputField INTERPOLATED_FIELD_ONLY]

        #write the result
        results_file = TMP_PATH + "test_37.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_38(self):
        """Test #38 : Tester l'option --outputField INCLUDE_REFERENCE_FIELD avec pas de champs a interpole. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_pres_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >>[Select --fieldName TT,UU] >> [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName TT --interpolationType LINEAR --extrapolationType NEAREST --outputField INCLUDE_REFERENCE_FIELD]

        #write the result
        results_file = TMP_PATH + "test_38.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == False)


    def test_regtest_39(self):
        """Test #39 : Interpolation vertical with a file containing many forecast hours (ens glb). _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2015081700_024_ensglb_shortTTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 10.0,100.0,400.0,700.0,850.0,925.0,1000.0 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_39.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2015081700_024_ensglb_shortTTGZUUVV_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_40(self):
        """Test #40 : Interpolation vertical avec un fichier hybrid pour les champs QC et TD. _SIMILIAR_"""
        # open and read source
        source0 = plugin_test_dir + "2011070818_054_hyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName QC,TD] >> [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100,200,300,400,500,600,700,800,900,1000 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        #write the result
        results_file = TMP_PATH + "test_40.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011070818_054_hyb_QCTT_NEXT_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_41(self):
        """Test #41 : Interpolation vertical pour tester les parametres_--valueAbove et --valueBelow"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 1,500,1100 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType FIXED --valueAbove 777.7 --valueBelow -777.7] >> [WriterStd --output {destination_path} ]

        #write the result
        results_file = TMP_PATH + "test_41.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "valueAboveBelow_file2cmp.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


    def test_regtest_41(self):
        """Test #41 : Interpolation vertical avec un fichier hybrid 5005 pour les champs QC et TD. _SIMILIAR_"""
        # open and read source
        source0 = plugin_test_dir + "coord_5005_big.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()


        #compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[Select --fieldName QC,TD] >> ', '[InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100,200,300,400,500,600,700,800,900,1000 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ] >> ', '[WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]']

        #write the result
        results_file = TMP_PATH + "test_41.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_41.std"

        #compare results
        res = fstcomp(results_file,file_to_compare)
        assert(res == True)


