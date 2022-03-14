# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pandas as pd
import pytest
import rpnpy.librmn.all as rmn
import spookipy.all as spooki
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + "InterpolationHorizontalGrid/testsFiles/"


def test_1(plugin_test_dir):
    """Interpolation with multiple different input grid"""
    # open and read source

    source0 = plugin_test_dir + "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    # compute Pressure
    df = spooki.InterpolationHorizontalGrid(
        src_df0,
        method='user',
        grtyp='N',
        ni=191,
        nj=141,
        param1=79.0,
        param2=117.0,
        param3=57150.0,
        param4=21.0,
        interpolation_type='bi-linear',
        extrapolation_type='maximum').compute()
    # "[ReaderStd --input {sources[0]}] >>
    # [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 191,141 -p 79.0,117.0,57150.0,21.0 --interpolationType BI-LINEAR --extrapolationType MAXIMUM] >>
    # [Zap --nbitsForDataStorage E32]>>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]"
    # df.loc[:,'typvar'] = 'PI'
    df.loc[df.etiket == 'R1558V0N', 'etiket'] = 'R1558V0_N'
    df.loc[df.etiket == 'G0928V4N', 'etiket'] = 'G0928V4_N'
    df.loc[df.etiket == 'MXWIND', 'etiket'] = 'MXWIND__X'
    df.loc[df.typvar == 'P', 'typvar'] = 'PI'
    # df['datyp'] = 5
    # df['nbits'] = 32
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "interpolationHoriz_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_1"
    # print(file_to_compare)

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.126)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Interpolation with scalar fields only"""
    # open and read source
    source0 = plugin_test_dir + "4panneaux_input4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Pressure
    df = spooki.InterpolationHorizontalGrid(
        src_df0,
        method='user',
        grtyp='N',
        ni=191,
        nj=141,
        param1=79.0,
        param2=117.0,
        param3=57150.0,
        param4=21.0,
        interpolation_type='bi-linear',
        extrapolation_type='maximum').compute()
    # "configuration": "[ReaderStd --input {sources[0]}] >>
    # [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 191,141 -p 79.0,117.0,57150.0,21.0 --interpolationType BI-LINEAR --extrapolationType MAXIMUM] >>
    # [Zap --nbitsForDataStorage E32]>>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]",
    df.loc[:, 'typvar'] = 'PI'
    df.loc[df.etiket == 'R1558V0N', 'etiket'] = 'R1558V0_N'
    df.loc[df.etiket == 'G0928V4N', 'etiket'] = 'G0928V4_N'
    df.loc[df.etiket == 'MXWIND', 'etiket'] = 'MXWIND__X'
    # df['datyp'] = 5
    # df['nbits'] = 32
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "interpolationHorizScalar_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_2"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_3(plugin_test_dir):
    """Interpolation with vectorial fields only"""
    # open and read source
    source0 = plugin_test_dir + "inputUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Pressure
    df = spooki.InterpolationHorizontalGrid(
        src_df0,
        method='user',
        grtyp='N',
        ni=191,
        nj=141,
        param1=79.0,
        param2=117.0,
        param3=57150.0,
        param4=21.0,
        interpolation_type='bi-linear',
        extrapolation_type='maximum').compute()
    # "[ReaderStd --input {sources[0]}] >>
    # [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 191,141 -p 79.0,117.0,57150.0,21.0 --interpolationType BI-LINEAR --extrapolationType MAXIMUM] >>
    # [Zap --nbitsForDataStorage E32]>>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]"
    df.loc[:, 'typvar'] = 'PI'
    df.loc[df.etiket == 'R1558V0N', 'etiket'] = 'R1558V0_N'
    df.loc[df.etiket == 'G0928V4N', 'etiket'] = 'G0928V4_N'
    df.loc[df.etiket == 'MXWIND', 'etiket'] = 'MXWIND__X'
    # df['datyp'] = 5
    # df['nbits'] = 32
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "interpolationHorizVectorial_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_3"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_5(plugin_test_dir):
    """Interpolation with FIELD_DEFINED"""
    # open and read source
    source0 = plugin_test_dir + "TTUUVVKTRT.std"

    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.InterpolationHorizontalGrid
    df = spooki.InterpolationHorizontalGrid(
        src_df0,
        method='field',
        nomvar='RT',
        interpolation_type='nearest',
        extrapolation_type='nearest').compute()
    # [ReaderStd --input {sources[0]}] >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName RT --interpolationType NEAREST --extrapolationType NEAREST] >>
    # [WriterStd --output {destination_path} --makeIP1EncodingWorkWithTests]

    df = spooki.convip(df, style=rmn.CONVIP_ENCODE_OLD)
    df.loc[(~df.nomvar.isin(['KT','PT','RT'])) & (df.typvar == 'P'), 'typvar'] = 'PI'

    # df.loc[:,'datyp'] = 5
    # df.loc[:,'nbits'] = 32

    # print(df[['nomvar','etiket','ip1','ip2','ig1','ig2']].to_string())
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "fieldDefined_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_5"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir):
    """Interpolation with FIELD_DEFINED, make sure HY follow"""
    # open and read source
    source0 = plugin_test_dir + "TT_RT_reghyb"

    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.select_with_meta(src_df0, ['TT', 'RT'])
    # compute spooki.InterpolationHorizontalGrid
    df = spooki.InterpolationHorizontalGrid(
        src_df0,
        method='field',
        nomvar='RT',
        interpolation_type='nearest',
        extrapolation_type='nearest').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,RT] >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName RT --interpolationType NEAREST --extrapolationType NEAREST] >>
    # [WriterStd --output {destination_path} ]

    df.loc[(df.nomvar!='RT') & (df.typvar == 'P'), 'typvar'] = 'PI'
    # df['datyp'] = 5
    # df['nbits'] = 32
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "fieldDefinedWithHY_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_6"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_7(plugin_test_dir):
    """Interpolation d'un champ scalaire (TT) d'une grille U vers une grille Z"""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"

    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ["TT"])

    source1 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df1 = fstpy.select_with_meta(src_df1, ["ES"])

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)

    # print(src_df[['nomvar','ni','nj','ip1','ip2','ig1','ig2']])
    # compute spooki.InterpolationHorizontalGrid
    df = spooki.InterpolationHorizontalGrid(
        src_df,
        method='field',
        nomvar='ES',
        interpolation_type='bi-cubic',
        extrapolation_type='nearest').compute()
    # ([ReaderStd --input {sources[0]}] >> [Select --fieldName TT]) +
    # ([ReaderStd --input {sources[1]}] >> [Select --fieldName ES]) >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName ES --interpolationType BI-CUBIC --extrapolationType NEAREST] >>
    # [WriterStd --output {destination_path}]
    df.loc[(df.nomvar=='TT') & (df.typvar == 'P'), 'typvar'] = 'PI'

    # df['datyp'] = 5
    # df['nbits'] = 32
    # df.loc[df.nomvar=='!!','nbits']=64

    df = spooki.convip(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "InterpHorizGridUtoZ_rmn19_file2cmp.std+20210517"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_7"

    # compare results
    res = fstcomp(results_file, file_to_compare, exclude_meta=True)
    fstpy.delete_file(results_file)
    assert(res)


def test_8(plugin_test_dir):
    """Interpolation d'un champ scalaire (TT) d'une grille Z vers une grille U"""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"

    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ["ES"])

    source1 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"

    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df1 = fstpy.select_with_meta(src_df1, ["TT"])

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)

    # compute spooki.InterpolationHorizontalGrid
    df = spooki.InterpolationHorizontalGrid(
        src_df,
        method='field',
        nomvar='ES',
        interpolation_type='bi-cubic',
        extrapolation_type='nearest').compute()
    # "([ReaderStd --input {sources[0]}] >> [Select --fieldName ES]) +
    # ([ReaderStd --input {sources[1]}] >> [Select --fieldName TT]) >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName ES --interpolationType BI-CUBIC --extrapolationType NEAREST] >>
    # [Zap --nbitsForDataStorage E32]>>[WriterStd --output {destination_path} ]",
    df.loc[df.nomvar.isin(['TT','P0']) & (df.typvar == 'P'), 'typvar'] = 'PI'
    # for i in df.index:
    #     if df.at[i,'nomvar'] != 'ES':
    # df['datyp'] = 5
    # df['nbits'] = 32
    df.loc[df.nomvar == '!!', 'nbits'] = 64
    df = spooki.convip(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "InterpHorizGridZtoU_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_8"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_9(plugin_test_dir):
    """Interpolation de champs vectoriels (UU,VV) d'une grille U vers une grille Z"""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ["UU", "VV"])

    source1 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df1 = fstpy.select_with_meta(src_df1, ["TT"])

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)

    # compute spooki.InterpolationHorizontalGrid
    df = spooki.InterpolationHorizontalGrid(
        src_df,
        method='field',
        nomvar='TT',
        interpolation_type='bi-cubic',
        extrapolation_type='nearest').compute()
    # ([ReaderStd --input {sources[0]}] >> [Select --fieldName UU,VV]) +
    # ([ReaderStd --input {sources[1]}] >> [Select --fieldName TT]) >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName TT --interpolationType BI-CUBIC --extrapolationType NEAREST] >>
    # [Select --fieldName UU,VV] >>
    # [WriterStd --output {destination_path} ]

    df = fstpy.select_with_meta(df, ['UU', 'VV'])
    df.loc[df.typvar == 'P', 'typvar'] = 'PI'

    # df['datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    df = spooki.convip(df)
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "InterpHorizGridUtoZ_UUVV_file2cmp.std+20210517"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_9"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_10(plugin_test_dir):
    """Interpolation de champs vectoriels (UU,VV) d'une grille Z vers une grille U"""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ["TT"])

    source1 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df1 = fstpy.select_with_meta(src_df1, ["UU", "VV"])

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)

    # compute spooki.InterpolationHorizontalGrid
    df = spooki.InterpolationHorizontalGrid(
        src_df,
        method='field',
        nomvar='TT',
        interpolation_type='bi-cubic',
        extrapolation_type='nearest').compute()
    # ([ReaderStd --input {sources[0]}] >> [Select --fieldName TT]) +
    # ([ReaderStd --input {sources[1]}] >> [Select --fieldName UU,VV]) >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName TT --interpolationType BI-CUBIC --extrapolationType NEAREST] >>
    # [Select --fieldName UU,VV] >>
    # [WriterStd --output {destination_path} ]

    df = fstpy.select_with_meta(df, ['UU', 'VV'])
    df = df.loc[df.nomvar != 'P0']
    df.loc[df.typvar == 'P', 'typvar'] = 'PI'
    # df['datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits']=32
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "InterpHorizGridZtoU_UUVV_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_10"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_11(plugin_test_dir):
    """Interpolation de champs vectoriels et scalaires d'une grille Z vers une grille U avec un fichier a interpoler contenant 2 toctocs."""
    # open and read source
    source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ["TT", "UU", "VV"])

    source1 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df1 = fstpy.select_with_meta(src_df1, ["ES"])

    # source2 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"
    # src_df2 = fstpy.StandardFileReader(source2)

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)
    # print('src_df\n',src_df[['nomvar', 'typvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'datyp', 'nbits', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4','grid']].to_string())
    # compute spooki.InterpolationHorizontalGrid
    df = spooki.InterpolationHorizontalGrid(
        src_df,
        method='field',
        nomvar='ES',
        interpolation_type='bi-cubic',
        extrapolation_type='nearest').compute()
    # ([ReaderStd --input {sources[0]}] >> [Select --fieldName TT,UU,VV]) +
    # ([ReaderStd --input {sources[1]}] >> [Select --fieldName ES]) >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName ES --interpolationType BI-CUBIC --extrapolationType NEAREST] >> [WriterStd --output {destination_path} ]

    # df['datyp'] = 5
    # df[df.nomvar!='!!','nbits'] = 32
    # df.loc[df.nomvar=='!!','nbits']=64
    df = spooki.convip(df)
    df.loc[(df.nomvar!='ES') & (df.typvar == 'P'), 'typvar'] = 'PI'

    # print('df\n',df[['nomvar', 'typvar', 'etiket', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'datyp', 'nbits', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4','grid']].to_string())
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "InterpHorizGridUtoZ_manyToctocs_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_11"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.6)
    fstpy.delete_file(results_file)
    assert(res)


def test_13(plugin_test_dir):
    """test extrapolation with negative value"""
    # open and read source
    source0 = plugin_test_dir + "TT_RT_reghyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ["TT"])

    # compute spooki.InterpolationHorizontalGrid
    df = spooki.InterpolationHorizontalGrid(
        src_df0,
        method='user',
        grtyp='N',
        ni=152,
        nj=120,
        param1=52.0,
        param2=120.0,
        param3=50000.0,
        param4=21.0,
        interpolation_type='nearest',
        extrapolation_type='value',
        extrapolation_value=-888.8).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName TT] >>
    # [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 152,120 -p 52.0,120.0,50000.0,21.0 --interpolationType NEAREST --extrapolationType VALUE=-888.8] >>
    #  [WriterStd --output {destination_path} ]

    # df['datyp'] = 5
    # df['nbits'] = 32
    # df.loc[df.nomvar=='!!','nbits']=64

    df = df.loc[df.nomvar != 'HY']
    df.loc[df.typvar == 'P', 'typvar'] = 'PI'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "extrapolationNegativeValue_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_13"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_14(plugin_test_dir):
    """Interpolation de champs vectoriels (UU,VV) d'une grille U vers une grille Z en parallele"""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ["UU", "VV"])

    source1 = plugin_test_dir + "2015072100_240_TTESUUVV_GridZ.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df1 = fstpy.select_with_meta(src_df1, ["TT"])

    src_df = pd.concat([src_df0, src_df1], ignore_index=True)

    # compute spooki.InterpolationHorizontalGrid
    df = spooki.InterpolationHorizontalGrid(
        src_df,
        method='field',
        nomvar='TT',
        interpolation_type='bi-cubic',
        extrapolation_type='nearest',
        parallel=True).compute()
    # ([ReaderStd --input {sources[0]}] >> [Select --fieldName UU,VV]) +
    # ([ReaderStd --input {sources[1]}] >> [Select --fieldName TT]) >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName TT --interpolationType BI-CUBIC --extrapolationType NEAREST] >>
    # [Select --fieldName UU,VV] >>
    # [WriterStd --output {destination_path} ]

    df = fstpy.select_with_meta(df, ['UU', 'VV'])
    df.loc[df.typvar == 'P', 'typvar'] = 'PI'
    # df['datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    df = spooki.convip(df)
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "InterpHorizGridUtoZ_UUVV_file2cmp.std+20210517"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/InterpolationHorizontalGrid/result_test_9"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
