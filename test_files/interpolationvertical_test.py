

# -*- coding: utf-8 -*-
import os
import sys


import unittest
import pytest


prefix = "/".join(os.getcwd().split("/")[0:-1])

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")

TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/" % HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/" % (HOST_NUM, USER)


plugin_test_dir = TEST_PATH + "InterpolationVertical/testsFiles/"


class TestInterpolationVertical(unittest.TestCase):

    def test_1(self):
        """Tester l'option --outputGridDefinitionMethod avec une valeur invalide _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical --outputGridDefinitionMethod DEFINED_SOMEHOW --interpolationType LINEAR --extrapolationType NEAREST ]

        # write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """Tester l'option --interpolationType avec une valeur invalide _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GRID --interpolationType INTERPOLATE_SOMEHOW --extrapolationType NEAREST ]

        # write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """Tester l'option --extrapolationType avec une valeur invalide _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GRID --interpolationType LINEAR --extrapolationType EXTRAPOLATE_SOMEHOW ]

        # write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """Tester l'option --outputGridDefinitionMethod FIELD_DEFINED sans l'option --referenceFieldName _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --interpolationType LINEAR --extrapolationType NEAREST ]

        # write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """Tester l'option --outputGridDefinitionMethod USER_DEFINED sans l'option --verticalLevel _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ]

        # write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """Tester l'option --verticalLevel avec des valeurs invalides _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 50,-20,100,A,200 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ]

        # write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_7(self):
        """Tester l'option --verticalLevel avec un intervalle sans --verticalLevelRangeIncrement. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100@200,300 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ]

        # write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_8(self):
        """Tester l'option --outputGridDefinitionMethod USER_DEFINED sans l'option --verticalLevelType _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100,200,300 --interpolationType LINEAR --extrapolationType NEAREST ]

        # write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_9(self):
        """Tester l'option --verticalLevelType avec une valeur invalide _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevelType SOME_VERTICALLEVELTYPE --verticalLevel 100,200,300 --interpolationType LINEAR --extrapolationType NEAREST ]

        # write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_10(self):
        """Tester l'option --referenceFieldName avec un champ qui n'est pas dans le fichier d'input. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GRID --interpolationType LINEAR --extrapolationType NEAREST ]

        # write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_11(self):
        """Tester l'option --referenceFieldName avec un champ sur plusieurs grilles. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_reghyb_pres_TTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # ([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT]) ) >> [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName TT --interpolationType LINEAR --extrapolationType NEAREST ]

        # write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_12(self):
        """ Interpolation vertical hybrid (reg) to millibars. _BETTER_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regpres_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # ([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) ) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "2014031800_024_regpres_hy_shortTTGZUUVV_NEXT_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_13(self):
        """ Interpolation vertical millibars (reg) to hybrid. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regpres_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_reghyb_pres_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # ([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) ) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "2014031800_024_reghyb_pres_shortTTGZUUVV_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_15(self):
        """ Interpolation vertical hybrid staggered (glb) to millibars. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbhyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical --verticalLevel 950,700,350,100,20 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST -m USER_DEFINED] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "2014031800_024_glbpres_hystag_shortTTGZUUVV_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_16(self):
        """ Interpolation vertical eta (glb) to hybrid staggered. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_glbhyb_eta_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # ([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> (([Select --fieldName TT] >> [Zap --fieldName GRID]) +([Select --fieldName UU] >> [Zap --fieldName GRDU]))) ) >> (([Select --fieldName TT,GZ,GRID] >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY]) + ([Select --fieldName UU,VV,GRDU] >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRDU -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY])) >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "2014031800_024_glbhyb_eta_shortTTGZUUVV_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_18(self):
        """ Interpolation vertical millibars (glb) to hybrid staggered. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbpres_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_glbhyb_pres_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # (([ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --noMetadata]) + ([ReaderStd --ignoreExtended --input {sources[1]}] >> (([Select --fieldName TT] >> [Zap --fieldName GRID]) +([Select --fieldName UU] >> [Zap --fieldName GRDU]))) ) >> (([Select --fieldName TT,GZ,GRID] >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY]) + ([Select --fieldName UU,VV,GRDU] >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRDU -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY])) >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "2014031800_024_glbhyb_pres_shortTTGZUUVV_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_20(self):
        """ Interpolation vertical hybrid (reg) to eta. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # ([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) ) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "2014031800_024_regeta_hy_shortTTGZUUVV_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_22(self):
        """ Interpolation vertical eta (reg) to millibars. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical --verticalLevel 950,700,350,100,20 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST -m USER_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "2014031800_024_regpres_eta_shortTTGZUUVV_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_24(self):
        """ Interpolation vertical millibars to meter sea level. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2011051818_000.UUVVTTGZ.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,GZ] >> [InterpolationVertical --verticalLevel 1000,2000,3000,4000,6000 --verticalLevelType METER_SEA_LEVEL --interpolationType LINEAR --extrapolationType NEAREST -m USER_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_24.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interpolationvertical_meter_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_25(self):
        """ Interpolation vertical hybrid to meter sea level. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2011070818_054_hyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName GZ,TT] >> [InterpolationVertical --verticalLevel 1000,2000,3000,4000,6000 --verticalLevelType METER_SEA_LEVEL --interpolationType LINEAR --extrapolationType FIXED --valueAbove 999.0 --valueBelow 999.0 -m USER_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_25.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "from_hybrid_to_meter_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_26(self):
        """ Teste l'option --verticalLevelType MILLIBARS_ABOVE_LEVEL sans l'option --referenceLevel. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical -m USER_DEFINED --verticalLevel 100 --verticalLevelType MILLIBARS_ABOVE_LEVEL ]

        # write the result
        results_file = TMP_PATH + "test_26.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_27(self):
        """ Teste l'option --verticalLevelType MILLIBARS_ABOVE_LEVEL sans l'option --referenceLevel. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical -m USER_DEFINED --verticalLevel 100 --verticalLevelType MILLIBARS_ABOVE_LEVEL ]

        # write the result
        results_file = TMP_PATH + "test_27.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_28(self):
        """ Interpolation vertical eta (glb) to millibars above ground. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Pressure --referenceField TT --coordinateType AUTODETECT] + [Select --fieldName GZ,TT,UU,VV]) >> [InterpolationVertical -m USER_DEFINED --verticalLevel 100 --verticalLevelType MILLIBARS_ABOVE_LEVEL --referenceLevel SURFACE ] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_28.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "from_to_eta_millibars_above_ground.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_29(self):
        """ Interpolation vertical with extrapolationType ABORT _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2011070818_054_hyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --fieldName GZ,TT] + [Pressure --referenceField TT --coordinateType AUTODETECT]) >> [InterpolationVertical -T 1 --verticalLevel 900,500,300,200,100 --verticalLevelType METER_SEA_LEVEL --interpolationType LINEAR --extrapolationType ABORT --valueAbove 999.0 --valueBelow 999.0 -m USER_DEFINED ]

        # write the result
        results_file = TMP_PATH + "test_29.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_30(self):
        """ Interpolation vertical with interpolationType NEAREST _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbhyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical -m USER_DEFINED --verticalLevel 1000,3000,6000 --verticalLevelType METER_GROUND_LEVEL --interpolationType NEAREST --extrapolationType NEAREST] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_30.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interpolationType_nearest_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_31(self):
        """ Interpolation vertical with interpolationLevelType METER_GROUND_LEVEL _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_glbhyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical -m USER_DEFINED --verticalLevel 1000,3000,6000 --verticalLevelType METER_GROUND_LEVEL --interpolationType LINEAR --extrapolationType NEAREST] >> [WriterStd --output {destination_path} --ignoreExtended]

        # write the result
        results_file = TMP_PATH + "test_31.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "verticalLevelType_meterGroundLevel_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_32(self):
        """Tester l'option --outputField avec une valeur invalide."""
        # open and read source
        source0 = plugin_test_dir + "inputFile.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GZ --outputField INCLUDE_SOMETHING --interpolationType LINEAR --extrapolationType NEAREST]

        # write the result
        results_file = TMP_PATH + "test_32.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_33(self):
        """ Interpolation vertical hybrid (reg) to eta --outputField INCLUDE_REFERENCE_FIELD. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # ([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID])) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --outputField INCLUDE_REFERENCE_FIELD --referenceFieldName GRID -m FIELD_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_33.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "includeReferenceField_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_34(self):
        """Interpolation vertical hybrid (reg) to eta --outputField INCLUDE_ALL_FIELDS. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # ([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName GZ] >> [Zap --fieldName OUT])) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --outputField INCLUDE_ALL_FIELDS --referenceFieldName GRID -m FIELD_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_34.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "includeAllFields_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_35(self):
        """Interpolation vertical hybrid (reg) to eta --outputField INTERPOLATED_FIELD_ONLY _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # ([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName GZ] >> [Zap --fieldName OUT])) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --outputField INTERPOLATED_FIELD_ONLY --referenceFieldName GRID -m FIELD_DEFINED ] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_35.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interpolatedFieldsOnly_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_36(self):
        """Interpolation vertical hybrid (reg) to eta avec le parametre --outputField INTERPOLATED_FIELD_ONLY _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # ([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName GZ] >> [Zap --fieldName OUT])) >> [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_36.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "interpolatedFieldsOnly_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_37(self):
        """Tester l'option --outputField INTERPOLATED_FIELD_ONLY avec pas de champs a interpole. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_pres_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >>[Select --fieldName TT,UU] >> [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName TT --interpolationType LINEAR --extrapolationType NEAREST --outputField INTERPOLATED_FIELD_ONLY]

        # write the result
        results_file = TMP_PATH + "test_37.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_38(self):
        """Tester l'option --outputField INCLUDE_REFERENCE_FIELD avec pas de champs a interpole. _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_reghyb_pres_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >>[Select --fieldName TT,UU] >> [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName TT --interpolationType LINEAR --extrapolationType NEAREST --outputField INCLUDE_REFERENCE_FIELD]

        # write the result
        results_file = TMP_PATH + "test_38.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_39(self):
        """Interpolation vertical with a file containing many forecast hours (ens glb). _OK_"""
        # open and read source
        source0 = plugin_test_dir + "2015081700_024_ensglb_shortTTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 10.0,100.0,400.0,700.0,850.0,925.0,1000.0 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_39.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + \
            "2015081700_024_ensglb_shortTTGZUUVV_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_40(self):
        """Interpolation vertical avec un fichier hybrid pour les champs QC et TD. _SIMILIAR_"""
        # open and read source
        source0 = plugin_test_dir + "2011070818_054_hyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName QC,TD] >> [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100,200,300,400,500,600,700,800,900,1000 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_40.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "2011070818_054_hyb_QCTT_NEXT_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_41(self):
        """Interpolation vertical pour tester les parametres_--valueAbove et --valueBelow"""
        # open and read source
        source0 = plugin_test_dir + "2014031800_024_regeta_TTGZUUVV.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 1,500,1100 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType FIXED --valueAbove 777.7 --valueBelow -777.7] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = TMP_PATH + "test_41.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "valueAboveBelow_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_41(self):
        """Interpolation vertical avec un fichier hybrid 5005 pour les champs QC et TD. _SIMILIAR_"""
        # open and read source
        source0 = plugin_test_dir + "coord_5005_big.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute InterpolationVertical
        df = InterpolationVertical(src_df0).compute()
        #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[Select --fieldName QC,TD] >> ', '[InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100,200,300,400,500,600,700,800,900,1000 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ] >> ', '[WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]']

        # write the result
        results_file = TMP_PATH + "test_41.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_41.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
