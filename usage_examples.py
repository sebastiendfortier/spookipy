import os
import fstpy.all as fstpy
import spookipy
import datetime
import numpy as np
import pandas as pd
spooki_dir = os.environ['SPOOKI_DIR']
print('SPOOKI_DIR should be set to /home/spst900/spooki/spooki_dir_ppp3/')
user = os.environ['USER']
fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# class MultiplyElementsByPointError(Exception):
#     pass
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MultiplyElementsByPoint/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.OpElementsByColumn(df,operator=np.prod,operation_name='MultiplyElementsByPoint',exception_class=MultiplyElementsByPointError,group_by_forecast_hour=True,group_by_level=True,nomvar_out='MUEP',etiket='MULEPT').compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/TotalTotalsIndex/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.TotalTotalsIndex(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/GridPointDistance/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.GridPointDistance(df, axis=['x','y'], difference_type='centered').compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/GridCut/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.GridCut(df, start_point=(5,16), end_point=(73,42)).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/WindMax/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.WindMax(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/SetUpperBoundary/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.SetUpperBoundary(df, value=1.).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/InterpolationHorizontalGrid/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.InterpolationHorizontalGrid(df=df,method='user',grtyp='N',ni=191,nj=141,param1=79.0,param2=117.0,param3=57150.0,param4=21.0,interpolation_type='bi-linear',extrapolation_type='value',extrapolation_value=99.9).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MultiplyElementBy/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.MultiplyElementBy(df, value=10.).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/DewPointDepression/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.DewPointDepression(df, ice_water_phase='both', temp_phase_switch=-40, temp_phase_switch_unit='celsius').compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/AddToElement/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.AddToElement(df, value=1.).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MultiplyElementsByPoint/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.MultiplyElementsByPoint(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/Mask/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.Mask(df,thresholds=[0.0,10.0,15.0,20.0],values=[0.0,10.0,15.0,20.0],operators=['>=','>=','>=','>=']).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MinMaxVertically/testsFiles/inputFile.std').to_pandas()
# tt_df = fstpy.select_with_meta(df, ['TT'])
# minidx_df = spookipy.SetConstantValue(tt_df, min_index=True, nomvar_out='KBAS', bi_dimensionnal=True).compute()
# maxidx_df = spookipy.SetConstantValue(tt_df, max_index=True, nomvar_out='KTOP', bi_dimensionnal=True).compute()
# all_df = pd.concat([df,minidx_df,maxidx_df], ignore_index=True)
# res_df = spookipy.MinMaxVertically(all_df, nomvar="TT", min=True, max=True, bounded=True).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/WaterVapourMixingRatio/testsFiles/inputFile.std').to_pandas()
# hu_df = fstpy.select_with_meta(df, ['HU'])
# res_df = spookipy.WaterVapourMixingRatio(hu_df,ice_water_phase='both',temp_phase_switch=-40,rpn=True).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/TemperaturePotential/testsFiles/inputFile.std').to_pandas()
res_df = spookipy.TemperaturePotential(df).compute()
fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/SubtractElementsVertically/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.SubtractElementsVertically(df, direction='ascending').compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/WindModulusAndDirection/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.WindModulus(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/FilterDigital/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.FilterDigital(df, filter=[1,2,1], repetitions=2).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/GridPointDifference/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.GridPointDifference(df, axis=['x','y'], difference_type='centered').compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/TemperatureDewPoint/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.TemperatureDewPoint(df, ice_water_phase='both', temp_phase_switch=-40, temp_phase_switch_unit='celsius').compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/AddElementsByPoint/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.AddElementsByPoint(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/PrecipitationAmount/testsFiles/inputFile.std').to_pandas()
# range = (datetime.timedelta(hours=0),datetime.timedelta(hours=48))
# interval = datetime.timedelta(hours=3)
# step = datetime.timedelta(hours=1)
# res_df = spookipy.PrecipitationAmount(df, nomvar='SN', forecast_hour_range=range, interval=interval, step=step).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/WindChill/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.WindChill(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/TimeIntervalDifference/testsFiles/inputFile.std').to_pandas()
# range1 = (datetime.timedelta(hours=0),datetime.timedelta(hours=177))
# range2 = (datetime.timedelta(hours=0),datetime.timedelta(hours=160))
# interval1 = datetime.timedelta(hours=12)
# interval2 = datetime.timedelta(hours=3)
# step1 = datetime.timedelta(hours=24)
# step2 = datetime.timedelta(hours=6)
# res_df = spookipy.TimeIntervalDifference(df, nomvar='PR', forecast_hour_range=[range1, range2], interval=[interval1, interval2], step=[step1, step2]).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/TimeIntervalMinMax/testsFiles/inputFile.std').to_pandas()
# range1 = (datetime.timedelta(hours=0),datetime.timedelta(hours=177))
# range2 = (datetime.timedelta(hours=0),datetime.timedelta(hours=160))
# interval1 = datetime.timedelta(hours=12)
# interval2 = datetime.timedelta(hours=3)
# step1 = datetime.timedelta(hours=24)
# step2 = datetime.timedelta(hours=6)
# res_df = spookipy.TimeIntervalMinMax(df, nomvar='PR', min=True, forecast_hour_range=[range1, range2], interval=[interval1, interval2], step=[step1, step2]).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/AddToElement/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.ApplyUnary(df,function=np.sqrt,nomvar_in='UU*',nomvar_out='UUSQ',etiket='SQRT').compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MatchLevelIndexToValue/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.MatchLevelIndexToValue(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/SetConstantValue/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.SetConstantValue(df, value=4.).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/Humidex/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.Humidex(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/SaturationVapourPressure/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.SaturationVapourPressure(df, ice_water_phase='both', temp_phase_switch=0.01).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/SetLowerBoundary/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.SetLowerBoundary(df, value=1.).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/Pressure/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.Pressure(df, reference_field='TT').compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MinMaxLevelIndex/testsFiles/inputFile.std').to_pandas()
# minidx_df = spookipy.SetConstantValue(df, min_index=True, nomvar_out='KBAS', bi_dimensionnal=True).compute()
# maxidx_df = spookipy.SetConstantValue(df, max_index=True, nomvar_out='KTOP', bi_dimensionnal=True).compute()
# all_df = pd.concat([df,minidx_df,maxidx_df], ignore_index=True)
# res_df = spookipy.MinMaxLevelIndex(all_df, nomvar="UU", min=True, ascending=True).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/CoriolisParameter/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.CoriolisParameter(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/VapourPressure/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.VapourPressure(df, ice_water_phase='both', temp_phase_switch=-40, temp_phase_switch_unit='celsius').compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/ArithmeticMeanByPoint/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.ArithmeticMeanByPoint(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/HumidityRelative/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.HumidityRelative(df, ice_water_phase='both', temp_phase_switch=-40).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# class MultiplyElementsByError(Exception):
#     pass
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MultiplyElementBy/testsFiles/inputFile.std').to_pandas()
# def mult_value(a, v):
#     return a * v 
# res_df = spookipy.OpElementsByValue(df,
#                                  value=(1/3),
#                                  operation_name='MultiplyElementBy',
#                                  nomvar_out='MV',
#                                  operator=mult_value,
#                                  exception_class=MultiplyElementsByError,
#                                  etiket='MULEBY').compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# # #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/InterpolationHorizontalPoint/testsFiles/inputFile.std').to_pandas()
# # build lat lon dataframe
# base = {'shape': (1,1),  'dateo': 0,  'datev': 0, 'path': None, 'typvar': 'X', 'ni': 1, 'nj': 1, 'nk': 1, 'ip1': 0, 'ip2': 0, 'ip3': 0, 'deet': 0, 'npas': 0, 'datyp': 5, 'nbits': 32, 'grtyp': 'L', 'ig1': 100, 'ig2': 100, 'ig3': 9000, 'ig4': 0}
# lat = base.copy()
# lat['nomvar'] = 'LAT'
# lon = base.copy()
# lon['nomvar'] = 'LON'
# lat['d'] = np.expand_dims(np.array([45.73, 43.40, 49.18], dtype=np.float32), axis=-1)
# lat['ni'] = lat['d'].shape[0]
# lat['nj'] = lat['d'].shape[1]
# lon['d'] = np.expand_dims( np.array([-73.75, -79.38, -123.18], dtype=np.float32), axis=-1)
# lon['ni'] = lon['d'].shape[0]
# lon['nj'] = lon['d'].shape[1]
# latlon = [lat, lon]
# latlon_df =  pd.DataFrame(latlon)
# res_df = spookipy.InterpolationHorizontalPoint(df,latlon_df,interpolation_type='bi-linear',extrapolation_type='value',extrapolation_value=99.9).compute()
# print(res_df.dtypes)
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# ######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/CloudFractionDiagnostic/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.CloudFractionDiagnostic(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/HumiditySpecific/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.HumiditySpecific(df, ice_water_phase='both', temp_phase_switch=-40).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
# #######################################################
# df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/GeorgeKIndex/testsFiles/inputFile.std').to_pandas()
# res_df = spookipy.GeorgeKIndex(df).compute()
# fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()
# fstpy.delete_file(f'/tmp/{user}/outputFile.std')
