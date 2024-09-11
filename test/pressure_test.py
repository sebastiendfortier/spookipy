# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy
import rpnpy.librmn.all as rmn

pytestmark = [pytest.mark.regressions]

@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "Pressure"

def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test sur un fichier sortie de modele eta avec l'option --coordinateType ETA_COORDINATE. VCODE 1002"""
    # open and read source
    source0 = plugin_test_path / "tt_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0, "TT").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType ETA_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel R1580V0N] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # Pour respecter le zap et l'encodage du test original
    df.loc[:, 'etiket'] = 'R1580V0N'
    df = spookipy.convip(df, style=rmn.CONVIP_ENCODE_OLD)

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "px_eta_file2cmp.std"
    # file_to_compare =  "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_1"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert(res)


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test sur un fichier sortie de modele eta avec les options --coordinateType ETA_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_path / "tt_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0, 
                                reference_field="TT", 
                                standard_atmosphere=True).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >>
    # [Pressure --coordinateType ETA_COORDINATE --standardAtmosphere --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Nouveau fichier sans --ignoreExtended --IP1EncodingStyle OLDSTYLE et sans Zap du pdsLabel du test en CPP
    file_to_compare = plugin_test_path / "px_eta_std_file2cmp.std+PY20240118"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

# # def test_3(plugin_test_path):
# # Test identique au test 1 puisque --coordinateType n'est plus une option dans la version python

# # def test_4(plugin_test_path):
# # Test identique au test 2 puisque --coordinateType n'est plus une option dans la version python

def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test sur un fichier sortie de modele Sigma, avec l'option --coordinateType SIGMA_COORDINATE. VCODE 1001"""
    # open and read source
    source0 = plugin_test_path / "hu_sig_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0, "HU").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType SIGMA_COORDINATE --referenceField HU ] >>
    # [Zap --pdsLabel R1580V0N] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Nouveau fichier de comparaison sans --ignoreExtended --IP1EncodingStyle OLDSTYLE et sans Zap du pdsLabel du test en CPP
    file_to_compare = plugin_test_path / "px_sig_file2cmp.std+PY20240118"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.1)
    assert(res)


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test sur un fichier sortie de modele Sigma, avec les options --coordinateType SIGMA_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_path / "hu_sig_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0, 
                                reference_field="HU", 
                                standard_atmosphere=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >>
    # [Pressure --coordinateType SIGMA_COORDINATE --standardAtmosphere --referenceField HU] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

     # Nouveau fichier de comparaison sans --ignoreExtended --IP1EncodingStyle OLDSTYLE et sans Zap du pdsLabel du test en CPP
    file_to_compare = plugin_test_path / "px_sig_std_file2cmp.std+PY20240118"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

# # def test_7(plugin_test_path):
# # Test identique au test 5 puisque --coordinateType n'est plus une option dans la version python

# # def test_8(plugin_test_path):
# # Test identique au test 5 puisque --coordinateType n'est plus une option dans la version python

def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test sur un fichier sortie de modele hybrid, avec l'option --coordinateType HYBRID_COORDINATE."""
    # open and read source
    source0 = plugin_test_path / "tt_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0, 
                                reference_field="TT").compute()
    # ['[ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType HYBRID_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel R1580V0N] >>
    # [WriterStd --output {destination_path} --ignoreExtended]']

    #  Pour respecter le Zap du test en CPP
    df.loc[:, 'etiket'] = 'R1580V0N'

    # write the result
    results_file = test_tmp_path / "test_9.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "px_hyb_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert(res)


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test sur un fichier sortie de modele Hybrid avec les options --coordinateType HYBRID_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_path / "tt_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0, 
                                reference_field = "TT",
                                standard_atmosphere = True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >>
    # [Pressure --coordinateType HYBRID_COORDINATE --standardAtmosphere --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_10.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Nouveau fichier de comparaison sans --ignoreExtended --IP1EncodingStyle OLDSTYLE et sans Zap du pdsLabel du test en CPP
    file_to_compare = plugin_test_path / "px_hyb_std_file2cmp.std+PY20240118"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test sur un fichier sortie de modele Hybrid."""
    # open and read source
    source0 = plugin_test_path / "input_hyb_2011100712_012.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Pressure --coordinateType AUTODETECT --referenceField TT] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    #write the result
    results_file = test_tmp_path / "test_11.std"
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # Nouveau fichier de comparaison sans --ignoreExtended du test en CPP
    file_to_compare = plugin_test_path / "px_hyb2_file2cmp.std+PY20240118"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


# # def test_12(plugin_test_path):
# # Test identique au test 10 puisque --coordinateType n'est plus une option dans la version python

def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test sur un fichier sortie de modele Hybrid staggered, avec l'option --coordinateType HYBRID_STAGGERED_COORDINATE."""
    # open and read source
    source0 = plugin_test_path / "px_hyb_stg_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "UU").compute()
    # [ReaderStd --input {sources[0]}] >>
    # [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --referenceField UU] >>
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_13.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "px_hyb_stg_file2cmp.std+PY20240118"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test sur un fichier sortie de modele Hybrid staggered, avec les options --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_path / "px_hyb_stg_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0, 
                                reference_field="UU", 
                                standard_atmosphere=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --standardAtmosphere --referenceField UU] >>
    # [WriterStd --output {destination_path}]

    # write the result
    results_file = test_tmp_path / "test_14.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "px_hyb_stg_std_file2cmp.std+20240118"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


# # def test_15(plugin_test_path):
# # Test identique au test 13 puisque --coordinateType n'est plus une option dans la version python

# # def test_16(plugin_test_path):
# # Test identique au test 14 puisque --coordinateType n'est plus une option dans la version python


def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test sur un fichier sortie de modele en pression, avec l'option --coordinateType PRESSURE_COORDINATE."""
    # open and read source
    source0 = plugin_test_path / "tt_pres_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType PRESSURE_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel R1580V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_17.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Nouveau fichier de comparaison 
    file_to_compare = plugin_test_path / "px_pres_file2cmp.std+20240408"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_18(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test sur un fichier sortie de modele en pression avec les options --coordinateType PRESSURE_COORDINATE --standardAtmosphere."""
    # open and read source
    source0 = plugin_test_path / "tt_pres_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0, 
                                reference_field="TT",
                                standard_atmosphere=True).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Zap --pdsLabel PRESSURE --doNotFlagAsZapped] >>
    # [Pressure --coordinateType PRESSURE_COORDINATE --standardAtmosphere --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]
    
    # write the result
    results_file = test_tmp_path / "test_18.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Nouveau fichier de comparaison 
    file_to_compare = plugin_test_path / "px_pres_std_file2cmp.std+20240408"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


# # def test_19(plugin_test_path):
# # Test identique au test 17 puisque --coordinateType n'est plus une option dans la version python

# # def test_20(plugin_test_path):
# # Test identique au test 18 puisque --coordinateType n'est plus une option dans la version python


########################################################################################################################
## Les tests 21 a 29 (version C++) ne sont plus necessaires.  Ces derniers servaient a valider
## le coordinateType demande avec l'information du fichier d'entree.
## Dans la version python, l'option coordinateType n'existe plus, on fait la detection du type de 
## fichier (AUTODETECT)
########################################################################################################################

def test_30(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier contenant differentes heures de prevision."""
    # open and read source
    source0 = plugin_test_path / "input_vrpcp24_00_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0, "TT").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType AUTODETECT --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE --noMetadata]

    # write the result
    results_file = test_tmp_path / "test_30.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # Nouveau fichier de comparaison sans --ignoreExtended --IP1EncodingStyle OLDSTYLE et sans Zap du pdsLabel du test en CPP
    file_to_compare = plugin_test_path / "input_vrpcp24_00_file2cmp.std+PY20240118"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_31(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier contenant differentes heures de prevision."""
    # open and read source
    source0 = plugin_test_path / "input_test_31.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = src_df0.loc[~src_df0.nomvar.isin(["PX"])].reset_index(drop=True)

    #compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0).compute()
    #  [ReaderStd --ignoreExtended --input {sources[0]}] >>  
    #  [Select --exclude --fieldName PX] >> 
    #  [Pressure --coordinateType AUTODETECT --referenceField TT] >> 
    #  [Zap --pdsLabel EH02558_X --metadataZappable --doNotFlagAsZapped]>>
    #  [Select --metadataFieldName P0,>>,^^ --exclude] >>
    #  [WriterStd --output {destination_path} --ignoreExtended ]

    df = df.loc[~df.nomvar.isin(["P0", ">>", "^^"])].reset_index(drop=True)
    df.loc[:, 'etiket'] = 'EH02558_X'

    #write the result
    results_file = test_tmp_path / "test_31.std"
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_31_TT.std"

    #compare results
    res = call_fstcomp(results_file,file_to_compare, e_max=0.01)
    assert(res)


def test_32(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier glbpres, avec TT en coordonnes HYBRID_STAGGERED_COORDINATE"""
    # open and read source
    source0 = plugin_test_path / "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # On veut seulement concerver le TT au niveau 1 hy
    tt_df = fstpy.select_with_meta(src_df0, ['TT'])
    tt_df = tt_df.loc[(tt_df.ip1 == 93423264) | (tt_df.nomvar != "TT")]

    #compute spookipy.Pressure
    df = spookipy.Pressure(tt_df, 'TT').compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Pressure --coordinateType HYBRID_STAGGERED_COORDINATE --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended ]

    #write the result
    results_file = test_tmp_path / "test_32.std"
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # Nouveau fichier de comparaison avec etikets differentes du test en CPP
    file_to_compare = plugin_test_path / "glbpres_hybrid_staggered_coordinate_file2cmp.std+PY20240118"

    #compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_33(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier glbpres, TT en coordonnes PRESSURE_COORDINATE"""
    # open and read source
    source0 = plugin_test_path / "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])
    tt_df   = tt_df.loc[tt_df.ip1 != 93423264]

    # compute spookipy.Pressure
    df      = spookipy.Pressure(tt_df, "TT").compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType PRESSURE_COORDINATE --referenceField TT] >>
    # [WriterStd --output {destination_path} --ignoreExtended ]

    # Pour respecter le test en CPP
    df.loc[df.nomvar == 'PX', 'etiket'] = 'PRESSR'

    # write the result
    results_file = test_tmp_path / "test_33.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_pressure_coordinate_file2cmp.std+20210517"
    
    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_34(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier qui genere des artefacts dans les cartes"""
    # open and read source
    source0 = plugin_test_path / "2019091000_000_input.orig"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df      = spookipy.Pressure(src_df0, "TT").compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>
    # [Pressure --coordinateType ETA_COORDINATE --referenceField TT] >>
    # [Zap --pdsLabel G1_7_0_0N --nbitsForDataStorage e32]>>
    # [WriterStd --output {destination_path} --ignoreExtended --noMetadata --IP1EncodingStyle OLDSTYLE]

    # Pour respecter le Zap et encoding OLDSTYLE du test en CPP
    df.loc[:, 'etiket'] = 'G1_7_0_0N'
    df = spookipy.convip(df, style=rmn.CONVIP_ENCODE_OLD)

    # write the result
    results_file = test_tmp_path / "test_34.std"
    fstpy.StandardFileWriter(results_file, df, no_meta=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "d.compute_pressure_varicelle_rslt.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_35(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE thermodynamic"""
    # open and read source
    source0 = plugin_test_path / "coord_5005_big.std"
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
    results_file = test_tmp_path / "test_35.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_35_TT.std"
    # file_to_compare = "/fs/site4/eccc/cmd/w/sbf000/testFiles/Pressure/result_test_35"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, exclude_meta=True, e_max=0.01)
    assert(res)


def test_36(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier 5005 avec l'option --coordinateType HYBRID_5005_COORDINATE"""
    # open and read source
    source0 = plugin_test_path / "coord_5005_big.std"
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
    results_file = test_tmp_path / "test_36.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()
    
    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_36_UU.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, exclude_meta=True, e_max=0.01)
    assert(res)


def test_37(plugin_test_path):
    """Test avec un fichier 5005 - P0 manquant donc ne peut fonctionner """
    # open and read source
    source0 = plugin_test_path / "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    #compute spookipy.Pressure
    # [ReaderStd --ignoreExtended --input {sources[0]} --group5005] >>
    # [Pressure --coordinateType HYBRID_5005_COORDINATE --referenceField CK] 

    # # compute MatchLevelIndexToValue
    with pytest.raises(Exception):
        _ = spookipy.Pressure(src_df0, "CK").compute()

# # def test_38(plugin_test_path):
# # Test qui ne semble plus pertinent car teste le groupement lors de la lecture
        
@pytest.mark.skip(reason="En attente pour traitement des fichiers 5100")
def test_39(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier 5100 - thermodynamic"""
    # open and read source
    source0 = plugin_test_path / "2020022912_024_slv"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT").compute()
    # ['[ReaderStd --input {sources[0]} --group5005 ]>>
    # [Pressure --coordinateType AUTODETECT --referenceField TT] >>
    # [WriterStd --output {destination_path}]']

    # write the result
    results_file = test_tmp_path / "test_39.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2020022912_024_slv_PX_thermo_file2cmp.std+20230815"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

#  Tests 39 et 40 sont nouveaux en python seulement
#  De nouveaux tests 39 a 43 ont été créés par la suite en CPP; il seront donc decales ici
#  
def test_39a(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier glbpres """
    # Nouveau test en python; amalgame des tests 32 et 33 pour calculer la pression sur les 2 types
    # de coordonnees (pressure et hybrid)

    # open and read source
    source0 = plugin_test_path / "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # On veut seulement concerver tous les TT (hy et mb)
    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])

    #compute spookipy.Pressure
    df      = spookipy.Pressure(tt_df, 'TT').compute()

    # Pour respecter les memes etiket que le test en CPP
    df.loc[df.nomvar == 'PX', 'etiket'] = 'PRESSR'

    #write the result
    results_file = test_tmp_path / "test_39a.std"
    fstpy.StandardFileWriter(results_file,df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "glbpres_2types_of_coordinate_file2cmp.std+20240408"

    #compare results
    res = call_fstcomp(results_file,file_to_compare)
    assert(res)

@pytest.mark.skip(reason="En attente pour traitement des fichiers 5100")
def test_40(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier 5100 - momentum"""
    # open and read source
    source0 = plugin_test_path / "2020022912_024_slv"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT").compute()
    # ['[ReaderStd --input {sources[0]} --group5005 ]>>
    # [Pressure --coordinateType AUTODETECT --referenceField UU] >>
    # [WriterStd --output {destination_path} ]']

    # write the result
    results_file = test_tmp_path / "test_40.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2020022912_024_slv_PX_momentum_file2cmp.std+20230815"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)


def test_40a(plugin_test_path, test_tmp_path, call_fstcomp):
    """2 groupes de TT avec dates d'origine differentes mais dates de validity identiques """

    source  = plugin_test_path / "Regeta_TTHUES_differentDateoSameDatev.std"
    src_df  = fstpy.StandardFileReader(source).to_pandas()
    tt_df   = fstpy.select_with_meta(src_df, ['TT'])


    # compute spookipy.DewPointDepression
    df      = spookipy.Pressure(tt_df, 'TT').compute()
    # spooki_run.py  "[ReaderStd --input Regeta_TTHUES_differentDateoSameDatev.std] >> 
    # [Pressure --referenceField TT --plugin_language CPP  --coordinateType ETA_COORDINATE ] >> 
    # [WriterStd --output Test40.std ]"

    # Pour respecter les memes etiket que le test cree en CPP
    df.loc[df.nomvar == 'PX', 'etiket'] = '__PRESSRX000'

     # write the result
    results_file = test_tmp_path / "test_40a.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # # open and read comparison file
    file_to_compare = plugin_test_path / "Regeta_differentDateoSameDatev_file2cmp.std"
    # compare results 
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

def test_41(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test que le ptop est pris dans les donnees du champ HY et non dans son ip1"""
    # open and read source
    source0 = plugin_test_path / "2016031912_012_with_hy"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute spookipy.Pressure
    df = spookipy.Pressure(src_df0, "TT").compute()
    # ['[ReaderStd --input {sources[0]}  ]>>
    # [Pressure --coordinateType AUTODETECT --referenceField TT] >>
    # [WriterStd --output {destination_path}]']

    # write the result
    results_file = test_tmp_path / "test_40.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "test41_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, e_max=0.02)
    assert(res) 

@pytest.mark.skip(reason="En attente pour traitement des fichiers 5100")
def test_42(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier 5100 - thermodynamic"""
    # open and read source
    source0 = plugin_test_path / "2020010100_048.slv"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])

    # compute spookipy.Pressure
    df = spookipy.Pressure(tt_df, "TT").compute()
    # ['[ReaderStd --input {sources[0]} --group5005 ]>>
    # [Select --fieldName TT]>>
    # [Pressure --coordinateType AUTODETECT --referenceField TT] >>
    # [WriterStd --output {destination_path}]']

    # write the result
    results_file = test_tmp_path / "test_42.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2020010100_048_slv_PX_thermo_file2cmp.std+20230815"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)

@pytest.mark.skip(reason="En attente pour traitement des fichiers 5100")
def test_43(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test avec un fichier 5100 - thermodynamic"""
    # open and read source
    source0 = plugin_test_path / "2020010100_048.slv"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    tt_df   = fstpy.select_with_meta(src_df0, ['TT'])

    # compute spookipy.Pressure
    df = spookipy.Pressure(tt_df, "UU").compute()
    # ['[ReaderStd --input {sources[0]} --group5005 ]>>
    # [Select --fieldName UU]>>
    # [Pressure --coordinateType AUTODETECT --referenceField UU] >>
    # [WriterStd --output {destination_path}]']

    # write the result
    results_file = test_tmp_path / "test_43.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2020010100_048_slv_PX_momentum_file2cmp.std+20230815"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert(res)
