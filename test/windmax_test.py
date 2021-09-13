# -*- coding: utf-8 -*-
import fstpy.all as fstpy
import pytest
from test import TMP_PATH,TEST_PATH
from ci_fstcomp import fstcomp
import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/WindMax/testsFiles/'


def test_1(plugin_test_dir):
    """Calcul de Wind Max avec un fichier ayant des niveaux en millibars"""
    # open and read source
    source0 = plugin_test_dir + "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute WindMax
    df = spooki.WindMax(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindMax] >> [WriterStd --output {destination_path} --ignoreExtended ]

    # df.loc[:,'nbits'] = 32
    # df.loc[:,'datyp'] = 5
    #write the result
    results_file = TMP_PATH + "test_1.std"
    # print(results_file)
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windMax_pres_file2cmp.std"
    # file_to_compare = '/fs/site4/eccc/cmd/w/sbf000/testFiles/WindMax/test_1.std'

    #compare results
    res = fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Calcul de Wind Max avec un fichier ayant des niveaux en eta"""
    # open and read source
    source0 = plugin_test_dir + "UUVV_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute WindMax
    df = spooki.WindMax(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindMax] >> [WriterStd --output {destination_path} --ignoreExtended ]
    # df.loc[:,'nbits'] = 32
    # df.loc[:,'datyp'] = 5
    #write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windMax_eta_file2cmp.std+20210517"
    # file_to_compare = '/fs/site4/eccc/cmd/w/sbf000/testFiles/WindMax/test_2.std'

    #compare results
    res = fstcomp(results_file,file_to_compare,e_max=0.001)#,e_max=0.0003)
    fstpy.delete_file(results_file)
    assert(res)


def test_3(plugin_test_dir):
    """Calcul de Wind Max avec un fichier ayant des niveaux en eta et des PX"""
    # open and read source
    source0 = plugin_test_dir + "input_WindMax"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()


    #compute WindMax
    df = spooki.WindMax(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [WindMax] >> [WriterStd --output {destination_path} --ignoreExtended]
    # df.loc[:,'nbits'] = 32
    # df.loc[:,'datyp'] = 5
    #write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windMax_file2cmp.std+20210517"
    # file_to_compare = '/fs/site4/eccc/cmd/w/sbf000/testFiles/WindMax/test_3.std'

    #compare results
    res = fstcomp(results_file,file_to_compare,e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)
