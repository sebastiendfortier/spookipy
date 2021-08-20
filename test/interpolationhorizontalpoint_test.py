# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, convip

import pytest
import fstpy.all as fstpy
import spookipy.all as spooki
import numpy as np
import pandas as pd
import rpnpy.librmn.all as rmn


pytestmark = [pytest.mark.to_skip]

# ::::::::::::::
# inputFile.csv
# ::::::::::::::
# pds:LAT,LATLON
# level:1.0
# 45.73,43.40,49.18

# pds:LON,LATLON
# level:1.0
# -73.75,-79.38,-123.18

# def date_of_origin():
#     d = datetime.datetime(year=2015, month=8, day=5,hour=9,minute=42,second=30)
#     return d


def base_dict():
    base = {'shape':(1,1),'datev':0,'path':None,'typvar':'X', 'ni':1,'nj':1,'nk':1,'ip1':0,'ip2':0,'ip3':0, 'deet':0,'npas':0,'datyp':5,'nbits':32, 'grtyp':'L','ig1':100,'ig2':100,'ig3':9000,'ig4':0}
    lat = base.copy()
    lat['nomvar'] = 'LAT'
    lon = base.copy()
    lon['nomvar'] = 'LON'
    return lat,lon

@pytest.fixture
def simple_input_df():
    lat,lon = base_dict()
    lat['d'] = np.expand_dims(np.array([45.73,43.40,49.18],dtype='float32'),axis=-1)
    lat['ni'] = lat['d'].shape[0]
    lat['nj'] = lat['d'].shape[1]
    lon['d'] = np.expand_dims(np.array([-73.75,-79.38,-123.18],dtype='float32'),axis=-1)
    lon['ni'] = lon['d'].shape[0]
    lon['nj'] = lon['d'].shape[1]
    latlon = [lat,lon]
        # {'nomvar':'LAT','etiket':'LATLON','level':'1.0','d':np.array([45.73,43.40,49.18],dtype='float32'),axis=-1),'date_of_origin':date_of_origin},
        # {'nomvar':'LON','etiket':'LATLON','level':'1.0','d':np.array([-73.75,-79.38,-123.18],dtype='float32'),axis=-1),'date_of_origin':date_of_origin}
        # ]
    return pd.DataFrame(latlon)


# ::::::::::::::
# latlonExtrapolation_fileSrc.csv
# ::::::::::::::
# pds:LAT,LATLON
# level:1.0
# 43.86,-43.4,43.61,43.47,43.22,-44.0

# pds:LON,LATLON
# level:1.0
# -78.926,77.7,-78.380,-79.26,-78.72,70.0
@pytest.fixture
def latlon_extrapolation_df():
    lat,lon = base_dict()
    lat['d'] = np.expand_dims(np.array([43.86,-43.4,43.61,43.47,43.22,-44.0],dtype='float32'),axis=-1)
    lat['ni'] = lat['d'].shape[0]
    lat['nj'] = lat['d'].shape[1]
    lon['d'] = np.expand_dims(np.array([-78.926,77.7,-78.380,-79.26,-78.72,70.0],dtype='float32'),axis=-1)
    lon['ni'] = lon['d'].shape[0]
    lon['nj'] = lon['d'].shape[1]
    latlon = [lat,lon]
        # {'nomvar':'LAT','etiket':'LATLON','level':'1.0','d':np.array([43.86,-43.4,43.61,43.47,43.22,-44.0],dtype='float32'),axis=-1),'date_of_origin':date_of_origin},
        # {'nomvar':'LON','etiket':'LATLON','level':'1.0','d':np.array([-78.926,77.7,-78.380,-79.26,-78.72,70.0],dtype='float32'),axis=-1),'date_of_origin':date_of_origin},
        # ]
    return pd.DataFrame(latlon)

# ::::::::::::::
# latlonWithGrid_fileSrc.csv
# ::::::::::::::
# gds:TYPE_L,1,2,3

# pds:LAT,LATLON
# level:1.0
# 45.73,43.40,49.18

# pds:LON,LATLON
# level:1.0
# -73.75,-79.38,-123.18
@pytest.fixture
def latlon_with_grid_df():
    lat,lon = base_dict()
    lat['d'] = np.expand_dims(np.array([45.73,43.40,49.18],dtype='float32'),axis=-1)
    lat['ni'] = lat['d'].shape[0]
    lat['nj'] = lat['d'].shape[1]
    lon['d'] = np.expand_dims(np.array([-73.75,-79.38,-123.18],dtype='float32'),axis=-1)
    lon['ni'] = lon['d'].shape[0]
    lon['nj'] = lon['d'].shape[1]
    latlon = [lat,lon]
        # {'nomvar':'LAT','etiket':'LATLON','level':'1.0','grtyp':'L','d':np.array([45.73,43.40,49.18],dtype='float32'),axis=-1),'date_of_origin':date_of_origin},
        # {'nomvar':'LON','etiket':'LATLON','level':'1.0','grtyp':'L','d':np.array([-73.75,-79.38,-123.18],dtype='float32'),axis=-1),'date_of_origin':date_of_origin},
        # ]
    latlon_df = pd.DataFrame(latlon)
    latlon_df['ip2'] = 2
    latlon_df['ip3'] = 3
    return latlon_df

# ::::::::::::::
# latlonYY_fileSrc.csv
# ::::::::::::::
# pds:LAT,LATLON
# level:1000.0
# 46.60,14.098,-45.828,-13.458,51.048,-8.49,56.056,-43.81,-4.7,-51.8,-80.11,-14.034,-15.68,34.63,36.22,76.28

# pds:LON,LATLON
# level:1000.0
# -67.368,-44.74,-33.34,38.155,31.50,116.93,158.32,170.64,-52.73,-59.236,100.28,127.28,40.56,-140.24,-30.495,-99.63
@pytest.fixture
def latlon_yy_df():
    lat,lon = base_dict()
    lat['d'] = np.expand_dims(np.array([46.60,14.098,-45.828,-13.458,51.048,-8.49,56.056,-43.81,-4.7,-51.8,-80.11,-14.034,-15.68,34.63,36.22,76.28],dtype='float32'),axis=-1)
    lat['ni'] = lat['d'].shape[0]
    lat['nj'] = lat['d'].shape[1]
    lon['d'] = np.expand_dims(np.array([-67.368,-44.74,-33.34,38.155,31.50,116.93,158.32,170.64,-52.73,-59.236,100.28,127.28,40.56,-140.24,-30.495,-99.63],dtype='float32'),axis=-1)
    lon['ni'] = lon['d'].shape[0]
    lon['nj'] = lon['d'].shape[1]
    latlon = [lat,lon]
        # {'nomvar':'LAT','etiket':'LATLON','level':'1000.0','d':np.array([46.60,14.098,-45.828,-13.458,51.048,-8.49,56.056,-43.81,-4.7,-51.8,-80.11,-14.034,-15.68,34.63,36.22,76.28],dtype='float32'),axis=-1),'date_of_origin':date_of_origin},
        # {'nomvar':'LON','etiket':'LATLON','level':'1000.0','d':np.array([-67.368,-44.74,-33.34,38.155,31.50,116.93,158.32,170.64,-52.73,-59.236,100.28,127.28,40.56,-140.24,-30.495,-99.63],dtype='float32'),axis=-1),'date_of_origin':date_of_origin},
        # ]
    return pd.DataFrame(latlon)
# ::::::::::::::
# latlon_fileSrc.csv
# ::::::::::::::
# pds:LAT,LATLON
# level:1.0
# 45.73,43.40,49.18

# pds:LON,LATLON
# level:1.0
# -73.75,-79.38,-123.18
@pytest.fixture
def latlon_df():
#     gds:TYPE_Y,0,1,2

# pds:LAT,LATLON
# level:1.0
# 45.73,43.40,49.18

# pds:LON,LATLON
# level:1.0
# -73.75,-79.38,-123.18

    lat,lon = base_dict()
    lat['d'] = np.expand_dims(np.array([45.73,43.40,49.18],dtype='float32'),axis=-1)
    lat['ni'] = lat['d'].shape[0]
    lat['nj'] = lat['d'].shape[1]
    lon['d'] = np.expand_dims(np.array([-73.75,-79.38,-123.18],dtype='float32'),axis=-1)
    lon['ni'] = lon['d'].shape[0]
    lon['nj'] = lon['d'].shape[1]
    latlon = [lat,lon]
        # {'nomvar':'LAT','etiket':'LATLON','level':'1.0','d':np.array([45.73,43.40,49.18],dtype='float32'),axis=-1),'date_of_origin':date_of_origin},
        # {'nomvar':'LON','etiket':'LATLON','level':'1.0','d':np.array([-73.75,-79.38,-123.18],dtype='float32'),axis=-1),'date_of_origin':date_of_origin},
        # ]
    return pd.DataFrame(latlon)

# ::::::::::::::
# latlon_fileSrc2.csv
# ::::::::::::::
# pds:LAT,LATLON
# level:1.0
# 45.73,43.40,49.18,53.13

# pds:LON,LATLON
# level:1.0
# -73.75,-79.38,-123.18,-108.15
@pytest.fixture
def latlon2_df():
    lat,lon = base_dict()
    lat['d'] = np.expand_dims(np.array([45.73,43.40,49.18,53.13],dtype='float32'),axis=-1)
    lat['ni'] = lat['d'].shape[0]
    lat['nj'] = lat['d'].shape[1]
    lon['d'] = np.expand_dims(np.array([-73.75,-79.38,-123.18,-108.15],dtype='float32'),axis=-1)
    lon['ni'] = lon['d'].shape[0]
    lon['nj'] = lon['d'].shape[1]
    latlon = [lat,lon]
        # {'nomvar':'LAT','etiket':'LATLON','level':'1.0','d':np.array([45.73,43.40,49.18,53.13],dtype='float32'),'date_of_origin':date_of_origin},
        # {'nomvar':'LON','etiket':'LATLON','level':'1.0','d':np.array([-73.75,-79.38,-123.18,-108.15],dtype='float32'),'date_of_origin':date_of_origin},
        # ]
    return pd.DataFrame(latlon)

# @pytest.fixture
# def stationsdf_df():
#     lat,lon = base_dict()
#     lat['d'] = np.expand_dims(STATIONSFB['Latitude'].to_numpy().astype('float32'),axis=-1)
#     lat['ni'] = lat['d'].shape[0]
#     lat['nj'] = lat['d'].shape[1]
#     lon['d'] = np.expand_dims(STATIONSFB['Longitude'].to_numpy().astype('float32'),axis=-1)
#     lon['ni'] = lon['d'].shape[0]
#     lon['nj'] = lon['d'].shape[1]
#     latlon = [lat,lon]
#         # {'nomvar':'LAT','etiket':'LATLON','level':'1.0','d':STATIONSFB['Latitude'].to_numpy().astype('float32'),'date_of_origin':date_of_origin},
#         # {'nomvar':'LON','etiket':'LATLON','level':'1.0','d':STATIONSFB['Longitude'].to_numpy().astype('float32'),'date_of_origin':date_of_origin},
#         # ]
#     latlon_df =  pd.DataFrame(latlon)
#     latlon_df['ip2'] = 222
#     latlon_df['ip3'] = 333
#     return latlon_df

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH +"InterpolationHorizontalPoint/testsFiles/"


def test_1(plugin_test_dir,latlon_df):
    """test_onlyscalarR1Operational"""
    # open and read source
    source0 = plugin_test_dir + "4panneaux_input4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo']=368660482
    latlon_df['dateo']=368660482

    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon_df).compute()
    #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df['etiket'] = 'R1558V0_N'
    df.loc[df.nomvar == '^^','etiket'] = 'R1INTHPTN'
    df.loc[df.nomvar == '>>','etiket'] = 'R1INTHPTN'

    # df['datyp']=5
    # df['nbits']=32

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resultOnlyScalarR1Operational_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_1"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir,latlon_df):
    """test_onlyscalar"""
    # open and read source
    source0 = plugin_test_dir + "4panneaux_input4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo']=368660482
    latlon_df['dateo']=368660482

    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon_df).compute()
    #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df['etiket']='R1558V0_N'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'

    # df['dateo']=368660482

    # df['datyp']=5
    # df['nbits']=32

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resultOnlyScalar_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_2"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_3(plugin_test_dir,latlon_df):
    """test_scalarvectorial"""
    # open and read source
    source0 = plugin_test_dir + "tape10.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo']=368660482
    latlon_df['dateo']=368660482
    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon_df).compute()
    #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df['etiket']='R1558V0_N'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'
    # df['dateo']=368660482

    # df['datyp']=5
    # df['nbits']=32

    df.loc[df.nomvar == 'VS','etiket'] = 'XVSHEAR_X'

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resultScalarVectorial_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_3"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_4(plugin_test_dir,latlon2_df):
    """test_scalarvectorial2"""
    # open and read source
    source0 = plugin_test_dir + "2011072100_006_eta_small"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0.loc[src_df0.nomvar!='P0','dateo']=368660482
    latlon2_df['dateo']=368660482
    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon2_df).compute()
    #[ReaderStd --input {sources[0]}] >>
    # [ReaderCsv --input {sources[1]}] >>
    # [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >>
    # [InterpolationHorizontalPoint] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df.loc[:,'etiket']='R1580V0_N'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'
    # df = df.loc[df.nomvar!='PT']
    # print('df\n',df[['nomvar', 'typvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'datyp', 'nbits', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4','grid']].to_string())
    # df['dateo']=368660482

    # df['datyp']=5
    # df['nbits']=32
# P0   P  R1580V0_N           4       1     1 20110210 215210             0         6         0      450       48  R 16  Y     0     0     0     0
# P0   PI R1580V0_N           4       1     1 20110721 000000             0         6         0      450       48  R 16  Y     0     0     0     0

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_4.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resultScalarVectorial2_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_4"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.01)#,e_max=0.00105,e_moy=0.001)
    fstpy.delete_file(results_file)
    assert(res)

def test_5(plugin_test_dir,latlon_df):
    """test_nearest"""
    # open and read source
    source0 = plugin_test_dir + "tape10.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo']=368660482
    latlon_df['dateo']=368660482

    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon_df,interpolation_type='nearest').compute()
    #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint --interpolationType NEAREST] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]
    df['etiket']='R1558V0_N'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'
    # df['dateo']=368660482

    # df['datyp']=5
    # df['nbits']=32

    df.loc[df.nomvar == 'VS','etiket'] = 'XVSHEAR_X'

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resultNearest_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_5"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir,latlon_df):
    """test_linear"""
    # open and read source
    source0 = plugin_test_dir + "tape10.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo']=368660482
    latlon_df['dateo']=368660482

    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon_df,interpolation_type='bi-linear').compute()
    #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint --interpolationType BI-LINEAR] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]
    df['etiket']='R1558V0_N'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'
    # df['dateo']=368660482

    # df['datyp']=5
    # df['nbits']=32

    df.loc[df.nomvar == 'VS','etiket'] = 'XVSHEAR_X'

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resultLinear_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_6"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_7(plugin_test_dir,latlon_with_grid_df):
    """test_withGridInCsv"""
    # open and read source
    source0 = plugin_test_dir + "tape10.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo']=368660482
    latlon_with_grid_df['dateo']=368660482

    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon_with_grid_df,interpolation_type='nearest').compute()
    #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint --interpolationType NEAREST] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df['etiket']='R1558V0_N'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'
    # df['dateo']=368660482

    # df['datyp']=5
    # df['nbits']=32

    df.loc[df.nomvar == 'VS','etiket'] = 'XVSHEAR_X'

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "result_withGridInCsv_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_7"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_8(plugin_test_dir,latlon_extrapolation_df):
    """test_extrapolationValue"""
    # open and read source
    source0 = plugin_test_dir + "tape10.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo']=368660482
    latlon_extrapolation_df['dateo']=368660482

    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon_extrapolation_df,interpolation_type='bi-cubic', extrapolation_type='value', extrapolation_value=999.9).compute()
    #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType VALUE=999.9] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df['etiket']='R1558V0_N'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'
    # df['dateo']=368660482

    # df['datyp']=5
    # df['nbits']=32

    df.loc[df.nomvar == 'VS','etiket'] = 'XVSHEAR_X'

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_8.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "result_extrapolValue_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_8"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_9(plugin_test_dir,latlon_extrapolation_df):
    """test_negativeValue"""
    # open and read source
    source0 = plugin_test_dir + "tape10.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo']=368660482
    latlon_extrapolation_df['dateo']=368660482

    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon_extrapolation_df,interpolation_type='bi-cubic', extrapolation_type='value', extrapolation_value=-99.9).compute()
    #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType VALUE=-99.9] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df['etiket']='R1558V0_N'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'

    # df['datyp']=5
    # df['nbits']=32

    df.loc[df.nomvar == 'VS','etiket'] = 'XVSHEAR_X'

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_9.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "result_negativeValue_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_9"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_10(plugin_test_dir,latlon_extrapolation_df):
    """test_extrapolationMax"""
    # open and read source
    source0 = plugin_test_dir + "tape10.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo']=368660482
    latlon_extrapolation_df['dateo']=368660482

    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon_extrapolation_df,interpolation_type='bi-cubic', extrapolation_type='maximum').compute()
    #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType MAXIMUM] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df['etiket']='R1558V0_N'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'

    # df['datyp']=5
    # df['nbits']=32

    df.loc[df.nomvar == 'VS','etiket'] = 'XVSHEAR_X'

    # df['datyp']=5
    # df['nbits']=32
    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_10.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "result_extrapolMax_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_10"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_11(plugin_test_dir,latlon_extrapolation_df):
    """test_extrapolationMin"""
    # open and read source
    source0 = plugin_test_dir + "tape10.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo']=368660482
    latlon_extrapolation_df['dateo']=368660482
    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon_extrapolation_df,interpolation_type='bi-cubic', extrapolation_type='minimum').compute()
    #[ReaderStd --input {sources[0]}] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType MINIMUM] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df['etiket']='R1558V0_N'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'

    # df['datyp']=5
    # df['nbits']=32

    df.loc[df.nomvar == 'VS','etiket'] = 'XVSHEAR_X'

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_11.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "result_extrapolMin_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_11"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

# need to fix stations order for it to work
# def test_12(plugin_test_dir,stationsdf_df):
#     """test_stations"""
#     # open and read source
#     source0 = plugin_test_dir + "2011072100_006_eta_small"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     src_df0 = src_df0.loc[src_df0.nomvar.isin(["GZ","UU","VV","TT",">>","^^","!!"])].reset_index(drop=True)

#     #compute spooki.InterpolationHorizontalPoint
#     df = spooki.InterpolationHorizontalPoint(src_df0,stationsdf_df).compute()
#     #[ReaderStd --input {sources[0]}] >> [Select --fieldName GZ,UU,VV,TT] >> [GetDictionaryInformation --dataBase STATIONS --outputAttribute LAT,LON --advancedRequest SELECT_Latitude,Longitude_FROM_STATIONSFB] >> [spooki.InterpolationHorizontalPoint] >> [Zap --metadataZappable --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

#     df['etiket']='R1580V0_N'
#     df['dateo']=368660482

#     df['datyp']=5
#     df['nbits']=32

#     #write the result
#     results_file = TMP_PATH + "test_interppoint_reg_12.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "result_stations_file2cmp.std"
#     file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_12"

#     #compare results
#     res = fstpy.fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)


def test_13(plugin_test_dir,latlon_df):
    """test with 2 grids and 3 fields on each grid"""
    # open and read source
    source0 = plugin_test_dir + "2011110112_045_small"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "2011110112_048_small"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0,src_df1],ignore_index=True)

    src_df['dateo']=368660482
    latlon_df['dateo']=368660482
    #compute spooki.InterpolationHorizontalPoint

    df = spooki.InterpolationHorizontalPoint(src_df,latlon_df).compute()
    #[ReaderStd --input {sources[0]}] >> [ReaderStd --input {sources[1]}] >>
    # [ReaderCsv --input {sources[2]}] >> [spooki.InterpolationHorizontalPoint] >>
    # [Zap --metadataZappable --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --makeIP1EncodingWorkWithTests]

    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'
    # df['dateo']=368660482

    # df['datyp']=5
    # df['nbits']=32

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_13.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "result_2grids_3fields_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_13"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare,e_max=0.01)
    # fstpy.delete_file(results_file)
    assert(res)

# strangly the result file ni nj for lat and lon is reversed
def test_14(plugin_test_dir):
    """test_DanielPoints"""
    # open and read source
    source0 = plugin_test_dir + "2012022712_012_glbdiag"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar.isin(["2Z",">>","^^","!!"])].reset_index(drop=True)

    source1 = plugin_test_dir + "latlong_stn_ALL.fst"
    src_df1 = fstpy.StandardFileReader(source1,load_data=True).to_pandas()
    src_df1['ip1']=0

    src_df0.loc[:,'dateo']=368660482
    src_df1.loc[:,'dateo']=368660482

    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,src_df1,interpolation_type='bi-cubic',extrapolation_type='value', extrapolation_value=999.9).compute()
    #[ReaderStd --input {sources[0]}] >> [Select --fieldName 2Z] >> [ReaderStd --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType VALUE=999.9] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]
    df['etiket'] = 'EDYNTRP_X'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'
    #fix for reversed ni nj in results
    df.loc[df.nomvar.isin(['^^','>>']),'ni'] = 1
    df.loc[df.nomvar.isin(['^^','>>']),'nj'] = 177

    # df['datyp']=5
    # df['nbits']=32

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_14.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "result_DanielPoints_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_14"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_15(plugin_test_dir):
    """test_northPole_southPole"""
    # open and read source
    source0 = plugin_test_dir + "2012022712_012_glbdiag"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar.isin(["SN",">>","^^","!!"])].reset_index(drop=True)

    source1 = plugin_test_dir + "latlong_stn_ALL.fst"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df1['ip1']=0

    src_df0.loc[:,'dateo']=368660482
    src_df1.loc[:,'dateo']=368660482

    #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,src_df1,interpolation_type='bi-cubic',extrapolation_type='value', extrapolation_value=999.9).compute()
    #[ReaderStd --input {sources[0]}] >> [Select --fieldName SN] >> [ReaderStd --ignoreExtended --input {sources[1]}] >> [Zap --dateOfOrigin 20110210T215210 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint --interpolationType BI-CUBIC --extrapolationType VALUE=999.9] >> [WriterStd --output {destination_path}]
    df['etiket'] = 'G133K80_N'
    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'
    #fix for reversed ni nj in results
    df.loc[df.nomvar.isin(['^^','>>']),'ni'] = 1
    df.loc[df.nomvar.isin(['^^','>>']),'nj'] = 177
    # df['datyp']=5
    # df['nbits']=32
    # print('df',df)
    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_15.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "northSouthPole_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_15"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_16(plugin_test_dir,simple_input_df):
    """Test avec un fichier YinYang"""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar.isin(["TT","^>","!!"])].reset_index(drop=True)

    #zap all but !! HY
    src_df0.loc[~src_df0.nomvar.isin(['!!','HY']),'dateo']=404008736
    simple_input_df['dateo']=404008736
     #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,simple_input_df,interpolation_type='bi-linear',extrapolation_type='value', extrapolation_value=99.9).compute()
    #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20150805T094230 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint --interpolationType BI-LINEAR --extrapolationType VALUE=99.9] >> [WriterStd --output {destination_path}]

    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'
    # df['datyp']=5
    # df['nbits']=32

    df = convip(df,nomvar='',style=rmn.CONVIP_ENCODE)

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_16.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "InterpGridUtoGridY_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_16"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_17(plugin_test_dir,latlon_yy_df):
    """Test avec un fichier YinYang en entree et des lat-lon sur les grilles Yin et Yang."""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar.isin(["TT","^>","!!"])].reset_index(drop=True)

    #zap all but !! HY
    src_df0.loc[~src_df0.nomvar.isin(['!!','HY']),'dateo']=404008736

    latlon_yy_df['dateo']=404008736
     #compute spooki.InterpolationHorizontalPoint
    df = spooki.InterpolationHorizontalPoint(src_df0,latlon_yy_df,interpolation_type='bi-linear',extrapolation_type='value', extrapolation_value=99.9).compute()
    #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >> [ReaderCsv --input {sources[1]}] >> [Zap --dateOfOrigin 20150805T094230 --doNotFlagAsZapped] >> [spooki.InterpolationHorizontalPoint --interpolationType BI-LINEAR --extrapolationType VALUE=99.9] >> [WriterStd --output {destination_path}]

    df.loc[df.nomvar == '^^','etiket'] = '__INTHPTX'
    df.loc[df.nomvar == '>>','etiket'] = '__INTHPTX'
    # df['datyp']=5
    # df['nbits']=32

    df = convip(df,nomvar='',style=rmn.CONVIP_ENCODE)

    #write the result
    results_file = TMP_PATH + "test_interppoint_reg_17.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "InterpGridU_manyPts_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalPoint/" +  "result_test_17"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
