# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp
import secrets

pytestmark = [pytest.mark.skip]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + "InterpolationVertical/testsFiles/"


def test_1(plugin_test_dir):
    """Tester l'option --outputGridDefinitionMethod avec une valeur invalide _OK_"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical --outputGridDefinitionMethod DEFINED_SOMEHOW --interpolationType LINEAR --extrapolationType NEAREST ]


def test_2(plugin_test_dir):
    """Tester l'option --interpolationType avec une valeur invalide _OK_"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GRID --interpolationType INTERPOLATE_SOMEHOW --extrapolationType NEAREST ]

def test_3(plugin_test_dir):
    """Tester l'option --extrapolationType avec une valeur invalide _OK_"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GRID --interpolationType LINEAR --extrapolationType EXTRAPOLATE_SOMEHOW ]


def test_4(plugin_test_dir):
    """Tester l'option --outputGridDefinitionMethod FIELD_DEFINED sans l'option --referenceFieldName _OK_"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --interpolationType LINEAR --extrapolationType NEAREST ]


def test_5(plugin_test_dir):
    """Tester l'option --outputGridDefinitionMethod USER_DEFINED sans l'option --verticalLevel _OK_"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ]


def test_6(plugin_test_dir):
    """Tester l'option --verticalLevel avec des valeurs invalides _OK_"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 50,-20,100,A,200 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ]


def test_7(plugin_test_dir):
    """Tester l'option --verticalLevel avec un intervalle sans --verticalLevelRangeIncrement. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100@200,300 --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ]


def test_8(plugin_test_dir):
    """Tester l'option --outputGridDefinitionMethod USER_DEFINED sans l'option --verticalLevelType _OK_"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100,200,300 --interpolationType LINEAR --extrapolationType NEAREST ]


def test_9(plugin_test_dir):
    """Tester l'option --verticalLevelType avec une valeur invalide _OK_"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevelType SOME_VERTICALLEVELTYPE 
    # --verticalLevel 100,200,300 --interpolationType LINEAR --extrapolationType NEAREST ]


def test_10(plugin_test_dir):
    """Tester l'option --referenceFieldName avec un champ qui n'est pas dans le fichier d'input. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GRID --interpolationType LINEAR --extrapolationType NEAREST ]


def test_11(plugin_test_dir):
    """Tester l'option --referenceFieldName avec un champ sur plusieurs grilles. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "2014031800_024_reghyb_pres_TTGZUUVV.std"
    src_df1 = fstpy.StandardFileReader(source1)

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # ([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT]) ) >> [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName TT --interpolationType LINEAR --extrapolationType NEAREST ]

def test_12(plugin_test_dir):
    """ Interpolation vertical hybrid (reg) to millibars. _BETTER_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "2014031800_024_regpres_hy_shortTTGZUUVV.std"
    src_df1 = fstpy.StandardFileReader(source1)

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # ([ReaderStd --ignoreExtended --input {sources[0]}] + 
    # ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) ) >> 
    # [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID -m FIELD_DEFINED 
    # --outputField INTERPOLATED_FIELD_ONLY] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_12.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "2014031800_024_regpres_hy_shortTTGZUUVV_NEXT_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_13(plugin_test_dir):
    """ Interpolation vertical millibars (reg) to hybrid. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_regpres_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "2014031800_024_reghyb_pres_shortTTGZUUVV.std"
    src_df1 = fstpy.StandardFileReader(source1)

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # ([ReaderStd --ignoreExtended --input {sources[0]}] + 
    # ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) ) >> 
    # [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID 
    # -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_13.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "2014031800_024_reghyb_pres_shortTTGZUUVV_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_15(plugin_test_dir):
    """ Interpolation vertical hybrid staggered (glb) to millibars. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_glbhyb_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [InterpolationVertical --verticalLevel 950,700,350,100,20 --verticalLevelType MILLIBARS --interpolationType LINEAR 
    # --extrapolationType NEAREST -m USER_DEFINED] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_15.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "2014031800_024_glbpres_hystag_shortTTGZUUVV_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_16(plugin_test_dir):
    """ Interpolation vertical eta (glb) to hybrid staggered. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "2014031800_024_glbhyb_eta_shortTTGZUUVV.std"
    src_df1 = fstpy.StandardFileReader(source1)

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # ([ReaderStd --ignoreExtended --input {sources[0]}] + 
    # ([ReaderStd --ignoreExtended --input {sources[1]}] >> 
    # (([Select --fieldName TT] >> [Zap --fieldName GRID]) +([Select --fieldName UU] >> [Zap --fieldName GRDU]))) ) >> 
    # (([Select --fieldName TT,GZ,GRID] >> 
    # [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID 
    # -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY]) + ([Select --fieldName UU,VV,GRDU] >> 
    # [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRDU 
    # -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY])) >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_16.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "2014031800_024_glbhyb_eta_shortTTGZUUVV_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_18(plugin_test_dir):
    """ Interpolation vertical millibars (glb) to hybrid staggered. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_glbpres_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "2014031800_024_glbhyb_pres_shortTTGZUUVV.std"
    src_df1 = fstpy.StandardFileReader(source1)

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # (([ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --noMetadata]) + ([ReaderStd --ignoreExtended --input {sources[1]}] >> 
    # (([Select --fieldName TT] >> [Zap --fieldName GRID]) +([Select --fieldName UU] >> [Zap --fieldName GRDU]))) ) >> 
    # (([Select --fieldName TT,GZ,GRID] >> 
    # [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID 
    # -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY]) + ([Select --fieldName UU,VV,GRDU] >> 
    # [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRDU 
    # -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY])) >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_18.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "2014031800_024_glbhyb_pres_shortTTGZUUVV_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_20(plugin_test_dir):
    """ Interpolation vertical hybrid (reg) to eta. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
    src_df1 = fstpy.StandardFileReader(source1)

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # ([ReaderStd --ignoreExtended --input {sources[0]}] + 
    # ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) ) >> 
    # [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID 
    # -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_20.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "2014031800_024_regeta_hy_shortTTGZUUVV_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_22(plugin_test_dir):
    """ Interpolation vertical eta (reg) to millibars. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_regeta_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [InterpolationVertical --verticalLevel 950,700,350,100,20 --verticalLevelType MILLIBARS --interpolationType LINEAR 
    # --extrapolationType NEAREST -m USER_DEFINED ] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_22.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "2014031800_024_regpres_eta_shortTTGZUUVV_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_24(plugin_test_dir):
    """ Interpolation vertical millibars to meter sea level. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2011051818_000.UUVVTTGZ.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,GZ] >> 
    # [InterpolationVertical --verticalLevel 1000,2000,3000,4000,6000 --verticalLevelType METER_SEA_LEVEL 
    # --interpolationType LINEAR --extrapolationType NEAREST -m USER_DEFINED ] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_24.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "interpolationvertical_meter_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_25(plugin_test_dir):
    """ Interpolation vertical hybrid to meter sea level. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2011070818_054_hyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName GZ,TT] >> 
    # [InterpolationVertical --verticalLevel 1000,2000,3000,4000,6000 --verticalLevelType METER_SEA_LEVEL 
    # --interpolationType LINEAR --extrapolationType FIXED --valueAbove 999.0 --valueBelow 999.0 -m USER_DEFINED ] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_25.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "from_hybrid_to_meter_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_26(plugin_test_dir):
    """ Teste l'option --verticalLevelType MILLIBARS_ABOVE_LEVEL sans l'option --referenceLevel. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical -m USER_DEFINED --verticalLevel 100 --verticalLevelType MILLIBARS_ABOVE_LEVEL ]


def test_27(plugin_test_dir):
    """ Teste l'option --verticalLevelType MILLIBARS_ABOVE_LEVEL sans l'option --referenceLevel. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical -m USER_DEFINED --verticalLevel 100 --verticalLevelType MILLIBARS_ABOVE_LEVEL ]


def test_28(plugin_test_dir):
    """ Interpolation vertical eta (glb) to millibars above ground. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_glbeta_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # ([Pressure --referenceField TT --coordinateType AUTODETECT] + [Select --fieldName GZ,TT,UU,VV]) >> 
    # [InterpolationVertical -m USER_DEFINED --verticalLevel 100 --verticalLevelType MILLIBARS_ABOVE_LEVEL 
    # --referenceLevel SURFACE ] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_28.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "from_to_eta_millibars_above_ground.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_29(plugin_test_dir):
    """ Interpolation vertical with extrapolationType ABORT _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2011070818_054_hyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # ([Select --fieldName GZ,TT] + [Pressure --referenceField TT --coordinateType AUTODETECT]) >> 
    # [InterpolationVertical -T 1 --verticalLevel 900,500,300,200,100 --verticalLevelType METER_SEA_LEVEL 
    # --interpolationType LINEAR --extrapolationType ABORT --valueAbove 999.0 --valueBelow 999.0 -m USER_DEFINED ]


def test_30(plugin_test_dir):
    """ Interpolation vertical with interpolationType NEAREST _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_glbhyb_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [InterpolationVertical -m USER_DEFINED --verticalLevel 1000,3000,6000 --verticalLevelType METER_GROUND_LEVEL 
    # --interpolationType NEAREST --extrapolationType NEAREST] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_30.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "interpolationType_nearest_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_31(plugin_test_dir):
    """ Interpolation vertical with interpolationLevelType METER_GROUND_LEVEL _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_glbhyb_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [InterpolationVertical -m USER_DEFINED --verticalLevel 1000,3000,6000 --verticalLevelType METER_GROUND_LEVEL 
    # --interpolationType LINEAR --extrapolationType NEAREST] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_31.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "verticalLevelType_meterGroundLevel_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_32(plugin_test_dir):
    """Tester l'option --outputField avec une valeur invalide."""
    # open and read source
    source0 = plugin_test_dir + "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName GZ 
    # --outputField INCLUDE_SOMETHING --interpolationType LINEAR --extrapolationType NEAREST]


def test_33(plugin_test_dir):
    """ Interpolation vertical hybrid (reg) to eta --outputField INCLUDE_REFERENCE_FIELD. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
    src_df1 = fstpy.StandardFileReader(source1)

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # ([ReaderStd --ignoreExtended --input {sources[0]}] + ([ReaderStd --ignoreExtended --input {sources[1]}] >> 
    # [Select --fieldName TT] >> [Zap --fieldName GRID])) >> 
    # [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --outputField INCLUDE_REFERENCE_FIELD 
    # --referenceFieldName GRID -m FIELD_DEFINED ] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_33.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "includeReferenceField_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_34(plugin_test_dir):
    """Interpolation vertical hybrid (reg) to eta --outputField INCLUDE_ALL_FIELDS. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
    src_df1 = fstpy.StandardFileReader(source1)

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # ([ReaderStd --ignoreExtended --input {sources[0]}] + 
    # ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) + 
    # ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName GZ] >> [Zap --fieldName OUT])) >> 
    # [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --outputField INCLUDE_ALL_FIELDS 
    # --referenceFieldName GRID -m FIELD_DEFINED ] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_34.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "includeAllFields_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_35(plugin_test_dir):
    """Interpolation vertical hybrid (reg) to eta --outputField INTERPOLATED_FIELD_ONLY _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
    src_df1 = fstpy.StandardFileReader(source1)

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # ([ReaderStd --ignoreExtended --input {sources[0]}] + 
    # ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) + 
    # ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName GZ] >> [Zap --fieldName OUT])) >> 
    # [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --outputField INTERPOLATED_FIELD_ONLY 
    # --referenceFieldName GRID -m FIELD_DEFINED ] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_35.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "interpolatedFieldsOnly_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_36(plugin_test_dir):
    """Interpolation vertical hybrid (reg) to eta avec le parametre --outputField INTERPOLATED_FIELD_ONLY _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_reghyb_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    source1 = plugin_test_dir + "2014031800_024_regeta_hy_shortTTGZUUVV.std"
    src_df1 = fstpy.StandardFileReader(source1)

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # ([ReaderStd --ignoreExtended --input {sources[0]}] + 
    # ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName TT] >> [Zap --fieldName GRID]) + 
    # ([ReaderStd --ignoreExtended --input {sources[1]}] >> [Select --fieldName GZ] >> [Zap --fieldName OUT])) >> 
    # [InterpolationVertical --interpolationType LINEAR --extrapolationType NEAREST --referenceFieldName GRID 
    # -m FIELD_DEFINED --outputField INTERPOLATED_FIELD_ONLY] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_36.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "interpolatedFieldsOnly_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_37(plugin_test_dir):
    """Tester l'option --outputField INTERPOLATED_FIELD_ONLY avec pas de champs a interpole. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_reghyb_pres_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>[Select --fieldName TT,UU] >> 
    # [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName TT --interpolationType LINEAR 
    # --extrapolationType NEAREST --outputField INTERPOLATED_FIELD_ONLY]

def test_38(plugin_test_dir):
    """Tester l'option --outputField INCLUDE_REFERENCE_FIELD avec pas de champs a interpole. _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_reghyb_pres_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    with pytest.raises(spooki.InterpolationVerticalError):
        _ = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >>[Select --fieldName TT,UU] >> 
    # [InterpolationVertical --outputGridDefinitionMethod FIELD_DEFINED --referenceFieldName TT --interpolationType LINEAR 
    # --extrapolationType NEAREST --outputField INCLUDE_REFERENCE_FIELD]


def test_39(plugin_test_dir):
    """Interpolation vertical with a file containing many forecast hours (ens glb). _OK_"""
    # open and read source
    source0 = plugin_test_dir + "2015081700_024_ensglb_shortTTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 10.0,100.0,400.0,700.0,850.0,925.0,1000.0 
    # --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ] >>
    #  [Zap --nbitsForDataStorage E32] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_39.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + \
        "2015081700_024_ensglb_shortTTGZUUVV_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_40(plugin_test_dir):
    """Interpolation vertical avec un fichier hybrid pour les champs QC et TD. _SIMILIAR_"""
    # open and read source
    source0 = plugin_test_dir + "2011070818_054_hyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName QC,TD] >> 
    # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100,200,300,400,500,600,700,800,900,1000 
    # --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_40.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "2011070818_054_hyb_QCTT_NEXT_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_41(plugin_test_dir):
    """Interpolation vertical pour tester les parametres_--valueAbove et --valueBelow"""
    # open and read source
    source0 = plugin_test_dir + "2014031800_024_regeta_TTGZUUVV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> 
    # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 1,500,1100 
    # --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType FIXED --valueAbove 777.7 
    # --valueBelow -777.7] >> 
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_41.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "valueAboveBelow_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)

def test_41(plugin_test_dir):
    """Interpolation vertical avec un fichier hybrid 5005 pour les champs QC et TD. _SIMILIAR_"""
    # open and read source
    source0 = plugin_test_dir + "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute InterpolationVertical
    df = spooki.InterpolationVertical(src_df0).compute()
    #[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName QC,TD] >> 
    # [InterpolationVertical --outputGridDefinitionMethod USER_DEFINED --verticalLevel 100,200,300,400,500,600,700,800,900,1000 
    # --verticalLevelType MILLIBARS --interpolationType LINEAR --extrapolationType NEAREST ] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

    # write the result
    results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_41.std"])
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "resulttest_41.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    assert(res)
