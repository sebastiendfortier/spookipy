# # -*- coding: utf-8 -*-
# from test import TMP_PATH,TEST_PATH
# import pytest
# import fstpy.all as fstpy
# import spookipy.all as spooki

# pytestmark = [pytest.mark.regressions]

# @pytest.fixture
# def plugin_test_dir():
#     return TEST_PATH + '/GeorgeKIndex/testsFiles/'


# def test_regtest_1(plugin_test_dir):
#     """Test #1 :  Calcul de l'indice à partir d'une matrice de températures de 5x4x3 et d'écarts de point de rosée de 5x4x2"""
#     # open and read source
#     source0 = plugin_test_dir + "inputFileSimple.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #compute GeorgeKIndex
#     df = spooki.GeorgeKIndex(src_df0).compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]

#     #write the result
#     results_file = TMP_PATH + "test_1.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "TTES_GeorgeKIndex_file2cmp.std"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     print('res=',res)
#     assert(False == True)


# def test_regtest_2(plugin_test_dir):
#     """Test #2 :  Calcul de l'indice avec un vrai fichier de données"""
#     # open and read source
#     source0 = plugin_test_dir + "inputFile.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #compute GeorgeKIndex
#     df = spooki.GeorgeKIndex(src_df0).compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]

#     #write the result
#     results_file = TMP_PATH + "test_2.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "GeorgeKIndex_file2cmp.std"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     print('res=',res)
#     assert(False == True)


# def test_regtest_with_TT_TD(plugin_test_dir):
#     """Test #3 :  Calcul de l'indice avec un fichier de données contenant TT et TD mais pas ES"""
#     # open and read source
#     source0 = plugin_test_dir + "inputFileSimpleTD_TT.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #compute GeorgeKIndex
#     df = spooki.GeorgeKIndex(src_df0).compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]

#     #write the result
#     results_file = TMP_PATH + "test_with_TT_TD.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "TTTD_GeorgeKIndex_file2cmp.std"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     print('res=',res)
#     assert(False == True)


# def test_regtest_TT_ES_differentsUnites(plugin_test_dir):
#     """Test #4 :  Calcul de l'indice avec un fichier contenant des TT et des ES d'unités différentes"""
#     # open and read source
#     source0 = plugin_test_dir + "inputFileSimple.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #compute GeorgeKIndex
#     df = spooki.GeorgeKIndex(src_df0).compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> ( ([Select --fieldName TT] >> [UnitConvert --unit kelvin]) + [Select --fieldName ES] ) >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]

#     #write the result
#     results_file = TMP_PATH + "test_TT_ES_differentsUnites.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "TTES_GeorgeKIndex_file2cmp.std"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     print('res=',res)
#     assert(False == True)


# def test_regtest_PlusieursForecastHours(plugin_test_dir):
#     """Test #5 :  Calcul avec un fichier ayant plusieurs forecastHour - Ne doit pas fonctionner car des niveaux sont manquants pour un forecastHour"""
#     # open and read source
#     source0 = plugin_test_dir + "2016122000_006_NatPres.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #compute GeorgeKIndex
#     df = spooki.GeorgeKIndex(src_df0).compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex] 

#     assert(False == False)


# def test_regtest_6(plugin_test_dir):
#     """Test #6 :  Calcul avec un fichier ayant plusieurs forecastHour"""
#     # open and read source
#     source0 = plugin_test_dir + "2016122000_006_NatPres.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     src_df0 = src_df0.query('ip2==6').reset_index(drop=True)

#     #compute GeorgeKIndex
#     df = spooki.GeorgeKIndex(src_df0).compute()
#     #['[ReaderStd --ignoreExtended --input {sources[0]}] >>', '[Select --forecastHour 6] >> [GeorgeKIndex] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

#     #write the result
#     results_file = TMP_PATH + "test_6.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "TTES_2016122000_file2cmp.std"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     print('res=',res)
#     assert(False == True)


