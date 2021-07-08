# # -*- coding: utf-8 -*-
# from test import TMP_PATH,TEST_PATH
# import pytest
# import fstpy.all as fstpy
# import spookipy.all as spooki
# import pandas as pd

# pytestmark = [pytest.mark.regressions]

# @pytest.fixture
# def plugin_test_dir():
#     return TEST_PATH + '/DewPointDepression/testsFiles/'

# def test_regtest_1(plugin_test_dir):
#     """Test #1 :  Calcul du point de rosée; utilisation de --iceWaterPhase BOTH mais sans --temperaturePhaseSwitch."""
#     # open and read source
#     source0 = plugin_test_dir + "inputFile.std"
#     src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()


#     #compute spooki.DewPointDepression
#     df = spooki.DewPointDepression(src_df0,ice_water_phase='both').compute()
#     #[ReaderStd --input {sources[0]}] >> [spooki.DewPointDepression --iceWaterPhase BOTH ]

#     #write the result
#     results_file = TMP_PATH + "test_1.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "nan"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     print(res)
#     assert(False == False)


# def test_regtest_3(plugin_test_dir):
#     """Test #3 :  Calcul de l'écart du point de rosée (ES) à partir de l'humidité spécifique (HU)."""
#     # open and read source
#     source0 = plugin_test_dir + "2011100712_012_glbhyb"
#     src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()

#     src_df0 = src_df0.query('nomvar in ["TT","HU"]').reset_index(drop=True)

#     #compute spooki.DewPointDepression
#     df = spooki.DewPointDepression(src_df0,ice_water_phase='water').compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >> [spooki.DewPointDepression --iceWaterPhase WATER ] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

#     #write the result
#     results_file = TMP_PATH + "test_3.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_hu_nonRpn_file2cmp.std"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     print(res)
#     assert(False == False)

# def test_regtest_5(plugin_test_dir):
#     """Test #5 :  Calcul de l'écart du point de rosée (ES) à partir de l'humidité relative (HR)."""
#     # open and read source
#     source0 = plugin_test_dir + "2011100712_012_glbhyb"
#     src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()

#     src_df0 = src_df0.query('nomvar in ["TT","HR"]').reset_index(drop=True)

#     #compute spooki.DewPointDepression
#     df = spooki.DewPointDepression(src_df0,ice_water_phase='water').compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HR] >> [spooki.DewPointDepression --iceWaterPhase WATER ] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

#     #write the result
#     results_file = TMP_PATH + "test_5.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_hr_nonRpn_file2cmp.std"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     print(res)
#     assert(False == False)


# def test_regtest_6(plugin_test_dir):
#     """Test #6 :  Calcul de l'écart du point de rosée (ES) à partir de la température du point de rosée (TD), option --RPN."""
#     # open and read source
#     source0 = plugin_test_dir + "2011100712_012_glbhyb"
#     src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()

#     src_df0 = src_df0.query('nomvar in ["TT","HU"]').reset_index(drop=True)
    
#     tt_df = src_df0.query('nomvar=="TT"').reset_index(drop=True)

#     #compute spooki.DewPointDepression
#     df = spooki.DewPointDepression(src_df0,ice_water_phase='water').compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >> ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >> [spooki.DewPointDepression --iceWaterPhase WATER --RPN] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

#     new_df = pd.concat([tt_df,df],ignore_index=True)

#     df = spooki.DewPointDepression(new_df,ice_water_phase='water', rpn=True).compute()
#     #write the result
#     results_file = TMP_PATH + "test_6.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_td_file2cmp.std"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     print(res)
#     assert(False == False)


# def test_regtest_7(plugin_test_dir):
#     """Test #7 :  Calcul de l'écart du point de rosée (ES) à partir de la température du point de rosée (TD)."""
#     # open and read source
#     source0 = plugin_test_dir + "2011100712_012_glbhyb"
#     src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()


#     #compute spooki.DewPointDepression
#     df = spooki.DewPointDepression(src_df0,ice_water_phase='water').compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,HU] >> ([Select --fieldName TT] + [TemperatureDewPoint --iceWaterPhase WATER]) >> [spooki.DewPointDepression --iceWaterPhase WATER] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

#     #write the result
#     results_file = TMP_PATH + "test_7.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_td_file2cmp.std"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res == True)


# def test_regtest_9(plugin_test_dir):
#     """Test #9 :  Calcul de l'écart du point de rosée (ES) à partir du rapport de mélange de la vapeur d'eau (QV)."""
#     # open and read source
#     source0 = plugin_test_dir + "2011100712_012_glbhyb_QV"
#     src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()


#     #compute spooki.DewPointDepression
#     df = spooki.DewPointDepression(src_df0,ice_water_phase='water').compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.DewPointDepression --iceWaterPhase WATER] >> [Zap --pdsLabel G133K80N --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended]

#     #write the result
#     results_file = TMP_PATH + "test_9.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "2011100712_012_glbhyb_qv_nonRpn_file2cmp.std"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     print(res)
#     assert(False == False)


