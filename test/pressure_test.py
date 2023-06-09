# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets
from spookipy.pressure.pressure import \
    PressureError
pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + "Pressure/testsFiles/"


def test_1(plugin_test_dir):
    """Test sur un fichier sortie de modele eta avec l'option --coordinateType ETA_COORDINATE. VCODE 1002"""
    # open and read source
    source0 = plugin_test_dir + "tt_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType ETA_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel R1580V0N] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df.loc[:, 'etiket'] = 'R1580V0N'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_eta_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_1"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Test sur un fichier sortie de modele eta avec les options --coordinateType ETA_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT", standard_atmosphere=True).compute()

    # df.loc[df.nomvar.isin(['>>','^^','P0','PT']),'etiket'] = 'R1580V0N'
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >>
    # [Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_2.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_eta_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_2"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

# # def test_3(plugin_test_dir):
# # Test identique au test 1 puisque --coordinateType n'est plus une option dans la version python

# # def test_4(plugin_test_dir):
# # Test identique au test 2 puisque --coordinateType n'est plus une option dans la version python

def test_5(plugin_test_dir):
    """Test sur un fichier sortie de modele Sigma, avec l'option --coordinateType SIGMA_COORDINATE. VCODE 1001"""
    # open and read source
    source0 = plugin_test_dir + "hu_sig_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "HU").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType SIGMA_COORDINATE --referenceField HU ] >>
    # [Zap --pdsLabel R1580V0N] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    df.loc[df.nomvar != 'P0', 'etiket'] = 'R1580V0N'
    # df.loc[df.nomvar=='P0','etiket'] = 'GA72A16N'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_5.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_sig_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_5"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir):
    """Test sur un fichier sortie de modele Sigma, avec les options --coordinateType SIGMA_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "hu_sig_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "HU", standard_atmosphere=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >>
    # [Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField HU] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # df.loc[df.nomvar=='P0','etiket'] = 'GA72A16N'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_6.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_sig_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_6"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

# # def test_7(plugin_test_dir):
# # Test identique au test 5 puisque --coordinateType n'est plus une option dans la version python

# # def test_8(plugin_test_dir):
# # Test identique au test 5 puisque --coordinateType n'est plus une option dans la version python

def test_9(plugin_test_dir):
    """Test sur un fichier sortie de modele hybrid, avec l'option --coordinateType HYBRID_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT").compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType HYBRID_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel R1580V0N] >>
    # [WriterStd --output {destination_path} --ignoreExtended]']
    df.loc[:, 'etiket'] = 'R1580V0N'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_9.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_9"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_10(plugin_test_dir):
    """Test sur un fichier sortie de modele Hybrid avec les options --coordinateType HYBRID_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT",standard_atmosphere=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >>
    # [Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_10"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_11(plugin_test_dir):
    """Test sur un fichier sortie de modele Hybrid."""
    # open and read source
    source0 = plugin_test_dir + "input_hyb_2011100712_012.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spookipy.Pressure
    df = spookipy.Pressure(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Pressure --coordinateType AUTODETECT --referenceField TT] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb2_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


# # def test_12(plugin_test_dir):
# # Test identique au test 10 puisque --coordinateType n'est plus une option dans la version python

def test_13(plugin_test_dir):
    """Test sur un fichier sortie de modele Hybrid staggered, avec l'option --coordinateType HYBRID_STAGGERED_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "UU").compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --referenceField UU] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    df.loc[df.nomvar.isin(['!!', '>>', '^^', 'P0']), 'etiket'] = 'PRESS'
    # print(df[['nomvar','etiket']])

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_stg_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_13"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_14(plugin_test_dir):
    """Test sur un fichier sortie de modele Hybrid staggered, avec les options --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "UU", standard_atmosphere=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField UU] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_14.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_stg_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_14"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


# # def test_15(plugin_test_dir):
# # Test identique au test 13 puisque --coordinateType n'est plus une option dans la version python

# # def test_16(plugin_test_dir):
# # Test identique au test 14 puisque --coordinateType n'est plus une option dans la version python


def test_17(plugin_test_dir):
    """Test sur un fichier sortie de modele en pression, avec l'option --coordinateType PRESSURE_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "tt_pres_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType PRESSURE_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    df.loc[:, 'etiket'] = 'R1580V0N'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_17.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_pres_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_17"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_18(plugin_test_dir):
    """Test sur un fichier sortie de modele en pression avec les options --coordinateType PRESSURE_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_pres_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT",standard_atmosphere=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >>
    # [Pressure --coordinateType PRESSURE_COORDINATE --standardAtmosphere --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # df.loc[df.nomvar.isin(['^^','>>']),'etiket'] = 'R1580V0N'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_18.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_pres_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_18"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


# # def test_19(plugin_test_dir):
# # Test identique au test 17 puisque --coordinateType n'est plus une option dans la version python

# # def test_20(plugin_test_dir):
# # Test identique au test 18 puisque --coordinateType n'est plus une option dans la version python


########################################################################################################################
## Les tests 21 a 29 (version C++) ne sont plus necessaires.  Ces derniers servaient a valider
## le coordinateType demande avec l'information du fichier d'entree.
## Dans la version python, l'option coordinateType n'existe plus, on fait la detection du type de 
## fichier (AUTODETECT)
########################################################################################################################

def test_30(plugin_test_dir):
    """Test avec un fichier contenant differentes heures de prevision."""
    # open and read source
    source0 = plugin_test_dir + "input_vrpcp24_00_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType AUTODETECT --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noMetadata]
    df.loc[:, 'etiket'] = 'R110K80N'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_30.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "input_vrpcp24_00_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_30"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_31(plugin_test_dir):
    """Test avec un fichier contenant differentes heures de prevision."""
    # open and read source
    source0 = plugin_test_dir + "input_test_31.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    # src_df0 = src_df0.loc([src_df0.nomvar != 'PX'])
    src_df0 = src_df0.loc[~src_df0.nomvar.isin(["PX"])].reset_index(drop=True)

    #compute spookipy.Pressure
    df = spookipy.Pressure(src_df0).compute()
    df = df.loc[~df.nomvar.isin(["P0", ">>", "^^"])].reset_index(drop=True)
    #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[Select --exclude --fieldName PX] >> ', '[Pressure --coordinateType AUTODETECT --referenceField TT] >>', '[Zap --pdsLabel EH02558_X --metadataZappable --doNotFlagAsZapped]>>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended ]']
    df.loc[:, 'etiket'] = 'EH02558_X'

    #write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_31.std"])
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_31_TT.std"

    #compare results
    res = fstcomp(results_file,file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_32(plugin_test_dir):
    """Test avec un fichier glbpres, avec TT en coordonnes HYBRID_STAGGERED_COORDINATE"""
    # open and read source
    source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # On veut seulement concerver le TT au niveau 1 hy
    tt_df = fstpy.select_with_meta(src_df0, ['TT'])
    tt_df = tt_df.loc[(tt_df.ip1 == 93423264) | (tt_df.nomvar != "TT")]

    #compute spookipy.Pressure
    df = spookipy.Pressure(tt_df, 'TT').compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --referenceField TT] >>[WriterStd --output {destination_path} --ignoreExtended ]

    #write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_32.std"])
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_hybrid_staggered_coordinate_file2cmp.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_33(plugin_test_dir):
    """Test avec un fichier glbpres, TT en coordonnes PRESSURE_COORDINATE"""
    # open and read source
    source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0, ['TT'])
    tt_df = tt_df.loc[tt_df.ip1 != 93423264]

    # compute spookipy.Pressure
    df = spookipy.Pressure(tt_df, "TT").compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType PRESSURE_COORDINATE --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_33.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_pressure_coordinate_file2cmp.std+20210517"
    
    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_34(plugin_test_dir):
    """Test avec un fichier qui genere des artefacts dans les cartes"""
    # open and read source
    source0 = plugin_test_dir + "2019091000_000_input.orig"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType ETA_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel G1_7_0_0N --nbitsForDataStorage e32]>>
    # [WriterStd --output {destination_path} --ignoreExtended --noMetadata --IP1EncodingStyle OLDSTYLE]
    df.loc[:, 'etiket'] = 'G1_7_0_0N'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_34.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "d.compute_pressure_varicelle_rslt.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_35(plugin_test_dir):
    """Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE thermodynamic"""
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT").compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]} ]>>
    # [Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>
    # [Select --metadataFieldName P0,>>,^^ --exclude] >>
    # [WriterStd --output {destination_path} --ignoreExtended]']
    df.loc[:, 'etiket'] = 'R1_V710_N'
    df = df.loc[~df.nomvar.isin(["^^", ">>", "P0"])]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_35.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_35_TT.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_35"

    # compare results
    res = fstcomp(results_file, file_to_compare, exclude_meta=True, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_36(plugin_test_dir):
    """Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE"""
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "UU").compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]} ]>>
    # [Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField UU] >>
    # [Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>
    # [Select --metadataFieldName P0,>>,^^ --exclude] >>
    # [WriterStd --output {destination_path} --ignoreExtended]']
    df.loc[:, 'etiket'] = 'R1_V710_N'
    df = df.loc[~df.nomvar.isin(["^^", ">>", "P0"])]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_36.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()
    
    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_36_UU.std"

    # compare results
    res = fstcomp(results_file, file_to_compare, exclude_meta=True, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_37(plugin_test_dir):
    """Test avec un fichier 5005 - P0 manquant donc ne peut fonctionner """
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spookipy.Pressure
    # [ReaderStd --ignoreExtended --input {sources[0]} --group5005] >>
    # [Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField CK] 

    # # compute MatchLevelIndexToValue
    with pytest.raises(PressureError):
        _ = spookipy.Pressure(src_df0, "CK").compute()

# # def test_38(plugin_test_dir):
# # Test qui ne semble plus pertinent car teste le groupement lors de la lecture

def test_39(plugin_test_dir):
    """Test avec un fichier glbpres """
    # Nouveau test en python; amalgame des tests 32 et 33 pour calculer la pression sur les 2 types
    # de coordonnees (pressure et hybrid)

    # open and read source
    source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # On veut seulement concerver tous les TT (hy et mb)
    tt_df = fstpy.select_with_meta(src_df0, ['TT'])

    #compute spookipy.Pressure
    df = spookipy.Pressure(tt_df, 'TT').compute()

    #write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_39.std"])
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_2types_of_coordinate_file2cmp.std"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
