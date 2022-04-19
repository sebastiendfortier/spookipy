# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + "Pressure/testsFiles/"


def test_1(plugin_test_dir):
    """Test sur un fichier sortie de modele eta avec l'option --coordinateType ETA_COORDINATE. VCODE 1002"""
    # open and read source
    source0 = plugin_test_dir + "tt_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "TT").compute()
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
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_1"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_2(plugin_test_dir):
    """Test sur un fichier sortie de modele eta avec les options --coordinateType ETA_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "TT", standard_atmosphere=True).compute()

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
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_2"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


# # def test_3(plugin_test_dir):
# #     """Test sur un fichier sortie de modele eta avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_eta_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField TT] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_3.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_eta_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


# # def test_4(plugin_test_dir):
# #     """Test sur un fichier sortie de modele eta avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_eta_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT ] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_4.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_eta_std_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


def test_5(plugin_test_dir):
    """Test sur un fichier sortie de modele Sigma, avec l'option --coordinateType SIGMA_COORDINATE. VCODE 1001"""
    # open and read source
    source0 = plugin_test_dir + "hu_sig_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "HU").compute()
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
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_5"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.1)
    fstpy.delete_file(results_file)
    assert(res)


def test_6(plugin_test_dir):
    """Test sur un fichier sortie de modele Sigma, avec les options --coordinateType SIGMA_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "hu_sig_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "HU", standard_atmosphere=True).compute()
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
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_6"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


# # def test_7(plugin_test_dir):
# #     """Test sur un fichier sortie de modele Sigma, avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "hu_sig_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField HU] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_7.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_sig_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


# # def test_8(plugin_test_dir):
# #     """Test sur un fichier sortie de modele Sigma, avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "hu_sig_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField HU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_8.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_sig_std_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


def test_9(plugin_test_dir):
    """Test sur un fichier sortie de modele hybrid, avec l'option --coordinateType HYBRID_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "TT").compute()
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
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_9"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_10(plugin_test_dir):
    """Test sur un fichier sortie de modele Hybrid avec les options --coordinateType HYBRID_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "TT",standard_atmosphere=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >>
    # [Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # df.loc[df.nomvar.isin(['>>','^^','HY','P0']),'etiket'] = 'R1580V0N'

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_10.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_10"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


# # def test_11(plugin_test_dir):
# #     """Test sur un fichier sortie de modele Hybrid, avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "input_hyb_2011100712_012.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_11.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb2_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


# # def test_12(plugin_test_dir):
# #     """Test sur un fichier sortie de modele Hybrid avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb_std_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


def test_13(plugin_test_dir):
    """Test sur un fichier sortie de modele Hybrid staggered, avec l'option --coordinateType HYBRID_STAGGERED_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "UU").compute()
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
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_13"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_14(plugin_test_dir):
    """Test sur un fichier sortie de modele Hybrid staggered, avec les options --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "UU", standard_atmosphere=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField UU] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # df.loc[df.nomvar.isin(['!!','P0','^^','>>']),'etiket'] = '__PRESSX'
    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_14.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_stg_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_14"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


# # def test_15(plugin_test_dir):
# #     """Test sur un fichier sortie de modele hybrid staggered, avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --input {sources[0]}] >>
# [Pressure --coordinateType AUTODETECT --referenceField UU] >>
# [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_15.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb_stg_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


# # def test_16(plugin_test_dir):
# #     """Test sur un fichier sortie de modele Hybrid staggered, avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField UU] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_16.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb_stg_std_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


def test_17(plugin_test_dir):
    """Test sur un fichier sortie de modele en pression, avec l'option --coordinateType PRESSURE_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "tt_pres_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "TT").compute()
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
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_17"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_18(plugin_test_dir):
    """Test sur un fichier sortie de modele en pression avec les options --coordinateType PRESSURE_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_pres_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "TT",standard_atmosphere=True).compute()
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
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_18"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


# # def test_19(plugin_test_dir):
# #     """Test sur un fichier sortie de modele en pression l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --referenceField TT] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_19.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_pres_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


# # def test_20(plugin_test_dir):
# #     """Test sur un fichier sortie de modele en pression avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_20.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_pres_std_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


# # def test_21(plugin_test_dir):
# #     """Test avec -- coordinateType ETA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees ETA - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_21.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res)


# # def test_22(plugin_test_dir):
# #     """Test avec l'option -- coordinateType ETA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees ETA - Champs PT et P0 sont absents."""
# #     # open and read source
# #     source0 = plugin_test_dir + "input_eta_2008061012_000_model_noPTnoP0.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_22.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res)


# # def test_23(plugin_test_dir):
# #     """Test avec -- coordinateType SIGMA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees SIGMA - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_23.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res)


# # def test_24(plugin_test_dir):
# #     """Test avec l'option -- coordinateType SIGMA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees SIGMA - Champ P0 est absent."""
# #     # open and read source
# #     source0 = plugin_test_dir + "hu_sig_noP0_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField HU] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_24.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res)


# # def test_25(plugin_test_dir):
# #     """Test avec l'option -- coordinateType HYBRID_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_25.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res)


# # def test_26(plugin_test_dir):
# #     """Test avec l'option -- coordinateType HYBRID_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID - Champs P0 et HY sont absents."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_hyb_noP0noHYnoBB_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_26.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res)


# # def test_27(plugin_test_dir):
# #     """Test avec l'option -- coordinateType HYBRID_STAGGERED_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID STAGGERED - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_27.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res)


# # def test_28(plugin_test_dir):
# #     """Test avec l'option -- coordinateType HYBRID_STAGGERED_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID STAGGERED- Champs P0 et HY sont absents."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_hyb_noP0noHYnoBB_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_28.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res)


# # def test_29(plugin_test_dir):
# #     """Test avec l'option -- coordinateType PRESSURE_COORDINATE alors que le fichier d'entree n'est pas en pression."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_eta_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType PRESSURE_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_29.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res)


def test_30(plugin_test_dir):
    """Test avec un fichier contenant differentes heures de prevision."""
    # open and read source
    source0 = plugin_test_dir + "input_vrpcp24_00_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "TT").compute()
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
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_30"

    # compare results
    res = fstcomp(results_file, file_to_compare, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


# # def test_31(plugin_test_dir):
# #     """Test avec un fichier contenant differentes heures de prevision."""
# #     # open and read source
# #     source0 = plugin_test_dir + "input_test_31.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[Select --exclude --fieldName PX] >> ', '[Pressure --coordinateType AUTODETECT --referenceField TT] >>', '[Zap --pdsLabel EH02558_X --metadataZappable --doNotFlagAsZapped]>>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended ]']

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_31.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "resulttest_31_TT.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


# # def test_32(plugin_test_dir):
# #     """Test avec un fichier glbpres avec l'option --coordinateType HYBRID_STAGGERED_COORDINATE"""
# #     # open and read source
# #     source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --referenceField TT] >>[WriterStd --output {destination_path} --ignoreExtended ]

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_32.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "glbpres_hybrid_staggered_coordinate_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res)


def test_33(plugin_test_dir):
    """Test avec un fichier glbpres avec l'option --coordinateType PRESSURE_COORDINATE"""
    # open and read source
    source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0, ['TT'])
    tt_df = tt_df.loc[tt_df.ip1 != 93423264]

    # compute spooki.Pressure
    df = spooki.Pressure(tt_df, "TT").compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType PRESSURE_COORDINATE --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended ]
    # df['etiket'] = 'PRESSR'
    # df.loc[df.nomvar.isin(['!!','^^','>>']),'etiket'] = 'G1_4_0_0N'

    # write the result
    
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_33.std"])
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "glbpres_pressure_coordinate_file2cmp.std+20210517"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_33"
    # !!   X  G1_4_0_0N           3      51     1 00000000 000000         52341     87193         0        0        0  E 64  X  2001     0     0     0 cmp_file
    # !!   X  G1_4_0_0N           3     164     1 00000000 000000         52341     87193         0        0        0  E 64  X  5002    75   450   450 spookipy

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_34(plugin_test_dir):
    """Test avec un fichier qui genere des artefacts dans les cartes"""
    # open and read source
    source0 = plugin_test_dir + "2019091000_000_input.orig"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "TT").compute()
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
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_34"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_35(plugin_test_dir):
    """Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE thermodynamic"""
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "TT").compute()
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
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_35"

    # compare results
    res = fstcomp(results_file, file_to_compare, exclude_meta=True, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


def test_36(plugin_test_dir):
    """Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE"""
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spooki.Pressure
    df = spooki.Pressure(src_df0, "UU").compute()
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
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_36"

    # compare results
    res = fstcomp(results_file, file_to_compare, exclude_meta=True, e_max=0.01)
    fstpy.delete_file(results_file)
    assert(res)


# # def test_37(plugin_test_dir):
# #     """Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE thermo sub grid - attendu fail"""
# #     # open and read source
# #     source0 = plugin_test_dir + "coord_5005_big.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #['[ReaderStd --ignoreExtended --input {sources[0]} ]>> ', '[Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField CK] >> ', '[Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

# #     #write the result
# #     results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_37.std"])
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res)
