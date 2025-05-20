# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
from spookipy.rmn_interface import RmnInterface
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "MultiplyElementBy"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_factor1"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_1_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute MultiplyElementBy
    df = spookipy.MultiplyElementBy(src_df0, value=3).compute()
    # [ReaderStd --input {sources[0]}] >> [MultiplyElementBy --value 3.0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df = spookipy.convip(df, style=RmnInterface.CONVIP_ENCODE_OLD)
    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "factor_file2cmp.std"

    # compare results - on exclut l'etiket
    cols = [
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
        "datyp",
        "nbits",
        "grtyp",
        "ig1",
        "ig2",
        "ig3",
        "ig4",
    ]
    res = call_fstcomp(results_file, file_to_compare, columns=cols)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_factor2"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_1_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute MultiplyElementBy
    df = spookipy.MultiplyElementBy(src_df0, value=0.333).compute()
    # [ReaderStd --input {sources[0]}] >> [MultiplyElementBy --value 0.333] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df = spookipy.convip(df, style=RmnInterface.CONVIP_ENCODE_OLD)
    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "factor2_file2cmp.std"

    # compare results - on exclut l'etiket
    cols = [
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
        "datyp",
        "nbits",
        "grtyp",
        "ig1",
        "ig2",
        "ig3",
        "ig4",
    ]
    res = call_fstcomp(results_file, file_to_compare, columns=cols)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Utilisation de l'option outputFieldName alors que plus d'un champ - requete invalide."""

    source = plugin_test_path / "inputFile.std"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    with pytest.raises(spookipy.MultiplyElementByError):
        _ = spookipy.MultiplyElementBy(src_df, value=2, nomvar_out="ABCD").compute()
