# -*- coding: utf-8 -*-
import fstpy.all as fstpy
import pytest
from test import TMP_PATH,TEST_PATH

import spookipy.all as spooki
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/CloudFractionDiagnostic/testsFiles/'



def test_1(plugin_test_dir):
    """Test regulier des donnees venant avec la demande de plugin"""
    # open and read source
    source0 = plugin_test_dir + "HR_27_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute CloudFractionDiagnostic
    df = spooki.CloudFractionDiagnostic(src_df0).compute()
    #[ReaderStd --input {sources[0]}] >> [CloudFractionDiagnostic] >>
    # [Zap --pdsLabel CLDFRACTION --doNotFlagAsZapped] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df.loc[:,'etiket'] = 'CLDFRACTION'
    # df.loc[:,'datyp'] = 5
    # df.loc[:,'nbits'] = 32

    #write the result
    results_file = TMP_PATH + "test_cfd_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "cfd_file2cmp.std"
    # file_to_compare = "/home/sbf000/data/testFiles/CloudFractionDiagnostic/result_test_cfd_1"

    #compare results
    res = fstcomp(results_file,file_to_compare)#,e_max=0.6)
    fstpy.delete_file(results_file)
    assert(res)
