# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions1]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "GridCut"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester sur une zone de 3x4 depuis une extremite de la matrice."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridCut
    df = spookipy.GridCut(src_df0, start_point=(0, 0), end_point=(2, 3)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 0,0 --end_point 2,3] >> [WriterStd --output {destination_path} --ignoreExtended]

    df = spookipy.convip(df)
    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "gc_test_1.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester sur une zone de 3x4 depuis un point quelconque de la matrice"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridCut
    df = spookipy.GridCut(src_df0, start_point=(2, 1), end_point=(4, 4)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 2,1 --end_point 4,4] >> [WriterStd --output {destination_path} --ignoreExtended]

    df = spookipy.convip(df)
    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "gc_test_2.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test selection de toute la matrice"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridCut
    df = spookipy.GridCut(src_df0, start_point=(0, 0), end_point=(4, 4)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 0,0 --end_point 4,4] >>
    # [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]

    # write the result
    results_file = test_tmp_path / "test_3.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "UUVV5x5x2_fileSrc.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester sur une zone plus grande que la matrice d'origine"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridCut
    with pytest.raises(spookipy.GridCutError):
        _ = spookipy.GridCut(src_df0, start_point=(0, 0), end_point=(4, 5)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 0,0 --end_point 4,5]


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester sur une zone de 25x25 avec meta products et depuis un point quelconque de la matrice"""
    # open and read source
    source0 = plugin_test_path / "2014031800_024_reghyb_TT.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridCut
    df = spookipy.GridCut(src_df0, start_point=(4, 6), end_point=(28, 30)).compute()

    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 4,6 --end_point 28,30] >> [WriterStd --output {destination_path} --ignoreExtended]

    # write the result
    results_file = test_tmp_path / "test_5.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "gc_test_5.std+20240515"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester coupure en 2 avec !! 64 bits"""
    # open and read source
    source0 = plugin_test_path / "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    # print('src_df0',src_df0[['nomvar','ni','nj','grid','ip1','ip2','ig1','ig2']].to_string())
    # compute GridCut
    df = spookipy.GridCut(src_df0, start_point=(0, 0), end_point=(511, 399)).compute()
    # [ReaderStd --ignoreExtended --input {sources[0]}] >> [GridCut --start_point 0,0 --end_point 511,399] >> [WriterStd --output {destination_path} --ignoreExtended]
    # print('after gridcut',df[['nomvar','ni','nj','grid','ip1','ip2','ig1','ig2']].to_string())
    # temp fix for missing !!
    # toctoc = df.loc[(df.nomvar=="!!") & (df.ig1==5002)].reset_index(drop=True)
    # df = df.loc[df.nomvar!="!!"].reset_index(drop=True)

    # df = pd.safe_concat([toctoc,df])
    # write the result
    results_file = test_tmp_path / "test_6.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "gc_test_6.std+20240516"

    # compare results
    res = call_fstcomp(results_file, file_to_compare, exclude_meta=True)
    # res = fstcomp(results_file, file_to_compare,exclude_meta=True)
    assert res


@pytest.mark.skip(
    reason="Fait planter un test dans une autre suite de test... gridpointdifference_test.py::test_28 : 2 groupes de TT avec dates d'origine differentes mais dates de validity identiques FAILED"
)
def test_7(plugin_test_path):
    """Tester avec un type de grille qui n'est pas supporte (yinyang)"""
    # open and read source
    source0 = plugin_test_path / "2015072100_240_TTESUUVV_YinYang.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridCut
    with pytest.raises(spookipy.GridCutError):
        _ = spookipy.GridCut(src_df0, start_point=(0, 0), end_point=(4, 5)).compute()


def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Comme test 5 mais avec grid_tag (22,333,4444)"""
    # open and read source
    source0 = plugin_test_path / "2014031800_024_reghyb_TT.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridCut
    df = spookipy.GridCut(src_df0, start_point=(4, 6), end_point=(28, 30), grid_tag=(22, 333, 4444)).compute()

    # write the result
    results_file = test_tmp_path / "test_8.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "gc_test_8.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_9(plugin_test_path):
    """Tester mauvais parametre pour grid_tag, manque une valeur"""
    # open and read source
    source0 = plugin_test_path / "2014031800_024_reghyb_TT.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridCut
    with pytest.raises(spookipy.GridCutError):
        _ = spookipy.GridCut(src_df0, start_point=(0, 0), end_point=(4, 5), grid_tag=(22, 333)).compute()


def test_10(plugin_test_path):
    """Tester mauvais parametre pour grid_tag, une valeur n'est pas un entier"""
    # open and read source
    source0 = plugin_test_path / "2014031800_024_reghyb_TT.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridCut
    with pytest.raises(spookipy.GridCutError):
        _ = spookipy.GridCut(src_df0, start_point=(0, 0), end_point=(4, 5), grid_tag=("bad", 333, 4444)).compute()


def test_11(plugin_test_path):
    """Tester mauvais parametre pour grid_tag, une valeur n'est pas un entier positif"""
    # open and read source
    source0 = plugin_test_path / "2014031800_024_reghyb_TT.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute GridCut
    with pytest.raises(spookipy.GridCutError):
        _ = spookipy.GridCut(src_df0, start_point=(0, 0), end_point=(4, 5), grid_tag=(-22, 333, 4444)).compute()


# def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Interpolation Verticale 1/16 pieces 649x672 664Mo"""
#     # open and read source
#     source0 = plugin_test_path / "2011100712_012_regpres"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     source1 = plugin_test_path / "2011100712_012_reghyb"
#     src_df1 = fstpy.StandardFileReader(source1).to_pandas()

#     src_df = pd.safe_concat([src_df0,src_df1])

#     #compute GridCut
#     df = spookipy.GridCut(src_df,start_point=(0,0),end_point=(648,42)).compute()
#     #[ReaderStd --input {sources[0]}] + ([ReaderStd --input {sources[1]}] >>
#     # ([Select --fieldName GZ --verticalLevel SURFACE] + [Select --metadataFieldName P0] )) >>
#     # [Select --xAxisMatrixSize 649 --yAxisMatrixSize 672] >>
#     # (([GridCut --start_point 0,0 --end_point 648,42] >>
# [InterpolationVertical -m FIELD_DEFINED --outputField INCLUDE_ALL_FIELDS --extrapolationType FIXED --valueAbove -300 --valueBelow -300 --referenceFieldName TT]) +
# ([GridCut --start_point 0,43 --end_point 648,84] >>
# [InterpolationVertical -m FIELD_DEFINED --outputField INCLUDE_ALL_FIELDS --extrapolationType FIXED --valueAbove -300 --valueBelow -300 --referenceFieldName TT]) ) >>
# [WriterStd --output {destination_path} --ignoreExtended --noUnitConversion]

#     #write the result
#     results_file = test_tmp_path / "test_14.std"
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_path / "2011100712_012_regpres_ud850_file2cmp.std+20210517"

#     #compare results
#     res = fstcomp(results_file,file_to_compare)
#     assert(res)

# same as 1, no multithread in python
# def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
#     """Tester SingleThread. Comme le test 1 mais en singlethread"""
#     # open and read source
#     source0 = plugin_test_path / "UUVV5x5x2_fileSrc.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()


#     #compute GridCut
#     df = spookipy.GridCut(src_df0, start_point=(0,0), end_point=(2,3)).compute()
#     #[ReaderStd --ignoreExtended --input {sources[0]}] >>
#     # [GridCut -T 1 --start_point 0,0 --end_point 2,3] >>
#     #  [WriterStd --output {destination_path} --ignoreExtended]
#     df = spookipy.convip(df)
#     #write the result
#     results_file = test_tmp_path / "test_15.std"
#     fstpy.delete_file(results_file)
#     fstpy.StandardFileWriter(results_file, df).to_fst()

#     # open and read comparison file
#     file_to_compare = plugin_test_path / "gc_test_1.std"

#     #compare results
#     res = fstcomp(results_file,file_to_compare)
#     fstpy.delete_file(results_file)
#     assert(res)
