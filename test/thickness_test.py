# -*- coding: utf-8 -*-
from spookipy.thickness.thickness import ParametersValuesError
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions2]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "Thickness"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #1 : Test avec un fichier de coordonnées UNKNOWN avec valeur de base plus haute dans l'atmosphère que valeur de top."""

    # open and read source
    source0 = plugin_test_path / "GZ_12000_10346_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    # compute Thickness
    df = spookipy.Thickness(src_df0, base=1.0, top=0.8346, coordinate_type="UNKNOWN").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Thickness --base 1.0 --top 0.8346 --coordinateType SIGMA_COORDINATE] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Thick_test1-2_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #2 : Test avec un fichier de coordonnées UNKNOWN avec valeur de base plus basse dans l'atmosphère que valeur de top."""
    # open and read source
    source0 = plugin_test_path / "GZ_12000_10346_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Thickness
    df = spookipy.Thickness(src_df0, base=0.8346, top=1.0, coordinate_type="UNKNOWN").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Thickness --base 0.8346 --top 1.0 --coordinateType SIGMA_COORDINATE] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Thick_test1-2_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #3 : Test avec un fichier en pression avec valeur de base plus haute dans l'atmosphère que valeur de top."""

    # open and read source
    source0 = plugin_test_path / "GZ_1000_500_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Thickness
    df = spookipy.Thickness(src_df0, base=1000, top=500, coordinate_type="PRESSURE_2001").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Thickness --base 1000 --top 500 --coordinateType PRESSURE_COORDINATE] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Thick_test3-4_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #4 : Test avec un fichier en pression avec valeur de base plus basse dans l'atmosphère que valeur de top."""

    # open and read source
    source0 = plugin_test_path / "GZ_1000_500_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Thickness
    df = spookipy.Thickness(src_df0, base=500, top=1000, coordinate_type="PRESSURE_2001").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Thickness --base 500 --top 1000 --coordinateType PRESSURE_COORDINATE] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Thick_test3-4_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #5 : Test en utilisant le même niveau pour base et top; requête invalide."""
    with pytest.raises(ParametersValuesError):
        # open and read source
        source0 = plugin_test_path / "GZ_1000_500_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0).to_pandas()
        # compute Thickness
        spookipy.Thickness(src_df0, base=1000, top=1000, coordinate_type="PRESSURE_2001").compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >>
        # [Thickness --base 1000 --top 1000 --coordinateType PRESSURE_COORDINATE]


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #6 : Test avec un fichier hybride."""
    # open and read source
    source0 = plugin_test_path / "2016031600_024_reghyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Thickness
    df = spookipy.Thickness(src_df0, base=1.0, top=0.607, coordinate_type="HYBRID_5001").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Thickness --base 1 --top 0.607 --coordinateType HYBRID_COORDINATE] >>
    # [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Thick_test6_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
