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
    df      = spookipy.AddElementsByPoint(src_df0, 
                                          nomvar_out='ACCU').compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [AddElementsByPoint --outputFieldName ACCU] >> 
    # [Zap --pdsLabel ADDFIELDS --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    df['etiket'] = 'ADDFIELDS'
    df['nbits']  = 16               # Pour correspondre a R16
    df['datyp']  = 1

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
    df      = spookipy.AddElementsByPoint(src_df0, 
                                          nomvar_out='ACCU').compute()
    # [ReaderStd --input {sources[0]}] >>
    # [AddElementsByPoint --outputFieldName ACCU] >>
    # [Zap --pdsLabel ADDFIELDS --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    df['etiket'] = 'ADDFIELDS'
    df['datyp']  = 1                # Pour correspondre a R16
    df['nbits']  = 16               


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
    # Test uniquement du cote spookipy

    # open and read source
    source0 = plugin_test_dir + "TTUUVV_12h.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_dir + "TTUUVV_24h.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df  = pd.concat([src_df0 , src_df1])

    # compute AddElementsByPoint
    df      = spookipy.AddElementsByPoint(src_df, 
                                          group_by_nomvar=True).compute()

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

def test_6a(plugin_test_dir):
    """Test avec 1 champ, differents forecastHours. Additionne les valeurs des TT des differents ForecastHours pour chaque niveau."""
    # Test inexistant du cote Spooki 

    # open and read source
    source0 = plugin_test_dir + "TTUUVV_12h.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_dir + "TTUUVV_24h.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df  = pd.concat([src_df0 , src_df1])

    tt_df   = src_df.loc[src_df['nomvar'] == "TT"]

    # compute AddElementsByPoint
    df      = spookipy.AddElementsByPoint(tt_df).compute()

    # Test similaire au test 6, mais en selectionnant TT et en n'utilisant pas l'option group_by_nomvar nomvar
    
    # Valide de cette facon: 
    # spooki_run.py "[ReaderStd --input $inputFile1 $inputFile2] >>  [Select --fieldName TT] >>  
    # [AddElementsByPoint --plugin_language CPP]

    df.sort_values(by=['nomvar', 'level'],ascending=[True, False],inplace=True)

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test6a_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
#  spooki_run.py "[ReaderStd --input /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/AddElementsByPoint/testsFiles/2021071400_024_masked_fields.std] >> [Select --fieldName WHP1,WHP0 --typeOfField MASK] >> [GridCut --startPoint 750,160 --endPoint 770,170] >> [WriterStd --output TestChampsMasked.std]"


# Fichier de comparaison version Spooki CPP recree: 
# spooki_run.py "[ReaderStd --input  2021071400_024_masked_fields.std] >>  
#                (  ([Select --typeOfField MASK --fieldName WHP0,WHP1] >> 
#                    [AddElementsByPoint --outputFieldName HP01 --plugin_language  CPP] >>  
#                    [SetUpperBoundary --value 1 --plugin_language CPP] >> [Zap --nbitsForDataStorage I32]) 
#                   +
#                   [Select --fieldName WHP0,WHP1]  
#                ) >> 
#                [WriterStd --output test7_file2cmp_20231204.cpp --plugin_language CPP--encodeIP2andIP3 ]"
def test_7(plugin_test_dir):
    """Test addition de MASK; teste que le masque est bien additionne et que les champs sortent avec le bon typeOfField @@ et @P."""
    # open and read source
    source0   = plugin_test_dir + "2021071400_024_masked_fields.std"

    src_df0   = fstpy.StandardFileReader(source0).to_pandas()

    meta_df   = src_df0.loc[src_df0.nomvar.isin(["^^", ">>"])].reset_index(drop=True)
    
    src_df0   = src_df0.loc[src_df0.nomvar.isin(['WHP0', 'WHP1'])]
    masked_df = src_df0.loc[src_df0.typvar.str.contains('@@')]

    # compute AddElementsByPoint - addition des champs "mask"
    res_df    = spookipy.AddElementsByPoint(masked_df, 
                                            nomvar_out="HP01", reduce_df = True).compute()

    res_df    = spookipy.SetUpperBoundary(res_df, 
                                          value=1).compute()

    # Concatene les champs originaux "mask" avec le resultat "bounded" a 1
    # Note: l'utilisation du copy_input n'est pas utilise a l'appel de AddElem... car on ne veut pas borne les champs 
    #       d'input a 1 par la suite.  Pas de gain a le faire de cette facon.
    df = pd.concat([res_df , src_df0, meta_df])

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test7_file2cmp_20231204.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

# Test existant du cote python seulement
def test_7a(plugin_test_dir):
    """Addition de MASK, similaire au test7; fichier reduit et copy_input = True."""
    # open and read source
    source0   = plugin_test_dir + "2021071400_024_masked_fields_reduit.std"
    src_df    = fstpy.StandardFileReader(source0).to_pandas()
    src_df0   = src_df.loc[(src_df.nomvar.isin(['WHP0', 'WHP1'])) & (src_df.typvar == '@@')]
 
    # # compute AddElementsByPoint
    res_df    = spookipy.AddElementsByPoint(src_df0, 
                                            nomvar_out="HP01",
                                            copy_input=True).compute()
    # spooki_run.py "[ReaderStd --input 2021071400_024_masked_fields_reduit.std] >> 
    #                ( [Select --typeOfField MASK --fieldName WHP0,WHP1] >> 
    #                  ([Copy] + ([AddElementsByPoint --outputFieldName HP01] >> [Zap --nbitsForDataStorage I32]))
    #                )  >> 
    #                [WriterStd --output test7a_file2cmp.std  --noMetadata --plugin_language CPP]"


    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7a.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, res_df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "test7a_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

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
    df = spookipy.AddElementsByPoint(src_df0, 
                                     nomvar_out='ACCU',
                                     copy_input=True).compute()
   
    # [ReaderStd --input {sources[0]}] >>
    # [AddElementsByPoint --outputFieldName ACCU] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    df['nbits']  = 16               # Pour correspondre a R16
    df['datyp']  = 1

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier de comparaison, sans zap des champs
    file_to_compare = plugin_test_dir + "test9_file2cmp_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_10(plugin_test_dir):
    """Additionne des champs qui n'ont pas le meme nombre de niveaux et de grilles differentes"""
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
    source1  = plugin_test_dir + "UUVV5x5_enc_fileSrc.std"
    src_df1  = fstpy.StandardFileReader(source1).to_pandas()
    tt_uu_vv = pd.concat([tt_uu_df, vv_df, src_df1], ignore_index=True)
    cols = ["nomvar", "grid", "ip1"]
    print(f'Input:  tt_uu_vv = \n{tt_uu_vv[cols]} \n')
    # compute AddElementsByPoint
    df = spookipy.AddElementsByPoint(tt_uu_vv, 
                                     nomvar_out='ACCU').compute()
    
    #  ( ( [ReaderStd --input glbpres_TT_UU_VV.std] >> 
    #       ( [Select --fieldName TT,UU --verticalLevel 1000,925,850] + [Select --fieldName VV --verticalLevel 1000,925] ) 
    #    ) + 
    #    [ReaderStd --input UUVV5x5_enc_fileSrc.std]
    #  ) >> 
    #  [AddElementsByPoint --outputFieldName ACCU] >> 
    #  [Zap --pdsLabel ADDFIELDS --doNotFlagAsZapped] >> 
    #  [WriterStd --output {destination_path} --noMetadata --ignoreExtended]"
    
    # Pour respecter le zap du test original
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
    # Test existant seulement du cote python

    # open and read source
    source0  = plugin_test_dir + "TTES2x2x4_manyForecastHours.std"
    src_df0  = fstpy.StandardFileReader(source0).to_pandas()
    tt_es_df = fstpy.select_with_meta(src_df0, ['TT', 'ES'])

    # compute AddElementsByPoint
    df = spookipy.AddElementsByPoint(tt_es_df, 
                                     group_by_forecast_hour=True).compute()

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Nouveau fichier de tests, sans zap d'etiket et de typvar.
    # open and read comparison file
    file_to_compare = plugin_test_dir + "test11_file2cmp_20231026.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_12(plugin_test_dir):
    """Test avec 2 groupes de donnees, 1er groupe sans niveaux communs, 2ieme groupe a les niveaux communs. """
    # Test existant en python seulement

    # open and read source
    source0 = plugin_test_dir + "2021071400_024_masked_fields.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ['UD','VD','WH'])

    source1 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df1 = fstpy.select_with_meta(src_df1, ['UU','VV'])

    df      = pd.concat([src_df0, src_df1], ignore_index=True)

    # 2 groupements de donnees: UV,VD et WH n'ont pas de niveaux communs aux 3
    #                           UU et VV ont les memes niveaux
 
    res_df = spookipy.AddElementsByPoint(df).compute()
    # Correspond a cette requete:
    # spooki_run.py  "[ReaderStd --input 2021071400_024_masked_fields.std UUVV5x5_fileSrc.std] >> 
    # [Select --fieldName UD,VD,WH,UU,VV] >> [AddElementsByPoint --plugin_language CPP]

    # ATTENTION:  Comportement different en CPP; arrete sans succes car un des groupes n'a pas de niveaux communs.
    #             En python, on a decide d'ameliorer le comportement.  Le plugin regarde les autres groupes et 
    #             fait le traitement si un groupe remplit la condition ie. si les niveaux sont communs.

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, res_df).to_fst()

    # Nouveau fichier de tests, sans zap d'etiket et de typvar.
    # open and read comparison file
    file_to_compare = plugin_test_dir + "test12_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_13(plugin_test_dir):
    """Test avec 3 champs masques; 1 champ n'est pas sur les memes niveaux.  Pas de niveaux communs aux 3 champs. """
    # open and read source
    source0 = plugin_test_dir + "2021071400_024_masked_fields.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ['UD','VD','WH'])

    with pytest.raises(spookipy.AddElementsByPointError):
        # compute AddElementsByPoint
        _ = spookipy.AddElementsByPoint(src_df0).compute()

if __name__ == "__main__":
    test_1(TEST_PATH + '/AddElementsByPoint/testsFiles/')
