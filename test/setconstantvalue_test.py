# # -*- coding: utf-8 -*-
# import unittest, pytest
# 
# import pandas as pd
# from tests import TMP_PATH, TEST_PATH
# 

# plugin_test_dir=TEST_PATH +"SetConstantValue/testsFiles/"

# class TestSetConstantValue(unittest.TestCase):

#     def test_regtest_1(self):
#         """Test #1 :  Création d'un champ 3D nommé RES identique au champ UU du fichier d'entrée avec 0.33323 comme valeurs."""
#         # open and read source
#         source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
#         src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#         uu = src_df0.query('nomvar == "UU"').reset_index(drop=True)
#         #compute SetConstantValue
#         uudf = SetConstantValue(uu, value=0.33323, nomvar_out='UU*').compute()
#         vv = src_df0.query('nomvar == "VV"').reset_index(drop=True)
#         #compute SetConstantValue
#         vvdf = SetConstantValue(uu, value=0.33323, nomvar_out='VV*').compute()
#         #[ReaderStd --input {sources[0]}] >> ( ([Select --fieldName UU] >> [SetConstantValue --value 0.33323 --outputFieldName UU*]) + ([Select --fieldName VV] >> [SetConstantValue --value 0.33323 --outputFieldName VV*]) ) >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

#         df = pd.concat([uudf,vvdf],ignore_index=True)
#         #write the result
#         results_file = TMP_PATH + "test_1.std"
#         StandardFileWriter(results_file, df)()

#         # open and read comparison file
#         file_to_compare = plugin_test_dir + "assign_file2cmp.std"

#         #compare results
#         res = fstcomp(results_file,file_to_compare)
#         fstpy.delete_file(results_file)
#         assert(res == True)


#     def test_regtest_2(self):
#         """Test #2 :  Création d'un champ 2D identique au champ UU du fichier d'entrée avec 0 comme valeur (MININDEX)."""
#         # open and read source
#         source0 = plugin_test_dir + "generate2D_fileSrc.std"
#         src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#         uu = src_df0.query('nomvar == "UU"').reset_index(drop=True)
#         #compute SetConstantValue
#         df = SetConstantValue(uu, min_index=True, bi_dimensionnal=True).compute()
#         #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetConstantValue --value MININDEX --bidimensional] >> [Zap --fieldName RES --pdsLabel GENERATE2D --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

#         df['nomvar']='RES'
#         df['etiket']='GENERATE2D'
#         #write the result
#         results_file = TMP_PATH + "test_2.std"
#         StandardFileWriter(results_file, df)()

#         # open and read comparison file
#         file_to_compare = plugin_test_dir + "g2d1_file2cmp.std"

#         #compare results
#         res = fstcomp(results_file,file_to_compare)
#         assert(res == True)


#     def test_regtest_3(self):
#         """Test #3 :  Création d'un champ 2D identique au champ UU du fichier d'entrée avec MAXINDEX comme valeurs"""
#         # open and read source
#         source0 = plugin_test_dir + "2011072100_006_eta_small"
#         src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#         uu = src_df0.query('nomvar == "UU"').reset_index(drop=True)
#         uu['etiket']='580V0N'
#         #compute SetConstantValue
#         df = SetConstantValue(uu, max_index=True, bi_dimensionnal=True).compute()
#         #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [Zap --metadataZappable --pdsLabel 580V0N] >> [SetConstantValue --value MAXINDEX --bidimensional] >> [Zap --fieldName RES --pdsLabel GENERATE2D --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

#         df['nomvar']='RES'
#         df['etiket']='GENERATE2D'
#         #write the result
#         results_file = TMP_PATH + "test_3.std"
#         StandardFileWriter(results_file, df)()

#         # open and read comparison file
#         file_to_compare = plugin_test_dir + "g2d2_file2cmp.std"

#         #compare results
#         res = fstcomp(results_file,file_to_compare)
#         assert(res == True)


#     def test_regtest_4(self):
#         """Test #4 :  Création d'un champ 2D identique au champ UU du fichier d'entrée avec 1.0 comme valeurs"""
#         # open and read source
#         source0 = plugin_test_dir + "generate2D_fileSrc.std"
#         src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#         uu = src_df0.query('nomvar == "UU"').reset_index(drop=True)
#         #compute SetConstantValue
#         df = SetConstantValue(uu, value=-1, bi_dimensionnal=True).compute()
#         #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetConstantValue --value -1.0 --bidimensional] >> [Zap --fieldName RES --pdsLabel GENERATE2D --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

#         df['nomvar']='RES'
#         df['etiket']='GENERATE2D'
#         #write the result
#         results_file = TMP_PATH + "test_4.std"
#         StandardFileWriter(results_file, df)()

#         # open and read comparison file
#         file_to_compare = plugin_test_dir + "g2d3_file2cmp.std"

#         #compare results
#         res = fstcomp(results_file,file_to_compare)
#         assert(res == True)


#     def test_regtest_5(self):
#         """Test #5 :  Création de 2 champs 2D identiques au champ UU, le premier avec MININDEX comme valeurs et le deuxième avec MAXINDEX."""
#         # open and read source
#         source0 = plugin_test_dir + "generate2D_fileSrc.std"
#         src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#         uu = src_df0.query('nomvar == "UU"').reset_index(drop=True)
#         #compute SetConstantValue
#         df1 = SetConstantValue(uu, min_index=True, bi_dimensionnal=True).compute()
#         df1['nomvar']='KBAS'
#         df1['etiket']='GENERATE2D'
#         #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> ( ([SetConstantValue --value MININDEX --bidimensional] >> [Zap --fieldName KBAS --pdsLabel GENERATE2D --doNotFlagAsZapped]) + ([SetConstantValue --value MAXINDEX --bidimensional] >> [Zap --fieldName KTOP --pdsLabel GENERATE2D --doNotFlagAsZapped]) ) >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

#         df2 = SetConstantValue(uu, max_index=True, bi_dimensionnal=True).compute()
#         df2['nomvar']='KTOP'
#         df2['etiket']='GENERATE2D'

#         df = pd.concat([df1,df2],ignore_index=True)
#         #write the result
#         results_file = TMP_PATH + "test_5.std"
#         StandardFileWriter(results_file, df)()

#         # open and read comparison file
#         file_to_compare = plugin_test_dir + "g2d4_file2cmp.std"

#         #compare results
#         res = fstcomp(results_file,file_to_compare)
#         assert(res == True)


#     def test_regtest_6(self):
#         """Test #6 :  Création d'un champ 2D identique au champ UU du fichier d'entrée avec NBLEVELS comme valeurs"""
#         # open and read source
#         source0 = plugin_test_dir + "2011072100_006_eta_small"
#         src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#         uu = src_df0.query('nomvar == "UU"').reset_index(drop=True)
#         uu['etiket']='580V0N'
#         #compute SetConstantValue
#         df = SetConstantValue(uu, nb_levels=True, bi_dimensionnal=True, out_name='RES').compute()
#         #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [Zap --metadataZappable --pdsLabel 580V0N] >> [SetConstantValue --value NBLEVELS --bidimensional --outputFieldName RES] >> [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

#         #write the result
#         results_file = TMP_PATH + "test_6.std"
#         StandardFileWriter(results_file, df)()

#         # open and read comparison file
#         file_to_compare = plugin_test_dir + "nbLevels_file2cmp.std"

#         #compare results
#         res = fstcomp(results_file,file_to_compare)
#         assert(res == True)


# if __name__ == "__main__":
#     unittest.main()