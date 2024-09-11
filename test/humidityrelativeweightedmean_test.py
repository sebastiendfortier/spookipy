# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.humidity]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "HumidityRelativeWeightedMean"

def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un petit fichier contenant des valeurs verifiees a la main."""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.HumidityRelativeWeightedMean(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [HumidityRelativeWeightedMean ] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Test1_file2Cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert(res)

def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec une sortie de modele."""

    # open and read source
    source = plugin_test_path / "2020030412_024"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    df = spookipy.HumidityRelativeWeightedMean(src_df).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [HumidityRelativeWeightedMean ] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2020030412_test2_encoded_file2Cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert(res)

def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec une sortie de modele avec une valeur pour capper les resultats."""

    # open and read source
    source = plugin_test_path / "2020030412_024"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    df = spookipy.HumidityRelativeWeightedMean(src_df, capped_value=1.0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [HumidityRelativeWeightedMean --capped 1.0] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2020030412_test3_encoded_file2Cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert(res)

def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """2 groupes de TT avec dates d'origine differentes mais dates de validity identiques """

    source  = plugin_test_path / "Regpres_TTHUES_differentDateoSameDatev.std"
    src_df  = fstpy.StandardFileReader(source).to_pandas()

    df = spookipy.HumidityRelativeWeightedMean(src_df).compute()
    
     # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    file_to_compare = plugin_test_path / "Regpres_diffDateoSameDatev_file2cmp.std"

    # compare results 
    res = call_fstcomp(results_file, file_to_compare) 
    assert(res)
