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
    return "TotalTotalsIndex"

def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de l'indice total-total avec TT à 850 et 500 mb et ES à 850 mb."""
    # open and read source
    source0 = plugin_test_path / "TT850_500_ES_850_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TotalTotalsIndex
    df = spookipy.TotalTotalsIndex(src_df0).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [TotalTotalsIndex] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # Note:  Fichier de comparaison recree en 20231026 en ne tenant pas compte du ignoreExtended.

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "TotalTotalsIndex_file2cmp_20231026.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)
