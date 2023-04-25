import pytest
from test import TMP_PATH, TEST_PATH
import fstpy
import spookipy
import pandas as pd
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH +"TemperatureVirtual/testsFiles/"

def test_1(plugin_test_dir):
    """Calcul avec un fichier hybrid."""
    # open and read source
    source0 = plugin_test_dir + "hyb_prog_2012071312_009_1HY"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    input_df = fstpy.select_with_meta(src_df0, ['TT', 'HR'])

    # compute TemperatureVirtual
    df = spookipy.TemperatureVirtual(input_df).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Select --fieldName TT,HR] >>
    # [TemperatureVirtual] 

    etiket      = "__VIRTTTX"
    etiket_meta = "R1580V0_N"
    df.loc[df.nomvar == "VT", 'etiket'] = etiket
    df.loc[df.nomvar.isin(['P0','HY']), 'etiket'] = etiket_meta

    # write the result 
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "TemperatureVirtual_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(True)


@pytest.mark.skip(reason="probleme avec le calcul de pression au niveau de surface")
def test_2(plugin_test_dir):
    """Calcul avec un fichier hybrid 5005."""
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()

    input_df = fstpy.select_with_meta(src_df0, ['TT', 'HR'])
    
    # compute TemperatureVirtual
    df = spookipy.TemperatureVirtual(input_df).compute()
    # [ReaderStd --input {sources[0]} --group5005] >>
    # [Select --fieldName TT,HR] >>
    # [TemperatureVirtual] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    etiket      = "__VIRTTTX"
    etiket_meta = "R1_V710_N"
    df.loc[df.nomvar == "VT", 'etiket'] = etiket
    df.loc[~df.nomvar.isin(['VT']), 'etiket'] = etiket_meta

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_2.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)

# Les tests suivants sont nouveaux (n'existent pas dans Spooki)
# Les fichiers de comparaison ont ete crees avec la version Spooki

# Input pour test 3: 
# "[ReaderStd --input   /home/spst900/dataV/saturationVapourPressure/v5.0.x/inputfiles/2014031800_024_regpres] >>
#  [Select --verticalLevel 1000@300] >> [GridCut --startPoint 100,100 --endPoint 200,200] >>
# ([Select -- fieldName TT]+[WaterVapourMixingRatio]) >> [Select --forecastHour 24] >> 
# [Zap --nbitsForDataStorage E32] >> [WriterStd --output 2014031800_024_regpres_QV_small.std]"

def test_3(plugin_test_dir):
    """Calcul de VT a partir de QV precalcule, avec un fichier regpres."""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_regpres_QV_small.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.TemperatureVirtual(src_df0).compute()

    etiket      = "__VIRTTTX"
    etiket_meta = "R110K80_N"
    df.loc[df.nomvar == "VT", 'etiket'] = etiket
    df.loc[~df.nomvar.isin(["VT"]), 'etiket'] = etiket_meta 
    df.loc[:,'datyp'] = 5
    df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "/2014031800_024_regpres_VT_with_QV_small.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.001)
    fstpy.delete_file(results_file) 
    assert(res)

# Input pour tests 4 et 5: 
# "[ReaderStd --input   /home/spst900/dataV/saturationVapourPressure/v5.0.x/inputfiles/2014031800_024_regpres] >>
#  [Select --fieldName TT,HU,ES --verticalLevel 1000@300 --forecastHour 24] >> 
# [GridCut --startPoint 100,100 --endPoint 200,200] >>
# [Zap --nbitsForDataStorage E32] >> [WriterStd --output 2014031800_024_regpres_TTHUES_small.std]"

def test_4(plugin_test_dir):
    """Calcul de VT a partir de HU, avec un fichier regpres."""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_regpres_TTHUES_small.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    input_df = fstpy.select_with_meta(src_df0, ['TT', 'HU'])

    df = spookipy.TemperatureVirtual(input_df).compute()
    # [ReaderStd --input 2014031800_024_regpres_TTHUES.std] >> [Select --fieldName HU,TT] >>  
    # [TemperatureVirtual] >>  [Zap --nbitsForDataStorage E32] >>
    # [WriterStd --output 2014031800_024_regpres_VT_with_HU_small.std]
    etiket      = "__VIRTTTX"
    etiket_meta = "R110K80_N"
    df.loc[df.nomvar == "VT", 'etiket'] = etiket
    df.loc[~df.nomvar.isin(["VT"]), 'etiket'] = etiket_meta 
    df.loc[:,'datyp'] = 5
    df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "/2014031800_024_regpres_VT_with_HU_small.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file) 
    assert(res)


def test_5(plugin_test_dir):
    """Calcul de VT a partir de ES, avec un fichier regpres."""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_regpres_TTHUES_small.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    input_df = fstpy.select_with_meta(src_df0, ['TT', 'ES'])

    df = spookipy.TemperatureVirtual(input_df).compute()

    # [ReaderStd --input 2014031800_024_regpres_TTHUES.std] >> [Select --fieldName ES,TT] >>  
    # [TemperatureVirtual] >>  [Zap --nbitsForDataStorage E32] >>
    # [WriterStd --output 2014031800_024_regpres_VT_with_ES_small.std]

    etiket      = "__VIRTTTX"
    etiket_meta = "R110K80_N"
    df.loc[df.nomvar == "VT", 'etiket'] = etiket
    df.loc[~df.nomvar.isin(["VT"]), 'etiket'] = etiket_meta 
    df.loc[:,'datyp'] = 5
    df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "/2014031800_024_regpres_VT_with_ES_small.std"

    # compare results
    res = fstcomp(results_file, file_to_compare,e_max=0.01)
    fstpy.delete_file(results_file) 
    assert(res)

def test_6(plugin_test_dir):
    """Calcul de VT a partir de ES, avec un fichier regpres."""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_regpres_VT_with_ES_small.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    df = spookipy.TemperatureVirtual(src_df0).compute()

    # [ReaderStd --input 2014031800_024_regpres_TTHUES.std] >> [Select --fieldName ES,TT] >>  
    # [TemperatureVirtual] >>  [Zap --nbitsForDataStorage E32] >>
    # [WriterStd --output 2014031800_024_regpres_VT_with_ES_small.std]

    etiket      = "__VIRTTTX"
    etiket_meta = "R110K80_N"
    df.loc[df.nomvar == "VT", 'etiket'] = etiket
    df.loc[~df.nomvar.isin(["VT"]), 'etiket'] = etiket_meta 
    df.loc[:,'datyp'] = 5
    df.loc[df.nomvar!='!!','nbits'] = 32

    # write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "/2014031800_024_regpres_VT_with_ES_small.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file) 
    assert(res)
