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
    return "WindMax"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de Wind Max avec un fichier ayant des niveaux en millibars"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WindMax
    df = spookipy.WindMax(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [WindMax] >> [WriterStd --output {destination_path} --ignoreExtended ]

    df['etiket'] = 'WNDMAX'

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "windMax_pres_file2cmp.std+20240422"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de Wind Max avec un fichier ayant des niveaux en eta"""
    # open and read source
    source0 = plugin_test_path / "UUVV_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WindMax
    df = spookipy.WindMax(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [WindMax] >> [WriterStd --output {destination_path} --ignoreExtended ]

    # write the result
    df.loc[df.nomvar.isin(['UU','VV','UV','PX']),'etiket'] = 'WNDMAX'

    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "windMax_eta_file2cmp.std+20210817"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)  # ,e_max=0.0003)
    assert(res)


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de Wind Max avec un fichier ayant des niveaux en eta et des PX"""
    # open and read source
    source0 = plugin_test_path / "input_WindMax"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WindMax
    df = spookipy.WindMax(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [WindMax] >> [WriterStd --output {destination_path} --ignoreExtended]

    df['etiket'] = 'WNDMAX'

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "windMax_file2cmp.std+20210817"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert(res)
