# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/AbsoluteValue/testsFiles/'


def test_1(plugin_test_dir):
    """Calcule la valeur absolue de chaque champ."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AbsoluteValue
    df = AbsoluteValue(src_df0).compute()
    #['[ReaderStd --input {sources[0]}]', ' >> [AbsoluteValue]', ' >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE --ignoreExtended]']

    #write the result
    results_file = TMP_PATH + "test_1.std"
    StandardFileWriter(results_file, df)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "AbsoluteValue_file2cmp_test1.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res)


def test_2(plugin_test_dir):
    """Utilisation de --outputFieldName alors qu'on a plusieurs champs dans le fichier d'entrée."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AbsoluteValue
    df = AbsoluteValue(src_df0).compute()
    #[ReaderStd --input {sources[0]}] >> [AbsoluteValue --outputFieldName ABCD]

    #write the result
    results_file = TMP_PATH + "test_2.std"
    StandardFileWriter(results_file, df)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "nan"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res)


def test_3(plugin_test_dir):
    """Utilisation de --outputFieldName avec une valeur > 4 caractères."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AbsoluteValue
    df = AbsoluteValue(src_df0).compute()
    #[ReaderStd --input {sources[0]}] >> [AbsoluteValue --outputFieldName ABCDEF]

    #write the result
    results_file = TMP_PATH + "test_3.std"
    StandardFileWriter(results_file, df)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "nan"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res)


def test_4(plugin_test_dir):
    """Calcule la valeur absolue d'un champ et utilise --outputFieldName pour renommer le résultat."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_minus2_fileSrc2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AbsoluteValue
    df = AbsoluteValue(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU ] >> [AbsoluteValue --outputFieldName ABCD ] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE --ignoreExtended --noUnitConversion]

    #write the result
    results_file = TMP_PATH + "test_4.std"
    StandardFileWriter(results_file, df)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "AbsoluteValue_file2cmp_test4.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res)
