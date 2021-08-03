# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import pandas as pd
import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/SetConstantValue/testsFiles/'


def test_1(plugin_test_dir):
    """Test #1 :  Création d'un champ 3D nommé RES identique au champ UU du fichier d'entrée avec 0.33323 comme valeurs."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0,['UU'])

    #compute SetConstantValue
    resuu_df = spooki.SetConstantValue(uu_df, value=0.33323, nomvar_out='UU*').compute()

    vv_df = fstpy.select_with_meta(src_df0,['VV'])

    #compute SetConstantValue
    resvv_df = spooki.SetConstantValue(vv_df, value=0.33323, nomvar_out='VV*').compute()
    #[ReaderStd --input {sources[0]}] >> 
    # ( ([Select --fieldName UU] >> [SetConstantValue --value 0.33323 --outputFieldName UU*]) + 
    # ([Select --fieldName VV] >> [SetConstantValue --value 0.33323 --outputFieldName VV*]) ) >> 
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df = pd.concat([resuu_df,resvv_df],ignore_index=True)
    df.loc[:,'etiket'] ='SETVAL'

    #write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "assign_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_2(plugin_test_dir):
    """Test #2 :  Création d'un champ 2D identique au champ UU du fichier d'entrée avec 0 comme valeur (MININDEX)."""
    # open and read source
    source0 = plugin_test_dir + "generate2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0,['UU'])
    #compute SetConstantValue
    df = spooki.SetConstantValue(uu_df, min_index=True, bi_dimensionnal=True).compute()
    #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetConstantValue --value MININDEX --bidimensional] >> 
    # [Zap --fieldName RES --pdsLabel GENERATE2D --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    df.loc[df.nomvar=='UU','nomvar'] = 'RES'
    df.loc[:,'etiket'] = 'GENERATE2D'

    #write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "g2d1_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_3(plugin_test_dir):
    """Test #3 :  Création d'un champ 2D identique au champ UU du fichier d'entrée avec MAXINDEX comme valeurs"""
    # open and read source
    source0 = plugin_test_dir + "2011072100_006_eta_small"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0,['UU'])
    
    #compute SetConstantValue
    df = spooki.SetConstantValue(uu_df, max_index=True, bi_dimensionnal=True).compute()
    #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [Zap --metadataZappable --pdsLabel 580V0N] >> 
    # [SetConstantValue --value MAXINDEX --bidimensional] >> [Zap --fieldName RES --pdsLabel GENERATE2D --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    df.loc[df.nomvar=='UU','nomvar'] = 'RES'
    df.loc[df.nomvar=='RES','etiket'] = 'GENERATE2D'
    df.loc[df.nomvar.isin(['^^','>>']),'etiket'] = '580V0N'

    #write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "g2d2_file2cmp.std+20210517"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_4(plugin_test_dir):
    """Test #4 :  Création d'un champ 2D identique au champ UU du fichier d'entrée avec 1.0 comme valeurs"""
    # open and read source
    source0 = plugin_test_dir + "generate2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0,['UU'])

    #compute SetConstantValue
    df = spooki.SetConstantValue(uu_df, value=-1, bi_dimensionnal=True).compute()
    #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetConstantValue --value -1.0 --bidimensional] >> 
    # [Zap --fieldName RES --pdsLabel GENERATE2D --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    df.loc[df.nomvar=='UU','nomvar'] = 'RES'
    df.loc[df.nomvar=='RES','etiket'] = 'GENERATE2D'
    df.loc[df.nomvar.isin(['^^','>>']),'etiket'] = '580V0N'

    #write the result
    results_file = TMP_PATH + "test_4.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "g2d3_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_5(plugin_test_dir):
    """Test #5 :  Création de 2 champs 2D identiques au champ UU, le premier avec MININDEX comme valeurs et le deuxième avec MAXINDEX."""
    # open and read source
    source0 = plugin_test_dir + "generate2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0,['UU'])

    #compute SetConstantValue
    df1 = spooki.SetConstantValue(uu_df, min_index=True, bi_dimensionnal=True).compute()
    df1.loc[df1.nomvar=='UU','nomvar'] = 'KBAS'
    df1.loc[df1.nomvar=='KBAS','etiket'] = 'GENERATE2D'
    df2 = spooki.SetConstantValue(uu_df, max_index=True, bi_dimensionnal=True).compute()
    df2.loc[df2.nomvar=='UU','nomvar'] = 'KTOP'
    df2.loc[df2.nomvar=='KTOP','etiket'] = 'GENERATE2D'
    #[ReaderStd --input {sources[0]}] >> 
    # [Select --fieldName UU] >> ( ([SetConstantValue --value MININDEX --bidimensional] >> [Zap --fieldName KBAS --pdsLabel GENERATE2D --doNotFlagAsZapped]) + 
    # ([SetConstantValue --value MAXINDEX --bidimensional] >> [Zap --fieldName KTOP --pdsLabel GENERATE2D --doNotFlagAsZapped]) ) >> 
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    df = pd.concat([df1,df2],ignore_index=True)
    # df.loc[df.nomvar.isin(['^^','>>']),'etiket'] = '580V0N'

    #write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "g2d4_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_6(plugin_test_dir):
    """Test #6 :  Création d'un champ 2D identique au champ UU du fichier d'entrée avec NBLEVELS comme valeurs"""
    # open and read source
    source0 = plugin_test_dir + "2011072100_006_eta_small"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0,['UU'])
    #compute SetConstantValue
    df = spooki.SetConstantValue(uu_df, nb_levels=True, bi_dimensionnal=True, nomvar_out='RES').compute()
    #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [Zap --metadataZappable --pdsLabel 580V0N] >> 
    # [SetConstantValue --value NBLEVELS --bidimensional --outputFieldName RES] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]
    
    df.loc[df.nomvar=='RES','etiket'] = 'SETVAL'
    df.loc[df.nomvar.isin(['^^','>>']),'etiket'] = '580V0N'

    #write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "nbLevels_file2cmp.std+20210517"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)
