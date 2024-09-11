# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy
from fstpy.dataframe_utils import select_with_meta

# pytestmark = [pytest.mark.skip]
pytestmark = [pytest.mark.regressions]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "WindDirection"

# Equivalent au test 3 de WindModulusAndDirection
def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test le calcul de la direction du vent, GRILLE de type Z."""
    # open and read source
    source = plugin_test_path / "windModulusAndDirection_fileSrc.std"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    # compute spookipy.WindDirection
    df     = spookipy.WindDirection(src_df).compute()

    # Fichier de comparaison cree de cette facon:
    # [ReaderStd --input--input {sources[0]}] >>
    # [WindModulusAndDirection] >>
    # ( ([Select --metadataFieldName ^^,>>] >> [Zap --metadataZappable --pdsLabel 558V0 --run R1 --implementation OPERATIONAL]) +
    #   ([Select --fieldName WD] >> [Zap --pdsLabel WNDDIR --doNotFlagAsZapped])) >>
    # [WriterStd --output {destination_path}  --IP1EncodingStyle OLDSTYLE --plugin_language CPP --noModificationFlag]"

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "windModulusAndDirection_test1_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


# Equivalent au test 1 de WindModulusAndDirection mais pour calculer WD et non UV 
# Nouveau test du cote python
def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test le calcul de la direction du vent, GRILLE de type N."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.WindDirection
    df      = spookipy.WindDirection(src_df0).compute()

    # Fichier de comparaison cree de cette facon:
    # [ReaderStd --input--input {sources[0]}] >>
    # [WindModulusAndDirection] >> [Select --fieldName WD] >> 
    # [Zap --pdsLabel WNDDIR --doNotFlagAsZapped]  >> 
    # [WriterStd --output TestWd.std --noModificationFlag  --IP1EncodingStyle OLDSTYLE --plugin_language CPP] "

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "UUVV5x5_test2_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

# Equivalent au test 7 de VectorModulusAndDirection mais pour calculer WD seulement
# Nouveau test du cote python
def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test le calcul de la direction du vent, GRILLE de type U."""
    # open and read source
    source0 = plugin_test_path / "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.WindDirection
    df      = spookipy.WindDirection(src_df0).compute()
    df      = spookipy.convip(df)
    df.loc[df['nomvar'].isin([">>", "^^"]), 'etiket'] = "INTERPX"
    
    # Fichier de comparaison cree de cette facon:
    # [ReaderStd --input {sources[0]}] >>
    # [WindModulusAndDirection --plugin_language CPP ] >> [Select --fieldName WD] >> 
    # [Zap --pdsLabel WNDDIR --doNotFlagAsZapped]  >> 
    # [WriterStd --output TestWd.std --noModificationFlag --plugin_language CPP] "

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "TTESUUVV_YinYang_test3_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_4(plugin_test_path):
    """Test un fichier standard avec des champs sur une grille autre que celle autorisé."""
    # open and read source
    source0 = plugin_test_path / "dm2001092012-00-00_000.fst"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.WindDirection
    with pytest.raises(spookipy.WindDirectionError):
        _ = spookipy.WindDirection(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [WindDirection --orientationType WIND] >> [WriterStd --output {destination_path}]

# Equivalent au test 4 de VectorModulusAndDirection
def test_5(plugin_test_path):
    """Test un fichier standard avec des champs sur une grille Y avec les tictic tactac définis sur une grille N."""
    # open and read source
    source0 = plugin_test_path / "Ygrid_Ntypetictac_UUVV.fst"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.WindDirection
    with pytest.raises(spookipy.WindDirectionError):
        _ = spookipy.WindDirection(src_df0).compute()

# Similaire au test 1 de VectorModulusAndDirection mais avec UU et VV    
def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec une grille Y."""
    # open and read source
    source0 = plugin_test_path / "inputInterpolatedToStation.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = select_with_meta(src_df0, ['VV', 'UU'])

    # compute spookipy.WindDirection
    df = spookipy.WindDirection(src_df).compute()

    # Creation du fichier de comparaison:
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >>
    #  [Select --fieldName UU,VV]  >> 
    #  [VectorModulusAndDirection --orientationType WIND] >> 
    #  [Select --fieldName DIR] >> 
    #  [Zap --fieldName WD --pdsLabel WNDDIR --run __  --doNotFlagAsZapped] >> 
    #  [WriterStd --output {destination_path} --noModificationFlag]"

    df      = spookipy.convip(df)
    df.loc[df['nomvar'].isin([">>", "^^"]), 'etiket'] = "INTERPX"

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "GridY_test6_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.008)
    assert(res)
