# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/AddElementsVertically/testsFiles/'

def test_1(plugin_test_dir):
    """Utilisation de --outputFieldName avec une valeur > 4 caractères - requete invalide."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AddElementsVertically
    df = AddElementsVertically(src_df0).compute()
    #[ReaderStd --input {sources[0]}] >> [AddElementsVertically --outputFieldName TROPLONG]

    #write the result
    results_file = TMP_PATH + "test_1.std"
    StandardFileWriter(results_file, df)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "nan"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res)


def test_2(plugin_test_dir):
    """Effectue un test avec --outputFieldName mais plusieurs champs en entree - requete invalide."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AddElementsVertically
    df = AddElementsVertically(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [AddElementsVertically --outputFieldName ABCD]

    #write the result
    results_file = TMP_PATH + "test_2.std"
    StandardFileWriter(results_file, df)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "nan"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res)


def test_3(plugin_test_dir):
    """Test avec un fichier de deux champs et 2 niveaux."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AddElementsVertically
    df = AddElementsVertically(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [AddElementsVertically] >> [Zap --pdsLabel ADDCOLUMNS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_3.std"
    StandardFileWriter(results_file, df)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "AddVert_test3_file2cmp.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res)


def test_4(plugin_test_dir):
    """Test avec un fichier de 2 champs; selection d'un champ et utilisation de --outputFieldName."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AddElementsVertically
    df = AddElementsVertically(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU] >> [AddElementsVertically --outputFieldName ACCU] >> [Zap --pdsLabel ADDCOLUMNS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended --noUnitConversion]

    #write the result
    results_file = TMP_PATH + "test_4.std"
    StandardFileWriter(results_file, df)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "AddVert_test4_file2cmp.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res)


def test_5(plugin_test_dir):
    """Test avec un fichier de 2 champs pour lesquels on choisit un seul niveau."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AddElementsVertically
    df = AddElementsVertically(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 500] >> [AddElementsVertically] >> [Zap --pdsLabel ADDCOLUMNS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_5.std"
    StandardFileWriter(results_file, df)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "AddVert_test5_file2cmp.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res)


def test_6(plugin_test_dir):
    """Test sur un fichier dont les champs possèdent des intervalles - requete invalide."""
    # open and read source
    source0 = plugin_test_dir + "inputTest6.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AddElementsVertically
    df = AddElementsVertically(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [AddElementsVertically]

    #write the result
    results_file = TMP_PATH + "test_6.std"
    StandardFileWriter(results_file, df)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "nan"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res)
