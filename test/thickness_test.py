# -*- coding: utf-8 -*-
from spookipy.thickness.thickness import Thickness
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pandas as pd
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp
import secrets


pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + "/Thickness/testsFiles/"

def test_1(plugin_test_dir):
     """Test avec un fichier de coordonnées Sigma."""
     # open and read source
     source0 = plugin_test_dir + "GZ_12000_10346_fileSrc.std"
     src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()
     print("std:")
     print(src_df0)
     # compute Thickness
     df = Thickness(src_df0,base=1.0,top=0.8346,coordinate_type='SIGMA_1001').compute()
     print(df)
     # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Thickness --base 1.0 --top 0.8346 --coordinateType SIGMA_COORDINATE] >> [WriterStd --output {destination_path} --encodeIP2andIP3 --ignoreExtended]
     # write the result
     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
     fstpy.StandardFileWriter(results_file, df)
     # open and read comparison file
     file_to_compare = plugin_test_dir + "Thick_test1-2_file2cmp.std"
     # compare results
     res = fstcomp(results_file, file_to_compare)
     assert(res)
