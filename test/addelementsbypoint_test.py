# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/AddElementsByPoint/testsFiles/'


def test_regtest_1(plugin_test_dir):
    """Test #1 : Additionne des champs 2D."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0,load_data=True).to_pandas()

    #compute AddElementsByPoint
    df = spooki.AddElementsByPoint(src_df0, nomvar_out='ACCU').compute()
    df['etiket']='ADDFIELDS'
    #[ReaderStd --input {sources[0]}] >> [AddElementsByPoint --outputFieldName ACCU] >> [Zap --pdsLabel ADDFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    #write the result
    results_file = TMP_PATH + "test_1.std"

    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "add2d_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)

def test_regtest_2(plugin_test_dir):
    """Test #2 : Additionne des champs 3D."""
    # open and read source
    source0 = plugin_test_dir + "UUVVTT5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute AddElementsByPoint
    df = spooki.AddElementsByPoint(src_df0, nomvar_out='ACCU').compute()
    df['etiket']='ADDFIELDS'
    #[ReaderStd --input {sources[0]}] >> [AddElementsByPoint --outputFieldName ACCU] >> [Zap --pdsLabel ADDFIELDS --doNotFlagAsZapped] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    #write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "add3d_file2cmp.std"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)

    #delete results
    fstpy.delete_file(results_file)

    assert(res == True)


def test_regtest_3(plugin_test_dir):
    """Test #3 : Utilisation de --outputFieldName avec une valeur > 4 caractères."""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spooki.AddElementsByPointError):
        #compute AddElementsByPoint
        df = spooki.AddElementsByPoint(src_df0, nomvar_out='TROPLONG').compute()
        #[ReaderStd --input {sources[0]}] >> [AddElementsByPoint --outputFieldName TROPLONG] 



def test_regtest_4(plugin_test_dir):
    """Test #4 : Essaie d'additionner lorsqu'il y a seulement 1 champ en entrée."""
    # open and read source 
    source0 = plugin_test_dir + "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.query( 'nomvar == "UU"')
    
    with pytest.raises(spooki.AddElementsByPointError):
        #compute AddElementsByPoint
        df = spooki.AddElementsByPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU] >> [AddElementsByPoint] 


def test_regtest_5(plugin_test_dir):
    """Test #5 : Essaie d'additionner lorsqu'il y a plusieurs champs mais pas sur la même grille."""
    # open and read source
    source0 = plugin_test_dir + "tt_gz_px_2grilles.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.query( 'nomvar in ["TT","GZ"]')

    with pytest.raises(ValueError):
        #compute AddElementsByPoint
        df = spooki.AddElementsByPoint(src_df0).compute()
        #[ReaderStd --input {sources[0]}] >> [Select --fieldName TT,GZ ] >> [AddElementsByPoint] 
