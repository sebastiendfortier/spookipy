# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pytest
import spookipy

pytestmark = [pytest.mark.regressions, pytest.mark.regressions2, pytest.mark.humidity]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "TemperaturePotential"


def test_1(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la température potentielle à partir d'un fichier standard."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_reghyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute TemperaturePotential
    df = spookipy.TemperaturePotential(src_df0).compute()
    # [ReaderStd --input {sources[0]}] >> [TemperaturePotential] >> [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_1.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "TemperaturePotential_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_2(plugin_test_path, test_tmp_path, call_fstcomp):
    """Calcul de la température potentielle à partir d'un fichier standard."""
    # open and read source
    source0 = plugin_test_path / "2011100712_012_reghyb"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    tt_df = fstpy.select_with_meta(src_df0, ["TT"])

    ttk_df = fstpy.unit_convert(tt_df, to_unit_name="kelvin")

    # compute TemperaturePotential
    df = spookipy.TemperaturePotential(ttk_df).compute()
    # [ReaderStd --input {sources[0]}] >> [Select --fieldName TT] >>
    # [UnitConvert --unit kelvin] >> [TemperaturePotential] >>
    # [WriterStd --output {destination_path} ]

    # write the result
    results_file = test_tmp_path / "test_2.std"
    fstpy.StandardFileWriter(results_file, df).to_fst()

    # open and read comparison file
    file_to_compare = plugin_test_path / "TemperaturePotential_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res
