# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH

import fstpy.all as fstpy
import pandas as pd
import pytest
import spookipy.all as spooki
from ci_fstcomp import fstcomp

pytestmark = [pytest.mark.regressions]


@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/GridPointDifference/testsFiles/'


def test_1(plugin_test_dir):
    """--axis X,Y --differenceType CENTERED"""
    # open and read source
    source0 = plugin_test_dir + "6x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo'] = '20080529T133415'
    src_df0['nbits'] = 16
    src_df0['datyp'] = 1

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x','y'], difference_type='centered').compute()
    df.loc[df.nomvar=='FDX','nomvar'] = 'FFDX'
    df.loc[df.nomvar=='FDY','nomvar'] = 'FFDY'
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --unit scalar --doNotFlagAsZapped] >> 
    # ([Copy] + [GridPointDifference --axis X,Y --differenceType CENTERED]) >> 
    # [ZapSmart --fieldNameFrom FDX --fieldNameTo FFDX] >> [ZapSmart --fieldNameFrom FDY --fieldNameTo FFDY] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

    # write the result
    results_file = TMP_PATH + "test_1.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XYCentered_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_2(plugin_test_dir):
    """test_gridPointDifference_Z_centered"""
    # open and read source
    source0 = plugin_test_dir + "4z2x2y_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo'] = '20080529T133415'
    src_df0['nbits'] = 16
    src_df0['datyp'] = 1

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['z'], difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> 
    # [GridPointDifference --axis Z --differenceType CENTERED] >> [Zap --fieldName FFDZ --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    df.loc[df.nomvar=='FDZ','nomvar'] = 'FFDZ'
    # write the result
    results_file = TMP_PATH + "test_2.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "new_ZCentered_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_3(plugin_test_dir):
    """test_gridPointDifference_XY_forward"""
    # open and read source
    source0 = plugin_test_dir + "6x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo'] = '20080529T133415'
    src_df0['nbits'] = 16
    src_df0['datyp'] = 1

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='forward').compute()
    df.loc[df.nomvar=='FDX','nomvar'] = 'FFDX'
    df.loc[df.nomvar=='FDY','nomvar'] = 'FFDY'
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> 
    # [GridPointDifference --axis X,Y --differenceType FORWARD] >> 
    # [ZapSmart --fieldNameFrom FDX --fieldNameTo FFDX] >> [ZapSmart --fieldNameFrom FDY --fieldNameTo FFDY] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = TMP_PATH + "test_3.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XYForward_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_4(plugin_test_dir):
    """test_gridPointDifference_Z_forward"""
    # open and read source
    source0 = plugin_test_dir + "4z2x2y_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo'] = '20080529T133415'
    src_df0['nbits'] = 16
    src_df0['datyp'] = 1

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['z'], difference_type='forward').compute()
    df.loc[df.nomvar=='FDZ','nomvar'] = 'FFDZ'
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> 
    # [GridPointDifference --axis Z --differenceType FORWARD] >> [Zap --fieldName FFDZ --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = TMP_PATH + "test_4.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "new_ZForward_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_5(plugin_test_dir):
    """test_gridPointDifference_XY_backward"""
    # open and read source
    source0 = plugin_test_dir + "6x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo'] = '20080529T133415'
    src_df0['nbits'] = 16
    src_df0['datyp'] = 1

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x','y'], difference_type='backward').compute()
    df.loc[df.nomvar=='FDX','nomvar'] = 'FFDX'
    df.loc[df.nomvar=='FDY','nomvar'] = 'FFDY'    
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> 
    # [GridPointDifference --axis X,Y --differenceType BACKWARD] >> 
    # [ZapSmart --fieldNameFrom FDX --fieldNameTo FFDX] >> [ZapSmart --fieldNameFrom FDY --fieldNameTo FFDY] >> 
    # [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = TMP_PATH + "test_5.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XYBackward_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_6(plugin_test_dir):
    """test_gridPointDifference_Z_backward"""
    # open and read source
    source0 = plugin_test_dir + "4z2x2y_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0['dateo'] = '20080529T133415'
    src_df0['nbits'] = 16
    src_df0['datyp'] = 1

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['z'], difference_type='backward').compute()
    df.loc[df.nomvar=='FDZ','nomvar'] = 'FFDZ'    
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> 
    # [GridPointDifference --axis Z --differenceType BACKWARD] >> [Zap --fieldName FFDZ --doNotFlagAsZapped] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = TMP_PATH + "test_6.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "new_ZBackward_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_7(plugin_test_dir):
    """test_gridPointDifference_XY_centered2"""
    # open and read source
    source0 = plugin_test_dir + "tape10_UU.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x','y'], difference_type='centered').compute()
    df.loc[df.nomvar=='FDX','nomvar'] = 'UUDX'    
    df.loc[df.nomvar=='FDY','nomvar'] = 'UUDY'    
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # ([Copy] + [GridPointDifference --axis X,Y --differenceType CENTERED]) >> 
    # [ZapSmart --fieldNameFrom FDX --fieldNameTo UUDX] >> 
    # [ZapSmart --fieldNameFrom FDY --fieldNameTo UUDY] >> 
    # [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion --IP1EncodingStyle OLDSTYLE]
    res_df = pd.concat([src_df0, df], ignore_index=True)
    # write the result
    results_file = TMP_PATH + "test_7.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, res_df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XYCentered2_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_8(plugin_test_dir):
    """test_gridPointDifference_Z_1level"""
    # open and read source
    source0 = plugin_test_dir + "4z2x2y_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0, decode_metadata=True).to_pandas()

    src_df0 = src_df0.loc[src_df0.level == 0.]
    src_df0['dateo'] = '20080529T133415'
    src_df0['nbits'] = 16
    src_df0['datyp'] = 1

    # compute GridPointDifference
    with pytest.raises(spooki.GridPointDifferenceError):
        _ = spooki.GridPointDifference(src_df0, axis=['z'], difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --verticalLevel 0] >> 
    # [Zap --dateOfOrigin 20080529T133415 --nbitsForDataStorage R16 --doNotFlagAsZapped] >> 
    # [GridPointDifference --axis Z --differenceType CENTERED]


def test_9(plugin_test_dir):
    """test_gridPointDifference_Xsize1"""
    # open and read source
    source0 = plugin_test_dir + "tictac.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar=='BB']

    # compute GridPointDifference
    with pytest.raises(spooki.GridPointDifferenceError):
        _ = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName BB] >> 
    # [GridPointDifference --axis X --differenceType CENTERED]


def test_10(plugin_test_dir):
    """test_gridPointDifference_Ysize1"""
    # open and read source
    source0 = plugin_test_dir + "tictac.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0.nomvar=='AA']

    # compute GridPointDifference
    with pytest.raises(spooki.GridPointDifferenceError):
        _ = spooki.GridPointDifference(src_df0, axis=['y'], difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName AA] >> [GridPointDifference --axis Y --differenceType CENTERED]

def test_11(plugin_test_dir):
    """test_gridPointDifference_moreThan1PDS"""
    # open and read source
    source0 = plugin_test_dir + "tape10.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    with pytest.raises(spooki.GridPointDifferenceError):
        _ = spooki.GridPointDifference(src_df0).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridPointDifference --axis X,Y --differenceType CENTERED]


def test_12(plugin_test_dir):
    """Difference centree avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[(src_df0.nomvar=='TT') & (src_df0.level==1000.)]

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x','y'], difference_type='centered').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName TT --verticalLevel 1000] >> 
    # [GridPointDifference --axis X,Y --differenceType CENTERED] >> 
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = TMP_PATH + "test_12.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XYCentered_YY_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_13(plugin_test_dir):
    """Difference vers l'avant (forward) avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[(src_df0.nomvar=='TT') & (src_df0.level==1000.)]

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x','y'], difference_type='forward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName TT --verticalLevel 1000] >> 
    # [GridPointDifference --axis X,Y --differenceType FORWARD] >> 
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = TMP_PATH + "test_13.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XYForward_YY_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)

def test_14(plugin_test_dir):
    """Difference vers l'arriere  avec fichier YinYang en entree."""
    # open and read source
    source0 = plugin_test_dir + "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[(src_df0.nomvar=='TT') & (src_df0.level==1000.)]

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x','y'], difference_type='backward').compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> 
    # [Select --fieldName TT --verticalLevel 1000] >> 
    # [GridPointDifference --axis X,Y --differenceType BACKWARD] >> 
    # [WriterStd --output {destination_path} --noUnitConversion]

    # write the result
    results_file = TMP_PATH + "test_14.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "XYBackward_YY_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_15(plugin_test_dir):
    """Test #15 : Différence vers l'arriere avec un fichier global réduit (grille type Z)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[(src_df0.nomvar=='TT') & (src_df0.level==1000.)]

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='backward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[Select --fieldName TT --verticalLevel 1000] >> ",
#                 "[GridPointDifference --axis X --differenceType BACKWARD] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"


    # write the result
    results_file = TMP_PATH + "test_15.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test15_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_16(plugin_test_dir):
    """Test #16 : Différence vers l'avant avec un fichier global réduit (grille type Z)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[(src_df0.nomvar=='TT') & (src_df0.level==1000.)]

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='forward').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >>",
#                 "[Select --fieldName TT --verticalLevel 1000] >> ",
#                 "[GridPointDifference --axis X --differenceType FORWARD] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = TMP_PATH + "test_16.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test16_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_17(plugin_test_dir):
    """Test #17 : Différence centrée avec un fichier global réduit (grille type Z)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPresReduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[Select --fieldName TT --verticalLevel 1000] >> ",
#                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    src_df0 = src_df0.loc[(src_df0.nomvar=='TT') & (src_df0.level==1000.)]
    
    # write the result
    results_file = TMP_PATH + "test_17.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test17_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_18(plugin_test_dir):
    """Test #18 : Différence centrée avec un fichier global réduit (grille type A)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPres_gridA.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >>",
#                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = TMP_PATH + "test_18.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test18_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_19(plugin_test_dir):
    """Test #19 : Différence centrée avec un fichier global réduit (grille type B)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPres_gridB.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = TMP_PATH + "test_19.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test19_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_20(plugin_test_dir):
    """Test #20 : Différence centrée avec un fichier global réduit (grille type L avec longitude qui ne se repete pas)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPres_gridL1.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"


    # write the result
    results_file = TMP_PATH + "test_20.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test20_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_21(plugin_test_dir):
    """Test #21 : Différence centrée avec un fichier global réduit (grille type L avec 1ere longitude qui se repete a la fin)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPres_gridL2.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"


    # write the result
    results_file = TMP_PATH + "test_21.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test21_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_22(plugin_test_dir):
    """Test #22 : Différence centrée avec un fichier global réduit (grille type L avec longitude qui fait plus que le tour de la terre)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPres_gridL3.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ", 
#                 "[GridPointDifference --axis X --differenceType CENTERED] >> ", 
#                 "[WriterStd --output {destination_path} --noUnitConversion]"


    # write the result
    results_file = TMP_PATH + "test_22.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test22_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_23(plugin_test_dir):
    """Test #23 : Différence centrée avec un fichier global réduit (grille type L avec longitude qui ne fait pas le tour de la terre)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPres_gridL4.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDifference --axis X --differenceType CENTERED] >> ", 
#                 "[WriterStd --output {destination_path} --noUnitConversion]"


    # write the result
    results_file = TMP_PATH + "test_23.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test23_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_24(plugin_test_dir):
    """Test #24 : Différence centrée avec un fichier global réduit (grille type L avec longitude qui ne fait pas le tour de la terre)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPres_gridL5.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"


    # write the result
    results_file = TMP_PATH + "test_24.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test24_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


#             " INFORMATIONS SUPPLEMENTAIRES": "Le test suivant sert a tester la fonction IsGlobalGrid particulierement. Cas ou l'increment de la grille ne divise pas parfaitement le globe",
def test_25(plugin_test_dir):
    """Test #25 : Différence centrée avec un fichier global réduit (fait le tour de la terre, 1ere longitude ne se repete pas mais distance inegale entre le dernier point et le point 0; considéré comme une grille globale)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPres_gridL6.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"


    # write the result
    results_file = TMP_PATH + "test_25.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test25_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_26(plugin_test_dir):
    """Test #26 : Différence centrée avec un fichier global réduit (fait le tour de la terre, 1ere longitude se repete mais longitude differente entre le dernier point et le point 0; considéré comme une grille NON globale)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbPres_gridL7.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = TMP_PATH + "test_26.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbpres_test26_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)


def test_27(plugin_test_dir):
    """Test #27 : Différence centrée avec une grille de type G (grille globale par defaut sans repetition de longitude)."""
    # open and read source    
    source0 = plugin_test_dir + "GlbHyb_gridG_reduit.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridPointDifference
    df = spooki.GridPointDifference(src_df0, axis=['x'], difference_type='centered').compute()
#                 "[ReaderStd --ignoreExtended --input {sources[0]}] >> ",
#                 "[GridPointDifference --axis X --differenceType CENTERED] >> ",
#                 "[WriterStd --output {destination_path} --noUnitConversion]"

    # write the result
    results_file = TMP_PATH + "test_27.std"
    fstpy.delete_file(results_file)
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_dir + "glbhyb_test27_file2cmp.std"

    # compare results
    res = fstcomp(results_file, file_to_compare)
    fstpy.delete_file(results_file)
    assert(res)
