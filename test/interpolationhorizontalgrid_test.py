# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import rpnpy.librmn.all as rmn
import spookipy
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
    df = spookipy.InterpolationHorizontalGrid(
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
    #"[ReaderStd --input {sources[0]}] >>
    # [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 191,141 -p 79.0,117.0,57150.0,21.0 --interpolationType BI-LINEAR --extrapolationType MAXIMUM] >>
    # [Zap --nbitsForDataStorage E32]>>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]"

    df = spookipy.convip(df, style=rmn.CONVIP_ENCODE_OLD)
    
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "interpolationHoriz_file2cmp.std"

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
    df      = spookipy.InterpolationHorizontalGrid( src_df0,
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
    #"[ReaderStd --input {sources[0]}] >>
    # [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 191,141 -p 79.0,117.0,57150.0,21.0 --interpolationType BI-LINEAR --extrapolationType MAXIMUM] >>
    # [Zap --nbitsForDataStorage E32]>>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]",

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "interpolationHorizScalar_file2cmp.std"

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
    df      = spookipy.InterpolationHorizontalGrid( src_df0,
                                                    method             = 'user',
                                                    grtyp              = 'N',
                                                    ni                 = 191,
                                                    nj                 = 141,
                                                    param1             = 79.0,
                                                    param2             = 117.0,
                                                    param3             = 57150.0,
                                                    param4             = 21.0,
                                                    interpolation_type ='bi-linear',
                                                    extrapolation_type ='maximum').compute()
    #"[ReaderStd --input {sources[0]}] >>
    # [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 191,141 -p 79.0,117.0,57150.0,21.0 --interpolationType BI-LINEAR --extrapolationType MAXIMUM] >>
    # [Zap --nbitsForDataStorage E32]>>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]"

    df = spookipy.convip(df, style=rmn.CONVIP_ENCODE_OLD)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "interpolationHorizVectorial_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_5(plugin_test_dir):
    """Interpolation with FIELD_DEFINED"""
    # open and read source
    source0 = plugin_test_dir + "TTUUVVKTRT.std"

    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.InterpolationHorizontalGrid
    df      = spookipy.InterpolationHorizontalGrid( src_df0,
                                                    method='field',
                                                    nomvar='RT',
                                                    interpolation_type='nearest',
                                                    extrapolation_type='nearest').compute()
    # [ReaderStd --input {sources[0]}] >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName RT --interpolationType NEAREST --extrapolationType NEAREST] >>
    # [WriterStd --output {destination_path} --makeIP1EncodingWorkWithTests]

    df = spookipy.convip(df, style=rmn.CONVIP_ENCODE_OLD)
    
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "fieldDefined_file2cmp.std"

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
    # compute spookipy.InterpolationHorizontalGrid
    df      = spookipy.InterpolationHorizontalGrid( src_df0,
                                                    method='field',
                                                    nomvar='RT',
                                                    interpolation_type='nearest',
                                                    extrapolation_type='nearest').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,RT] >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName RT --interpolationType NEAREST --extrapolationType NEAREST] >>
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "fieldDefinedWithHY_file2cmp.std"

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

    src_df  = pd.concat([src_df0, src_df1], ignore_index=True)

    # print(src_df[['nomvar','ni','nj','ip1','ip2','ig1','ig2']])
    # compute spookipy.InterpolationHorizontalGrid
    df      = spookipy.InterpolationHorizontalGrid(src_df,
                                                   method='field',
                                                   nomvar='ES',
                                                   interpolation_type='bi-cubic',
                                                   extrapolation_type='nearest').compute()
    # ([ReaderStd --input {sources[0]}] >> [Select --fieldName TT]) +
    # ([ReaderStd --input {sources[1]}] >> [Select --fieldName ES]) >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName ES --interpolationType BI-CUBIC --extrapolationType NEAREST] >>
    # [WriterStd --output {destination_path}]

    # On force l'encodage pour agir comme le WriterStd 
    df = spookipy.convip(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "InterpHorizGridUtoZ_rmn19_file2cmp.std+20210517"

    # compare results
    res = fstcomp(results_file, file_to_compare)
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

    # compute spookipy.InterpolationHorizontalGrid
    df     = spookipy.InterpolationHorizontalGrid(src_df,
                                                  method='field',
                                                  nomvar='ES',
                                                  interpolation_type='bi-cubic',
                                                  extrapolation_type='nearest').compute()
    # "([ReaderStd --input {sources[0]}] >> [Select --fieldName ES]) +
    # ([ReaderStd --input {sources[1]}] >> [Select --fieldName TT]) >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName ES --interpolationType BI-CUBIC --extrapolationType NEAREST] >>
    # [Zap --nbitsForDataStorage E32]>>[WriterStd --output {destination_path} ]",
 
    # On force l'encodage pour agir comme le WriterStd 
    df = spookipy.convip(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "InterpHorizGridZtoU_file2cmp.std+20231227"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
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

    src_df  = pd.concat([src_df0, src_df1], ignore_index=True)

    # compute spookipy.InterpolationHorizontalGrid
    df      = spookipy.InterpolationHorizontalGrid(src_df,
                                                   method='field',
                                                   nomvar='TT',
                                                   interpolation_type='bi-cubic',
                                                   extrapolation_type='nearest').compute()
    # ([ReaderStd --input {sources[0]}] >> [Select --fieldName UU,VV]) +
    # ([ReaderStd --input {sources[1]}] >> [Select --fieldName TT]) >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName TT --interpolationType BI-CUBIC --extrapolationType NEAREST] >>
    # [Select --fieldName UU,VV] >>
    # [WriterStd --output {destination_path} ]

    # On selection UU,VV car par defaut (sans option output_fields) tous les champs sont resortis.
    df = fstpy.select_with_meta(df, ['UU', 'VV'])

    # On force l'encodage pour agir comme le WriterStd 
    df = spookipy.convip(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir +  "InterpHorizGridUtoZ_UUVV_file2cmp.std+20210517"
    
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

    src_df  = pd.concat([src_df0, src_df1], ignore_index=True)

    # compute spookipy.InterpolationHorizontalGrid
    df      = spookipy.InterpolationHorizontalGrid(src_df,
                                                   method='field',
                                                   nomvar='TT',
                                                   interpolation_type='bi-cubic',
                                                   extrapolation_type='nearest').compute()
    # ([ReaderStd --input {sources[0]}] >> [Select --fieldName TT]) +
    # ([ReaderStd --input {sources[1]}] >> [Select --fieldName UU,VV]) >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName TT --interpolationType BI-CUBIC --extrapolationType NEAREST] >>
    # [Select --fieldName UU,VV] >>
    # [WriterStd --output {destination_path} ]

    # On selection UU,VV car par defaut (sans option output_fields) tous les champs sont resortis.
    df = fstpy.select_with_meta(df, ['UU', 'VV'])

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "InterpHorizGridZtoU_UUVV_file2cmp.std"

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

    src_df  = pd.concat([src_df0, src_df1], ignore_index=True)
    
    # compute spookipy.InterpolationHorizontalGrid
    df = spookipy.InterpolationHorizontalGrid(
        src_df,
        method='field',
        nomvar='ES',
        interpolation_type='bi-cubic',
        extrapolation_type='nearest').compute()
    # ([ReaderStd --input {sources[0]}] >> [Select --fieldName TT,UU,VV]) +
    # ([ReaderStd --input {sources[1]}] >> [Select --fieldName ES]) >>
    # [InterpolationHorizontalGrid -m FIELD_DEFINED --fieldName ES 
    #                              --interpolationType BI-CUBIC --extrapolationType NEAREST] >> 
    # [WriterStd --output {destination_path} ]


    # On force l'encodage pour agir comme le WriterStd 
    df = spookipy.convip(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "InterpHorizGridUtoZ_manyToctocs_file2cmp.std"

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

    # compute spookipy.InterpolationHorizontalGrid
    df      = spookipy.InterpolationHorizontalGrid( src_df0,    
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
    # [InterpolationHorizontalGrid -m USER_DEFINED --gridType TYPE_N --xyDimensions 152,120 
    #                         -p 52.0,120.0,50000.0,21.0 --interpolationType NEAREST --extrapolationType VALUE=-888.8] >>
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "extrapolationNegativeValue_file2cmp.std+20231222"

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

    src_df  = pd.concat([src_df0, src_df1], ignore_index=True)

    # compute spookipy.InterpolationHorizontalGrid
    df      = spookipy.InterpolationHorizontalGrid( src_df,
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

    # On selection UU,VV car par defaut (sans option output_fields) tous les champs sont resortis.
    df = fstpy.select_with_meta(df, ['UU', 'VV'])

    # On force l'encodage pour agir comme le WriterStd
    df = spookipy.convip(df)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_14.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "InterpHorizGridUtoZ_UUVV_file2cmp.std+20210517"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
