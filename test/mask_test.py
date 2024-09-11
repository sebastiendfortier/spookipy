# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import rpnpy.librmn.all as rmn
import spookipy

pytestmark = [pytest.mark.regressions]

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
        src_df0, thresholds=[
            0.0, 10.0, 15.0, 20.0], values=[
            0.0, 10.0, 15.0, 20.0], operators=[
                '>=', '>=', '>=', '>=']).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Mask --thresholds 0.0,10.0,15.0,20.0 --values 0.0,10.0,15.0,20.0 --operators ge,ge,ge,ge] >>
    # [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df = spookipy.convip(df, rmn.CONVIP_ENCODE_OLD)

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest1_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """seuils: -15,-15,-5,10,20 valeurs: -20,-15,-5,10,20 ops: le,ge,ge,ge,ge"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Mask
    df = spookipy.Mask(src_df0, thresholds=[-15, -15, -5, 10, 20], values=[-20, -
                     15, -5, 10, 20], operators=['<=', '>=', '>=', '>=', '>=']).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Mask --thresholds -15,-15,-5,10,20 --values -20,-15,-5,10,20 --operators le,ge,ge,ge,ge] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest2_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """seuils: -10,0,10 valeurs: 1,2,3 ops: le,eq,gt"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Mask
    df = spookipy.Mask(src_df0,
                     thresholds=[-10,
                                 0,
                                 10],
                     values=[1,
                             2,
                             3],
                     operators=['<=',
                                '==',
                                '>']).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Mask --thresholds -10,0,10 --values 1,2,3 --operators le,eq,gt] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest3_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_4(plugin_test_path):
    """ERREUR: pas le meme nombre de valeurs associe a seuils, valeurs, et ops"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.MaskError):
        # compute Mask
        _ = spookipy.Mask(
            src_df0, thresholds=[-10, 0, 10], values=[1, 2], operators=['<=', '==']).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds -10,0,10 --values 1,2 --operators le,eq] >>
        # [WriterStd --output {destination_path} --noUnitConversion]

def test_5(plugin_test_path):
    """ERREUR: valeur invalide associee a operators (TT)"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.MaskError):
        # compute Mask
        _ = spookipy.Mask(
            src_df0, thresholds=[-0, 10], values=[0, 10], operators=['<=', 'TT']).compute()
        # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Mask --thresholds -0,10 --values 0,10 --operators le,'TT'] >>
        # [WriterStd --output {destination_path} --noUnitConversion]


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """seuils: -10,0,10 valeurs: 1,2,3 ops: le,eq,gt + outputFieldName=TOTO"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Mask
    df = spookipy.Mask(src_df0,
                     thresholds=[-10, 0, 10],
                     values=[1, 2, 3],
                     operators=['<=', '==', '>'],
                     nomvar_out='TOTO').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    #  [Mask --thresholds -10,0,10 --values 1,2,3 --operators le,eq,gt --outputFieldName TOTO] >>
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest6_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)
