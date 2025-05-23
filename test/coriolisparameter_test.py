# -*- coding: utf-8 -*-
import numpy as np
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "CoriolisParameter"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calculate with a simple test data"""
    # open and read source
    source0 = plugin_test_path / "UUVVTT_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute CoriolisParameter
    df = spookipy.CoriolisParameter(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [CoriolisParameter] >>
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "coriop_file2cmp_test_1_20230124.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)  # ,e_max=0.13)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Spooki must succeed when inputs are in millibars"""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ["UU"])

    # compute CoriolisParameter
    df = spookipy.CoriolisParameter(src_df0).compute()

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "coriop_file2cmp_test_2_20230124.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calculate with a simple test data with d as a ndarray"""
    # open and read source
    source0 = plugin_test_path / "UUVVTT_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.compute(src_df0)
    src_df0.loc[:, "path"] = None
    src_df0.loc[:, "key"] = None
    src_df0["d"] = src_df0.apply(lambda row: np.asarray(row["d"]), axis=1)

    # compute CoriolisParameter
    df = spookipy.CoriolisParameter(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >>
    # [CoriolisParameter] >>
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "coriop_file2cmp_test_1_20230124.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)  # ,e_max=0.13)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Spooki must succeed when inputs are in millibars with d as a ndarray"""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_regpres"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.select_with_meta(src_df0, ["UU"])

    src_df0 = fstpy.compute(src_df0)
    src_df0.loc[:, "path"] = None
    src_df0.loc[:, "key"] = None
    src_df0["d"] = src_df0.apply(lambda row: np.asarray(row["d"]), axis=1)

    # compute CoriolisParameter
    df = spookipy.CoriolisParameter(src_df0).compute()

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "coriop_file2cmp_test_2_20230124.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
