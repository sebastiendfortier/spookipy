# -*- coding: utf-8 -*-
from test import TMP_PATH,TEST_PATH             # get the test directory definitions
import pytest                                   # pytest is used to manage tests
import fstpy.all as fstpy                       # fstpy is used to get dataframes from fst files
import spookipy.all as spooki                   # refers to this library
from ci_fstcomp import fstcomp                  # tool used to compare fst files, just like fstcomp but in python

pytestmark = [pytest.mark.regressions]          # group of tests this test is associated with, see $project_root/test/pytest.ini to define test marks

# input and comparison files are kept here
# ask anyone from spooki team to create de directories for you
# this refers to directories mirrored on /fs/site[3|4]/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/ExamplePlugin/testsFiles
@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/ExamplePlugin/testsFiles/' 

def test_1(plugin_test_dir):
    """Test description"""
    # open and read source
    source0 = plugin_test_dir + "source_file_in_plugin_test_dir_path.std"            # set the path of the file to read from
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()                          # get a dataframe from that file

    # compute ExamplePlugin
    df = spooki.ExamplePlugin(src_df0).compute()                                     # execute our plugin

    # write our results                                                                                     
    results_file = TMP_PATH + "test_1.std"                                           # set the path of the temporary file we are writing to
    fstpy.delete_file(results_file)                                                  # make sure it does not exist  
    fstpy.StandardFileWriter(results_file, df).to_fst()                              # write our dataframe

    # open and read comparison file
    file_to_compare = plugin_test_dir + "windModulus_file2cmp.std"                   # set the path of the comparison file we are comparing to

    #compare results
    res = fstcomp(results_file,file_to_compare)                                      # compare files
    fstpy.delete_file(results_file)                                                  # cleanup our temporary file
    assert(res)                                                                      # assert the results matched
