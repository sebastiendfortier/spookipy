# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/FilterDigital/testsFiles/'


def test_1(plugin_test_dir):
    """1 répétition avec un filtre standard."""
    # open and read source
    source0 = plugin_test_dir + "UUVVfil5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df0, filter=[
            1, 1, 1], repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1 --repetitions 1] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # df.loc[:,'etiket'] = 'PGSMUFIL'
    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "filter1_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_1'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """3 répétitions avec un filtre standard."""
    # open and read source
    source0 = plugin_test_dir + "UUVVfil5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df0, filter=[
            1, 1, 1], repetitions=3).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1 --repetitions 3] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    # df.loc[:,'etiket'] = 'PGSMUFIL'
    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "filter2_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_2'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_3(plugin_test_dir):
    """1 répétition avec un long filtre et un fichier provenant du site de rpn PGSM."""
    # open and read source
    source0 = plugin_test_dir + "UU11x11_1_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df0,
        filter=[
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1],
        repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1,1,1,1,1,1,1 --repetitions 1] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # df.loc[:,'etiket'] = 'UNAOPS'

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "filter3_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_3'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_4(plugin_test_dir):
    """3 répétitions avec un long filtre et un fichier provenant du site de rpn PGSM."""
    # open and read source
    source0 = plugin_test_dir + "UU11x11_1_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df0,
        filter=[
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1],
        repetitions=3).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1,1,1,1,1,1,1 --repetitions 3] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    # df.loc[:,'etiket'] = 'UNAOPS'

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "filter4_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_4'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_5(plugin_test_dir):
    """1 répétition avec un filtre à 1 chiffre."""
    # open and read source
    source0 = plugin_test_dir + "UUVVfil5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spooki.FilterDigital(src_df0, filter=[1], repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1 --repetitions 1] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # df.loc[:,'etiket'] = 'PGSMUFIL'

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "filter5_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_5'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir):
    """1 répétition avec un long filtre et un gros fichier."""
    # open and read source
    source0 = plugin_test_dir + "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df0,
        filter=[
            1,
            1,
            1,
            2,
            2,
            1,
            1,
            1,
            1],
        repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1,2,2,1,1,1,1 --repetitions 1] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # file_to_compare = plugin_test_dir + "filter6_file2cmp.std"
    file_to_compare = plugin_test_dir + "filter6_file2cmp.std+PY20210812"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_6'

    # compare results
    res = fstcomp(results_file, file_to_compare)  # ,e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_7(plugin_test_dir):
    """3 répétitions avec un long filtre et un gros fichier."""
    # open and read source
    source0 = plugin_test_dir + "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df0,
        filter=[
            1,
            1,
            1,
            2,
            2,
            1,
            1,
            1,
            1],
        repetitions=3).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1,2,2,1,1,1,1 --repetitions 3] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # file_to_compare = plugin_test_dir + "filter7_file2cmp.std"
    file_to_compare = plugin_test_dir + "filter7_file2cmp.std+PY20210812"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_7'

    # compare results
    res = fstcomp(results_file, file_to_compare)  # ,e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_8(plugin_test_dir):
    """3 répétitions avec un long filtre, poids importants et un gros fichier."""
    # open and read source
    source0 = plugin_test_dir + "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df0,
        filter=[
            1,
            1,
            1,
            2,
            3,
            2,
            1,
            1,
            1],
        repetitions=3).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [FilterDigital --filter 1,1,1,2,3,2,1,1,1 --repetitions 3] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # file_to_compare = plugin_test_dir + "filter8_file2cmp.std"
    file_to_compare = plugin_test_dir + "filter8_file2cmp.std+PY20210812"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_8'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_9(plugin_test_dir):
    """Test de comparaison avec le programme pgsm FILTRE3PTS3X."""
    # open and read source
    source0 = plugin_test_dir + "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ['TT'])
    src_df = src_df.loc[src_df.etiket == 'R1558V0N']
    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df, filter=[
            2, 4, 2], repetitions=3).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel R1558V0N] >>
    # [FilterDigital --filter 2,4,2 --repetitions 3] >> [Zap --userDefinedIndex 303 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    df.loc[df.nomvar == 'TT', 'ip3'] = 303
    df.loc[df.nomvar == 'TT', 'datyp'] = 1
    df.loc[df.nomvar == 'TT', 'nbits'] = 16

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "filteredByPgsm1_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_9'

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file)
    assert(res)


def test_10(plugin_test_dir):
    """Test de comparaison avec le programme pgsm FILTRE3PTS1X."""
    # open and read source
    source0 = plugin_test_dir + "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ['TT'])
    src_df = src_df.loc[src_df.etiket == 'R1558V0N']

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df, filter=[
            2, 4, 2], repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel R1558V0N] >>
    # [FilterDigital --filter 2,4,2 --repetitions 1] >> [Zap --userDefinedIndex 301 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df.loc[df.nomvar == 'TT', 'ip3'] = 301
    df.loc[df.nomvar == 'TT', 'datyp'] = 1
    df.loc[df.nomvar == 'TT', 'nbits'] = 16

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "filteredByPgsm2_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_10'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_11(plugin_test_dir):
    """Test de comparaison avec le programme pgsm FILTRE5PTS2X."""
    # open and read source
    source0 = plugin_test_dir + "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ['TT'])
    src_df = src_df.loc[src_df.etiket == 'R1558V0N']

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df, filter=[
            1, 2, 4, 2, 1], repetitions=2).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel R1558V0N] >>
    # [FilterDigital --filter 1,2,4,2,1 --repetitions 2] >> [Zap --userDefinedIndex 502 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df.loc[df.nomvar == 'TT', 'ip3'] = 502
    df.loc[df.nomvar == 'TT', 'datyp'] = 1
    df.loc[df.nomvar == 'TT', 'nbits'] = 16

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # file_to_compare = plugin_test_dir + "filteredByPgsm3_file2cmp.std"
    file_to_compare = plugin_test_dir + "filteredByPgsm3_file2cmp.std+PY20210812"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_11'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_12(plugin_test_dir):
    """Test de comparaison avec le programme pgsm FILTRE9PTS1X."""
    # open and read source
    source0 = plugin_test_dir + "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ['TT'])
    src_df = src_df.loc[src_df.etiket == 'R1558V0N']

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df,
        filter=[
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1],
        repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel R1558V0N] >>
    # [FilterDigital --filter 1,1,1,1,1,1,1,1,1 --repetitions 1] >> [Zap --userDefinedIndex 901 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df.loc[df.nomvar == 'TT', 'ip3'] = 901
    df.loc[df.nomvar == 'TT', 'datyp'] = 1
    df.loc[df.nomvar == 'TT', 'nbits'] = 16

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # file_to_compare = plugin_test_dir + "filteredByPgsm4_file2cmp.std"
    file_to_compare = plugin_test_dir + "filteredByPgsm4_file2cmp.std+PY20210812"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_12'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_13(plugin_test_dir):
    """Test de comparaison."""
    # open and read source
    source0 = plugin_test_dir + "LATLON_L_9x11_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spooki.FilterDigital(src_df0, filter=[1], repetitions=1).compute()
    # [ReaderStd --input {sources[0]}] >> [FilterDigital --filter 1 --repetitions 1] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]

    df.loc[:, 'etiket'] = 'R1580V0_N'
    df.loc[df.typvar == 'P','typvar'] = 'PF'

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "LATLON_L_9x11_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_13'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_14(plugin_test_dir):
    """1 répétition avec un filtre standard et l'option outputFieldName."""
    # open and read source
    source0 = plugin_test_dir + "UUVVfil5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ['UU*'])

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df,
        filter=[
            1,
            1,
            1],
        repetitions=1,
        nomvar_out='abcd').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU* ] >>
    # [FilterDigital --filter 1,1,1 --repetitions 1 --outputFieldName abcd] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_14.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "filter9_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_14'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_14(plugin_test_dir):
    """1 répétition avec un filtre standard, l'option outputFieldName en parallele."""
    # open and read source
    source0 = plugin_test_dir + "UUVVfil5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ['UU*'])

    # compute FilterDigital
    df = spooki.FilterDigital(
        src_df,
        filter=[
            1,
            1,
            1],
        repetitions=1,
        nomvar_out='abcd',
        parallel=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU* ] >>
    # [FilterDigital --filter 1,1,1 --repetitions 1 --outputFieldName abcd] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # df.loc[:,'datyp'] = 5
    # df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_14.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "filter9_file2cmp.std"
    # file_to_compare = '/home/sbf000/data/testFiles/FilterDigital/result_test_14'

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
