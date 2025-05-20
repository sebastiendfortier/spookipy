# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "CloudFractionDiagnostic"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test regulier des donnees venant avec la demande de plugin"""
    # open and read source
    source0 = plugin_test_path / "HR_27_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute CloudFractionDiagnostic
    df = spookipy.CloudFractionDiagnostic(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [CloudFractionDiagnostic] >>
    # [Zap --pdsLabel CLDFRACTION --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df.loc[:, "etiket"] = "CLDFRACTION"

    # write the result
    results_file = test_tmp_path / "test_cfd_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "cfd_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)  # ,e_max=0.6)
    assert res
