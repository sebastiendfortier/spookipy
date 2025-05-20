# -*- coding: utf-8 -*-
from test import check_test_ssm_package

check_test_ssm_package()

import fstpy
import pandas as pd
import pytest
import spookipy
import os
import tempfile

pd.set_option("display.max_rows", 500, "display.max_columns", 500)

pytestmark = [pytest.mark.regressions, pytest.mark.regressions2]


@pytest.fixture(scope="module")
def plugin_name():
    """plugin_name in the path /fs/site5/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/{plugin_name}"""
    return "WriterStd"


def test_1(plugin_test_path):
    """Tester l'option --output avec un path qui n'existe pas!"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with tempfile.TemporaryDirectory() as tmpdirname:
        pass

    # tmpdirname shouldn't exist anymore
    assert not os.path.exists(tmpdirname)

    output = tmpdirname + "/toto.std"

    # compute WriterStd
    with pytest.raises(spookipy.WriterStdError):
        _ = spookipy.WriterStd(src_df0, output=output).compute()


def test_2(plugin_test_path):
    """Tester l'option --output avec un path qui existe mais qui est un nom de fichier!"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with tempfile.TemporaryDirectory() as tmpdirname:
        # temp dir is created

        file = tmpdirname + "/bidon"
        with open(file, "w") as f:
            pass

        output = file + "/toto.std"
        # compute WriterStd
        with pytest.raises(spookipy.WriterStdError):
            _ = spookipy.WriterStd(src_df0, output=output).compute()


def test_3(plugin_test_path):
    """Tester l'option --output avec un path existant qui est un répertoire mais dont on n'a pas les permissions!"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WriterStd
    with pytest.raises(Exception):  # TODO check if thats good enough (exception is in fstpy called in compute)
        _ = spookipy.WriterStd(src_df0, output="/media/toto.std").compute()


def test_4(plugin_test_path):
    """Tester l'option --writingMode avec une valeur invalide!"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    # compute WriterStd
    with pytest.raises(spookipy.WriterStdError):
        _ = spookipy.WriterStd(src_df0, output="/tmp/toto", writing_mode="TOTO").compute()


def test_5(plugin_test_path):
    """Tester l'option --writingMode avec la valeur NOPREVIOUS et un fichier de sortie existant. Il doit indiquer que le fichier d'output existe déjà!"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    with tempfile.TemporaryDirectory() as tmpdirname:
        # temp dir is created

        file = tmpdirname + "/toto.std"
        with open(file, "w") as f:
            pass

        # compute WriterStd
        with pytest.raises(spookipy.WriterStdError):
            _ = spookipy.WriterStd(src_df0, output=file, writing_mode="NOPREVIOUS").compute()


def test_6(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester l'option --writingMode avec la valeur NOPREVIOUS et un fichier de sortie inexistant. Aucun message d'erreur doit apparaître, donc tout devra fonctionner normalement!"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    results_file = test_tmp_path / "test_6.std"
    # compute WriterStd
    spookipy.WriterStd(
        src_df0, output=results_file, writing_mode="NOPREVIOUS", ip1_encoding_newstyle=False, ignore_extended=True
    ).compute()

    # compare results
    res = call_fstcomp(results_file, source0, e_max=0.01)
    assert res


def test_7(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester l'option --writingMode avec la valeur NEWFILEONLY et un fichier de sortie inexistant. Aucun message d'erreur doit apparaître, donc tout devra fonctionner normalement!"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    results_file = test_tmp_path / "test_7.std"
    # compute WriterStd
    spookipy.WriterStd(
        src_df0, output=results_file, writing_mode="NOPREVIOUS", ip1_encoding_newstyle=False, ignore_extended=True
    ).compute()

    # compare results
    res = call_fstcomp(results_file, source0, e_max=0.01)
    assert res


def test_8(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester l'option --writingMode avec la valeur NEWFILEONLY et un fichier de sortie existant. Un message d'avertissement doit apparaître et tout devra fonctionner normalement!"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    with tempfile.TemporaryDirectory() as tmpdirname:
        # temp dir is created

        file = tmpdirname + "/toto.std"
        with open(file, "w") as f:
            pass

        # compute WriterStd
        with pytest.warns():
            _ = spookipy.WriterStd(
                src_df0, output=file, writing_mode="NEWFILEONLY", ip1_encoding_newstyle=False, ignore_extended=True
            ).compute()

        # compare results
        res = call_fstcomp(file, source0, e_max=0.01)
        fstpy.delete_file(file)
        assert res


# Check len of label when making etiket
def test_9(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester la partie pdsLabel de l'etiket. Comme le pdsLabel SHORT a seulement 5 caractères un caractère _ sera ajouter pour que cette partie soit de longueur 6."""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.add_columns(src_df0)

    src_df0["label"] = "SHORT"

    results_file = test_tmp_path / "test_9.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
    ).compute()

    # open and read comparison file
    file_to_compare = plugin_test_path / "NEW/UUVV5x5_extended_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_10(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test que la partie implementation de l'etiket est bien écrit avec la bonne valeur OPERATIONAL = N, PARALLEL = P et EXPERIMENTAL = X"""
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.add_columns(src_df0)

    src_df0.loc[src_df0["nomvar"] == "UU", "implementation"] = "N"
    src_df0.loc[src_df0["nomvar"] == "VV", "implementation"] = "P"
    src_df0.loc[src_df0["nomvar"] == "TT", "implementation"] = "X"

    results_file = test_tmp_path / "test_10.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
        run_id="R1",
    ).compute()

    # open and read comparison file
    file_to_compare = plugin_test_path / "UUVVTT5x5_implementationRR_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_11(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test que la partie ensemble member de l'etiket est bien écrit avec la bonne valeur"""
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.add_columns(src_df0)

    src_df0["ensemble_member"] = "077"

    results_file = test_tmp_path / "test_11.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
        run_id="R1",
    ).compute()

    # open and read comparison file
    file_to_compare = plugin_test_path / "UUVVTT5x5_ensemble_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_12(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test que la partie run de l'etiket est bien écrit avec la bonne valeur"""
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0["etiket"] = src_df0.apply(lambda row: "__" + row["etiket"][2:], axis=1)
    src_df0 = fstpy.add_columns(src_df0)

    results_file = test_tmp_path / "test_12.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
        run_id="G3",
    ).compute()

    # open and read comparison file
    file_to_compare = plugin_test_path / "UUVVTT5x5_run_file2cmp.std"

    # compare results
    res = call_fstcomp(results_file, file_to_compare)
    assert res


def test_13(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test la lecture d'un fichier très simple, 1 grille et 2 champs"""
    # open and read source
    source0 = plugin_test_path / "UUVV5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    results_file = test_tmp_path / "test_13.std"
    spookipy.WriterStd(src_df0, output=results_file, ip1_encoding_newstyle=False, ignore_extended=True).compute()

    # compare results
    res = call_fstcomp(results_file, source0, e_max=0.01)
    assert res


def test_14(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test la lecture d'un fichier complexe, plusieurs grilles et plusieurs champs"""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    results_file = test_tmp_path / "test_14.std"
    spookipy.WriterStd(src_df0, output=results_file, ip1_encoding_newstyle=False, ignore_extended=True).compute()

    # compare results
    res = call_fstcomp(results_file, source0, e_max=0.01)
    assert res


def test_15(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test la lecture d'un fichier de modèle en pression"""
    # open and read source
    source0 = plugin_test_path / "input_model"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    src_df0 = src_df0.loc[src_df0["nomvar"].isin(["UU", "VV", "TT", ">>", "^^"])]

    results_file = test_tmp_path / "test_15.std"
    spookipy.WriterStd(src_df0, output=results_file, ip1_encoding_newstyle=False, ignore_extended=True).compute()

    # compare results
    file_to_compare = plugin_test_path / "sigma12000_pressure_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_16(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test la clé paramétrable --noMetadata. Le fichier résultant devrait contenir seulement les champs de données. Les tictic tactac ne seront pas écrit."""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    results_file = test_tmp_path / "test_16.std"
    spookipy.WriterStd(
        src_df0, output=results_file, ip1_encoding_newstyle=False, no_metadata=True, ignore_extended=True
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "input_big_noMeta_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_17(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test la clé paramétrable --metadataOnly. Le fichier résultant devrait contenir seulement les champs de metadata"""
    # open and read source
    source0 = plugin_test_path / "input_big_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    results_file = test_tmp_path / "test_17.std"
    spookipy.WriterStd(
        src_df0, output=results_file, ip1_encoding_newstyle=False, metadata_only=True, ignore_extended=True
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "input_big_metaOnly_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_18(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test la lecture d'un fichier qui contiendrait plusieurs grilles. Le fichier écrit contiendra une seule grille et les champs seront combinés."""
    # open and read source
    source0 = plugin_test_path / "fstdWithDuplicatedGrid_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    results_file = test_tmp_path / "test_18.std"
    spookipy.WriterStd(src_df0, output=results_file, ip1_encoding_newstyle=False, ignore_extended=True).compute()

    # compare results
    file_to_compare = plugin_test_path / "readDuplicatedGrid_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_19(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test la lecture et la réécriture d'un champ(!!) 64 bits"""
    # open and read source
    source0 = plugin_test_path / "tt_stg_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    results_file = test_tmp_path / "test_19.std"
    spookipy.WriterStd(src_df0, output=results_file, ip1_encoding_newstyle=False, ignore_extended=True).compute()

    # compare results
    file_to_compare = plugin_test_path / "tt_stg_fileSrc.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_20(plugin_test_path, test_tmp_path):
    """Tester avec un champ qui a un pdsName plus grand que 4! Un message d'erreur indiquant que le pds n'a pas pu être enregistré car la longueur du _pdsName est trop grande pour les fichiers standards."""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    results_file = test_tmp_path / "test_20.std"
    src_df0.loc[src_df0["nomvar"] == "UU", "nomvar"] = "UUUUU"

    with pytest.raises(Exception):
        spookipy.WriterStd(
            src_df0,
            output=results_file,
            ip1_encoding_newstyle=False,
        ).compute()


def test_21(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester avec un champ qui a un pdsName égale à 4! Aucun message d'erreur doit apparaître, donc tout devra fonctionner normalement!"""
    # open and read source
    source0 = plugin_test_path / "inputFile.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    src_df0.loc[src_df0["nomvar"] == "UU", "nomvar"] = "UUUU"

    results_file = test_tmp_path / "test_21.std"
    spookipy.WriterStd(src_df0, output=results_file, ip1_encoding_newstyle=False, ignore_extended=True).compute()

    # compare results
    file_to_compare = plugin_test_path / "fieldName4characters_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


# This test doesn't work in C++ anymore because of Zap, it doesn't really apply anymore.
# def test_22(plugin_test_path):
#     """Tester avec un forecast hour qui devra être arrondit à l'entier supérieur Forecast hour arrondit à l'entier supérieur et fichier écrit sans problème"""
#     # ??????? aller voir fichier de comparaison dans test .cpp forecastHourRoundedUp_file2cmp
#     # open and read source
#     source0 = plugin_test_path / "inputFile.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # src_df0.loc['forecasthour'] = 10.6 # check this


#     results_file = test_tmp_path / "test_22.std"
#     fstpy.delete_file(results_file)

#     spookipy.WriterStd(
#             src_df0,
#             output=results_file,
#             ip1_encoding_newstyle=True,
#             ignore_extended=True
#             ).compute()

#     # compare results
#     # if "file_to_compare": "" -> compare with the source file
#     file_to_compare = plugin_test_path / "resulttest_22.std"

#     print(source0)
#     src_df1 = fstpy.StandardFileReader(results_file).to_pandas()
#     src_df2 = fstpy.StandardFileReader(file_to_compare).to_pandas()
#     src_df0 = fstpy.add_columns(src_df0)#,'ip_info')
#     src_df1 = fstpy.add_columns(src_df1)#,'ip_info')
#     src_df2 = fstpy.add_columns(src_df2)#,'ip_info')
#     print("source0")
#     print(src_df0)
#     print("results_file")
#     print(src_df1)
#     print("file_to_compare")
#     print(src_df2)

#     res = fstcomp(results_file, file_to_compare, e_max=0.01)

#     fstpy.delete_file(results_file)
#     assert(res)

# This test doesn't work in C++ anymore because of Zap, it doesn't really apply anymore.
# def test_23(plugin_test_path):
#     """Tester avec un forecast hour qui devra être arrondit à l'entier inférieur Forecast hour arrondit à l'entier inférieur et fichier écrit sans problème"""
#     # ???????
#     # open and read source
#     source0 = plugin_test_path / "inputFile.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     # src_df0.loc['forecasthour'] = 10.4 # check this

#     results_file = test_tmp_path / "test_23.std"
#     fstpy.delete_file(results_file)

#     spookipy.WriterStd(
#             src_df0,
#             output=results_file,
#             ip1_encoding_newstyle=True,
#             ignore_extended=True
#             ).compute()

#     # compare results
#     # if "file_to_compare": "" -> compare with the source file
#     file_to_compare = plugin_test_path / "forecastHourRoundedDown_file2cmp.std"
#     res = fstcomp(results_file, file_to_compare, e_max=0.01)
#     fstpy.delete_file(results_file)
#     assert(res)


def test_24(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test un pds_label plus grand que 6 mais avec implementation = 'EXPERIMENTAL'. Doit passer mais l'étiquette sera tronqué à 6 caractères."""
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.add_columns(src_df0)

    src_df0["label"] = "ABCDEFG"
    src_df0["implementation"] = "X"
    src_df0["typvar"] = "PZ"  # a cause du zap dans le test original

    results_file = test_tmp_path / "test_24.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
        ip1_encoding_newstyle=False,
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "UUVVTT5x5_pdsLabel_egale_a_7_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_25(plugin_test_path, test_tmp_path):
    """Test un pds_label plus grand que 6 mais avec implementation = 'OPERATIONAL'. L'écriture ne doit pas fonctionnée."""
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.add_columns(src_df0)

    src_df0["label"] = "ABCDEFG"

    results_file = test_tmp_path / "test_25.std"
    with pytest.raises(Exception):
        spookipy.WriterStd(
            src_df0,
            output=results_file,
            ip1_encoding_newstyle=False,
            implementation="N",
        ).compute()


def test_26(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test un pds_label égale à 6 et implementation = 'OPERATIONAL'. Ce test doit fonctionné."""
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.add_columns(src_df0)

    src_df0["label"] = "ABCDEF"

    # the zap in the original test add a Z in typvar
    src_df0["typvar"] = "PZ"

    results_file = test_tmp_path / "test_26.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
        ip1_encoding_newstyle=False,
        implementation="N",
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "UUVVTT5x5_pdsLabel_egale_a_7_N_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_27(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test lecture ecriture d'une grille #Ce test doit fonctionner."""
    # open and read source
    source0 = plugin_test_path / "dm2011042100-00-00_000_dieses_no_toctoc"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    results_file = test_tmp_path / "test_27.std"
    src_df0 = fstpy.add_columns(src_df0)

    spookipy.WriterStd(
        src_df0,
        output=results_file,
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "dieses_file2cmp.std+20231227"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_28(plugin_test_path, test_tmp_path, call_fstcomp):
    """Tester l'option --writingMode avec la valeur APPEND et un fichier de sortie déjà existant. Aucun message d'erreur doit apparaître, le contenue de la mémoire est ajouté au fichier"""
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    results_file = test_tmp_path / "test_28.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
    ).compute()

    spookipy.WriterStd(src_df0, output=results_file, writing_mode="APPEND").compute()

    # compare results
    file_to_compare = plugin_test_path / "test_28_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_29(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test que la partie implementation de l'etiket est bien écrit avec la bonne valeur OPERATIONAL = N, PARALLEL = P et EXPERIMENTAL = X et que la run est R1."""
    # open and read source
    source0 = plugin_test_path / "UUVVTT5x5_fileSrc.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = fstpy.add_columns(src_df0)

    src_df0.loc[src_df0["nomvar"] == "UU", "implementation"] = "N"
    src_df0.loc[src_df0["nomvar"] == "VV", "implementation"] = "P"

    results_file = test_tmp_path / "test_29.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
        run_id="R1",
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "UUVVTT5x5_implementationRRa_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


# check for metadata_cleanup !! missing
def test_32(plugin_test_path, test_tmp_path, call_fstcomp):
    """Teste la lecture suivi de l'écriture avec un fichier qui contient des IP's encodés."""
    # open and read source
    source0 = plugin_test_path / "FichierStandardAvecDifferendKind_file2cmp.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0 = spookipy.applyIgnoreExtended(src_df0)

    results_file = test_tmp_path / "test_32.std"
    spookipy.WriterStd(src_df0, output=results_file, ignore_extended=True, encode_ip2_and_ip3=True).compute()

    # compare results
    file_to_compare = plugin_test_path / "result_test_32_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


# Already tested in 32, 41 and 42, nothing new
# # check for metadata_cleanup !! missing
# def test_33(plugin_test_path):
#     """Teste la lecture suivi de l'écriture avec un fichier qui contient des IP's encodés mais qui seront pas encodés."""
#     # open and read source
#     source0 = plugin_test_path / "FichierStandardAvecDifferendKind_file2cmp.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     results_file = test_tmp_path / "test_33.std"
#     fstpy.delete_file(results_file)

#     spookipy.WriterStd(
#             src_df0,
#             output=results_file,
#             ignore_extended=True
#             ).compute()


#     # compare results
#     # if "file_to_compare": "" -> compare with the source file
#     file_to_compare = '/home/for000/ss5/spooki/build/spooki_liv/result_test_33_file2cmp.std'#plugin_test_path / "FichierStandardAvecDifferendKind_file2cmp.std"
#     file_to_compare = '/home/for000/ss5/spooki/build/spooki_liv/result_test_32_file2cmp.std'#plugin_test_path / "FichierStandardAvecDifferendKind_file2cmp.std"


# src_df1 = fstpy.StandardFileReader(results_file).to_pandas()
# src_df2 = fstpy.StandardFileReader(file_to_compare).to_pandas()

# print("------------")
# print(src_df1)
# print("------------")
# print(src_df2)
# print("------------")


#     res = fstcomp(results_file, file_to_compare, e_max=0.01)
#     fstpy.delete_file(results_file)
#     assert(res)

# # No modification flag in input file, does nothing
# # check for metadata_cleanup !! missing
# def test_34(plugin_test_path):
#     """Teste l'écriture avec noModificationFlag"""
#     # open and read source
#     source0 = plugin_test_path / "FichierStandardAvecDifferendKind_file2cmp.std"
#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()

#     results_file = test_tmp_path / "test_34.std"
#     fstpy.delete_file(results_file)

#     # TODO --noModificationFlag???
#     spookipy.WriterStd(
#             src_df0,
#             output=results_file,
#             ignore_extended=True # TODO remove

#             ).compute()

#     # compare results
#     # if "file_to_compare": "" -> compare with the source file
#     file_to_compare = plugin_test_path / "FichierStandardAvecDifferendKind_file2cmp.std"
#     file_to_compare = '/home/for000/ss5/spooki/build/spooki_liv/result_test_32_file2cmp.std'#plugin_test_path / "FichierStandardAvecDifferendKind_file2cmp.std"

#     res = fstcomp(results_file, file_to_compare, e_max=0.01)
#     fstpy.delete_file(results_file)
#     assert(res)


def test_35(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #35 : Teste l'écriture niveaux5005: surface"""
    # open and read source
    source0 = plugin_test_path / "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "ip_info")
    src_df0["flag5005"] = True

    spookipy.modify_5005_record(src_df0)

    results_file = test_tmp_path / "test_35.std"
    meta_df = src_df0.loc[src_df0["nomvar"].isin(["P0", ">>", "^^", "!!"])]
    src_df0 = src_df0.loc[src_df0["nomvar"] == "TT"]
    src_df0 = src_df0.loc[src_df0["level"] == 1.0]
    src_df0 = pd.safe_concat([src_df0, meta_df])
    # print(src_df0)
    spookipy.WriterStd(
        src_df0,
        output=results_file,
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "5005_surfaceonly_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_36(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #36 : Teste l'écriture niveaux5005: no surface"""
    # open and read source
    source0 = plugin_test_path / "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "ip_info")
    src_df0["flag5005"] = True
    spookipy.modify_5005_record(src_df0)

    results_file = test_tmp_path / "test_36.std"
    meta_df = src_df0.loc[src_df0["nomvar"].isin(["P0", ">>", "^^", "!!"])]
    src_df0 = src_df0.loc[src_df0["nomvar"] == "TT"]
    src_df0 = pd.safe_concat(
        [
            src_df0.loc[src_df0["level"] == 0.851188],
            src_df0.loc[src_df0["level"] == 0.829785],
            meta_df,
        ]
    )
    src_df0 = pd.safe_concat([src_df0, meta_df])
    spookipy.WriterStd(
        src_df0,
        output=results_file,
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "5005_nosurface_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_37(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #37 : Teste l'écriture niveaux5005: surface + 0.851188 level"""
    source0 = plugin_test_path / "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "ip_info")
    src_df0["flag5005"] = True
    spookipy.modify_5005_record(src_df0)

    results_file = test_tmp_path / "test_37.std"
    meta_df = src_df0.loc[src_df0["nomvar"].isin(["P0", ">>", "^^", "!!"])]
    src_df0 = src_df0.loc[src_df0["nomvar"] == "TT"]
    src_df0 = pd.safe_concat(
        [
            src_df0.loc[src_df0["level"] == 0.851188],
            src_df0.loc[src_df0["level"] == 1.0],
            meta_df,
        ]
    )
    src_df0 = pd.safe_concat([src_df0, meta_df])
    spookipy.WriterStd(
        src_df0,
        output=results_file,
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "5005_surface+1level_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_38(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #38 : Teste l'écriture niveaux5005: surface + 0.851188 and 0.829785 levels"""
    source0 = plugin_test_path / "coord_5005_big.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "ip_info")
    src_df0["flag5005"] = True
    spookipy.modify_5005_record(src_df0)

    results_file = test_tmp_path / "test_36.std"
    meta_df = src_df0.loc[src_df0["nomvar"].isin(["P0", ">>", "^^", "!!"])]
    src_df0 = src_df0.loc[src_df0["nomvar"] == "TT"]
    src_df0 = pd.safe_concat(
        [
            src_df0.loc[src_df0["level"] == 1.0],
            src_df0.loc[src_df0["level"] == 0.851188],
            src_df0.loc[src_df0["level"] == 0.829785],
            meta_df,
        ]
    )
    # src_df0 = pd.safe_concat([src_df0,meta_df])
    spookipy.WriterStd(
        src_df0,
        output=results_file,
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "5005_surface+2level_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_39(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #39 : Teste lecture et écriture d'une etiket de forme RRLLLLLIMMMM"""
    # open and read source
    source0 = plugin_test_path / "2021082706_000_analrms"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0["nomvar"].isin(["TT", "^>", "!!", "P0"])]  # should be this one

    results_file = test_tmp_path / "test_39.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "etiketformat2-5-1-4_file2cmp.std"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_40(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #40 : Teste lecture et écriture d'une etiket de forme RRLLLLLIALL"""
    # open and read source
    source0 = plugin_test_path / "2020021306_006_trialmean"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()

    src_df0 = src_df0.loc[src_df0["nomvar"].isin(["ES", "^>", "P0", "!!"])]
    # src_df0 = src_df0.loc[src_df0['nomvar'].isin(['ES','^>','P0'])]
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    print(src_df0)

    results_file = test_tmp_path / "test_40.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "ensemble_all_file2cmp.std+20230208"
    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_41(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #41 : test lecture d'un interval de 30min et ecriture AVEC --encodeIP2andIP3"""
    # open and read source
    source0 = plugin_test_path / "interval30min.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0.loc[src_df0["nomvar"] == "PR", "implementation"] = "X"

    results_file = test_tmp_path / "test_41.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
        encode_ip2_and_ip3=True,
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "result_test_41_file2cmp.std"

    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_42(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #42 : test lecture d'un interval de 30min et ecriture SANS --encodeIP2andIP3. Donne ip3 => 0 puisque 30min est arrondi a 0"""
    # open and read source
    source0 = plugin_test_path / "interval30min.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0.loc[src_df0["nomvar"] == "PR", "implementation"] = "X"

    results_file = test_tmp_path / "test_42.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
        encode_ip2_and_ip3=False,
    ).compute()

    # compare results
    file_to_compare = plugin_test_path / "result_test_42_file2cmp.std"

    res = call_fstcomp(results_file, file_to_compare, e_max=0.01)
    assert res


def test_50(plugin_test_path, test_tmp_path, call_fstcomp):
    """Test #50 : test l'ecriture des !!, doit garder juste le bon !!"""
    # open and read source
    source0 = plugin_test_path / "test_etiketformat_file2cmp.std"
    source1 = plugin_test_path / "interval30min.std"
    src_df0 = fstpy.StandardFileReader(source0).to_pandas()
    src_df1 = fstpy.StandardFileReader(source1).to_pandas()
    src_df2 = fstpy.StandardFileReader(source1).to_pandas()
    src_df2["grid"] = 7069177446
    src_df0 = pd.safe_concat([src_df0, src_df1, src_df2])
    src_df0 = src_df0.loc[src_df0["nomvar"].isin(["!!", "TT", "P0", "^>"])]
    src_df0 = fstpy.add_columns(src_df0, "etiket")
    src_df0["label"] = src_df0["etiket"]

    results_file = test_tmp_path / "test_50.std"
    spookipy.WriterStd(
        src_df0,
        output=results_file,
        override_pds_label=True,
    ).compute()

    # compare results
    res = call_fstcomp(results_file, source0, e_max=0.01)
    assert res
