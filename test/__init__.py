# -*- coding: utf-8 -*-
import fstpy
import os
import logging

logger = fstpy.setup_fstpy_logger()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")
SPOOKI_TMPDIR = os.getenv("SPOOKI_TMPDIR")
TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/" % HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/" % (HOST_NUM, USER)

def check_test_ssm_package():
    SSM_TEST_SPOOKIPY = os.getenv("SSM_TEST_SPOOKIPY")
    if SSM_TEST_SPOOKIPY:
        dir_livraison = os.path.dirname(os.path.realpath(__file__))
        root_dir = os.path.dirname(dir_livraison)
        import sys
        sys.path = sys.path[1:]
