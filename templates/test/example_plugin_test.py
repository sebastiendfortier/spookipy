# -*- coding: utf-8 -*-
# get the test directory definitions
from test import TEST_PATH, TMP_PATH

# fstpy is used to get dataframes from fst files
import fstpy
import pytest  # pytest is used to manage tests
import spookipy  # refers to this library

# tool used to compare fst files, just like fstcomp but in python
from ci_fstcomp import fstcomp
import secrets

# group of tests this test is associated with, see
# $project_root/test/pytest.ini to define test marks
pytestmark = [pytest.mark.regressions]

# input and comparison files are kept here
# ask anyone from spooki team to create de directories for you
# this refers to directories mirrored on
# /fs/site[3|4]/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/ExamplePlugin/testsFiles


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + "/ExamplePlugin/testsFiles/"


def test_1(plugin_test_dir):
    """Test description"""
    # open and read source
    # set the path of the file to read from
    source0 = plugin_test_dir + "source_file_in_plugin_test_dir_path.std"
    # get a dataframe from that file
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute ExamplePlugin
    # execute our plugin
    df = spookipy.ExamplePlugin(src_df0).compute()

    # write our results
    # set the path of the temporary file we are writing to
    results_file = "".join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    # make sure it does not exist
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()  # write our dataframe

    # open and read comparison file
    # set the path of the comparison file we are comparing to
    file_to_compare = plugin_test_dir + "windModulus_file2cmp.std"

    # compare results
    # compare files
    res = fstcomp(results_file, file_to_compare)
    # cleanup our temporary file
    fstpy.delete_file(results_file)
    # assert the results matched
    assert res
