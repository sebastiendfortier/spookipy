# -*- coding: utf-8 -*-
import pandas as pd
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets
pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/AddElementsByPoint/testsFiles/'


def test_1(plugin_test_dir):
    """Additionne des champs 2D."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute AddElementsByPoint
    df = spookipy.AddElementsByPoint(src_df0, nomvar_out='ACCU').compute()
    df['etiket'] = 'ADDFIELDS'
    # [ReaderStd --input {sources[0]}] >> [AddElementsByPoint --outputFieldName ACCU] >> [Zap --pdsLabel ADDFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "add2d_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Additionne des champs 3D."""
    # open and read source
    source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute AddElementsByPoint
    df = spookipy.AddElementsByPoint(src_df0, nomvar_out='ACCU').compute()
    df['etiket'] = 'ADDFIELDS'
    # [ReaderStd --input {sources[0]}] >> [AddElementsByPoint --outputFieldName ACCU] >> [Zap --pdsLabel ADDFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "add3d_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_3(plugin_test_dir):
    """Utilisation de --outputFieldName avec une valeur > 4 caractères."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.AddElementsByPointError):
        # compute AddElementsByPoint
        _ = spookipy.AddElementsByPoint(
            src_df0, nomvar_out='TROPLONG').compute()
        # [ReaderStd --input {sources[0]}] >> [AddElementsByPoint --outputFieldName TROPLONG]


def test_4(plugin_test_dir):
    """Essaie d'additionner lorsqu'il y a seulement 1 champ en entrée."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar == "UU"].reset_index(drop=True)

    with pytest.raises(spookipy.AddElementsByPointError):
        # compute AddElementsByPoint
        _ = spookipy.AddElementsByPoint(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [AddElementsByPoint]


def test_5(plugin_test_dir):
    """Essaie d'additionner lorsqu'il y a plusieurs champs mais pas sur la même grille."""
    # open and read source
    source0 = plugin_test_dir + "tt_gz_px_2grilles.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar.isin(
        ["TT", "GZ"])].reset_index(drop=True)

    with pytest.raises(spookipy.AddElementsByPointError):
        # compute AddElementsByPoint
        _ = spookipy.AddElementsByPoint(src_df0).compute()
        # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT,GZ ] >> [AddElementsByPoint]


def test_6(plugin_test_dir):
    """Test addition avec parametre group_by_nomvar."""
    # open and read source
    source0 = plugin_test_dir + "TTUUVV_12h.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_dir + "TTUUVV_24h.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df = pd.concat([src_df0 , src_df1])

    # compute AddElementsByPoint
    df = spookipy.AddElementsByPoint(src_df, group_by_nomvar=True).compute()
    # df['etiket'] = '__ADDEPTX'
    df.loc[~df.nomvar.isin(['!!', '^^', '>>', 'P0']), 'etiket'] = '__ADDEPTX'
    # [ReaderStd --input {sources[0]}] >> [AddElementsByPoint --outputFieldName ACCU] >> [Zap --pdsLabel ADDFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    df.sort_values(by=['nomvar', 'level'],ascending=[True, False],inplace=True)
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test6_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


# def test_7(plugin_test_dir):
#     """Test addition de MASK; teste que le masque est bien additionne et que les champs sortent avec le bon typeOfField @@ et @P."""
#     # open and read source
#     source0 = plugin_test_dir + "2021071400_024_masked_fields.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()
#     meta_df = src_df0.loc[src_df0.nomvar.isin(
#         ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)
#     src_df0 = src_df0.loc[src_df0.nomvar.isin(['WHP0', 'WHP1'])]
#     masked_df = src_df0.loc[src_df0.typvar.str.contains('@@')]


#     # compute AddElementsByPoint
#     res_df = spookipy.AddElementsByPoint(masked_df, nomvar_out="HP01").compute()
#     res_df = spookipy.SetUpperBoundary(res_df, value=1.).compute()
#     res_df.loc[res_df.nomvar.isin(['HP01']), 'typvar'] = '@@'
#     res_df.loc[res_df.nomvar.isin(['HP01']), 'etiket'] = '__ADDEPTX'
#     res_df.loc[res_df.nomvar == 'HP01', 'datyp'] = 2
#     res_df.loc[res_df.nomvar == 'HP01', 'nbits'] = 1

#     df = pd.concat([res_df , src_df0, meta_df])
#     df.loc[~df.nomvar.isin(
#         ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"]), 'ip2'] = 24

#     # [ReaderStd --input {sources[0]}] >> [AddElementsByPoint --outputFieldName ACCU] >> [Zap --pdsLabel ADDFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

#     df.sort_values(by=['nomvar', 'level'],ascending=[True, False],inplace=True)

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "test7_file2cmp.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     # fstpy.delete_file(results_file)
#     assert(res)

# def test_77(plugin_test_dir):
#     """Test addition de MASK; teste que le masque est bien additionne et que les champs sortent avec le bon typeOfField @@ et @P."""
#     # open and read source
#     source0 = "/home/gha000/ss5/SpookiBuild/spooki_build/InputReduitMask.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     meta_df = src_df0.loc[src_df0.nomvar.isin(
#         ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"])].reset_index(drop=True)
#     src_df0 = src_df0.loc[src_df0.nomvar.isin(['WHP0', 'WHP1'])]
#     masked_df = src_df0.loc[src_df0.typvar.str.contains('@@')]


#     # compute AddElementsByPoint
#     res_df = spookipy.AddElementsByPoint(masked_df, nomvar_out="HP01").compute()
#     # res_df = spookipy.SetUpperBoundary(res_df, value=1.).compute()
#     res_df.loc[res_df.nomvar.isin(['HP01']), 'typvar'] = '@@'
#     res_df.loc[res_df.nomvar.isin(['HP01']), 'etiket'] = '__ADDEPTX'
#     # res_df.loc[res_df.nomvar == 'HP01', 'datyp'] = 2
#     # res_df.loc[res_df.nomvar == 'HP01', 'nbits'] = 1

#     df = pd.concat([res_df , src_df0, meta_df])
#     df.loc[~df.nomvar.isin(
#         ["^^", ">>", "^>", "!!", "!!SF", "HY", "P0", "PT"]), 'ip2'] = 24

#     # [ReaderStd --input {sources[0]}] >> [AddElementsByPoint --outputFieldName ACCU] >> [Zap --pdsLabel ADDFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

#     df.sort_values(by=['nomvar', 'level'],ascending=[True, False],inplace=True)

#     # write the result
#     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_77.std"])
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_dir + "test7_file2cmp.std"

#     # compare results
#     res = fstcomp(results_file, file_to_compare)
#     # fstpy.delete_file(results_file)
#     assert(res)


def test_8(plugin_test_dir):
    """Utilisation de --outputFieldName et group_by_nomvar."""
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = src_df0.loc[src_df0.nomvar == 'UU'].reset_index(drop=True)

    with pytest.raises(spookipy.AddElementsByPointError):
        # compute AddElementsByPoint
        _ = spookipy.AddElementsByPoint(
            src_df0, group_by_nomvar=True, nomvar_out='TEST').compute()
        # [ReaderStd --input {sources[0]}] >> [AddElementsByPoint --outputFieldName TROPLONG]


def test_9(plugin_test_dir):
    """Additionne des champs 2D. Identique au test1 mais avec l'option copy_input """
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute AddElementsByPoint
    df = spookipy.AddElementsByPoint(src_df0, nomvar_out='ACCU',copy_input=True).compute()
    df['etiket'] = 'ADDFIELDS'
    # [ReaderStd --input {sources[0]}] >> [AddElementsByPoint --outputFieldName ACCU] >> [Zap --pdsLabel ADDFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test9_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_10(plugin_test_dir):
    """Additionne des champs qui n'ont pas le meme nombre de niveaux """
    # open and read source
    source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Selection de 3 niveaux pour TT et UU (100, 925 et 850 mb)
    tt_uu_df = fstpy.select_with_meta(src_df0, ['TT', 'UU'])
    tt_uu_df = tt_uu_df.loc[tt_uu_df.ip1.isin([39945888, 41819464, 41744464])]

    # Selection de  niveaux pour VV (100 et 925 mb)
    vv_df = fstpy.select_with_meta(src_df0, ['VV'])
    vv_df = vv_df.loc[vv_df.ip1.isin([39945888, 41819464])]

    # Selection de UU et VV sur une autre grille
    # source1 = plugin_test_dir + "test1.std"
    source1 = plugin_test_dir + "UUVV5x5_enc_fileSrc.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    tt_uu_vv = pd.concat([tt_uu_df, vv_df, src_df1], ignore_index=True)

    # compute AddElementsByPoint
    df = spookipy.AddElementsByPoint(tt_uu_vv, nomvar_out='ACCU',copy_input=False).compute()
    df['etiket'] = 'ADDFIELDS'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test10_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)

def test_11(plugin_test_dir):
    """Additionne des champs groupe selon le forecast hour """
    # open and read source
    # source0 = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
    source0 ="/fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/ArithmeticMeanByPoint/testsFiles/TTES2x2x4_manyForecastHours.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    tt_es_df = fstpy.select_with_meta(src_df0, ['TT', 'ES'])

    # compute AddElementsByPoint
    df = spookipy.AddElementsByPoint(tt_es_df, group_by_forecast_hour=True, copy_input=False).compute()
    df.loc[df.nomvar == 'ADEP','etiket'] = '__ADDFLDX'
    # this test doesn't exist in cpp, the file to compare was created without taking into account the proper typvar
    df.loc[df.nomvar == 'ADEP','typvar'] = 'PZ'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test11_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


if __name__ == "__main__":
    test_1(TEST_PATH + '/AddElementsByPoint/testsFiles/')
