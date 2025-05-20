# -*- coding: utf-8 -*-
import fstpy
import os
import logging

logger = fstpy.setup_fstpy_logger()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def check_test_ssm_package():
    SSM_TEST_SPOOKIPY = os.getenv("SSM_TEST_SPOOKIPY")
    if SSM_TEST_SPOOKIPY:
        dir_livraison = os.path.dirname(os.path.realpath(__file__))
        root_dir = os.path.dirname(dir_livraison)
        import sys

        sys.path = sys.path[1:]
