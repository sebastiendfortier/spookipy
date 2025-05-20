# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import numpy as np
import fstpy
import pytest
import spookipy

from spookipy.applyunary.applyunary import ApplyUnaryError

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "ApplyUnary"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec racine carree, avec nomvar_in et nomvar_out"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ApplyUnary
    df = spookipy.ApplyUnary(src_df0, function=np.sqrt, nomvar_in="UU*", nomvar_out="UUSQ", label="SQRT").compute()

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Test1_sqrt_file2Cmp.std"

    # compare results
    columns = [
        "nomvar",
        "typvar",
        "ni",
        "nj",
        "nk",
        "dateo",
        "ip1",
        "ip2",
        "ip3",
        "deet",
        "npas",
        "grtyp",
        "ig1",
        "ig2",
        "ig3",
        "ig4",
    ]
    res = call_fstcomp(results_file, file_to_compare, columns=columns)
    assert res


def test_2(plugin_test_path):
    """Utilisation de nomvar_out avec plusieurs champs d'entree - requete invalide"""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ApplyUnary
    with pytest.raises(ApplyUnaryError):
        _ = spookipy.ApplyUnary(src_df0, function=np.sqrt, nomvar_out="SQ", label="SQRT").compute()


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec racine carree, plusieurs champs d'entree, sans nomvar_out"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ApplyUnary
    df = spookipy.ApplyUnary(src_df0, function=np.sqrt, label="SQRT").compute()

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "Test3_sqrt_file2Cmp.std"

    # compare results
    columns = [
        "nomvar",
        "typvar",
        "ni",
        "nj",
        "nk",
        "dateo",
        "ip1",
        "ip2",
        "ip3",
        "deet",
        "npas",
        "grtyp",
        "ig1",
        "ig2",
        "ig3",
        "ig4",
    ]
    res = call_fstcomp(results_file, file_to_compare, columns=columns)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test que le plugin peut etre appele sans le parametre etiket"""

    # open and read source
    source0 = plugin_test_path / "UUVV5x5_4_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ApplyUnary
    df = spookipy.ApplyUnary(src_df0, function=np.log).compute()
