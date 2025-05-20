# -*- coding: utf-8 -*-
import re, pytest
from types import ModuleType
from ci_fstcomp import fstcomp
import secrets
import os
import shutil
from pathlib import Path

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")
SPOOKI_TMPDIR = os.getenv("SPOOKI_TMPDIR")
TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff" % HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir" % (HOST_NUM, USER)

DEFAULT_COLUMNS = [
    "nomvar",
    "etiket",
    "typvar",
    "ni",
    "nj",
    "nk",
    "dateo",
    "datev",
    "ip1",
    "ip2",
    "ip3",
    "deet",
    "npas",
    "datyp",
    "nbits",
    "grtyp",
    "ig1",
    "ig2",
    "ig3",
    "ig4",
]


def pytest_itemcollected(item):
    node = item.obj
    doc = str(node.__doc__.strip()) if node.__doc__ else str("")
    doc = re.sub("[ÀÂÄ]", "A", doc)
    doc = re.sub("[Çç]", "c", doc)
    doc = re.sub("[ÈÉÊË]", "E", doc)
    doc = re.sub("[ÎÏ]", "I", doc)
    doc = re.sub("[ÔÖ]", "O", doc)
    doc = re.sub("[ÙÛÜ]", "U", doc)
    doc = re.sub("[àâä]", "a", doc)
    doc = re.sub("[ç]", "c", doc)
    doc = re.sub("[èéêë]", "e", doc)
    doc = re.sub("[îï]", "i", doc)
    doc = re.sub("[ôö]", "o", doc)
    doc = re.sub("[ùû]", "u", doc)
    item._nodeid = " : ".join([item._nodeid, doc])


@pytest.fixture
def call_fstcomp():
    def _call_fstcomp(
        results_file,
        file_to_compare,
        columns=DEFAULT_COLUMNS,
        exclude_meta=False,
        cmp_number_of_fields=True,
        verbose=False,
        e_max=0.0001,
        e_c_cor=0.00001,
    ):
        return fstcomp(
            str(results_file),
            str(file_to_compare),
            columns=columns,
            exclude_meta=exclude_meta,
            cmp_number_of_fields=cmp_number_of_fields,
            verbose=verbose,
            e_max=e_max,
            e_c_cor=e_c_cor,
        )

    return _call_fstcomp


# can be used directly for profiling
def get_plugin_test_path(plugin_name):
    return Path(f"{TEST_PATH}/{plugin_name}/testsFiles")


@pytest.fixture(scope="module")
def plugin_test_path(plugin_name):
    return get_plugin_test_path(plugin_name)


@pytest.fixture(scope="module")
def test_tmp_path(plugin_name):
    return Path(f"{TMP_PATH}/{plugin_name + secrets.token_hex(16)}")


@pytest.fixture(scope="module", autouse=True)
def setup_before_tests(test_tmp_path):
    print(f"\n\nSetup, mkdir: {test_tmp_path}\n")
    test_tmp_path.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="module", autouse=True)
def cleanup(test_tmp_path, request):
    def remove_test_dir():
        if not request.config.getoption("--no-cleanup"):
            print(f"\n\nCleanup, rmtree: {test_tmp_path}\n")
            shutil.rmtree(test_tmp_path)
        else:
            print(f"\n\nCleanup, path NOT removed: {test_tmp_path}\n")

    request.addfinalizer(remove_test_dir)


def pytest_addoption(parser):
    parser.addoption("--no-cleanup", action="store_true", help="Skip cleanup of temporary directory")


def run_profiling(test_module: ModuleType, plugin_name: str, nb_lines: int = 30) -> None:
    """
    Run profiling on specified test function from given module and print results.

    :param test_module: The module containing the tests to be profiled.
    :type test_module: types.ModuleType
    :param plugin_name: The name of the plugin under test. Used to retrieve specific paths for testing.
    :type plugin_name: str
    :param nb_lines: Number of lines from the profile stats to print out, defaults to 30.
    :type nb_lines: int, optional
    :rtype: None

    Profiling is done using cProfile, and the results are sorted by cumulative time.
    The test function to be profiled is specified as a command-line argument.
    The results of the profile is printed out to standard output.
    """
    import argparse
    import cProfile
    import pstats
    from pstats import SortKey

    parser = argparse.ArgumentParser()
    parser.add_argument("test", help="Name of the test function to run")
    args = parser.parse_args()

    # Retrieve the test function based on command-line argument
    test_func = test_module.__dict__.get(args.test)
    if not callable(test_func):
        print(f"Unknown or invalid test function '{args.test}'")
        exit(1)

    plugin_test_path = get_plugin_test_path(plugin_name)

    # Run the profile
    profiler = cProfile.Profile()
    profiler.enable()
    test_func(plugin_test_path, None, None)
    profiler.disable()

    # Create stats object and sort
    stats = pstats.Stats(profiler)
    stats.sort_stats(SortKey.CUMULATIVE)
    stats.print_stats(nb_lines)
