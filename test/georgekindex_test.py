# -*- coding: utf-8 -*-
from fstpy.dataframe_utils import select_with_meta
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki
import pandas as pd
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/GeorgeKIndex/testsFiles/'


def test_1(plugin_test_dir):
    """Calcul de l'indice à partir d'une matrice de températures de 5x4x3 et d'écarts de point de rosée de 5x4x2"""
    # open and read source
    source0 = plugin_test_dir + "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute GeorgeKIndex
    df = spooki.GeorgeKIndex(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    #write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "TTES_GeorgeKIndex_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/GeorgeKIndex/result_test_1'

    #compare results
    res = fstcomp(results_file,file_to_compare,e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Calcul de l'indice avec un vrai fichier de données"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute GeorgeKIndex
    df = spooki.GeorgeKIndex(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]
    # df.loc[df.nomvar=='KI','grtyp'] = 'X'
    # df.loc[df.nomvar=='KI','ig1'] = 0
    # df.loc[df.nomvar=='KI','ig2'] = 0

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    #write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # file_to_compare = plugin_test_dir + "GeorgeKIndex_file2cmp.std"
    file_to_compare = plugin_test_dir + "GeorgeKIndex_file2cmp.std+PY20210812"
    # file_to_compare = '/home/sbf000/data/testFiles/GeorgeKIndex/result_test_2'

    #compare results
    res = fstcomp(results_file,file_to_compare)#,e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_3(plugin_test_dir):
    """Calcul de l'indice avec un fichier de données contenant TT et TD mais pas ES"""
    # open and read source
    source0 = plugin_test_dir + "inputFileSimpleTD_TT.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute GeorgeKIndex
    df = spooki.GeorgeKIndex(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]
    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    #write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "TTTD_GeorgeKIndex_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/GeorgeKIndex/result_test_3'

    #compare results
    res = fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_4(plugin_test_dir):
    """Calcul de l'indice avec un fichier contenant des TT et des ES d'unités différentes"""
    # open and read source
    source0 = plugin_test_dir + "inputFileSimple.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = select_with_meta(src_df0,['TT'])

    es_df = select_with_meta(src_df0,['ES'])

    src_df = pd.concat([tt_df,es_df],ignore_index=True)
    #compute GeorgeKIndex
    df = spooki.GeorgeKIndex(src_df).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> ( ([Select --fieldName TT] >> [UnitConvert --unit kelvin]) + [Select --fieldName ES] ) >> [GeorgeKIndex] >> [WriterStd --output {destination_path} --ignoreExtended]
    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    #write the result
    results_file = TMP_PATH + "test_4.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # file_to_compare = plugin_test_dir + "TTES_GeorgeKIndex_file2cmp.std"
    file_to_compare = plugin_test_dir + "TTES_GeorgeKIndex_file2cmp.std+PY20210812"
    # file_to_compare = '/home/sbf000/data/testFiles/GeorgeKIndex/result_test_4'

    #compare results
    res = fstcomp(results_file,file_to_compare)#,e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)

# in python vertsion this works but produces only one result
# def test_5(plugin_test_dir):
#     """Calcul avec un fichier ayant plusieurs forecastHour - Ne doit pas fonctionner car des niveaux sont manquants pour un forecastHour"""
#     # open and read source
#     source0 = plugin_test_dir + "2016122000_006_NatPres.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     #compute GeorgeKIndex
#     # with pytest.raises(spooki.GeorgeKIndexError):
#     df = spooki.GeorgeKIndex(src_df0).compute()
#     print(df)
#     assert(False)
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [GeorgeKIndex]


def test_6(plugin_test_dir):
    """Calcul avec un fichier ayant plusieurs forecastHour"""
    # open and read source
    source0 = plugin_test_dir + "2016122000_006_NatPres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    meta_df = src_df0.loc[src_df0.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)
    fh6_df = src_df0.loc[src_df0.ip2==6].reset_index(drop=True)

    src_df = pd.concat([meta_df,fh6_df],ignore_index=True)

    #compute GeorgeKIndex
    df = spooki.GeorgeKIndex(src_df).compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]}] >>', '[Select --forecastHour 6] >> [GeorgeKIndex] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']
    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    #write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "TTES_2016122000_file2cmp.std+20210517"
    # file_to_compare = '/home/sbf000/data/testFiles/GeorgeKIndex/result_test_6'

    #compare results
    res = fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
