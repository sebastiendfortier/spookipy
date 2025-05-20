# -*- coding: utf-8 -*-
from test import check_test_ssm_package
from spookipy.utils import VDECODE_IP_INFO

check_test_ssm_package()

import pandas as pd
import numpy as np
import sys
import fstpy
import pytest
import spookipy
from spookipy.rmn_interface import RmnInterface
from datetime import datetime, timedelta

pytestmark = [pytest.mark.regressions, pytest.mark.regressions2]
pd.options.mode.chained_assignment = None
pd.set_option("display.max_rows", 3800, "display.max_columns", 3800)
np.set_printoptions(threshold=sys.maxsize)

# Remarque : il a certains fichier de comparaison de tests qui sont pas identique a ceux du Select en C++
# il s'agit des anciennes version de ces fichiers , cette remarque concerne en particulier les tests qui query sur la SURFACE


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site6/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "Select"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #1 : Surface selection with hybrid vertical coordinate."""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, coordinate_type="BLABLABLA", reduce_df=False).compute()
    # "[Select --coordinateType BLABLABLA]"


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #2 : Tester l'option --verticalLevelType avec une valeur invalide!"""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, vertical_level_type="BLABLABLA", reduce_df=False).compute()
    # "[Select --verticalLevelType BLABLABLA]"


def test_3(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #3 : Tester l'option --typeOfField avec une valeur invalide!"""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, type_of_field="BLABLABLA", reduce_df=False).compute()
    # "[Select --typeOfField BLABLABLA]"


def test_4(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #4 : Tester l'option --forecastHour avec une valeur invalide!"""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, forecast_hour=[timedelta(hours=-2)], reduce_df=False).compute()
    # "[Select --forecastHour -2]"    \


def test_5(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #5 : Tester l'option --userDefinedIndex avec une valeur invalide!"""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, user_defined_index=[-5], reduce_df=False).compute()
    # "[Select --userDefinedIndex -5]"


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #6 : Tester l'option --xAxisMatrixSize avec une valeur invalide!"""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, x_axis_matrix_size=[-5], reduce_df=False).compute()
    # "[Select --xAxisMatrixSize -5]"


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #7 : Tester l'option --yAxisMatrixSize avec une valeur invalide!"""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, y_axis_matrix_size=[-5], reduce_df=False).compute()
    # "[Select --yAxisMatrixSize -5]"


def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #8 : Tester l'option --verticalLevel avec une valeur invalide!"""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, vertical_level=[-100], reduce_df=False).compute()
    # "[Select --verticalLevel -5]"


def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #9 : Tester l'option --dateOfOrigin avec une valeur invalide!"""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, date_of_observation=[142], reduce_df=False).compute()
    # "[Select --dateOfOrigin 142]"


# Remarque: ce test n'est pas necessaire etant donne quon test le meme comportement au test_9 , plus pertinent comme test pour le parse_config
def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #10 : Tester l'option --dateOfOrigin avec une valeur invalide car trop longue!"""

    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, date_of_observation=[201311201120254], reduce_df=False).compute()
    # "[Select --dateOfOrigin 201311201120254]"


def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #11 : Surface selection with hybrid vertical coordinate."""

    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, vertical_level="SURFACE", reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel SURFACE] >> [WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_11.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_glbhyb_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #12 : Surface selection with eta vertical coordinate."""

    # open and read source
    source0 = plugin_test_path / "2011100712_012_regeta"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, vertical_level="SURFACE", reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel SURFACE] >> [WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    df = spookipy.convip(df, style=RmnInterface.CONVIP_ENCODE)
    results_file = test_tmp_path / "test_12.std"

    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "2011100712_012_regeta_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #15 : Surface selection multiple verticals coordinates."""

    # open and read source
    source0 = plugin_test_path / "multiple_vertical_types.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, vertical_level="SURFACE", reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel SURFACE] >> [WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_15.std"

    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "multiple_vertical_types_file2cmp.std+20210517"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #16 : Select vertical level types which follow topography with multiple vertical level types."""

    # open and read source
    source0 = plugin_test_path / "multiple_vertical_types.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, vertical_level_type="FOLLOWTOPOGRAPHY", reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevelType FOLLOWTOPOGRAPHY] >> [WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_16.std"

    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "multiple_vertical_types_topography_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #17 : Spooki must fail when no vertical level type following topography is found"""

    # open and read source
    source0 = plugin_test_path / "multiple_vertical_types.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, vertical_level_type="MILLIBARS", reduce_df=False).compute()

    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(
            df, vertical_level_type="FOLLOWTOPOGRAPHY", fail_msg="TOTAL_FAIL!", reduce_df=False
        ).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevelType MILLIBARS]
    # >> [Select --verticalLevelType FOLLOWTOPOGRAPHY --failMsg TOTAL_FAIL!]"


def test_18(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #18 : Select missing fieldName using --noFail (should verify)."""

    # open and read source
    source0 = plugin_test_path / "2011100712_012_glbhyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["AAAA"], vertical_level="SURFACE", nofail=True, reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName AAAA --verticalLevel SURFACE --noFail]"

    assert df == pd.DataFrame


def test_19(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #19 : Select Surface and field TT using looseMatch."""

    # open and read source
    source0 = plugin_test_path / "multiple_vertical_types.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["TT"], vertical_level="SURFACE", loose_match=True, reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --verticalLevel SURFACE --looseMatch] >> [WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_19.std"

    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "surface_TT_looseMatch_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_20(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #20 : select one field by its field name"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["TT"], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_20.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_20.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_21(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #21 : select two fields by their field names"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["TT"], label=["558V0"], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel R1558V0N ] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_21.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_21.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_22(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #22 : select one field by its field name AND vertical level"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["TT"], vertical_level=[1.0], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --verticalLevel 1.0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_22.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_22.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_23(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #23 : select one field by its field name AND vertical level AND etiket"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["TT"], vertical_level=[1.0], label=["928V4"], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --verticalLevel 1.0 --pdsLabel G0928V4N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_23.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_23.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_24(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #24 : select one field by its field name AND vertical level AND etiket AND forecast hour"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(
        src_df0,
        nomvar=["TT"],
        vertical_level=[1.0],
        label=["928V4"],
        forecast_hour=[timedelta(hours=141)],
        reduce_df=False,
    ).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --verticalLevel 1.0 --pdsLabel G0928V4N --forecastHour 141] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_24.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_24.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_25(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #25 : select two fields by their field names"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["UU", "VV"], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU,VV] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_25.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_25.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_26(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #26 : select two fields by their field names AND vertical level"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["UU", "VV"], vertical_level=[1.0], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU,VV --verticalLevel 1.0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_26.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_26.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_27(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #27 : select GZ fields"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["GZ"], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName GZ] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_27.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_27.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_28(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #28 : select all fields not named GZ or VV"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["GZ", "VV"], exclude=True, reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName GZ,VV --exclude] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_28.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "inverseSelect_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_29(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #29 : select all fields not named FF. Note: Their is no FF field in the input file. The result should be all fields"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["FF"], exclude=True, reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName FF --exclude] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_29.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "input_big_fileSrc.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_30(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #30 : select all field with coordinate type ETA"""

    # open and read source
    source0 = plugin_test_path / "UUVV12000_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, coordinate_type="ETA_1002", reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --coordinateType ETA_COORDINATE] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_30.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resultSelectEta_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_31(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #31 : select all field with coordinate type HYBRID"""

    # open and read source
    source0 = plugin_test_path / "UUVV93423264_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, coordinate_type="HYBRID_5001", reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --coordinateType HYBRID_COORDINATE] >> [WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_31.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resultSelectHyb_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_32(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #32 : select all field with coordinate type PRESSURE"""

    # open and read source
    source0 = plugin_test_path / "UUVV1000_pres_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, coordinate_type="PRESSURE_2001", reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --coordinateType PRESSURE_COORDINATE] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_32.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resultSelectPres_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_33(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #33 : select all fields with coordinate type HYBRID_STAGGERED"""

    # open and read source
    source0 = plugin_test_path / "hyb_sg_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, coordinate_type="HYBRID_5002", reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --coordinateType HYBRID_STAGGERED_COORDINATE] >> [WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_33.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resultSelectStg_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_34(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #34 : select two fields by their field names"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["TT", "UU"], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,UU] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_34.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_34.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_35(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #35 : select type of field FORECAST"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, type_of_field="P", reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --typeOfField FORECAST] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_35.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_35.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_36(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #36 : Select fields by their etiket"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, label=["558V0"], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --pdsLabel R1558V0N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_36.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_36.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_37(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #37 : Select fields that match two different etiket"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, label=["558V0", "928V4"], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --pdsLabel R1558V0N,G0928V4N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_37.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_37.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_38(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #38 : select fields that match one date of origin"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, date_of_observation=[datetime(2006, 3, 8, 0, 0, 0)], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --dateOfOrigin 20060308000000] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_38.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SelectDateOfOrigin_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_39(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #39 : select fields that match two dates of origin"""

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(
        src_df0, date_of_observation=[datetime(2006, 3, 8, 0, 0, 0), datetime(2006, 7, 18, 0, 0, 0)], reduce_df=False
    ).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --dateOfOrigin 20060308000000,20060718000000] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_39.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SelectDateOfOrigin_m_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_40(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #40 : select fields that match a range of date of origin"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(
        src_df0, date_of_observation=[(datetime(2006, 3, 8, 0, 0, 0), datetime(2006, 7, 18, 0, 0, 0))], reduce_df=False
    ).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --dateOfOrigin 20060308000000@20060718000000] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_40.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SelectDateOfOrigin_r_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_41(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #41 : select fields that are on a particular vertical level"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, vertical_level=[1.0], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 1.0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_41.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_41.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_42(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #42 : select fields that are on two different vertical levels"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, vertical_level=[1.0, 0.995], reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 1.0,0.995] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_42.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_42.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_43(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #43 : select fields that are in a range of vertical levels"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, vertical_level=[(1.0, 0.9850)], reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 1.0@0.9850] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_43.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_43.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_44(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #44 : select fields that are in a range of vertical levels AND one particular level outside the range"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, vertical_level=[(1.0, 0.9850), 0.995], reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevel 1.0@0.9850,0.995] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_44.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_44.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_45(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #45 : select fields that match a forecast hour"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, forecast_hour=[timedelta(hours=141)], reduce_df=False).compute()

    # "configuration": "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --forecastHour 141] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]",

    # write the result
    results_file = test_tmp_path / "test_45.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_45.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_46(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #46 : select fields that match a list of forecast hour"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(
        src_df0, forecast_hour=[timedelta(hours=141), timedelta(hours=144), timedelta(hours=24)], reduce_df=False
    ).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --forecastHour 141,144,24] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_46.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_46.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_47(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #47 : select fields that have a userDefinedIndex equal to 0"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, user_defined_index=[0], reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --userDefinedIndex 0] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_47.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "reference_file_test_47.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_48(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #48 : select fields with an X axis equal to 576"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, x_axis_matrix_size=[576], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --xAxisMatrixSize 576] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_48.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SelectxAxisMatrixSize_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_49(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #49 : select fields with Y axis equal to 200 or 641"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, y_axis_matrix_size=[200, 641], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --yAxisMatrixSize 200,641] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_49.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SelectyAxisMatrixSize_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_50(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #50 : --fieldname AND --metadataFieldName"

    # open and read source
    source0 = plugin_test_path / "UUVV93423264_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["UU"], metadata_nomvar=["HY"], reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU --metadataFieldName HY] >> [WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_50.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "result_select_metadata_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_51(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #51 : --fieldname and --noMetadata"

    # open and read source
    source0 = plugin_test_path / "UUVV93423264_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["UU"], no_metadata=True, reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU --noMetadata] >> [WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_51.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "NEW/result_fieldname_and_nometadata_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_52(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #52 : --noMetadata only"

    # open and read source
    source0 = plugin_test_path / "UUVV93423264_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, no_metadata=True, reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --noMetadata] >> [WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_52.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "NEW/result_only_nometadata_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_53(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #53 : select only metadata fields ^^ and >>"

    # open and read source
    source0 = plugin_test_path / "UUVV93423264_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, metadata_nomvar=["^^"], reduce_df=False).compute()
    df2 = spookipy.Select(src_df0, metadata_nomvar=[">>"], reduce_df=False).compute()
    df = fstpy.safe_concatenate([df, df2])

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --metadataFieldName ^^] + [Select --metadataFieldName >>]) >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_53.std"
    fstpy.StandardFileWriter(results_file, df, meta_only=True).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "result_select_metadataOnly_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_54(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #54 : select ^^ AND all fields except ^^. Note: output file should equal input file"

    # open and read source
    source0 = plugin_test_path / "UUVV93423264_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df_exclude = spookipy.Select(src_df0, metadata_nomvar=["^^"], exclude=True, reduce_df=False).compute()

    df_include = spookipy.Select(src_df0, metadata_nomvar=["^^"], reduce_df=False).compute()

    df = fstpy.safe_concatenate([df_exclude, df_include])

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> ([Select --metadataFieldName ^^ --exclude] + [Select --metadataFieldName ^^]) >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_54.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "result_select_metadataAndExclude_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_55(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #55 : select everything except P0"

    # open and read source
    source0 = plugin_test_path / "UUVV93423264_hyb_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, metadata_nomvar=["P0"], exclude=True, reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --metadataFieldName P0 --exclude] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_55.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "result_select_metadata_exclude_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_56(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #56 : this tests strict sql selection on fieldName, it should not validate"""

    # open and read source
    source0 = plugin_test_path / "UUVV12000_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, nomvar=["UU", "VV", "UV"], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU,VV,UV] >> [WriterStd --output {destination_path} --noUnitConversion --ignoreExtended]"


def test_57(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #57 : this tests strict sql selection on fieldName with exclude flag, it should validate"

    # open and read source
    source0 = plugin_test_path / "UUVV12000_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["UU"], exclude=True, reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UU --exclude] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_57.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resultSelectStrictExclude_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_58(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #58 : this tests strict sql selection on fieldName with exclude flag, it should validate, the excluded field is absent"

    # open and read source
    source0 = plugin_test_path / "UUVV12000_eta_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["UV"], exclude=True, reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName UV --exclude] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_58.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resultSelectStrictExclude2_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_59(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #59 : this tests strict sql selection with all attributes that have multiple value possibilities - should work"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(
        src_df0,
        nomvar=["TT", "UU", "VV", "GZ"],
        type_of_field="P",
        label=["558V0", "928V4"],
        date_of_observation=[datetime(2006, 3, 8, 0, 0, 0), datetime(2006, 7, 18, 0, 0, 0)],
        vertical_level=[0.8571, 1.0],
        forecast_hour=[timedelta(hours=144), timedelta(hours=24)],
        reduce_df=False,
    ).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT,UU,VV,GZ --typeOfField FORECAST --pdsLabel R1558V0N,G0928V4N
    # --dateOfOrigin 20060308000000,20060718000000 --verticalLevel 0.8571,1.0 --forecastHour 144,24] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_59.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SelectStrictAllAttribs_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_60(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #60 : this tests wildcard in pdsLabel selection"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, label=["*928*"], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --pdsLabel *928*] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_60.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SelectWildCards_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_61(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #61 : this tests wildcard in pdsLabel selection"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, nomvar=["TT"], label=["*8??"], reduce_df=False).compute()
    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --fieldName TT --pdsLabel *V?N] >> [WriterStd --output {destination_path} --ignoreExtended --IP1EncodingStyle OLDSTYLE]"

    # write the result
    results_file = test_tmp_path / "test_61.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SelectWildCards2_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_62(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #62 : select fields that have a level type equal to HYBRID_LEVEL"

    # open and read source
    source0 = plugin_test_path / "GZ_TT_millibars.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, vertical_level_type="HYBRID", reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --verticalLevelType HYBRID] >> [PrintIMO] >> [WriterStd --output {destination_path} --ignoreExtended]"

    # write the result
    results_file = test_tmp_path / "test_62.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "select_coordinate_hybrid_only_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_63(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #63 : select coordinate type PRESSURE with file containing two types of vertical coordinates associated to the same grid"

    # open and read source
    source0 = plugin_test_path / "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, coordinate_type="PRESSURE_2001", reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --coordinateType PRESSURE_COORDINATE] >> [WriterStd --output {destination_path} --ignoreExtended ]"

    # write the result
    results_file = test_tmp_path / "test_63.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "select_coordinate_pressure_file2cmp.std+20210517"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_64(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #64 : select coordinate type HYBRID_STAGGERED with file containing two types of vertical coordinates associated to the same grid"

    # open and read source
    source0 = plugin_test_path / "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, coordinate_type="HYBRID_5002", reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]}] >> [Select --coordinateType HYBRID_STAGGERED_COORDINATE] >> [WriterStd --output {destination_path} --ignoreExtended ]"

    # write the result
    results_file = test_tmp_path / "test_64.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "select_coordinate_hybrid_staggered_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_65(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #65 : select fields that match a decimal forecast hour in a file that has 30 min intervals"

    # open and read source
    source0 = plugin_test_path / "30_min_interval_minimal.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, forecast_hour=[pd.to_timedelta("23:30:00")], reduce_df=False).compute()

    # "Test #65 : select fields that match a decimal forecast hour in a file thats has 30 min intervals"

    # write the result
    results_file = test_tmp_path / "test_65.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_65.std+20210517"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_66(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #66 : minute validation fail"

    # open and read source
    source0 = plugin_test_path / "30_min_interval_minimal.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.SelectError):
        _ = spookipy.Select(src_df0, forecast_hour=[pd.to_timedelta("23:30:001")], reduce_df=False).compute()

    # "[ReaderStd --input {sources[0]}] >> "[Select --forecastHour 23:30:001] >>"[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]"


# Ce test devrait echouer mais n'echoue pas car timedelta est tres robuste , puis soustrait 1 minute aux heures.
""" def test_67(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #67 :  second validation fail"

    # open and read source
    source0 = plugin_test_path / "30_min_interval_minimal.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.SelectError): 
        _= spookipy.Select(
                    src_df0, 
                    forecast_hour=[pd.to_timedelta('23:00:-1')],
                    reduce_df=False).compute()
    
    #"[ReaderStd --input {sources[0]}] >> "[Select --forecastHour 23:00:-1] >>"[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]" """

# Ce test devrait echouer mais n'echoue pas car timedelta est tres robuste , puis soustrait 1 minute aux heures.
""" def test_68(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #68 :  minute validation fail"

    # open and read source
    source0 = plugin_test_path / "30_min_interval_minimal.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.SelectError): 
        _= spookipy.Select(
                    src_df0, 
                    forecast_hour=[pd.to_timedelta('23:-1:00')],
                    reduce_df=False).compute()
    
    #"[ReaderStd --input {sources[0]}] >> "
    #"[Select --forecastHour 23:-1:00] >>"
    #"[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]" """

# Ce test devrait echouer mais n'echoue pas car timedelta est tres robuste , puis rajoute le 60 minute au heures.
""" def test_69(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #69 : minute validation fail"

    # open and read source
    source0 = plugin_test_path / "30_min_interval_minimal.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.SelectError): 
        _= spookipy.Select(
                    src_df0, 
                    forecast_hour=[pd.to_timedelta('23:-1:00')],
                    reduce_df=False).compute()
    
    #"[ReaderStd --input {sources[0]}] >> "
    #"[Select --forecastHour 23:-1:00] >>"
    #"[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]" """

# Ce test devrait echouer mais n'echoue pas car timedelta est tres robuste , puis converti 72 secondes en 1 minute et 12 secondes.
""" def test_70(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #70 : second validation fail"

    # open and read source
    source0 = plugin_test_path / "30_min_interval_minimal.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.SelectError): 
        _= spookipy.Select(
                    src_df0, 
                    forecast_hour=[pd.to_timedelta('23:00:72')],
                    reduce_df=False).compute()
    
    #"[ReaderStd --input {sources[0]}] >> "
    #"[Select --forecastHour 23:00:72] >>"
    #"[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]" """

# Ce test ne devrait pas echouer mais il ne peut pas se faire tester dans ce type de test
""" def test_71(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #71 : 2 forecastHour parameters"

    # open and read source
    source0 = plugin_test_path / "30_min_interval_minimal.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with pytest.raises(spookipy.SelectError): 
        _= spookipy.Select(
                    src_df0, 
                    forecast_hour=[pd.to_timedelta('23:00:00')],
                    forecast_hour=[pd.to_timedelta('23:00:00')]. 
                    reduce_df=False).compute()
    
    #"[ReaderStd --input {sources[0]}] >> "
    #"[Select --forecastHour 23] >>"
    #"[Select --forecastHour 23:00:00] >>"
    #"[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]" """

# Ce test ne devrait pas echouer mais il ne peut pas se faire tester dans ce type de test
""" def test_72(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #72 : select fieldname with extra comma at the end"

    # Open and read source
    source0 = plugin_test_path / "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Compute Select
    df = spookipy.Select(
                    src_df0, 
                    nomvar=['UU,'],
                    reduce_df=False).compute()
    
    #"[ReaderStd --input {sources[0]}] >> "
    #"[Select --fieldName UU,] >>"
    #"[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]" 

    # Write the result
    results_file = test_tmp_path / "test_72.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_72.std"

    # Compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert (res) """

# Ce test ne devrait pas echouer mais il ne peut pas se faire tester dans ce type de test
""" def test_73(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #73 : select fieldname with extra comma at the beginning"

    # Open and read source
    source0 = plugin_test_path / "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Compute Select
    df = spookipy.Select(
                    src_df0, 
                    nomvar=[',UU'],
                    reduce_df=False).compute()
    
    #"[ReaderStd --input {sources[0]}] >> "
    #"[Select --fieldName ,UU] >>"
    #"[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE]" 

    # Write the result
    results_file = test_tmp_path / "test_73.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_73.std"

    # Compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert (res) """


# Ce test n'echoueras pas il va retourner une df vide car dans Select.py , nous separons sur les ',' et puis supprimons les strings vide
""" def test_74(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #74 : select fieldname only with comma"

    # Open and read source
    source0 = plugin_test_path / "glbpres_TT_UU_VV.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Compute Select
    df = spookipy.Select(
                    src_df0, 
                    nomvar=[','],
                    reduce_df=False).compute()
    #"[ReaderStd --input {sources[0]}] >> "
    #"[Select --fieldName ,] >>"
    #"[WriterStd --output {destination_path} --IP1EncodingStyle OLDSTYLE] 
"""


def test_75(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #75 : select coordinate type HYBRID_5005_COORDINATE"

    # Open and read source
    source0 = plugin_test_path / "coord_5005_TT_GZ_ES.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Compute Select
    df = spookipy.Select(src_df0, coordinate_type="HYBRID_5005", reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]} --group5005] >> [Select --coordinateType HYBRID_5005_COORDINATE] >> [WriterStd --output {destination_path} --ignoreExtended ]"

    # Write the result
    results_file = test_tmp_path / "test_75.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Open and read comparison file
    file_to_compare = plugin_test_path / "coord_5005_TT_GZ_ES.std"

    # Compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_76(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #76 : select surface level from hybrid 5005 file"

    # Open and read source
    source0 = plugin_test_path / "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Compute Select
    df = spookipy.Select(src_df0, vertical_level="SURFACE", reduce_df=False).compute()

    # "[ReaderStd --ignoreExtended --input {sources[0]} --group5005] >> "
    # "[Select --verticalLevel SURFACE] >> "
    # "[WriterStd --output {destination_path} --ignoreExtended ]"

    # Write the result
    results_file = test_tmp_path / "test_76.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Open and read comparison file
    file_to_compare = plugin_test_path / "resulttest_76.std"

    # Compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_77(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #77 : select fields that match two dates of validity"

    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(
        src_df0, date_of_validity=[datetime(2006, 7, 23, 21, 0, 0), datetime(2006, 7, 24, 0, 0, 0)]
    ).compute()
    # "[ReaderStd --input {sources[0]}] >> [Select --dateOfValidity 20060723210000,20060724000000] >> [WriterStd --output {destination_path}]"

    df = spookipy.convip(df, style=RmnInterface.CONVIP_ENCODE)

    # write the result
    results_file = test_tmp_path / "test_77.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "SelectDateOfValidity_m_file2cmp.std"

    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_78(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #78 : select ensemble members 007 and 012"

    # open and read source
    source0 = plugin_test_path / "ensemble_members.std+20250123"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, ensemble_member=["007", "012"]).compute()
    # "[ReaderStd --input {sources[0]}] >> [Select --ensembleMember 007,012] >> [WriterStd --output {destination_path}]"

    # write the result
    results_file = test_tmp_path / "test_78.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "select_ensembleMember_007_012_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_79(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #79 : select ensemble member 013"

    # open and read source
    source0 = plugin_test_path / "ensemble_members.std+20250123"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute Select
    df = spookipy.Select(src_df0, ensemble_member=["013"]).compute()
    # "[ReaderStd --input {sources[0]}] >> [Select --ensembleMember 013] >> [WriterStd --output {destination_path}]"

    # write the result

    results_file = test_tmp_path / "test_79.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "select_ensembleMember_013_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


# Ce test echoue car HYBRID_5100_COORDINATE n'a pas encore ete implementer
""" def test_80(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #80 : select HYBRID_5100_COORDINATE"

    # Open and read source
    source0 = plugin_test_path / "2020022912_024_slv"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Compute Select
    df = spookipy.Select(
                    src_df0, 
                    coordinate_type=['HYBRID_5100'],
                    field_name=['TT'],
                    reduce_df=False).compute()

    # Write the result
    results_file = test_tmp_path / "test_80.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Open and read comparison file
    file_to_compare = plugin_test_path / "select_hybrid_5100_coordinate.std"

    # Compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert (res)

"""

# Ce test echoue car HYBRID_5100_COORDINATE n'a pas encore ete implementer
""" def test_81(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #81 : select TT and P0LS metadata. Note: also needs !! because P0LS is only kept with Sleve levels"

    # Open and read source
    source0 = plugin_test_path / "2020022912_024_slv"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Compute Select
    df = spookipy.Select(
                    src_df0, 
                    nomvar=['TT'],
                    metadata_nomvar=['P0LS', '!!'],
                    reduce_df=False).compute()

    # Write the result
    results_file = test_tmp_path / "test_81.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Open and read comparison file
    file_to_compare = plugin_test_path / "select_P0LS_metadata_file2cmp.std"

    # Compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert (res)  """


# Ce test a ete ajouter afin de tester la robustesse de la selection de Surface
def test_82(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #82 : select SURFACE with 3 distinct nomvar and 2 different forecasthours"

    # Open and read source
    source0 = plugin_test_path / "Regeta_TTHUES_differentDateoSameDatev.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Compute Select
    df = spookipy.Select(src_df0, vertical_level="SURFACE", reduce_df=False).compute()

    # "[ReaderStd --input {sources[0]}] >> [Select --verticalLevel SURFACE] >> [WriterStd --output {destination_path}]"
    # Write the result
    results_file = test_tmp_path / "test_82.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Open and read comparison file
    file_to_compare = plugin_test_path / "Regeta_TTHUES_differentDateoSameDatev_file2cmp.std"

    # Compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_83(plugin_test_path, test_tmp_path, call_fstcomp):
    "Test #83 : select SURFACE with 2 different grids and 2 different forecasthours"

    # Open and read source
    source0 = plugin_test_path / "manyhours_manygrids.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # Compute Select
    df = spookipy.Select(src_df0, vertical_level="SURFACE", reduce_df=False).compute()

    # "[ReaderStd --input {sources[0]}] >> [Select --verticalLevel SURFACE] >> [WriterStd --output {destination_path}]"
    # Write the result
    results_file = test_tmp_path / "test_83.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # Open and read comparison file
    file_to_compare = plugin_test_path / "manyhours_manygrids_file2cmp.std"

    # Compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
