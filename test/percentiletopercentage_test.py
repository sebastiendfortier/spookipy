import pytest
from test import TMP_PATH, TEST_PATH

pytestmark = [pytest.mark.regressions]

@pytest.fixture
def plugin_test_dir():
# ExamplePlugin/testsFiles is a folder that should be created in ~spst900/ppp3TestFiles/ and ~spst900/ppp4TestFiles/
    return TEST_PATH +"PercentileToPercentage/testsFiles/"

def test_1(input_file):
    """Dummy test"""
    assert(True)