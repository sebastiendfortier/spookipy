# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
from spookipy.rmn_interface import RmnInterface
import spookipy
from spookipy.power import PowerError

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "Power"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Valeur de nomvar_out invalide - trop long"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Power
    with pytest.raises(PowerError):
        df = spookipy.Power(src_df0, value=-3, nomvar_out="ABCDEF").compute()
        # [ReaderStd --input {sources[0]}] >> [Power --value 2 --outputFieldName ABCDEF]


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Traitement de champs differents sur meme grille, meme forecastHour avec nomvar_out - Requete invalide"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Power
    with pytest.raises(PowerError):
        df = spookipy.Power(src_df0, value=2, nomvar_out="ABCD").compute()
        # [ReaderStd --input {sources[0]}] >> [Power --value 2 ] >> [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE ]


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec 2 champs"""

    source0 = plugin_test_path / "UUVV5x5_2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Power(src_df0, value=2).compute()
    # [ReaderStd --input {sources[0]}] >> [Power --value 2 ] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE ]

    # Pour fins de comparaison avec fichier original
    df.loc[:, "etiket"] = "POWER"

    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "exponent_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test power avec nomvar_out"""
    # open and read source
    source0 = plugin_test_path / "inputUU.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.Power(src_df0, value=2, nomvar_out="SQRT").compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName UU*] >>
    # [Power --value 2 --outputFieldName SQRT] >>
    # [WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE --noUnitConversion]

    df = spookipy.convip(df, style=RmnInterface.CONVIP_ENCODE_OLD)
    # Pour fins de comparaison avec fichier original
    df.loc[:, "etiket"] = "POWER"

    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    file_to_compare = plugin_test_path / "Power_test4_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare)
    assert res
