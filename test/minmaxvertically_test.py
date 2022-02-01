
from test import TMP_PATH, TEST_PATH
from ci_fstcomp import fstcomp
import pandas as pd
import fstpy.all as fstpy
import spookipy.all as spooki
import pytest

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH +"MinMaxVertically/testsFiles/"

def test_1(plugin_test_dir):
    """Invalid request -- missing mandatory fields KBAS and KTOP with bounded option """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.MinMaxLevelIndex
    with pytest.raises(spooki.MinMaxVerticallyError):
        spooki.MinMaxVertically(
            src_df0, 
            nomvar="TT",
            min = True,
            bounded=True).compute()

def test_2(plugin_test_dir):
    """Invalid request -- missing mandatory fields KBAS and KTOP with bounded option, on the same grid as field UU  """
    # open and read source
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_dir + "KbasKtop_v2.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df  = pd.concat([src_df0 , src_df1])

    # compute spooki.MinMaxVertically
    with pytest.raises(spooki.MinMaxVerticallyError):
        spooki.MinMaxVertically(
            src_df0, 
            nomvar="UU",
            bounded=True).compute()

def test_3(plugin_test_dir):
    """7 niveaux de UU, recherche min et max"""
    source0 = plugin_test_dir + "TTGZUUVV_3x2x7_regpres.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute MinMaxVertically
    df = spooki.MinMaxVertically(
        src_df0, 
        nomvar="UU", 
        max=True,
        min=True,
        nomvar_max='UMAX',
        nomvar_min='UMIN').compute()

    # write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMaxVert_file2cmp_test3.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    # fstpy.delete_file(results_file)
    assert(res)

def test_4(plugin_test_dir):
    """3 niveaux de ICGA (sortie du plugin IcingRimeAppleman); BOUNDED, recherche MAX """
    # open and read source
    source = plugin_test_dir + "test_ICGA.std"
    # source90 = plugin_test_dir + "minmax_DOWNWARD_bounded_input"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxVertically(
        src_df, 
        nomvar="ICGA", 
        bounded=True,
        max=True,
        nomvar_max='UMAX').compute()
    
    # write the result
    results_file = TMP_PATH + "test_4.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMaxVert_file2cmp_test4.std"

    # # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)

def test_5(plugin_test_dir):
    """Test avec des fichiers ayant des grilles differentes mais les meme champs; recheche min et max . """
    # Test relie au test 20 de MinMaxLevelIndex

    # open and read source
    source0 = plugin_test_dir + "200906290606_TT_grid1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    source1 = plugin_test_dir + "200906290606_TT_grid2.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df = pd.concat([src_df0, src_df1])
    # compute spooki.MinMaxLevelIndex
    df = spooki.MinMaxVertically(
        src_df, 
        nomvar="TT",
        nomvar_max='UMAX',
        nomvar_min='UMIN').compute()
    
    # write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "MinMaxVert_file2cmp_test5.std"

    # # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)

    assert(res)
