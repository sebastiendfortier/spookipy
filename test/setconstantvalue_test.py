# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/SetConstantValue/testsFiles/'


def test_1(plugin_test_dir):
    """Création d'un champ 3D nommé RES identique au champ UU du fichier d'entrée avec 0.33323 comme valeurs."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0, ['UU'])

    # compute SetConstantValue
    resuu_df = spookipy.SetConstantValue(
        uu_df, value=0.33323, nomvar_out='UU*').compute()

    vv_df = fstpy.select_with_meta(src_df0, ['VV'])

    # compute SetConstantValue
    resvv_df = spookipy.SetConstantValue(
        vv_df, value=0.33323, nomvar_out='VV*').compute()
    # [ReaderStd --input {sources[0]}] >>
    # ( ([Select --fieldName UU] >> [SetConstantValue --value 0.33323 --outputFieldName UU*]) +
    # ([Select --fieldName VV] >> [SetConstantValue --value 0.33323 --outputFieldName VV*]) ) >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df = pd.concat([resuu_df, resvv_df], ignore_index=True)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "assign_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare,columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Création d'un champ 2D identique au champ UU du fichier d'entrée avec 0 comme valeur (MININDEX)."""
    # open and read source
    source0 = plugin_test_dir + "generate2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0, ['UU'])
    # compute SetConstantValue
    df = spookipy.SetConstantValue(
        uu_df,
        min_index=True,
        bi_dimensionnal=True).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetConstantValue --value MININDEX --bidimensional] >>
    # [Zap --fieldName RES --pdsLabel GENERATE2D --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    df.loc[df.nomvar == 'UU', 'nomvar'] = 'RES'
    df.loc[:, 'etiket'] = 'GENERATE2D'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "g2d1_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_3(plugin_test_dir):
    """Création d'un champ 2D identique au champ UU du fichier d'entrée avec MAXINDEX comme valeurs"""
    # open and read source
    source0 = plugin_test_dir + "2011072100_006_eta_small"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0, ['UU'])

    # compute SetConstantValue
    df = spookipy.SetConstantValue(
        uu_df,
        max_index=True,
        bi_dimensionnal=True).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [Zap --metadataZappable --pdsLabel 580V0N] >>
    # [SetConstantValue --value MAXINDEX --bidimensional] >> [Zap --fieldName RES --pdsLabel GENERATE2D --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    df.loc[df.nomvar == 'UU', 'nomvar'] = 'RES'
    df.loc[df.nomvar == 'RES', 'etiket'] = 'GENERATE2D'
    df.loc[df.nomvar.isin(['^^', '>>']), 'etiket'] = '580V0N'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "g2d2_file2cmp.std+20210517"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_4(plugin_test_dir):
    """Création d'un champ 2D identique au champ UU du fichier d'entrée avec 1.0 comme valeurs"""
    # open and read source
    source0 = plugin_test_dir + "generate2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0, ['UU'])

    # compute SetConstantValue
    df = spookipy.SetConstantValue(
        uu_df, value=-1, bi_dimensionnal=True).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [SetConstantValue --value -1.0 --bidimensional] >>
    # [Zap --fieldName RES --pdsLabel GENERATE2D --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    df.loc[df.nomvar == 'UU', 'nomvar'] = 'RES'
    df.loc[df.nomvar == 'RES', 'etiket'] = 'GENERATE2D'
    df.loc[df.nomvar.isin(['^^', '>>']), 'etiket'] = '580V0N'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "g2d3_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_5(plugin_test_dir):
    """Création de 2 champs 2D identiques au champ UU, le premier avec MININDEX comme valeurs et le deuxième avec MAXINDEX."""
    # open and read source
    source0 = plugin_test_dir + "generate2D_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0, ['UU'])

    # compute SetConstantValue
    df1 = spookipy.SetConstantValue(
        uu_df,
        min_index=True,
        bi_dimensionnal=True).compute()
    df1.loc[df1.nomvar == 'UU', 'nomvar'] = 'KBAS'
    df1.loc[df1.nomvar == 'KBAS', 'etiket'] = 'GENERATE2D'
    df2 = spookipy.SetConstantValue(
        uu_df,
        max_index=True,
        bi_dimensionnal=True).compute()
    df2.loc[df2.nomvar == 'UU', 'nomvar'] = 'KTOP'
    df2.loc[df2.nomvar == 'KTOP', 'etiket'] = 'GENERATE2D'
    # [ReaderStd --input {sources[0]}] >>
    # [Select --fieldName UU] >> ( ([SetConstantValue --value MININDEX --bidimensional] >> [Zap --fieldName KBAS --pdsLabel GENERATE2D --doNotFlagAsZapped]) +
    # ([SetConstantValue --value MAXINDEX --bidimensional] >> [Zap --fieldName KTOP --pdsLabel GENERATE2D --doNotFlagAsZapped]) ) >>
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    df = pd.concat([df1, df2], ignore_index=True)
    # df.loc[df.nomvar.isin(['^^','>>']),'etiket'] = '580V0N'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "g2d4_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir):
    """Création d'un champ 2D identique au champ UU du fichier d'entrée avec NBLEVELS comme valeurs"""
    # open and read source
    source0 = plugin_test_dir + "2011072100_006_eta_small"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    uu_df = fstpy.select_with_meta(src_df0, ['UU'])
    # compute SetConstantValue
    df = spookipy.SetConstantValue(
        uu_df,
        nb_levels=True,
        bi_dimensionnal=True,
        nomvar_out='RES').compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [Zap --metadataZappable --pdsLabel 580V0N] >>
    # [SetConstantValue --value NBLEVELS --bidimensional --outputFieldName RES] >>
    # [WriterStd --output {destination_path} --ignoreExtended --makeIP1EncodingWorkWithTests]

    df.loc[df.nomvar.isin(['^^', '>>']), 'etiket'] = '580V0N'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "nbLevels_file2cmp.std+20210517"

    # compare results
    res = fstcomp(results_file, file_to_compare,columns=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4'])
    fstpy.delete_file(results_file)
    assert(res)

def test_7(plugin_test_dir):
    """2 groupes de TT avec dates d'origine differentes mais dates de validity identiques, option reduce_df = True"""

    source  = source0 = plugin_test_dir + "Regpres_TTHUES_differentDateoSameDatev.std"
    src_df  = fstpy.StandardFileReader(source).to_pandas()
    tt_df   = fstpy.select_with_meta(src_df, ['TT'])

    df      = spookipy.SetConstantValue(tt_df,
                                        nb_levels=True,
                                        bi_dimensionnal=True,
                                        nomvar_out='RES',
                                        reduce_df = True).compute()
    
    # spooki_run.py "[ReaderStd --input Regpres_TTHUES_differentDateoSameDatev.std] >> 
    # [Select --fieldName TT] >> 
    # [SetConstantValue --value NBLEVELS --bidimensional --outputFieldName RES --plugin_language CPP] >> 
    # [WriterStd --output SetCst.std]"

     # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_20.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    file_to_compare = plugin_test_dir + "Regpres_diffDateoSameDatev_test7_file2cmp.std"

    # compare results 
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
