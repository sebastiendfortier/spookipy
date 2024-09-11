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
    return "MultiplyElementBy"

def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_factor1"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_1_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute MultiplyElementBy
    df = spookipy.MultiplyElementBy(src_df0, value=3).compute()
    # [ReaderStd --input {sources[0]}] >> [MultiplyElementBy --value 3.0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df = spookipy.convip(df, style=rmn.CONVIP_ENCODE_OLD)
    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "factor_file2cmp.std"

    # compare results - on exclut l'etiket
    cols=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 
          'datyp', 'nbits', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4']
    res = call_fstcomp(results_file, file_to_compare,columns=cols)
    assert(res)


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """test_factor2"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_1_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute MultiplyElementBy
    df = spookipy.MultiplyElementBy(src_df0, value=0.333).compute()
    # [ReaderStd --input {sources[0]}] >> [MultiplyElementBy --value 0.333] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df = spookipy.convip(df, style=rmn.CONVIP_ENCODE_OLD)
    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "factor2_file2cmp.std"

    # compare results - on exclut l'etiket
    cols=['nomvar', 'typvar', 'ni', 'nj', 'nk', 'dateo', 'ip1', 'ip2', 'ip3', 'deet', 'npas', 
          'datyp', 'nbits', 'grtyp', 'ig1', 'ig2', 'ig3', 'ig4']
    res = call_fstcomp(results_file, file_to_compare,columns=cols)
    assert(res)
