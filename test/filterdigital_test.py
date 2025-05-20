# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "FilterDigital"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """1 répétition avec un filtre standard."""
    # open and read source
    source0 = plugin_test_path / "UUVVfil5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df0, filter=[1, 1, 1], repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [FilterDigital --filter 1,1,1 --repetitions 1] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filter1_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """3 répétitions avec un filtre standard."""
    # open and read source
    source0 = plugin_test_path / "UUVVfil5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df0, filter=[1, 1, 1], repetitions=3).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [FilterDigital --filter 1,1,1 --repetitions 3] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filter2_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """1 répétition avec un long filtre et un fichier provenant du site de rpn PGSM."""
    # open and read source
    source0 = plugin_test_path / "UU11x11_1_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df0, filter=[1, 1, 1, 1, 1, 1, 1, 1, 1], repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [FilterDigital --filter 1,1,1,1,1,1,1,1,1 --repetitions 1] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filter3_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """3 répétitions avec un long filtre et un fichier provenant du site de rpn PGSM."""
    # open and read source
    source0 = plugin_test_path / "UU11x11_1_0_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df0, filter=[1, 1, 1, 1, 1, 1, 1, 1, 1], repetitions=3).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [FilterDigital --filter 1,1,1,1,1,1,1,1,1 --repetitions 3] >>
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filter4_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """1 répétition avec un filtre à 1 chiffre."""
    # open and read source
    source0 = plugin_test_path / "UUVVfil5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df0, filter=[1], repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [FilterDigital --filter 1 --repetitions 1] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filter5_file2cmp.std+PY20240116"
    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """1 répétition avec un long filtre et un gros fichier."""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df0, filter=[1, 1, 1, 2, 2, 1, 1, 1, 1], repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [FilterDigital --filter 1,1,1,2,2,1,1,1,1 --repetitions 1] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filter6_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """3 répétitions avec un long filtre et un gros fichier."""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df0, filter=[1, 1, 1, 2, 2, 1, 1, 1, 1], repetitions=3).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [FilterDigital --filter 1,1,1,2,2,1,1,1,1 --repetitions 3] >>
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_7.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filter7_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """3 répétitions avec un long filtre, poids importants et un gros fichier."""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df0, filter=[1, 1, 1, 2, 3, 2, 1, 1, 1], repetitions=3).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [FilterDigital --filter 1,1,1,2,3,2,1,1,1 --repetitions 3] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filter8_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test de comparaison avec le programme pgsm FILTRE3PTS3X."""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ["TT"])
    src_df = src_df.loc[src_df.etiket == "R1558V0N"]
    # compute FilterDigital
    df = spookipy.FilterDigital(src_df, filter=[2, 4, 2], repetitions=3).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT --pdsLabel R1558V0N] >>
    # [FilterDigital --filter 2,4,2 --repetitions 3] >>
    # [Zap --userDefinedIndex 303 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # Pour correspondre au Zap
    df.loc[df.nomvar == "TT", "ip3"] = 303
    df.loc[df.nomvar == "TT", "datyp"] = 1
    df.loc[df.nomvar == "TT", "nbits"] = 16

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filteredByPgsm1_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test de comparaison avec le programme pgsm FILTRE3PTS1X."""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ["TT"])
    src_df = src_df.loc[src_df.etiket == "R1558V0N"]

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df, filter=[2, 4, 2], repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT --pdsLabel R1558V0N] >>
    # [FilterDigital --filter 2,4,2 --repetitions 1] >>
    # [Zap --userDefinedIndex 301 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path}]

    # Pour correspondre au Zap
    df.loc[df.nomvar == "TT", "ip3"] = 301
    df.loc[df.nomvar == "TT", "datyp"] = 1
    df.loc[df.nomvar == "TT", "nbits"] = 16

    # write the result
    results_file = test_tmp_path / "test_10.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filteredByPgsm2_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test de comparaison avec le programme pgsm FILTRE5PTS2X."""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ["TT"])
    src_df = src_df.loc[src_df.etiket == "R1558V0N"]

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df, filter=[1, 2, 4, 2, 1], repetitions=2).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT --pdsLabel R1558V0N] >>
    # [FilterDigital --filter 1,2,4,2,1 --repetitions 2] >>
    # [Zap --userDefinedIndex 502 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} ]

    # Pour correspondre au Zap
    df.loc[df.nomvar == "TT", "ip3"] = 502
    df.loc[df.nomvar == "TT", "datyp"] = 1
    df.loc[df.nomvar == "TT", "nbits"] = 16

    # write the result
    results_file = test_tmp_path / "test_11.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filteredByPgsm3_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test de comparaison avec le programme pgsm FILTRE9PTS1X."""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ["TT"])
    src_df = src_df.loc[src_df.etiket == "R1558V0N"]

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df, filter=[1, 1, 1, 1, 1, 1, 1, 1, 1], repetitions=1).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT --pdsLabel R1558V0N] >>
    # [FilterDigital --filter 1,1,1,1,1,1,1,1,1 --repetitions 1] >>
    # [Zap --userDefinedIndex 901 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path}]

    # Pour correspondre au Zap
    df.loc[df.nomvar == "TT", "ip3"] = 901
    df.loc[df.nomvar == "TT", "datyp"] = 1
    df.loc[df.nomvar == "TT", "nbits"] = 16

    # write the result
    results_file = test_tmp_path / "test_12.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filteredByPgsm4_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test de comparaison."""
    # open and read source
    source0 = plugin_test_path / "LATLON_L_9x11_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df0, filter=[1], repetitions=1).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [FilterDigital --filter 1 --repetitions 1] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_13.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "LATLON_L_9x11_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
    """1 répétition avec un filtre standard et l'option outputFieldName."""
    # open and read source
    source0 = plugin_test_path / "UUVVfil5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ["UU*"])

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df, filter=[1, 1, 1], repetitions=1, nomvar_out="abcd").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName UU* ] >>
    # [FilterDigital --filter 1,1,1 --repetitions 1 --outputFieldName abcd] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_14.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE du test en CPP
    file_to_compare = plugin_test_path / "filter9_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


@pytest.mark.skip(reason="Problem with the option parallel=True - to be fixed")
def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    """1 répétition avec un filtre standard, l'option outputFieldName en parallele."""
    # open and read source
    source0 = plugin_test_path / "UUVVfil5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = fstpy.select_with_meta(src_df0, ["UU*"])

    # compute FilterDigital
    df = spookipy.FilterDigital(src_df0, filter=[1, 1, 1], repetitions=1, nomvar_out="abcd", parallel=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName UU* ] >>
    # [FilterDigital --filter 1,1,1 --repetitions 1 --outputFieldName abcd] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_15.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "filter9_file2cmp.std+PY20240116"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    """Idem au test 14 mais utilisation de l'option outputFieldName alors que plus d'un champ - requete invalide."""
    # open and read source
    source0 = plugin_test_path / "UUVVfil5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.FilterDigitalError):
        _ = spookipy.FilterDigital(src_df0, filter=[1, 1, 1], repetitions=1, nomvar_out="abcd").compute()
