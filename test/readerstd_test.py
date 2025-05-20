# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()
from spookipy.utils import VDECODE_IP_INFO
from spookipy.rmn_interface import RmnInterface

import fstpy
import spookipy
import pandas as pd
import numpy as np
import sys
import pytest
import ci_fstcomp
from datetime import timedelta
import rpnpy.librmn.all as rmn

pytestmark = [pytest.mark.regressions, pytest.mark.regressions2]
pd.set_option("display.max_rows", 3800, "display.max_columns", 3800)
np.set_printoptions(threshold=sys.maxsize)


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site6/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "ReaderStd"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test l'option --input avec un fichier qui n'existe pas!"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"

    # compute ReaderStd
    with pytest.raises(Exception):
        _ = spookipy.ReaderStd(df=None, input=source0 / "toto.fst").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}/toto.fst] >> [TrueOperation]


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier qui possède un champ de type entier (I3)."""
    # open and read source
    source0 = plugin_test_path / "regdiag_2012061300_012_fileSrc.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    df = spookipy.Select(df, nomvar=["UU", "VV", "T6"], reduce_df=False).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU,VV,T6] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "UU_VV_T6_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_2a(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier qui possède un champ de type entier compress (i6)."""
    # open and read source
    source0 = plugin_test_path / "compressed_unsigned_i6.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_2a.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "compressed_unsigned_i6.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
            "etiket",
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
        ],
    )
    assert res


def test_2b(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier qui possède un champ de type entier sign (S6)."""
    # open and read source
    source0 = plugin_test_path / "signed_S6.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_2b.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "signed_S6.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_write_small"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    df["datyp"] = 6
    df["nbits"] = 32
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "UUVV5x5_fileSrc.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_write_big"""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "input_big_fileSrc.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_write_sigma12000_pressure"""
    # open and read source
    source0 = plugin_test_path / "input_model"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    df = spookipy.Select(df, nomvar=["UU", "VV", "TT"], reduce_df=False).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU,VV,TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "sigma12000_pressure_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_write_big_noMetadata"""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --noMetadata --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_7.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "input_big_noMeta_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_file_with_duplicated_grid"""
    # open and read source
    source0 = plugin_test_path / "fstdWithDuplicatedGrid_fileSrc.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()

    df = spookipy.convip(df, style=RmnInterface.CONVIP_ENCODE)
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_8.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_2_file"""
    # open and read sources
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    source1 = plugin_test_path / "windChill_file2cmp.std"
    source2 = plugin_test_path / "windModulus_file2cmp.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=[source0, source1, source2]).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} {sources[1]} {sources[2]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_10.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()
    # open and read comparison file
    file_to_compare = plugin_test_path / "stdPlusstd_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_write_ip3"""
    # open and read source
    source0 = plugin_test_path / "ip3.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    df["datyp"] = 5
    df["nbits"] = 32
    # write the result
    results_file = test_tmp_path / "test_11.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "ip3.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_write_ip1_mb_newstyle"""
    # open and read source
    source0 = plugin_test_path / "UUVV93423264_hyb_fileSrc.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_12.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "UUVV93423264_hyb_fileSrc.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """test for file containing 2 HY"""
    # open and read source
    source0 = plugin_test_path / "2hy.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_13.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # compare results
    assert results_file.exists()


# ignore_extended is deprecated test_14 to test_18 are now invalid because of that
""" def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
    test reading fields with typvar == PZ
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5x2_fileSrc_PZ.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None,
                            input=source0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    df['datyp'] = 5
    df['nbits'] = 32
    # write the result
    results_file = test_tmp_path / "test_14.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "NEW/typvar_pz_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare,columns=[
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
    ])
    assert(res)

def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    test reading fields with typvar == PU
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5x2_fileSrc_PU.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None,
                            input=source0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    print(df)
    results_file = test_tmp_path / "test_15.std"
    spookipy.WriterStd(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "NEW/typvar_pu_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare,columns=[
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
    ])
    assert(res)

def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    test reading fields with typvar == PI
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5x2_fileSrc_PI.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None,
                            input=source0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_16.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "NEW/typvar_pi_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare,columns=[
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
    ])
    assert(res)

def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    test reading fields with typvar == PF
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5x2_fileSrc_PF.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None,
                            input=source0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_17.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "NEW/typvar_pf_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare,columns=[
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
    ])
    assert(res)

def test_18(plugin_test_path, test_tmp_path, call_fstcomp):
    test reading fields with typvar == PM
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5x2_fileSrc_PM.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None,
                            input=source0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_18.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "NEW/typvar_pm_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare,columns=[
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
    ])
    assert(res) """


def test_19(plugin_test_path, test_tmp_path, call_fstcomp):
    """test if HY is put in memory and written back when we have a grid with two kind of level, one of them being hybrid"""
    # open and read source
    source0 = plugin_test_path / "mb_plus_hybrid_fileSrc.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # [ReaderStd --input {sources[0]}] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_19.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "mb_plus_hybrid_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_20(plugin_test_path, test_tmp_path, call_fstcomp):
    """test if HY is put in memory and written back when we have a grid with hybrid level"""
    # open and read source
    source0 = plugin_test_path / "mb_plus_hybrid_fileSrc.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    df = spookipy.Select(df, nomvar=["FN"], reduce_df=False).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName FN] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_20.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "read_write_hy2_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_21(plugin_test_path, test_tmp_path, call_fstcomp):
    """test that the HY is NOT written back when the final grid don't have a hybrid level"""
    # open and read source
    source0 = plugin_test_path / "mb_plus_hybrid_fileSrc.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    df = spookipy.Select(df, nomvar=["PR"], reduce_df=False).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName PR] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_21.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "read_write_hy3_file2cmp.std+20210517"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_22(plugin_test_path, test_tmp_path, call_fstcomp):
    """test that PT is NOT read by the reader when the level type of the fields on the grid is not sigma"""
    # open and read source
    source0 = plugin_test_path / "pt_with_hybrid.std"

    "P0 manquant dans le fichier resultat vs comparaison qu'il en na un"
    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # [ReaderStd --input {sources[0]}] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_22.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "read_write_pt_when_no_sigma_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_23(plugin_test_path, test_tmp_path, call_fstcomp):
    """test that PT is NOT written back when there is a PT field created in memory and the level type of the fields on the grid is not sigma"""
    # open and read source
    source0 = plugin_test_path / "kt_ai_hybrid.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    df["nomvar"].replace("AI", "PT", inplace=True)
    "zapsmart pas encore implementer mais devrait fonctionner"
    # [ReaderStd --input {sources[0]}] >> [ZapSmart --fieldNameFrom AI --fieldNameTo PT] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_23.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "read_write_pt_when_no_sigma_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_25(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test la lecture avec ip2 != deet * npas"""
    # open and read source
    source0 = plugin_test_path / "2012121000_cancm3_m1_00_fileSrc.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()

    # [ReaderStd --input {sources[0]}] >> [WriterStd --output {destination_path} --writingMode APPEND]
    df = fstpy.add_columns(df, ["ip_info", "forecast_hour"])
    df = fstpy.reduce_columns(df)
    # write the result
    results_file = test_tmp_path / "test_25.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2012121000_cancm3_m1_00_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_26(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test la lecture d'un fichier pilot"""
    # open and read source
    source0 = plugin_test_path / "2015040800_030_piloteta"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # [ReaderStd --input {sources[0]}] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_26.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2015040800_030_piloteta"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_28(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test lecture fichiers contenant caractères spéciaux ET paramètre --input n'est pas le dernier"""
    # open and read sources
    source0 = plugin_test_path / "UUVV5x5_+fileSrc.std"
    source1 = plugin_test_path / "wind+Chill_file2cmp.std"
    source2 = plugin_test_path / "windModulus_file2cmp.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=[source0, source1, source2]).compute()
    # [ReaderStd --input {sources[0]} {sources[1]} {sources[2]} --ignoreExtended] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_28.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "stdPlusstd_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_29(plugin_test_path, test_tmp_path, call_fstcomp):
    """test lecture fichiers contenant des champs de donnees manquantes"""
    # open and read source
    source0 = plugin_test_path / "missingData.std+20231108"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()

    # ['[ReaderStd --input {sources[0]} --ignoreExtended] >> ', '[WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --flagMissingData]']

    # write the result
    results_file = test_tmp_path / "test_29.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_29.std+20231108"
    # modifier de resulttest_29.std+20231108 a resulttest_29.std+20240220 car PH devenait P?

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_30(plugin_test_path, test_tmp_path, call_fstcomp):
    """test lecture fichiers contenant des membres d'ensemble differents"""
    # open and read source
    source0 = plugin_test_path / "ensemble_members.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # ['[ReaderStd --input {sources[0]}] >> ', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

    # call of add and reduce columns fixes the etiket format
    df = fstpy.add_columns(df)
    df = fstpy.reduce_columns(df)

    # correction of encoding of ip1
    df = spookipy.convip(df, style=RmnInterface.CONVIP_ENCODE_OLD)

    # write the result
    results_file = test_tmp_path / "test_30.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_30.std+20210830"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
            "etiket",
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
        ],
    )
    assert res


def test_31(plugin_test_path, test_tmp_path, call_fstcomp):
    """test lecture fichiers contenant des masques"""
    # open and read source
    source0 = plugin_test_path / "data_with_mask.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    df = spookipy.Select(df, forecast_hour=[timedelta(hours=24)], reduce_df=False).compute()

    # ['[ReaderStd --input {sources[0]}] >> ', '[Select --forecastHour 24] >>', '[WriterStd --output {destination_path}]']

    # write the result
    results_file = test_tmp_path / "test_31"

    # WriterdStd of spookipy decodes ips and allows APPEND writing mode
    spookipy.WriterStd(df, results_file, writing_mode="APPEND").compute()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_31.std+2024-12-03"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_32(plugin_test_path, test_tmp_path, call_fstcomp):
    """test lecture fichiers contenant des membres d'ensemble differents"""
    # open and read source
    source0 = plugin_test_path / "ens_data_exclamation.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    df = spookipy.Select(df, nomvar=["WGEX"], reduce_df=False).compute()
    # ['[ReaderStd --input {sources[0]}] >>', '[Select --fieldName WGEX] >>', '[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]']

    # write the result
    results_file = test_tmp_path / "test_32.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_32.std+20210830"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_33(plugin_test_path, test_tmp_path, call_fstcomp):
    """test lecture fichiers contenant la coordonnee 5005"""
    # open and read source
    source0 = plugin_test_path / "resulttest_33.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # ['[ReaderStd --input {sources[0]}]>>', '[WriterStd --output {destination_path}]']

    # write the result
    results_file = test_tmp_path / "test_33.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_33.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_34(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test lecture fichiers contenant la coordonnée 5005 en groupant les données"""
    # open and read source
    source0 = plugin_test_path / "resulttest_33.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0, group5005=True).compute()

    # [ReaderStd --input {sources[0]} --group5005] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_34.std"
    spookipy.restore_5005_record(df)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_33.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_35(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test lecture fichiers contenant la coordonnée 5005"""
    # open and read source
    source0 = plugin_test_path / "coord_5005_big.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0, group5005=True).compute()
    # [ReaderStd --input {sources[0]} --group5005] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_35.std"
    spookipy.restore_5005_record(df)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_35.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


# --etiketFormat has yet to be implemented
""" def test_36(plugin_test_path, test_tmp_path, call_fstcomp):
    Test --etiketFormat. RUN=1, PDSLABEL=6, IMPLEMENTATION=1, MEMBER=3
    # open and read source
    source0 = plugin_test_path / "2021082706_000_analrms"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None,
                            input=source0,
                            etiketFormat="1,6,1,3").compute()
    df = spookipy.Select(
                    df, 
                    nomvar=['TT'],
                    reduce_df=False).compute()
    # [ReaderStd --input {sources[0]} --etiketFormat 1,6,1,3] >> [Select --fieldName TT] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_36.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test_etiketformat_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare,columns=[
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
    ])
    assert(res)
 """


def test_37(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test etiket with a dot, ex 'R1TR_0.3N'"""
    # open and read source
    source0 = plugin_test_path / "etiket_with_dot.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    df = spookipy.Select(df, label="TR_0.3", reduce_df=False).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --pdsLabel TR_0.3] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_37.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "etiket_with_dot_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_38(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test etiket spooki with ALL as the value of ensembleNumber, ex 'E1MEAN__NALL'"""
    # open and read source
    source0 = plugin_test_path / "etiket_RRLLLLLLIALL.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()

    df = spookipy.Select(df, label="MEAN__", reduce_df=False).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --pdsLabel MEAN__] >> [WriterStd --output {destination_path}]

    # write the result
    # New test file produced spookipy clean up of metadata has a different logic than spooki C++
    results_file = test_tmp_path / "test_38"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test_38_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


# hybrid_5100 has yet to be implemented in spookipy
""" def test_39(plugin_test_path, test_tmp_path, call_fstcomp):
    Test lecture fichiers contenant la coordonnée 5100
    # open and read source
    source0 = plugin_test_path / "2020022912_024_slv"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None,
                            input=source0).compute()
    # [ReaderStd --input {sources[0]}] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_39.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "read_write_5100_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare,columns=[
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
    ])
    assert(res)

def test_40(plugin_test_path, test_tmp_path, call_fstcomp):
    Test lecture fichiers contenant la coordonnée 5100 en groupant les données avec --group5005
    # open and read source
    source0 = plugin_test_path / "2020022912_024_slv"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None,
                            input=source0,
                            group5005=True).compute()
    # [ReaderStd --input {sources[0]} --group5005] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_40.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "read_write_5100_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare,columns=[
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
    ])
    assert(res) """


def test_41(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test etiket spooki with IIC as the value of ensembleNumber, ex 'R1558V0_N03H'"""
    # open and read sources
    source0 = plugin_test_path / "inputFile.std"
    source1 = plugin_test_path / "etiket_RR_LLLLLL_I_IIC.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=[source0, source1]).compute()
    df = spookipy.Select(df, ensemble_member="03H", reduce_df=False).compute()
    # [ReaderStd --input {sources[0]} {sources[1]}] >> [Select --ensembleMember 03H] >> [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_41.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "etiket_RR_LLLLLL_I_IIC.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


""" def test_42(plugin_test_path, test_tmp_path, call_fstcomp):
    Read write a TYPE_O grid
    # open and read source
    source0 = plugin_test_path / "grid_TYPE_O.std"

    # compute ReaderStd
    df = fstpy.StandardFileReader(source0).to_pandas()
    # [ReaderStd --input {sources[0]}] >> [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_42.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()
    
    # open and read comparison file
    file_to_compare = plugin_test_path / "grid_TYPE_O.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare,columns=[
        "etiket",
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
    ])
    assert(res)  """


def test_43(plugin_test_path, test_tmp_path, call_fstcomp):
    """Read write a typvar !@"""
    # open and read source
    source0 = plugin_test_path / "2024022612_cvd_CFS1_072"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()

    # forcing etiket replacement to pass the fstcomp , data is correct
    df.loc[df.nomvar.isin([">>", "^^"]), "etiket"] = "______X"

    # [ReaderStd --input {sources[0]}] >> [WriterStd --output {destination_path} --noUnitConversion --encodeIP2andIP3]

    # write the result
    results_file = test_tmp_path / "test_43.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_43_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
            "etiket",
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
        ],
    )
    assert res


def test_44(plugin_test_path, test_tmp_path, call_fstcomp):
    """Read a field with an encoded IP2 equal to 0.5H and DEET NPAS calculation that give the same result"""
    # open and read source
    source0 = plugin_test_path / "forecast_hour_0.5H.std"

    # compute ReaderStd
    df = spookipy.ReaderStd(df=None, input=source0).compute()
    # [ReaderStd --input {sources[0]}] >> [WriterStd --output {destination_path} --encodeIP2andIP3]

    # write the result
    results_file = test_tmp_path / "test_44.std"
    spookipy.WriterStd(df, results_file, encode_ip2_and_ip3=True).compute()

    # open and read comparison file
    file_to_compare = plugin_test_path / "forecast_hour_0.5H.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res


def test_45(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #45 : Read a file that have 2 identical records(META) except for ni. Only one record will be read and a warning message will be displayed."""
    # open and read sources
    source0 = plugin_test_path / "Gem_geophy.fst"

    # compute ReaderStd
    df0 = spookipy.ReaderStd(df=None, input=source0).compute()

    assert True


def test_46(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test lecture fichiers en chainant des appels au ReaderStd"""
    # open and read sources
    source0 = plugin_test_path / "UUVV5x5_+fileSrc.std"
    source1 = plugin_test_path / "wind+Chill_file2cmp.std"
    source2 = plugin_test_path / "windModulus_file2cmp.std"

    # compute ReaderStd
    df0 = spookipy.ReaderStd(df=None, input=source0).compute()

    df1 = spookipy.ReaderStd(df=df0, input=source1).compute()

    df2 = spookipy.ReaderStd(df=df1, input=source2).compute()

    # [ReaderStd --input {sources[0]} --ignoreExtended] >>
    # [ReaderStd --input {sources[1]} --ignoreExtended] >>
    # [ReaderStd --input {sources[2]} --ignoreExtended] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_46.std"
    fstpy.StandardFileWriter(results_file, df2).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "stdPlusstd_file2cmp.std"

    # compare results
    res = call_fstcomp(
        results_file,
        file_to_compare,
        columns=[
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
        ],
    )
    assert res
