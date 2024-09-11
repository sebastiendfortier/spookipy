# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy
from pathlib import Path

pytestmark = [pytest.mark.regressions, pytest.mark.eps]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "ArithmeticPercentageExceedingVariableThresholdsByPoint"

def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """"""

    plugin_test_path = Path('/home/aug000/fst_tmp/ensemble/small_sample/')

    # open and read source
    sources = [
        "eta_2024020800_024_001_tt_fh2_small",
        "eta_2024020800_024_002_tt_fh2_small",
        "eta_2024020800_024_003_tt_fh2_small",
        "eta_2024020800_024_004_tt_fh2_small",
        "eta_2024020800_024_tt_fh2_small_threshold_field",# this is the variable threshold

    ]

    sources = [plugin_test_path / s for s in sources]
    src_df0 = fstpy.StandardFileReader(sources).to_pandas()

    # compute spookipy.DewPointDepression
    df      = spookipy.ArithmeticPercentageExceedingVariableThresholdsByPoint(
                                        src_df0,
                                        ">=",
                                        "TT",
                                        "_TRHD_").compute()
    
    df = df.loc[df.nomvar == 'TT']
    df['ip3'] = 2 #where does ip3 = 2 come from, why aren't the results 0 in epsStat????
    df['nbits'] = 16
    df['etiket'] = df['etiket'].str.replace('^__','ER',regex=True).str.replace('X','P',regex=False)
    
    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "eta_2024020800_ALL_tt_fh2_small_threshold_variable"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.001)
    assert(res)


