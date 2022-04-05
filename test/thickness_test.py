# -*- coding: utf-8 -*-
from spookipy.thickness.thickness import Thickness,ParametersValuesError
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pandas as pd
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp
import secrets


pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + "/Thickness/testsFiles/"

def test_1(plugin_test_dir):
    """Test avec un fichier de coordonnées UNKNOWN."""

    # open and read source
    source0 = plugin_test_dir + "GZ_12000_10346_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()
    # compute Thickness
    df = Thickness(src_df0,base=1.0,top=0.8346,coordinate_type='UNKNOWN').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 1.0 --top 0.8346 --coordinateType SIGMA_COORDINATE] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]
    
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Thick_test1-2_file2cmp.std"
    
    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Test #2 : Test avec un fichier de coordonnées UNKNOWN avec valeur de base plus haute dans l'atmosphère que valeur de top."""
    # open and read source
    source0 = plugin_test_dir + "GZ_12000_10346_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()


    #compute Thickness
    df = Thickness(src_df0,base=0.8346,top=1.0,coordinate_type='UNKNOWN').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 0.8346 --top 1.0 --coordinateType SIGMA_COORDINATE] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    #write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Thick_test1-2_file2cmp.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_3(self):
    """Test #3 : Test avec un fichier en pression."""
    # open and read source
    source0 = plugin_test_dir + "GZ_1000_500_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0)


    #compute Thickness
    df = Thickness(src_df0,base=1000,top=500,coordinate_type='PRESSURE_2001').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 1000 --top 500 --coordinateType PRESSURE_COORDINATE] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    #write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.StandardFileWriter(results_file, df, erase=True)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Thick_test3-4_file2cmp.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res == True)


def test_4(self):
    """Test #4 : Test avec un fichier en pression avec valeur de base plus haute dans l'atmosphère que valeur de top."""
    # open and read source
    source0 = plugin_test_dir + "GZ_1000_500_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0)


    #compute Thickness
    df = Thickness(src_df0,base=500,top=1000,coordinate_type='PRESSURE_2001').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 500 --top 1000 --coordinateType PRESSURE_COORDINATE] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_4.std"
    fstpy.StandardFileWriter(results_file, df, erase=True)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Thick_test3-4_file2cmp.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res == True)


def test_5(self):
    """Test #5 : Test en utilisant le même niveau pour base et top; requête invalide."""
    with pytest.raises(ParametersValuesError):
        # open and read source
        source0 = plugin_test_dir + "GZ_1000_500_fileSrc.std"
        src_df0 = fstpy.StandardFileReader(source0,base=1000,top=1000,coordinate_type='PRESSURE_2001')
        #compute Thickness
        df = Thickness(src_df0).compute()
        #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 1000 --top 1000 --coordinateType PRESSURE_COORDINATE]



def test_6(self):
    """Test #6 : Test avec un fichier hybride."""
    # open and read source
    source0 = plugin_test_dir + "2016031600_024_reghyb"
    src_df0 = fstpy.StandardFileReader(source0)


    #compute Thickness
    df = Thickness(src_df0,base=1,top=0.607,coordinate_type='HYBRID_5001').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 1 --top 0.607 --coordinateType HYBRID_COORDINATE] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.StandardFileWriter(results_file, df, erase=True)()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "Thick_test6_file2cmp.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    assert(res == True)

if __name__ == "__main__":
    test_1(TEST_PATH + '/Thickness/testsFiles/')

