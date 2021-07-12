# -*- coding: utf-8 -*-
from spookipy.utils import select_with_meta
from test import TEST_PATH, TMP_PATH

import pytest
from fstpy.dataframe_utils import fstcomp
from fstpy.std_reader import StandardFileReader
from fstpy.std_writer import StandardFileWriter
from fstpy.utils import delete_file
import spookipy.all as spooki

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH +"Pressure/testsFiles/"


def write_result(results_file,df):
     delete_file(results_file)
     StandardFileWriter(results_file,df).to_fst()


def test_regtest_1(plugin_test_dir):
    """Test #1 : Test sur un fichier sortie de modele eta avec l'option --coordinateType ETA_COORDINATE. VCODE 1002"""
    # open and read source
    source0 = plugin_test_dir + "tt_eta_fileSrc.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = select_with_meta(src_df0,["TT"])
    # src_df0 = src_df0.query('nomvar in ["TT","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >>[spooki.Pressure --coordinateType ETA_COORDINATE --referenceField TT] >>[Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "test_pres_reg_1.std"
    write_result(results_file,df)
    
    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_eta_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_1"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


def test_regtest_2(plugin_test_dir):
    """Test #2 : Test sur un fichier sortie de modele eta avec les options --coordinateType ETA_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_eta_fileSrc.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = select_with_meta(src_df0,["TT"])
    # src_df0 = src_df0.query('nomvar in ["TT","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT",True).compute()
    df['etiket'] = 'PRESSR'
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [spooki.Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "test_pres_reg_2.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_eta_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_2"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


# # def test_regtest_3(plugin_test_dir):
# #     """Test #3 : Test sur un fichier sortie de modele eta avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_eta_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType AUTODETECT --referenceField TT] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_3.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_eta_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


# # def test_regtest_4(plugin_test_dir):
# #     """Test #4 : Test sur un fichier sortie de modele eta avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_eta_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [spooki.Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT ] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_4.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_eta_std_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


def test_regtest_5(plugin_test_dir):
    """Test #5 : Test sur un fichier sortie de modele Sigma, avec l'option --coordinateType SIGMA_COORDINATE. VCODE 1001"""
    # open and read source
    source0 = plugin_test_dir + "hu_sig_fileSrc.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = select_with_meta(src_df0,["HU"])
    # src_df0 = src_df0.query('nomvar in ["HU","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"HU").compute()
    df['etiket'] = 'R1580V0N'
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType SIGMA_COORDINATE --referenceField HU ] >>[Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "test_pres_reg_5.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_sig_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_5"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


def test_regtest_6(plugin_test_dir):
    """Test #6 : Test sur un fichier sortie de modele Sigma, avec les options --coordinateType SIGMA_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "hu_sig_fileSrc.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = select_with_meta(src_df0,["HU"])
    # src_df0 = src_df0.query('nomvar in ["HU","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"HU",True).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [spooki.Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField HU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    df['etiket'] = 'PRESSR'
    #write the result
    results_file = TMP_PATH + "test_pres_reg_6.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_sig_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_6"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


# # def test_regtest_7(plugin_test_dir):
# #     """Test #7 : Test sur un fichier sortie de modele Sigma, avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "hu_sig_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType AUTODETECT --referenceField HU] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_7.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_sig_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


# # def test_regtest_8(plugin_test_dir):
# #     """Test #8 : Test sur un fichier sortie de modele Sigma, avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "hu_sig_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField HU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_8.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_sig_std_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


def test_regtest_9(plugin_test_dir):
    """Test #9 : Test sur un fichier sortie de modele hybrid, avec l'option --coordinateType HYBRID_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = select_with_meta(src_df0,["TT"])
    # src_df0 = src_df0.query('nomvar in ["TT","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[spooki.Pressure --coordinateType HYBRID_COORDINATE --referenceField TT] >>', '[Zap --pdsLabel R1580V0N] >> ', '[WriterStd --output {destination_path} --ignoreExtended]']

    #write the result
    results_file = TMP_PATH + "test_pres_reg_9.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_9"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


def test_regtest_10(plugin_test_dir):
    """Test #10 : Test sur un fichier sortie de modele Hybrid avec les options --coordinateType HYBRID_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = select_with_meta(src_df0,["TT"])
    # src_df0 = src_df0.query('nomvar in ["TT","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT",True).compute()
    df['etiket'] = 'PRESSR'
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [spooki.Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = TMP_PATH + "test_pres_reg_10.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_10"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


# # def test_regtest_11(plugin_test_dir):
# #     """Test #11 : Test sur un fichier sortie de modele Hybrid, avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "input_hyb_2011100712_012.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType AUTODETECT --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_11.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb2_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


# # def test_regtest_12(plugin_test_dir):
# #     """Test #12 : Test sur un fichier sortie de modele Hybrid avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_hyb_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [spooki.Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_12.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb_std_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


def test_regtest_13(plugin_test_dir):
    """Test #13 : Test sur un fichier sortie de modele Hybrid staggered, avec l'option --coordinateType HYBRID_STAGGERED_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = select_with_meta(src_df0,["UU"])
    # src_df0 = src_df0.query('nomvar in ["UU","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"UU").compute()
    #[ReaderStd --input {sources[0]}] >> [spooki.Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --referenceField UU] >>[WriterStd --output {destination_path} --ignoreExtended]
    df['etiket'] = 'PRESSR'
    df.loc[df.nomvar.isin(['!!','>>','^^','P0']),'etiket'] = 'PRESS'
    print(df[['nomvar','etiket']])

    #write the result
    results_file = TMP_PATH + "test_pres_reg_13.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_stg_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_13"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


def test_regtest_14(plugin_test_dir):
    """Test #14 : Test sur un fichier sortie de modele Hybrid staggered, avec les options --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = select_with_meta(src_df0,["TT"])
    # src_df0 = src_df0.query('nomvar in ["UU","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"UU",True).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField UU] >> [WriterStd --output {destination_path} --ignoreExtended]
    df['etiket'] = 'PRESSR'
    #write the result
    results_file = TMP_PATH + "test_pres_reg_14.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_hyb_stg_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_14"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


# # def test_regtest_15(plugin_test_dir):
# #     """Test #15 : Test sur un fichier sortie de modele hybrid staggered, avec l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --input {sources[0]}] >> [spooki.Pressure --coordinateType AUTODETECT --referenceField UU] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_15.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb_stg_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


# # def test_regtest_16(plugin_test_dir):
# #     """Test #16 : Test sur un fichier sortie de modele Hybrid staggered, avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "px_hyb_stg_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField UU] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_16.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_hyb_stg_std_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


def test_regtest_17(plugin_test_dir):
    """Test #17 : Test sur un fichier sortie de modele en pression, avec l'option --coordinateType PRESSURE_COORDINATE."""
    # open and read source
    source0 = plugin_test_dir + "tt_pres_fileSrc.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = src_df0.query('nomvar in ["TT","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType PRESSURE_COORDINATE --referenceField TT] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "test_pres_reg_17.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_pres_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_17"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


def test_regtest_18(plugin_test_dir):
    """Test #18 : Test sur un fichier sortie de modele en pression avec les options --coordinateType PRESSURE_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_dir + "tt_pres_fileSrc.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = src_df0.query('nomvar in ["TT","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT",True).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [spooki.Pressure --coordinateType PRESSURE_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    df['etiket'] = 'PRESSR'
    #write the result
    results_file = TMP_PATH + "test_pres_reg_18.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "px_pres_std_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_18"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


# # def test_regtest_19(plugin_test_dir):
# #     """Test #19 : Test sur un fichier sortie de modele en pression l'option --coordinateType AUTODETECT."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [spooki.Pressure --coordinateType AUTODETECT --referenceField TT] >> [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_19.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_pres_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


# # def test_regtest_20(plugin_test_dir):
# #     """Test #20 : Test sur un fichier sortie de modele en pression avec les options --coordinateType AUTODETECT --standardAtmosphere."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >> [spooki.Pressure --coordinateType AUTODETECT --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_20.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "px_pres_std_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


# # def test_regtest_21(plugin_test_dir):
# #     """Test #21 : Test avec -- coordinateType ETA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees ETA - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_21.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res == False)


# # def test_regtest_22(plugin_test_dir):
# #     """Test #22 : Test avec l'option -- coordinateType ETA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees ETA - Champs PT et P0 sont absents."""
# #     # open and read source
# #     source0 = plugin_test_dir + "input_eta_2008061012_000_model_noPTnoP0.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_22.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res == False)


# # def test_regtest_23(plugin_test_dir):
# #     """Test #23 : Test avec -- coordinateType SIGMA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees SIGMA - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_23.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res == False)


# # def test_regtest_24(plugin_test_dir):
# #     """Test #24 : Test avec l'option -- coordinateType SIGMA_COORDINATE alors que le fichier d'entree n'est pas en coordonnees SIGMA - Champ P0 est absent."""
# #     # open and read source
# #     source0 = plugin_test_dir + "hu_sig_noP0_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField HU] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_24.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res == False)


# # def test_regtest_25(plugin_test_dir):
# #     """Test #25 : Test avec l'option -- coordinateType HYBRID_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_25.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res == False)


# # def test_regtest_26(plugin_test_dir):
# #     """Test #26 : Test avec l'option -- coordinateType HYBRID_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID - Champs P0 et HY sont absents."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_hyb_noP0noHYnoBB_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_26.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res == False)


# # def test_regtest_27(plugin_test_dir):
# #     """Test #27 : Test avec l'option -- coordinateType HYBRID_STAGGERED_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID STAGGERED - Kind invalide."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_pres_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_27.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res == False)


# # def test_regtest_28(plugin_test_dir):
# #     """Test #28 : Test avec l'option -- coordinateType HYBRID_STAGGERED_COORDINATE alors que le fichier d'entree n'est pas en coordonnees HYBRID STAGGERED- Champs P0 et HY sont absents."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_hyb_noP0noHYnoBB_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_28.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res == False)


# # def test_regtest_29(plugin_test_dir):
# #     """Test #29 : Test avec l'option -- coordinateType PRESSURE_COORDINATE alors que le fichier d'entree n'est pas en pression."""
# #     # open and read source
# #     source0 = plugin_test_dir + "tt_eta_fileSrc.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0,True).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType PRESSURE_COORDINATE --standardAtmosphere --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_29.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res == False)


def test_regtest_30(plugin_test_dir):
    """Test #30 : Test avec un fichier contenant differentes heures de prevision."""
    # open and read source
    source0 = plugin_test_dir + "input_vrpcp24_00_fileSrc.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = src_df0.query('nomvar in ["TT","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType AUTODETECT --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noMetadata]

    #write the result
    results_file = TMP_PATH + "test_pres_reg_30.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "input_vrpcp24_00_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_30"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


# # def test_regtest_31(plugin_test_dir):
# #     """Test #31 : Test avec un fichier contenant differentes heures de prevision."""
# #     # open and read source
# #     source0 = plugin_test_dir + "input_test_31.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #['[ReaderStd --ignoreExtended --input {sources[0]}] >> ', '[Select --exclude --fieldName PX] >> ', '[spooki.Pressure --coordinateType AUTODETECT --referenceField TT] >>', '[Zap --pdsLabel EH02558_X --metadataZappable --doNotFlagAsZapped]>>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended ]']

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_31.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "resulttest_31_TT.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


# # def test_regtest_32(plugin_test_dir):
# #     """Test #32 : Test avec un fichier glbpres avec l'option --coordinateType HYBRID_STAGGERED_COORDINATE"""
# #     # open and read source
# #     source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --referenceField TT] >>[WriterStd --output {destination_path} --ignoreExtended ]

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_32.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "glbpres_hybrid_staggered_coordinate_file2cmp.std"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     delete_file(results_file)
# #     assert(res == True)


def test_regtest_33(plugin_test_dir):
    """Test #33 : Test avec un fichier glbpres avec l'option --coordinateType PRESSURE_COORDINATE"""
    # open and read source
    source0 = plugin_test_dir + "glbpres_TT_UU_VV.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = src_df0.query('nomvar in ["TT","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType PRESSURE_COORDINATE --referenceField TT] >> [WriterStd --output {destination_path} --ignoreExtended ]
    df['etiket'] = 'PRESSR'
    #write the result
    results_file = TMP_PATH + "test_pres_reg_33.std"
    StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_pressure_coordinate_file2cmp.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_33"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


def test_regtest_34(plugin_test_dir):
    """Test #34 : Test avec un fichier qui genere des artefacts dans les cartes"""
    # open and read source
    source0 = plugin_test_dir + "2019091000_000_input.orig"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = src_df0.query('nomvar in ["TT","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [spooki.Pressure --coordinateType ETA_COORDINATE --referenceField TT] >> [Zap --pdsLabel G1_7_0_0N --nbitsForDataStorage e32]>>[WriterStd --output {destination_path} --ignoreExtended --noMetadata --IP1EncodingStyle OLDSTYLE]

    #write the result
    results_file = TMP_PATH + "test_pres_reg_34.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "d.compute_pressure_varicelle_rslt.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_34"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


def test_regtest_35(plugin_test_dir):
    """Test #35 : Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE thermodynamic"""
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = src_df0.query('nomvar in ["TT","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"TT").compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]} ]>> ', '[spooki.Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField TT] >>', '[Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

    #write the result
    results_file = TMP_PATH + "test_pres_reg_35.std"
    StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_35_TT.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_35"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


def test_regtest_36(plugin_test_dir):
    """Test #36 : Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE"""
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = StandardFileReader(source0).to_pandas()

    # src_df0 = src_df0.query('nomvar in ["UU","!!","P0","PT",">>","^^","^>","HY"]').reset_index(drop=True)

    #compute spooki.Pressure
    df = spooki.Pressure(src_df0,"UU").compute()
    #['[ReaderStd --ignoreExtended --input {sources[0]} ]>> ', '[spooki.Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField UU] >> ', '[Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

    #write the result
    results_file = TMP_PATH + "test_pres_reg_36.std"
    write_result(results_file,df)

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_36_UU.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/spooki.Pressure/result_test_36"

    #compare results
    res = fstcomp(results_file,file_to_compare)
    delete_file(results_file)
    assert(res == True)


# # def test_regtest_37(plugin_test_dir):
# #     """Test #37 : Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE thermo sub grid - attendu fail"""
# #     # open and read source
# #     source0 = plugin_test_dir + "coord_5005_big.std"
# #     src_df0 = StandardFileReader(source0).to_pandas()


# #     #compute spooki.Pressure
# #     df = spooki.Pressure(src_df0).compute()
# #     #['[ReaderStd --ignoreExtended --input {sources[0]} ]>> ', '[spooki.Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField CK] >> ', '[Zap --pdsLabel R1_V710_N --metadataZappable --doNotFlagAsZapped]  >>', '[Select --metadataFieldName P0,>>,^^ --exclude] >>', '[WriterStd --output {destination_path} --ignoreExtended]']

# #     #write the result
# #     results_file = TMP_PATH + "test_pres_reg_37.std"
# #     StandardFileWriter(results_file,df).to_fst()

# #     # open and read comparison file
# #     file_to_compare = plugin_test_dir + "nan"

# #     #compare results
# #     res = fstcomp(results_file,file_to_compare)
# #     assert(res == False)


