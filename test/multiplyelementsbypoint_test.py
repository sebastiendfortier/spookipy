# # -*- coding: utf-8 -*-
# import unittest, pytest
# 
# from tests import TMP_PATH, TEST_PATH
# 

# plugin_test_dir=TEST_PATH +"MultiplyElementsByPoint/testsFiles/"

# class TestMultiplyElementsByPoint(unittest.TestCase):

#     # def test_regtest_1(self):
#     #     """Test #1 : Utilisation de --outputFieldName avec une valeur > 4 caractères."""
#     #     # open and read source
#     #     source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
#     #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #     #compute MultiplyElementsByPoint
#     #     with pytest.raises(MultiplyElementsByPointError):
#     #         df = MultiplyElementsByPoint(src_df0, nomvar_out='TROPLONG').compute()
#     #         #[ReaderStd --input {sources[0]}] >> [MultiplyElementsByPoint --outputFieldName TROPLONG] 



#     # def test_regtest_2(self):
#     #     """Test #2 : Essaie de multiplier lorsqu'il y a seulement 1 champ en entrée."""
#     #     # open and read source
#     #     source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
#     #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #     src_df0 = src_df0.query( 'nomvar=="UU"').reset_index(drop=True)
#     #     #compute MultiplyElementsByPoint
#     #     with pytest.raises(MultiplyElementsByPointError):
#     #         df = MultiplyElementsByPoint(src_df0).compute()
#     #         #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [MultiplyElementsByPoint] 



#     # def test_regtest_3(self):
#     #     """Test #3 : Essaie de multiplier lorsqu'il y a plusieurs champs mais pas sur la même grille."""
#     #     # open and read source
#     #     source0 = plugin_test_dir + "tt_gz_px_2grilles.std"
#     #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     #     src_df0 = src_df0.query( 'nomvar in ["TT","GZ"]').reset_index(drop=True)
#     #     #compute MultiplyElementsByPoint
#     #     with pytest.raises(MultiplyElementsByPointError):
#     #         df = MultiplyElementsByPoint(src_df0).compute()
#     #         #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,GZ ] >> [MultiplyElementsByPoint] 


#     # def test_regtest_4(self):
#     #     """Test #4 : Multiplication des champs 2D."""
#     #     # open and read source
#     #     source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
#     #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #     #compute MultiplyElementsByPoint
#     #     df = MultiplyElementsByPoint(src_df0, nomvar_out='UU').compute()
#     #     #[ReaderStd --input {sources[0]}] >> [MultiplyElementsByPoint --outputFieldName UU] >> [Zap --pdsLabel MULTIPLYFIEL --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

#     #     df['etiket']='MULTIPLYFIEL'
#     #     #write the result
#     #     results_file = TMP_PATH + "test_4.std"
#     #     StandardFileWriter(results_file, df)()

#     #     # open and read comparison file
#     #     file_to_compare = plugin_test_dir + "Multiply2d_file2cmp.std"

#     #     #compare results
#     #     res = fstcomp(results_file,file_to_compare)
#     #     fstpy.delete_file(results_file)
#     #     assert(res == True)


#     # def test_regtest_5(self):
#     #     """Test #5 : Multiplication des champs 3D."""
#     #     # open and read source
#     #     source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
#     #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #     #compute MultiplyElementsByPoint
#     #     df = MultiplyElementsByPoint(src_df0, nomvar_out='TT').compute()
#     #     #[ReaderStd --input {sources[0]}] >> [MultiplyElementsByPoint --outputFieldName TT] >> [Zap --pdsLabel MULTIPLYFIEL --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

#     #     df['etiket']='MULTIPLYFIEL'
#     #     #write the result
#     #     results_file = TMP_PATH + "test_5.std"
#     #     StandardFileWriter(results_file, df)()

#     #     # open and read comparison file
#     #     file_to_compare = plugin_test_dir + "Multiply3d_file2cmp.std"

#     #     #compare results
#     #     res = fstcomp(results_file,file_to_compare)
#     #     fstpy.delete_file(results_file)
#     #     assert(res == True)


#     # def test_regtest_6(self):
#     #     """Test #6 : Test avec plusieurs champs, differents forecastHours; calcule les resulats pour chacuns des forecastHours."""
#     #     # open and read source
#     #     source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
#     #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #     #compute MultiplyElementsByPoint
#     #     df = MultiplyElementsByPoint(src_df0, group_by_forecast_hour=True).compute()
#     #     #[ReaderStd --input {sources[0]}] >> [MultiplyElementsByPoint --groupBy FORECAST_HOUR] >> [Zap --pdsLabel MULBYPT --doNotFlagAsZapped] >> [WriterStd --output {destination_path} ]

#     #     df['etiket']='MULBYPT'
#     #     #write the result
#     #     results_file = TMP_PATH + "test_6.std"
#     #     StandardFileWriter(results_file, df)()

#     #     # open and read comparison file
#     #     file_to_compare = plugin_test_dir + "Multiply_test6_file2cmp.std"

#     #     #compare results
#     #     res = fstcomp(results_file,file_to_compare)
#     #     fstpy.delete_file(results_file)
#     #     assert(res == True)


#     def test_regtest_7(self):
#         """Test #7 : Test avec plusieurs champs, differents forecastHours; fait la multiplication des champs de tous les forecastHours."""
#         # open and read source
#         source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
#         src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#         #compute MultiplyElementsByPoint
#         df = MultiplyElementsByPoint(src_df0).compute()
#         #[ReaderStd --input {sources[0]}] >> [MultiplyElementsByPoint] >> [Zap --pdsLabel MULBYPT --doNotFlagAsZapped] >> [WriterStd --output {destination_path} ]

#         df['etiket']='MULBYPT'
#         #write the result
#         results_file = TMP_PATH + "test_7.std"
#         StandardFileWriter(results_file, df)()

#         # open and read comparison file
#         file_to_compare = plugin_test_dir + "Multiply_test7_file2cmp.std"

#         #compare results
#         res = fstcomp(results_file,file_to_compare)
#         fstpy.delete_file(results_file)
#         assert(res == True)


# if __name__ == "__main__":
#     unittest.main()