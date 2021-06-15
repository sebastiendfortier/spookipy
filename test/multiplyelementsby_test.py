# # -*- coding: utf-8 -*-
# import unittest, pytest
# 
# from tests import TMP_PATH, TEST_PATH
# 

# plugin_test_dir=TEST_PATH +"MultiplyElementBy/testsFiles/"

# class TestMultiplyElementsBy(unittest.TestCase):

#     def test_regtest_1(self):
#         """Test #1 : test_factor1"""
#         # open and read source
#         source0 = plugin_test_dir + "UUVV5x5_1_fileSrc.std"
#         src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#         #compute MultiplyElementsBy
#         df = MultiplyElementsBy(src_df0, value=3).compute()
#         #[ReaderStd --input {sources[0]}] >> [MultiplyElementsBy --value 3.0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

#         df['ip1']=500
#         #write the result
#         results_file = TMP_PATH + "test_1.std"
#         StandardFileWriter(results_file, df)()

#         # open and read comparison file
#         file_to_compare = plugin_test_dir + "factor_file2cmp.std"

#         #compare results
#         res = fstcomp(results_file,file_to_compare)
#         fstpy.delete_file(results_file)
#         assert(res == True)


#     def test_regtest_2(self):
#         """Test #2 : test_factor2"""
#         # open and read source
#         source0 = plugin_test_dir + "UUVV5x5_1_fileSrc.std"
#         src_df0 = fstpy.StandardFileReader(source0).to_pandas()
#         
#         src_df0 = fstpy.load_data(src_df0)
#         print('src_df0',src_df0[['nomvar', 'ni', 'nj', 'nk', 'dateo', 'level', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4','path']].to_string())
#         #compute MultiplyElementsBy
#         df = MultiplyElementsBy(src_df0, value=0.333).compute()
#         #[ReaderStd --input {sources[0]}] >> [MultiplyElementsBy --value 0.333] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

#         df['ip1']=500
#         #write the result
#         results_file = TMP_PATH + "test_2.std"
#         StandardFileWriter(results_file, df)()

#         # open and read comparison file
#         file_to_compare = plugin_test_dir + "factor2_file2cmp.std"

#         #compare results
#         res = fstcomp(results_file,file_to_compare)
#         fstpy.delete_file(results_file)
#         assert(res == True)


# if __name__ == "__main__":
#     unittest.main()