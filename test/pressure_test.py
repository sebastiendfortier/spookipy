# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import pytest
import spookipy.all as spooki
import fstpy.all as fstpy
import pandas as pd

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH +"Pressure/testsFiles/"



def test_1(plugin_test_dir):
    """Test #1 : Test sur un fichier sortie de modele eta avec l'option --coordinateType ETA_COORDINATE. VCODE 1002"""
    # open and read source
    source0 = plugin_test_dir + "tt_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType ETA_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel R1580V0N] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()
    
    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_eta_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_1"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_2(plugin_test_dir):
    """Test #2 : Test sur un fichier sortie de modele eta avec les options --coordinateType ETA_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT",True).compute()
    df.loc[:,'etiket'] = 'PRESSR'
    df.loc[df.nomvar.isin(['>>','^^','P0','PT']),'etiket'] = 'R1580V0N'
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> 
    # [Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_eta_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_2"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


# # def test_3(plugin_test_dir):
# #     """Test #3 : Test sur un fichier sortie de modele eta avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_eta_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField TT] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_3.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_eta_file2cmp.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


# # def test_4(plugin_test_dir):
# #     """Test #4 : Test sur un fichier sortie de modele eta avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_eta_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT ] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_4.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_eta_std_file2cmp.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


def test_5(plugin_test_dir):
    """Test #5 : Test sur un fichier sortie de modele Sigma, avec l'option --coordinateType SIGMA_COORDINATE. VCODE 1001"""
    # open and read source
    source0 = plugin_test_dir + "hu_sig_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"HU").compute()
    df.loc[:,'etiket'] = 'R1580V0N'
    df.loc[df.nomvar=='P0','etiket'] = 'GA72A16N'

    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Pressure --coordinateType SIGMA_COORDINATE --referenceField HU ] >>
    # [Zap --pdsLabel R1580V0N] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_sig_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_5"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_6(plugin_test_dir):
    """Test #6 : Test sur un fichier sortie de modele Sigma, avec les options --coordinateType SIGMA_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "hu_sig_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"HU",True).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> 
    # [Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField HU] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df.loc[:,'etiket'] = 'PRESSR'
    df.loc[df.nomvar=='P0','etiket'] = 'GA72A16N'
    #write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_sig_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_6"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


# # def test_7(plugin_test_dir):
# #     """Test #7 : Test sur un fichier sortie de modele Sigma, avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "hu_sig_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField HU] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_7.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_sig_file2cmp.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


# # def test_8(plugin_test_dir):
# #     """Test #8 : Test sur un fichier sortie de modele Sigma, avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "hu_sig_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField HU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_8.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_sig_std_file2cmp.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


def test_9(plugin_test_dir):
    """Test #9 : Test sur un fichier sortie de modele hybrid, avec l'option --coordinateType HYBRID_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Pressure --coordinateType HYBRID_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel R1580V0N] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]']

    #write the result
    results_file = TMP_PATH + "test_9.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_9"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_10(plugin_test_dir):
    """Test #10 : Test sur un fichier sortie de modele Hybrid avec les options --coordinateType HYBRID_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT",True).compute()
    df['etiket'] = 'PRESSR'
    df.loc[df.nomvar.isin(['>>','^^','HY','P0']),'etiket'] = 'R1580V0N'
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> 
    # [Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_10.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_10"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


# # def test_11(plugin_test_dir):
# #     """Test #11 : Test sur un fichier sortie de modele Hybrid, avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "input_hyb_2011100712_012.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_11.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb2_file2cmp.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


# # def test_12(plugin_test_dir):
# #     """Test #12 : Test sur un fichier sortie de modele Hybrid avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_12.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb_std_file2cmp.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


def test_13(plugin_test_dir):
    """Test #13 : Test sur un fichier sortie de modele Hybrid staggered, avec l'option --coordinateType HYBRID_STAGGERED_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"UU").compute()
    #[ReaderStd --input {sources[0]}] >> 
    # [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --referenceField UU] >>
    # [WriterStd --output {destination_path} --ignoreExtended]
    df['etiket'] = 'PRESSR'
    df.loc[df.nomvar.isin(['!!','>>','^^','P0']),'etiket'] = 'PRESS'
    # print(df[['nomvar','etiket']])

    #write the result
    results_file = TMP_PATH + "test_13.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_stg_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_13"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_14(plugin_test_dir):
    """Test #14 : Test sur un fichier sortie de modele Hybrid staggered, avec les options --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"UU",True).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField UU] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]
    df.loc[:,'etiket'] = 'PRESSR'
    df.loc[df.nomvar.isin(['!!','P0','^^','>>']),'etiket'] = '__PRESSX'
    #write the result
    results_file = TMP_PATH + "test_14.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_stg_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_14"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


# # def test_15(plugin_test_dir):
# #     """Test #15 : Test sur un fichier sortie de modele hybrid staggered, avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --input {sources[0]}] >> 
# [Pressure --coordinateType AUTODETECT --referenceField UU] >> 
# [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_15.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb_stg_file2cmp.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


# # def test_16(plugin_test_dir):
# #     """Test #16 : Test sur un fichier sortie de modele Hybrid staggered, avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField UU] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_16.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb_stg_std_file2cmp.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


def test_17(plugin_test_dir):
    """Test #17 : Test sur un fichier sortie de modele en pression, avec l'option --coordinateType PRESSURE_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "tt_pres_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Pressure --coordinateType PRESSURE_COORDINATE --referenceField TT] >> 
    # [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "test_17.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_pres_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_17"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_18(plugin_test_dir):
    """Test #18 : Test sur un fichier sortie de modele en pression avec les options --coordinateType PRESSURE_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_pres_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT",True).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> 
    # [Pressure --coordinateType PRESSURE_COORDINATE --standardAtmosphere --referenceField TT] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df.loc[:,'etiket'] = 'PRESSR'
    df.loc[df.nomvar.isin(['^^','>>']),'etiket'] = 'R1580V0N'
    #write the result
    results_file = TMP_PATH + "test_18.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_pres_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_18"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


# # def test_19(plugin_test_dir):
# #     """Test #19 : Test sur un fichier sortie de modele en pression l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --referenceField TT] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_19.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_pres_file2cmp.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


# # def test_20(plugin_test_dir):
# #     """Test #20 : Test sur un fichier sortie de modele en pression avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_20.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_pres_std_file2cmp.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


# # def test_21(plugin_test_dir):
# #     """Test #21 : Test avec -- coordinateType ETA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees ETA - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_21.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     assert(res == True)


# # def test_22(plugin_test_dir):
# #     """Test #22 : Test avec l'option -- coordinateType ETA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees ETA - Champs PT et P0 sont absents."""
# #     # open and read source
# #     source0 = plugin_test_dir + "input_eta_2008061012_000_model_noPTnoP0.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_22.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     assert(res == True)


# # def test_23(plugin_test_dir):
# #     """Test #23 : Test avec -- coordinateType SIGMA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees SIGMA - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_23.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     assert(res == True)


# # def test_24(plugin_test_dir):
# #     """Test #24 : Test avec l'option -- coordinateType SIGMA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees SIGMA - Champ P0 est absent."""
# #     # open and read source
# #     source0 = plugin_test_dir + "hu_sig_noP0_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField HU] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_24.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     assert(res == True)


# # def test_25(plugin_test_dir):
# #     """Test #25 : Test avec l'option -- coordinateType HYBRID_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_25.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     assert(res == True)


# # def test_26(plugin_test_dir):
# #     """Test #26 : Test avec l'option -- coordinateType HYBRID_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID - Champs P0 et HY sont absents."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_hyb_noP0noHYnoBB_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_26.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     assert(res == True)


# # def test_27(plugin_test_dir):
# #     """Test #27 : Test avec l'option -- coordinateType HYBRID_STAGGERED_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID STAGGERED - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_27.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     assert(res == True)


# # def test_28(plugin_test_dir):
# #     """Test #28 : Test avec l'option -- coordinateType HYBRID_STAGGERED_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID STAGGERED- Champs P0 et HY sont absents."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_hyb_noP0noHYnoBB_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_28.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     assert(res == True)


# # def test_29(plugin_test_dir):
# #     """Test #29 : Test avec l'option -- coordinateType PRESSURE_COORDINATE alors que le fichier d'entree n'est pas en pression."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_eta_fileSrc.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType PRESSURE_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_29.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     assert(res == True)


def test_30(plugin_test_dir):
    """Test #30 : Test avec un fichier contenant differentes heures de prevision."""
    # open and read source
    source0 = plugin_test_dir + "input_vrpcp24_00_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Pressure --coordinateType AUTODETECT --referenceField TT] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noMetadata]

    #write the result
    results_file = TMP_PATH + "test_30.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "input_vrpcp24_00_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_30"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


# # def test_31(plugin_test_dir):
# #     """Test #31 : Test avec un fichier contenant differentes heures de prevision."""
# #     # open and read source
# #     source0 = plugin_test_dir + "input_test_31.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[Select --exclude --fieldName PX] >> ', '[Pressure --coordinateType AUTODETECT --referenceField TT] >>', '[Zap --pdsLabel EH02558_X --metadataZappable --doNotFlagAsZapped]>>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended ]']

# #     #write the result
# #     results_file = TMP_PATH + "test_31.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "resulttest_31_TT.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


# # def test_32(plugin_test_dir):
# #     """Test #32 : Test avec un fichier glbpres avec l'option --coordinateType HYBRID_STAGGERED_COORDINATE"""
# #     # open and read source
# #     source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --referenceField TT] >>[WriterStd --output {destination_path} --ignoreExtended ]

# #     #write the result
# #     results_file = TMP_PATH + "test_32.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "glbpres_hybrid_staggered_coordinate_file2cmp.std"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     fstpy.delete_file(results_file)
# #     assert(res == True)


def test_33(plugin_test_dir):
    """Test #33 : Test avec un fichier glbpres avec l'option --coordinateType PRESSURE_COORDINATE"""
    # open and read source
    source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df = src_df0.query('nomvar=="TT" and ip1!=93423264').reset_index(drop=True)
    # print(src_df[['nomvar','ip1']])
    meta_df = src_df0.query('nomvar in ["!!","HY","P0","PT","^^",">>"]').reset_index(drop=True)

    src_df = pd.concat([src_df,meta_df],ignore_index=True)
    # print(src_df[['nomvar','ip1']].to_string())
    #compute spooki.Pressure
    df = spooki.Pressure(src_df,"TT").compute()

    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Pressure --coordinateType PRESSURE_COORDINATE --referenceField TT] >> 
    # [WriterStd --output {destination_path} --ignoreExtended ]
    df['etiket'] = 'PRESSR'
    df.loc[df.nomvar.isin(['!!','^^','>>']),'etiket'] = 'G1_4_0_0N'

    #write the result

    results_file = TMP_PATH + "test_33.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_pressure_coordinate_file2cmp.std+20210517"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_33"
    # !!   X  G1_4_0_0N           3      51     1 00000000 000000         52341     87193         0        0        0  E 64  X  2001     0     0     0 cmp_file
    # !!   X  G1_4_0_0N           3     164     1 00000000 000000         52341     87193         0        0        0  E 64  X  5002    75   450   450 spookipy
    
    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_34(plugin_test_dir):
    """Test #34 : Test avec un fichier qui genere des artefacts dans les cartes"""
    # open and read source
    source0 = plugin_test_dir + "2019091000_000_input.orig"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Pressure --coordinateType ETA_COORDINATE --referenceField TT] >> 
    # [Zap --pdsLabel G1_7_0_0N --nbitsForDataStorage e32]>>
    # [WriterStd --output {destination_path} --ignoreExtended --noMetadata --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "test_34.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "d.compute_pressure_varicelle_rslt.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_34"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file) 
    assert(res == True)


def test_35(plugin_test_dir):
    """Test #35 : Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE thermodynamic"""
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]} ]>> 
    # [Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>
    # [Select --metadataFieldName P0,>>,^^ --exclude] >>
    # [WriterStd --output {destination_path} --ignoreExtended]']

    df = df.query('nomvar not in ["^^",">>","P0"]')
    #write the result
    results_file = TMP_PATH + "test_35.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_35_TT.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_35"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


def test_36(plugin_test_dir):
    """Test #36 : Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE"""
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"UU").compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]} ]>> 
    # [Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField UU] >> 
    # [Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>
    # [Select --metadataFieldName P0,>>,^^ --exclude] >>
    # [WriterStd --output {destination_path} --ignoreExtended]']
    df = df.query('nomvar not in ["^^",">>","P0"]')
    #write the result
    results_file = TMP_PATH + "test_36.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file,df).to_fst()
    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_36_UU.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_36"

    #compare results
    res = fstpy.fstcomp(results_file,file_to_compare)
    fstpy.delete_file(results_file)
    assert(res == True)


# # def test_37(plugin_test_dir):
# #     """Test #37 : Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE thermo sub grid - attendu fail"""
# #     # open and read source
# #     source0 = plugin_test_dir + "coord_5005_big.std"
# #     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #['[ReaderStd --ignoreExtended --input {sources[0]} ]>> ', '[Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField CK] >> ', '[Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

# #     #write the result
# #     results_file = TMP_PATH + "test_37.std"
# #     fstpy.StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstpy.fstcomp(results_file,file_to_compare)
# #     assert(res == True)

