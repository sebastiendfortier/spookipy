# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy
from spookipy.rmn_interface import RmnInterface

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "GridPointDifference"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """--axis X,Y --differenceType CENTERED"""
    # open and read source
    source0 = plugin_test_path / "6x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0["dateo"] = 347333813
    src_df0["nbits"] = 16
    src_df0["datyp"] = 1

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x", "y"], difference_type="centered", copy_input=True).compute()

    df.loc[df.nomvar == "FDX", "nomvar"] = "FFDX"
    df.loc[df.nomvar == "FDY", "nomvar"] = "FFDY"

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --unit scalar --doNotFlagAsZapped] >>
    # ([Copy] + [GridPointDifference --axis X,Y --differenceType CENTERED]) >>
    # [ZapSmart --fieldNameFrom FDX --fieldNameTo FFDX] >> [ZapSmart --fieldNameFrom FDY --fieldNameTo FFDY] >>
    # [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XYCentered_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDifference_Z_centered"""
    # open and read source
    source0 = plugin_test_path / "4z2x2y_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0["dateo"] = 347333813
    src_df0["nbits"] = 16
    src_df0["datyp"] = 1

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["z"], difference_type="centered").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [GridPointDifference --axis Z --differenceType CENTERED] >> [Zap --fieldName FFDZ --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df.loc[df.nomvar == "FF", "nomvar"] = "FFDZ"

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "new_ZCentered_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDifference_XY_forward"""
    # open and read source
    source0 = plugin_test_path / "6x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0["dateo"] = 347333813
    src_df0["nbits"] = 16
    src_df0["datyp"] = 1

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x", "y"], difference_type="forward").compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [GridPointDifference --axis X,Y --differenceType FORWARD] >>
    # [ZapSmart --fieldNameFrom FDX --fieldNameTo FFDX] >> [ZapSmart --fieldNameFrom FDY --fieldNameTo FFDY] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    df.loc[df.nomvar == "FDX", "nomvar"] = "FFDX"
    df.loc[df.nomvar == "FDY", "nomvar"] = "FFDY"

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XYForward_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDifference_Z_forward"""
    # open and read source
    source0 = plugin_test_path / "4z2x2y_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0["dateo"] = 347333813
    src_df0["nbits"] = 16
    src_df0["datyp"] = 1

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["z"], difference_type="forward").compute()

    df.loc[df.nomvar == "FF", "nomvar"] = "FFDZ"

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [GridPointDifference --axis Z --differenceType FORWARD] >> [Zap --fieldName FFDZ --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "new_ZForward_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDifference_XY_backward"""
    # open and read source
    source0 = plugin_test_path / "6x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0["dateo"] = 347333813
    src_df0["nbits"] = 16
    src_df0["datyp"] = 1

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x", "y"], difference_type="backward").compute()

    df.loc[df.nomvar == "FDX", "nomvar"] = "FFDX"
    df.loc[df.nomvar == "FDY", "nomvar"] = "FFDY"

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [GridPointDifference --axis X,Y --differenceType BACKWARD] >>
    # [ZapSmart --fieldNameFrom FDX --fieldNameTo FFDX] >> [ZapSmart --fieldNameFrom FDY --fieldNameTo FFDY] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XYBackward_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDifference_Z_backward"""
    # open and read source
    source0 = plugin_test_path / "4z2x2y_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0["dateo"] = 347333813
    src_df0["nbits"] = 16
    src_df0["datyp"] = 1

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["z"], difference_type="backward").compute()

    df.loc[df.nomvar == "FF", "nomvar"] = "FFDZ"

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [GridPointDifference --axis Z --differenceType BACKWARD] >> [Zap --fieldName FFDZ --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "new_ZBackward_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_gridPointDifference_XY_centered2"""
    # open and read source
    source0 = plugin_test_path / "tape10_UU.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x", "y"], difference_type="centered", copy_input=True).compute()

    df.loc[df.nomvar == "FDX", "nomvar"] = "UUDX"
    df.loc[df.nomvar == "FDY", "nomvar"] = "UUDY"
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # ([Copy] + [GridPointDifference --axis X,Y --differenceType CENTERED]) >>
    # [ZapSmart --fieldNameFrom FDX --fieldNameTo UUDX] >>
    # [ZapSmart --fieldNameFrom FDY --fieldNameTo UUDY] >>
    # [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_7.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XYCentered2_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_8(plugin_test_path):
    """test_gridPointDifference_Z_1level"""
    # open and read source
    source0 = plugin_test_path / "4z2x2y_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()

    src_df0 = src_df0.loc[src_df0.level == 0.0]
    src_df0["dateo"] = 347333813
    src_df0["nbits"] = 16
    src_df0["datyp"] = 1

    # compute GridPointDifference
    with pytest.raises(spookipy.GridPointDifferenceError):
        _ = spookipy.GridPointDifference(src_df0, axis=["z"], difference_type="centered").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --verticalLevel 0] >>
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >>
    # [GridPointDifference --axis Z --differenceType CENTERED]


def test_9(plugin_test_path):
    """test_gridPointDifference_Xsize1"""
    # open and read source
    source0 = plugin_test_path / "tictac.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar == "BB"]

    # compute GridPointDifference
    with pytest.raises(spookipy.GridPointDifferenceError):
        _ = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName BB] >>
    # [GridPointDifference --axis X --differenceType CENTERED]


def test_10(plugin_test_path):
    """test_gridPointDifference_Ysize1"""
    # open and read source
    source0 = plugin_test_path / "tictac.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar == "AA"]

    # compute GridPointDifference
    with pytest.raises(spookipy.GridPointDifferenceError):
        _ = spookipy.GridPointDifference(src_df0, axis=["y"], difference_type="centered").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName AA] >> [GridPointDifference --axis Y --differenceType CENTERED]


def test_11(plugin_test_path):
    """test_gridPointDifference_moreThan1PDS"""
    # open and read source
    source0 = plugin_test_path / "tape10.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    with pytest.raises(spookipy.GridPointDifferenceError):
        _ = spookipy.GridPointDifference(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDifference --axis X,Y --differenceType CENTERED]


def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
    """Difference centree avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_path / "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    meta_df = src_df0.loc[src_df0.nomvar.isin(["!!", "P0", "PT", ">>", "^^", "^>", "HY", "!!SF"])]
    src_df0 = fstpy.add_columns(src_df0, "ip_info")
    src_df0 = src_df0.loc[(src_df0.nomvar == "TT") & (src_df0.level == 1000.0)]
    src_df0 = pd.safe_concat([src_df0, meta_df])

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x", "y"], difference_type="centered").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT --verticalLevel 1000] >>
    # [GridPointDifference --axis X,Y --differenceType CENTERED] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # On convertit les ip1 car les donnees d'input sont en mb non encodes
    # et dans le fichier de comparaison, les ips etaient encodes.
    df = spookipy.convip(df, RmnInterface.CONVIP_ENCODE)

    # write the result
    results_file = test_tmp_path / "test_12.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XYCentered_YY_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """Difference vers l'avant (forward) avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_path / "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    meta_df = src_df0.loc[src_df0.nomvar.isin(["!!", "P0", "PT", ">>", "^^", "^>", "HY", "!!SF"])]
    src_df0 = fstpy.add_columns(src_df0, "ip_info")
    src_df0 = src_df0.loc[(src_df0.nomvar == "TT") & (src_df0.level == 1000.0)]
    src_df0 = pd.safe_concat([src_df0, meta_df])

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x", "y"], difference_type="forward").compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT --verticalLevel 1000] >>
    # [GridPointDifference --axis X,Y --differenceType FORWARD] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # On convertit les ip1 car les donnees d'input sont en mb non encodes
    # et dans le fichier de comparaison, les ips etaient encodes.
    df = spookipy.convip(df, RmnInterface.CONVIP_ENCODE)

    # write the result
    results_file = test_tmp_path / "test_13.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XYForward_YY_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
    """Difference vers l'arriere  avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_path / "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    meta_df = src_df0.loc[src_df0.nomvar.isin(["!!", "P0", "PT", ">>", "^^", "^>", "HY", "!!SF"])]
    src_df0 = fstpy.add_columns(src_df0, "ip_info")
    src_df0 = src_df0.loc[(src_df0.nomvar == "TT") & (src_df0.level == 1000.0)]
    src_df0 = pd.safe_concat([src_df0, meta_df])

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x", "y"], difference_type="backward").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT --verticalLevel 1000] >>
    # [GridPointDifference --axis X,Y --differenceType BACKWARD] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # On convertit les ip1 car les donnees d'input sont en mb non encodes
    # et dans le fichier de comparaison, les ips etaient encodes.
    df = spookipy.convip(df, RmnInterface.CONVIP_ENCODE)

    # write the result
    results_file = test_tmp_path / "test_14.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "XYBackward_YY_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence vers l'arriere avec un fichier global réduit (grille type Z)."""
    # open and read source
    source0 = plugin_test_path / "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    meta_df = src_df0.loc[src_df0.nomvar.isin(["!!", "P0", "PT", ">>", "^^", "^>", "HY", "!!SF"])]
    src_df0 = fstpy.add_columns(src_df0, "ip_info")
    src_df0 = src_df0.loc[(src_df0.nomvar == "TT") & (src_df0.level == 1000.0)]
    src_df0 = pd.safe_concat([src_df0, meta_df])

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="backward").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
    #                 "[Select --fieldName TT --verticalLevel 1000] >> ",
    #                 "[GridPointDifference --axis X --differenceType BACKWARD] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_15.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test15_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence vers l'avant avec un fichier global réduit (grille type Z)."""
    # open and read source
    source0 = plugin_test_path / "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    meta_df = src_df0.loc[src_df0.nomvar.isin(["!!", "P0", "PT", ">>", "^^", "^>", "HY", "!!SF"])]
    src_df0 = fstpy.add_columns(src_df0, "ip_info")
    src_df0 = src_df0.loc[(src_df0.nomvar == "TT") & (src_df0.level == 1000.0)]
    src_df0 = pd.safe_concat([src_df0, meta_df])

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="forward").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >>",
    #                 "[Select --fieldName TT --verticalLevel 1000] >> ",
    #                 "[GridPointDifference --axis X --differenceType FORWARD] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_16.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test16_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence centrée avec un fichier global réduit (grille type Z)."""
    # open and read source
    source0 = plugin_test_path / "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    meta_df = src_df0.loc[src_df0.nomvar.isin(["!!", "P0", "PT", ">>", "^^", "^>", "HY", "!!SF"])]
    src_df0 = fstpy.add_columns(src_df0, "ip_info")
    src_df0 = src_df0.loc[(src_df0.nomvar == "TT") & (src_df0.level == 1000.0)]
    src_df0 = pd.safe_concat([src_df0, meta_df])

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
    #                 "[Select --fieldName TT --verticalLevel 1000] >> ",
    #                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_17.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test17_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_18(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence centrée avec un fichier global réduit (grille type A)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridA.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >>",
    #                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_18.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test18_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_19(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence centrée avec un fichier global réduit (grille type B)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridB.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
    #                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_19.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test19_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_20(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence centrée avec un fichier global réduit (grille type L avec longitude qui ne se repete pas)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
    #                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_20.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test20_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_21(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence centrée avec un fichier global réduit (grille type L avec 1ere longitude qui se repete a la fin)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
    #                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_21.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test21_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_22(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence centrée avec un fichier global réduit (grille type L avec longitude qui fait plus que le tour de la terre)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL3.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
    #                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_22.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test22_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_23(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence centrée avec un fichier global réduit (grille type L avec longitude qui ne fait pas le tour de la terre)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL4.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
    #                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_23.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test23_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_24(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence centrée avec un fichier global réduit (grille type L avec longitude qui ne fait pas le tour de la terre)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL5.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
    #                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_24.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test24_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


#             " INFORMATIONS SUPPLEMENTAIRES": "Le test suivant sert a tester la fonction IsGlobalGrid particulierement. Cas ou l'increment de la grille ne divise pas parfaitement le globe",
def test_25(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence centrée avec un fichier global réduit (fait le tour de la terre, 1ere longitude ne se repete pas mais distance inegale entre le dernier point et le point 0; considéré comme une grille globale)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL6.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
    #                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = test_tmp_path / "test_25.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test25_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_26(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence centrée avec un fichier global réduit (fait le tour de la terre, 1ere longitude se repete mais longitude differente entre le dernier point et le point 0; considéré comme une grille NON globale)."""
    # open and read source
    source0 = plugin_test_path / "GlbPres_gridL7.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
    #                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"
    # write the result
    results_file = test_tmp_path / "test_26.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_test26_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_27(plugin_test_path, test_tmp_path, call_fstcomp):
    """Différence centrée avec une grille de type G (grille globale par defaut sans repetition de longitude)."""
    # open and read source
    source0 = plugin_test_path / "GlbHyb_gridG_reduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spookipy.GridPointDifference(src_df0, axis=["x"], difference_type="centered").compute()
    #                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
    #                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
    #                 "[WriterStd --output {destination_path} --noUnitConversion]"
    df.loc[~(df.nomvar == "TT"), "etiket"] = "Y3H9DNX"

    # write the result
    results_file = test_tmp_path / "test_27.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbhyb_test27_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_28(plugin_test_path, test_tmp_path, call_fstcomp):
    """2 groupes de TT avec dates d'origine differentes mais dates de validity identiques"""

    source = plugin_test_path / "Regpres_TTHUES_differentDateoSameDatev.std"
    src_df = fstpy.StandardFileReader(source).to_pandas()

    df = spookipy.GridPointDifference(src_df, axis=["x"], difference_type="centered").compute()

    # write the result
    results_file = test_tmp_path / "test_28.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    # [ReaderStd --input /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/testsFiles/Regpres_TTHUES_differentDateoSameDatev.std] >>
    # [GridPointDifference  --axis X --differenceType CENTERED --plugin_language CPP] >>
    # [WriterStd --output glbhyb_test28_file2cmp.std]"

    file_to_compare = plugin_test_path / "regpres_test28_file2cmp.std"
    # file_to_compare =  "/home/gha000/data/SpookiPython/spookipy/test/GDIFF.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
