# -*- coding: utf-8 -*-
from fstpy.dataframe_utils import select_with_meta
from test import TMP_PATH,TEST_PATH
import pytest
import fstpy.all as fstpy
import spookipy.all as spooki
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.skip]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/WindDirection/testsFiles/'

def test_1(plugin_test_dir):
    """Test l'option --orientationType avec la valeur WIND."""
    # open and read source
    source0 = plugin_test_dir + "inputInterpolatedToStation.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = select_with_meta(src_df0,['TT','UU'])

    #compute spooki.WindDirection
    df = spooki.WindDirection(src_df).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [PrintIMO] >>
    # [Select --fieldName UU,TT] >>
    # [spooki.WindDirection --orientationType WIND] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "VectorModulusAndDirection_ygrid_file2cmp.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Test un fichier standard avec des champs sur une grille Y avec les tictic tactac définis sur une grille N."""
    # open and read source
    source0 = plugin_test_dir + "Ygrid_Ntypetictac_UUVV.fst"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute spooki.WindDirection
    with pytest.raises(spooki.WindDirectionError):
        _ = spooki.WindDirection(src_df0).compute()
    #[ReaderStd --input {sources[0]}] >> [spooki.WindDirection --orientationType WIND] >> [WriterStd --output {destination_path}]



def test_3(plugin_test_dir):
    """Test un fichier standard avec des champs sur une grille autre que celle autorisé."""
    # open and read source
    source0 = plugin_test_dir + "pm2001092012-01-00_000.fst"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute spooki.WindDirection
    with pytest.raises(spooki.WindDirectionError):
        _ = spooki.WindDirection(src_df0).compute()
    #[ReaderStd --input {sources[0]}] >> [spooki.WindDirection --orientationType WIND] >> [WriterStd --output {destination_path}]



def test_4(plugin_test_dir):
    """Test un fichier standard avec des champs sur une grille autre que celle autorisé."""
    # open and read source
    source0 = plugin_test_dir + "dm2001092012-00-00_000.fst"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute spooki.WindDirection
    with pytest.raises(spooki.WindDirectionError):
        _ = spooki.WindDirection(src_df0).compute()
    #[ReaderStd --input {sources[0]}] >> [spooki.WindDirection --orientationType WIND] >> [WriterStd --output {destination_path}]




def test_5(plugin_test_dir):
    """Test avec une grille U le calcul de la vitesse et de la direction des vents, référentiel météorologique."""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = select_with_meta(src_df0,['VV','UU'])

    #compute spooki.WindDirection
    df = spooki.WindDirection(src_df).compute()
    #[ReaderStd --input {sources[0]}] >> [Select --fieldName UU,VV] >> [spooki.WindDirection --orientationType WIND] >>
    # [WriterStd --output {destination_path}]

    #write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "VecModAndDir_Ugrid_wind_file2cmp.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
