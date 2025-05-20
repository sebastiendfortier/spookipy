# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
from spookipy.rmn_interface import RmnInterface
import spookipy
import pandas as pd

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "Mask"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """seuils: 0,10,15,20 valeurs: 0,10,15,20 ops: ge,ge,ge,ge"""
    # open and read source
    source0 = plugin_test_path / "new_input.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Mask
    df = spookipy.Mask(
        src_df0, thresholds=[0.0, 10.0, 15.0, 20.0], values=[0.0, 10.0, 15.0, 20.0], operators=[">=", ">=", ">=", ">="]
    ).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Mask --thresholds 0.0,10.0,15.0,20.0 --values 0.0,10.0,15.0,20.0 --operators ge,ge,ge,ge] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df = spookipy.convip(df, RmnInterface.CONVIP_ENCODE_OLD)

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest1_20240829.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """seuils: -15,-15,-5,10,20 valeurs: -20,-15,-5,10,20 ops: le,ge,ge,ge,ge"""

    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Mask
    df = spookipy.Mask(
        src_df0,
        thresholds=[-15, -15, -5, 10, 20],
        values=[-20, -15, -5, 10, 20],
        operators=["<=", ">=", ">=", ">=", ">="],
    ).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Mask --thresholds -15,-15,-5,10,20 --values -20,-15,-5,10,20 --operators le,ge,ge,ge,ge] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest2_20240829.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """seuils: -10,0,10 valeurs: 1,2,3 ops: le,eq,gt"""

    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Mask
    df = spookipy.Mask(src_df0, thresholds=[-10, 0, 10], values=[1, 2, 3], operators=["<=", "==", ">"]).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Mask --thresholds -10,0,10 --values 1,2,3 --operators le,eq,gt] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest3_20240829.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path):
    """ERREUR: pas le meme nombre de valeurs associe a seuils, valeurs, et ops"""

    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.MaskError):
        # compute Mask
        _ = spookipy.Mask(src_df0, thresholds=[-10, 0, 10], values=[1, 2], operators=["<=", "=="]).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds -10,0,10 --values 1,2 --operators le,eq] >>
        # [WriterStd --output {destination_path} --noUnitConversion]


def test_5(plugin_test_path):
    """ERREUR: valeur invalide associee a operators (TT)"""

    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.MaskError):
        # compute Mask
        _ = spookipy.Mask(src_df0, thresholds=[-0, 10], values=[0, 10], operators=["<=", "TT"]).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds -0,10 --values 0,10 --operators le,'TT'] >>
        # [WriterStd --output {destination_path} --noUnitConversion]


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """seuils: -10,0,10 valeurs: 1,2,3 ops: le,eq,gt + outputFieldName=TOTO"""

    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Mask
    df = spookipy.Mask(
        src_df0, thresholds=[-10, 0, 10], values=[1, 2, 3], operators=["<=", "==", ">"], nomvar_out="TOTO"
    ).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    #  [Mask --thresholds -10,0,10 --values 1,2,3 --operators le,eq,gt --outputFieldName TOTO] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest6_20240829.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """Creation d'un binary mask avec seuils: 0.0,0.0,5.0 valeurs: 0.0,1.0,0.0 et ops: lt,ge,gt"""

    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    meta_df = src_df0.loc[src_df0.nomvar.isin(["^^", ">>", "P0", "PT"])].reset_index(drop=True)

    #  Selection des niveaux 1.0 a 0.9733
    df_reduit = src_df0.loc[src_df0.ip1.isin([12000, 11950, 11850, 11733])].copy()

    # compute Mask
    df_mask = spookipy.Mask(
        df_reduit, thresholds=[0.0, 0.0, 5.0], values=[0.0, 1.0, 0.0], operators=["<", ">=", ">"], binary_mask=True
    ).compute()

    # Champs input, pour respecter le : Zap --typeOfField FORECAST_MASKED
    df_reduit.loc[:, "typvar"] = "P@"

    # Concatenation des meta-donnees, des champs originaux avec typvar FORECAST_MASKET et resultats du mask
    df_final = pd.safe_concat([meta_df, df_mask, df_reduit])

    df_final["etiket"] = "G1_5_0_0N"
    df_final = spookipy.convip(df_final)

    # "[ReaderStd --input {sources[0]}] >>
    # [Select --verticalLevel 1.0@0.9733] >> ",
    # "([Mask --thresholds 0.0,0.0,5.0 --values 0.0,1.0,0.0 --operators LT,GE,GT --binaryMask] +
    #   [Zap --typeOfField FORECAST_MASKED]) >> ",
    # "[Zap --pdsLabel _5_0_0] >>
    # [WriterStd --output {destination_path}]"

    results_file = test_tmp_path / "test_7.std"
    fstpy.StandardFileWriter(results_file, df_final).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_7.std+20240415"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_8(plugin_test_path):
    """Creation d'un binary mask mais les valeurs ne sont pas 0.0 ou 1.0 uniquement - Requete invalide"""

    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #  Selection des niveaux 1.0 a 0.9733
    df_reduit = src_df0.loc[src_df0.ip1.isin([12000, 11950, 11850, 11733])]

    with pytest.raises(spookipy.MaskError):
        _ = spookipy.Mask(
            df_reduit,
            thresholds=[0.0, 0.0, 5.0],
            values=[0.0, 1.0, 999.0],
            operators=["<", ">=", ">"],
            binary_mask=True,
        ).compute()


def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """seuils: -10,0,10 valeurs: 1,2,3 ops: le,eq,gt + outputFieldName=TOTO - requete invalide"""

    source = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    with pytest.raises(spookipy.MaskError):
        _ = spookipy.Mask(
            src_df, thresholds=[-10, 0, 10], values=[1, 2, 3], operators=["<=", "==", ">"], nomvar_out="TOTO"
        ).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    #  [Mask --thresholds -10,0,10 --values 1,2,3 --operators le,eq,gt --outputFieldName TOTO] >>
    # [WriterStd --output {destination_path} --noUnitConversion]
