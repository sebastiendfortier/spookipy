

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


plugin_test_dir = TEST_PATH + "EnergyMeanIsothermMethod/testsFiles/"


class TestEnergyMeanIsothermMethod(unittest.TestCase):

    def test_1(self):
        """  Test with maxNbLayer = -1, it should stop because of invalid value."""
        # open and read source
        source0 = plugin_test_dir + "inputFileTests.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --doNotFlagAsZapped]) ) >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature CF --maxNbLayer 0]

        # write the result
        results_file = TMP_PATH + "test_1.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_2(self):
        """  Test with epsilonTemperature = -1, it should stop because of invalid value."""
        # open and read source
        source0 = plugin_test_dir + "inputFileTests.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature CF --epsilonTemperature -1 ]

        # write the result
        results_file = TMP_PATH + "test_2.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_3(self):
        """  Test with epsilonPressure = -1, it should stop because of invalid value."""
        # open and read source
        source0 = plugin_test_dir + "inputFileTests.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) ) >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature CF --epsilonPressure -1]

        # write the result
        results_file = TMP_PATH + "test_3.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "nan"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_4(self):
        """ Test avec un fichier maison de 10 cas, champs APX et NBVS non disponibles en input,  sans option."""
        # open and read source
        source0 = plugin_test_dir + "inputFileTests.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --doNotFlagAsZapped]) + [Pressure --coordinateType AUTODETECT --referenceField TT] ) >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature CF] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = TMP_PATH + "test_4.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EnergyMeanIsoMethod_noOptions_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_5(self):
        """ Test avec un fichier maison de 10 cas, champs APX et NBVS non disponibles en input, avec l'option --maxNbLayer 2"""
        # open and read source
        source0 = plugin_test_dir + "inputFileTests.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --doNotFlagAsZapped]) + [Pressure --coordinateType AUTODETECT --referenceField TT]) >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature CF --maxNbLayer 2 ] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = TMP_PATH + "test_5.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EnergyMeanIsoMethod_maxNb2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_6(self):
        """ Test avec un fichier maison de 10 cas, champs APX et NBVS disponibles en input,  sans option."""
        # open and read source
        source0 = plugin_test_dir + "inputFileTests.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --doNotFlagAsZapped]) + [Pressure --coordinateType AUTODETECT --referenceField TT] ) >> ( [Copy] + [VerticalScan --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonValueOrField 0 --outputVerticalRepresentation PRESSURE --epsilon 0.1e-05 --comparisonType CONSTANTVALUE] ) >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature CF ] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = TMP_PATH + "test_6.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EnergyMeanIsoMethod_noOptions_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_7(self):
        """ Test avec un fichier maison de 10 cas, champs APX et NBVS en input, avec l'option --maxNbLayer 2"""
        # open and read source
        source0 = plugin_test_dir + "inputFileTests.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --doNotFlagAsZapped]) + [Pressure --coordinateType AUTODETECT --referenceField TT] ) >> ( [Copy] + [VerticalScan --maxNbOccurrence 10 --consecutiveEvents INF --referenceField TT --comparisonValueOrField 0 --outputVerticalRepresentation PRESSURE --epsilon 0.1e-05 --comparisonType CONSTANTVALUE] ) >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature CF --maxNbLayer 2 ] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = TMP_PATH + "test_7.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "EnergyMeanIsoMethod_maxNb2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_8(self):
        """ Test avec un fichier maison de 10 cas, champs APX et NBVS disponibles en input (NBVS=1),  sans option."""
        # open and read source
        source0 = plugin_test_dir + "inputFileTests.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --doNotFlagAsZapped]) + [Pressure --coordinateType AUTODETECT --referenceField TT] ) >> ( [Copy] + [VerticalScan --maxNbOccurrence 1 --consecutiveEvents INF --referenceField TT --comparisonValueOrField 0 --outputVerticalRepresentation PRESSURE --epsilon 0.1e-05 --comparisonType CONSTANTVALUE] ) >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature CF ] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = TMP_PATH + "test_8.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_NBVSenInput_noOption_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_9(self):
        """ Test avec un fichier maison de 10 cas, champs APX et NBVS disponibles en input (NBVS=1), .--maxNbLayer 2"""
        # open and read source
        source0 = plugin_test_dir + "inputFileTests.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --doNotFlagAsZapped]) + [Pressure --coordinateType AUTODETECT --referenceField TT] ) >> ( [Copy] + [VerticalScan --maxNbOccurrence 1 --consecutiveEvents INF --referenceField TT --comparisonValueOrField 0 --outputVerticalRepresentation PRESSURE --epsilon 0.1e-05 --comparisonType CONSTANTVALUE] ) >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature CF --maxNbLayer 2] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

        # write the result
        results_file = TMP_PATH + "test_9.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_NBVSenInput_maxNb2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_10(self):
        """ Test avec un fichier reel, nombre de couches inferieur a ce qui est demande, epsilons passes en parametres."""
        # open and read source
        source0 = plugin_test_dir + "2013042906_048_reghyb"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> ( [Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF --unit scalar --doNotFlagAsZapped]) + [Pressure --coordinateType AUTODETECT --referenceField TT] ) >> ( [Copy] + [VerticalScan --maxNbOccurrence 2 --consecutiveEvents INF --referenceField TT --comparisonValueOrField 0 --outputVerticalRepresentation PRESSURE --epsilon 0.1e-05 --comparisonType CONSTANTVALUE] ) >>[EnergyMeanIsothermMethod --temperature TT --comparisonTemperature CF --maxNbLayer 8 --epsilonTemperature 0.000001 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = TMP_PATH + "test_10.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test10_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_11(self):
        """ Test avec 2 points d'un fichier du lam_nat, avec la cle pour tenir compte du LCL."""
        # open and read source
        source0 = plugin_test_dir + "lam_nat_2017042506_040_2pts"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "lam_nat_2017042506_040_LCL_2pts"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> ([Select --fieldName TT,GZ] + [TemperatureOfLiftedParcel --liftedFrom SURFACE --endLevel 100.0hPa --increment 10.0hPa]) >> ([Select --fieldName TT,GZ] + ([Select --fieldName TT,PX --pdsLabel TemperatureOfLiftedParcel --exclude] >> [InterpolationVertical -m FIELD_DEFINED --outputField INCLUDE_ALL_FIELDS --extrapolationType FIXED --valueAbove -300 --valueBelow -300 --referenceFieldName TTLP])) >>([Select --fieldName TTLP,TT] + [VerticalScan -r TTLP -t INTERSECTIONS -c TT -o PRESSURE -e INF -m 10 --epsilon 0.0 --crossover --valueToIgnore -300]) >>(([Select --verticalLevelType MILLIBARS] + [Select --fieldName APX]) + [ReaderStd --input {sources[1]}])>> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --valueToIgnore -300] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --ignoreExtended --noMetadata ]

        # write the result
        results_file = TMP_PATH + "test_11.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test11_v2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_12(self):
        """ Test avec 2 points d'un fichier du lam_nat, cle pour tenir compte du LCL. Cas ou un LCL coupe la couche positive."""
        # open and read source
        source0 = plugin_test_dir + "lam_nat_coupe_cas1a"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "lam_nat_coupe_cas1a_LCL"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]} {sources[1]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --ignoreExtended --noMetadata ]

        # write the result
        results_file = TMP_PATH + "test_12.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test12_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_13(self):
        """ Test avec 2 points d'un fichier du lam_nat, cle pour tenir compte du LCL. Aucun croisement."""
        # open and read source
        source0 = plugin_test_dir + "lam_nat_coupe_cas4"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "lam_nat_coupe_cas4_LCL"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]} {sources[1]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --ignoreExtended --noMetadata ]

        # write the result
        results_file = TMP_PATH + "test_13.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test13_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_14(self):
        """ Test avec 3 points d'un fichier du lam_nat, cle pour tenir compte du LCL. Avec croisements."""
        # open and read source
        source0 = plugin_test_dir + "Fichier3Pts_LCL.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "Fichier3Pts_TTinterpoles.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --fieldName PX,PLCL,ZLCL,TLCL] + [ReaderStd --input {sources[1]}] >> [Select --fieldName TT,TTLP,PLCL,TLCL] >>[EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --valueToIgnore -300] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} ]

        # write the result
        results_file = TMP_PATH + "test_14.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test14_V2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_15(self):
        """ Test avec cle pour tenir compte du LCL et calcul de l'energie bornee (Cas A,B,C,D et F)."""
        # open and read source
        source0 = plugin_test_dir + "FichierNRJ_CasABCDF.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOTH --lowerBoundary 20dam --upperBoundary 35dam --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_15.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test15_v2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_16(self):
        """ Test avec cle pour tenir compte du LCL et calcul de l'energie bornee (Cas E)."""
        # open and read source
        source0 = plugin_test_dir + "FichierNRJ_CasE.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOTH --lowerBoundary 0dam --upperBoundary 30dam --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_16.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test16_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_17(self):
        """ Test avec cle pour tenir compte du LCL et calcul de l'energie bornee (Cas E)."""
        # open and read source
        source0 = plugin_test_dir + "FichierNRJ_CasE.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOTH --lowerBoundary 22dam --upperBoundary 25dam --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_17.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test17_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_18(self):
        """ Test avec cle pour tenir compte du LCL et calcul de l'energie bornee (Cas G)."""
        # open and read source
        source0 = plugin_test_dir + "FichierNRJ_CasG.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOTH --lowerBoundary 5dam --upperBoundary 75dam --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_18.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test18_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_19(self):
        """ Test avec cle pour tenir compte du LCL et calcul de l'energie bornee (Cas I)."""
        # open and read source
        source0 = plugin_test_dir + "FichierNRJ_CasI.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOTH --lowerBoundary 22dam --upperBoundary 26dam --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_19.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test19_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_20(self):
        """ Test avec cle pour tenir compte du LCL et calcul de l'energie bornee (Cas I) avec --capeType BOUNDED."""
        # open and read source
        source0 = plugin_test_dir + "FichierNRJ_CasI.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOUNDED --lowerBoundary 22dam --upperBoundary 26dam --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_20.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test20_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_21(self):
        """ Test avec cle pour tenir compte du LCL et calcul de l'energie bornee (Cas I) avec --capeType UNBOUNDED."""
        # open and read source
        source0 = plugin_test_dir + "FichierNRJ_CasI.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType UNBOUNDED --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_21.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test21_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_22(self):
        """ Calcul de l'energie bornee avec des bornes qui englobent tous les niveaux."""
        # open and read source
        source0 = plugin_test_dir + "FichierNRJ_CasABCDF.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOTH --lowerBoundary 10C --upperBoundary -100C --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_22.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test22_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_23(self):
        """ Calcul de l'energie bornee avec des bornes qui n'englobent pas tous les niveaux."""
        # open and read source
        source0 = plugin_test_dir + "FichierNRJ_CasABCDF.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOUNDED --lowerBoundary 0.5C --upperBoundary -30C --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_23.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test23_v2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_24(self):
        """ Calcul de l'energie bornee avec des bornes dont les valeurs arrivent sur un niveau de  pression."""
        # open and read source
        source0 = plugin_test_dir + "FichierNRJ_CasABCDF.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOUNDED --lowerBoundary 1.6686C --upperBoundary -52.9392C --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_24.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test24_v2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_25(self):
        """ Calcul de l'energie bornee avec des bornes qui ne concordent pas avec aucun niveau de pression."""
        # open and read source
        source0 = plugin_test_dir + "FichierNRJ_CasABCDF.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOUNDED --lowerBoundary -60C --upperBoundary -152C --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_25.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test25_v2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_26(self):
        """ Calcul de l'energie bornee avec option MEAN_LAYER."""
        # open and read source
        source0 = plugin_test_dir + "SortieLFCEL_MEANLAYER_inc2mb_v2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature MTLP --forConvectiveEnergies --capeType BOTH --lowerBoundary 560dam --upperBoundary 800dam --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_26.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test26_v2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_27(self):
        """ Calcul de l'energie bornee avec option MEAN_LAYER; la borne inferieure est sous le niveau de depart de la parcelle, donc CAPE indefini."""
        # open and read source
        source0 = plugin_test_dir + "SortieLFCEL_MEANLAYER_inc2mb_v2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature MTLP --forConvectiveEnergies --capeType BOTH --lowerBoundary 400dam --upperBoundary 800dam --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_27.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test27_v2_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_28(self):
        """ Calcul de l'energie bornee avec option MOST_UNSTABLE."""
        # open and read source
        source0 = plugin_test_dir + "SortieLFCEL_MOSTUNSTABLE_inc2mb.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature UTLP --forConvectiveEnergies --capeType BOTH --lowerBoundary 100dam --upperBoundary 800dam --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_28.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test28_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_29(self):
        """ Calcul de l'energie bornee avec option MOST_UNSTABLE; la borne inferieure est sous le niveau de depart de la parcelle, donc CAPE indefini."""
        # open and read source
        source0 = plugin_test_dir + "SortieLFCEL_MOSTUNSTABLE_inc2mb.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature UTLP --forConvectiveEnergies --capeType BOTH --lowerBoundary 50dam --upperBoundary 800dam --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_29.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test29_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_30(self):
        """ Calcul de l'energie bornee; on ne trouve pas de valeurs pour la borne inferieure, donc EPB indefini."""
        # open and read source
        source0 = plugin_test_dir + "SortieLFCEL_SFC_inc10mb.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOUNDED --lowerBoundary 15C --upperBoundary -152C --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_30.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test30_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_31(self):
        """ Calcul de l'energie bornee; on frole la valeur de borne inferieure sans jamais l'atteindre, donc EPB indefini."""
        # open and read source
        source0 = plugin_test_dir + "SortieLFCEL_SFC_inc10mb.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOUNDED --lowerBoundary -28C --upperBoundary -152C --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_31.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test31_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_32(self):
        """ Calcul de l'energie bornee; borne inferieure plus grande que temperature du 1er niveau, calcul a partir du 1er niveau."""
        # open and read source
        source0 = plugin_test_dir + "SortieLFCEL_SFC_inc10mb_2.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOTH --lowerBoundary 6C --upperBoundary -152C --valueToIgnore -300 ] >> [Zap --nbitsForDataStorage E32] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]

        # write the result
        results_file = TMP_PATH + "test_32.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "NRJ_test32_file2cmp.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)

    def test_33(self):
        """ Calcul de l'energie bornee; bornes retrouvees au milieu des temperatures."""
        # open and read source
        source0 = plugin_test_dir + "minimal_TTTDGZ_5005.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()

        source1 = plugin_test_dir + "lcl_5005.std"
        src_df1 = fstpy.StandardFileReader(source1)

        # compute EnergyMeanIsothermMethod
        df = EnergyMeanIsothermMethod(src_df0).compute()
        #['[ReaderStd --input {sources[0]} {sources[1]}] >> ', '([Copy] + [Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField TT]) >> ', '[EnergyMeanIsothermMethod --temperature TT --comparisonTemperature TTLP --forConvectiveEnergies --capeType BOUNDED --lowerBoundary -10C --upperBoundary -21C --valueToIgnore -300 ] >> ', '[Zap --nbitsForDataStorage E32] >> ', '[WriterStd --output {destination_path} --encodeIP2andIP3 --noUnitConversion]']

        # write the result
        results_file = TMP_PATH + "test_33.std"
        StandardFileWriter(results_file, df)()

        # open and read comparison file
        file_to_compare = plugin_test_dir + "resulttest_33.std"

        # compare results
        res = fstcomp(results_file, file_to_compare)
        assert(res)
