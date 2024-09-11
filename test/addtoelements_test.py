# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "AddToElement"

def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_offset1"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_zeros_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute AddToElement
    df      = spookipy.AddToElement(src_df0,
                                    value=4).compute()
    # [ReaderStd --input {sources[0]}] >> [AddToElement --value +4.0] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df['etiket'] = "ADDTOE"  # Pour respecter le ignoreExtended

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "offset_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_offset2"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_zeros_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute AddToElement
    df      = spookipy.AddToElement(src_df0,
                                    value=-2).compute()
    # [ReaderStd --input {sources[0]}] >> [AddToElement --value -2.0] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    
    df['etiket'] = "ADDTOE"  # Pour respecter le ignoreExtended
    
    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "offset2_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)
