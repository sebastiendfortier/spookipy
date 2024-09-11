# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy

pytestmark = [pytest.mark.regressions]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "WindModulusAndDirection"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_select_write_UV"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WindModulus
    df = spookipy.WindModulus(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [WindModulus] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
 
    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "windModulus_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_select_write_UV2"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WindModulus
    df = spookipy.WindModulus(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [WindModulus] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
   
    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "windModulus3D_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

# def test_3(plugin_test_path):
#     pass


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_select_write_UV_already_calculated"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_UV_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WindModulus
    df = spookipy.WindModulus(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [WindModulus] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_4.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "windModulus_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_select_write_UV_already_calculated_without_UU_VV"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_UV_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WindModulus
    df = spookipy.WindModulus(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName UV,UU,VV] >> 
    # [WindModulus --optimizationLevel 1] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "windModulus_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_select_write_UV_already_calculated2"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_UV_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WindModulus
    df = spookipy.WindModulus(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [WindModulus] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "windModulus3D_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert(res)

# def test_7(plugin_test_path):
#     pass

# def test_8(plugin_test_path):
#     pass


def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_read_select_write_UV_GRID_X"""
    # open and read source
    source0 = plugin_test_path / "uu_850.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_path / "vv_850.std"
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()

    src_df  = pd.concat([src_df0, src_df1], ignore_index=True)

    # compute WindModulus
    df = spookipy.WindModulus(src_df).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]} {sources[1]}] >> 
    # [WindModulus] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "windmodulus3D850_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


# def test_10(plugin_test_path):
#     """test_read_select_write_UV with wind_modulus_cpp"""
#     # open and read source
#     source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     #compute WindModulus
#     df = spookipy.WindModulus(src_df0,True).compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindModulus] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
#     df.loc[:,'etiket'] = 'WINDMODULUS'
#     #write the result
#     results_file = test_tmp_path / "test_1.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_path / "windModulus_file2cmp.std"

#     #compare results
#     res = fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)
