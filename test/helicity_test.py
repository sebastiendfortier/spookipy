# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.skip]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "Helicity"

def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test du plugin Helicity"""
    # open and read source
    source0 = plugin_test_path / "UUVVGZ77x57x54_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Helicity
    df = spookipy.Helicity(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Helicity] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --makeIP1EncodingWorkWithTests]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "helicity3_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)
