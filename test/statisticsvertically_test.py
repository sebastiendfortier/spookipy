# -*- coding: utf-8 -*-
from test import TEST_PATH, TMP_PATH, check_test_ssm_package

check_test_ssm_package()

import pandas as pd
import fstpy
import pytest
import spookipy
from ci_fstcomp import fstcomp
import secrets
import rpnpy.librmn.all as rmn
import numpy as np
import glob

pytestmark = [pytest.mark.regressions]


# @pytest.fixture
# def plugin_test_dir():
#     return TEST_PATH + '/StatisticsVertically/testsFiles/'

@pytest.fixture
def plugin_test_dir():
    return TEST_PATH + '/WindMax/testsFiles/'



def test_1():
    """Check for a valid nomvar - invalid nomvar"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3])})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError):
        _ = spookipy.StatisticsVertically(df,nomvar='')

def test_2():
    """Check for a valid stat - invalid stat None"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3])})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError): 
        _ = spookipy.StatisticsVertically(df,stats=None)

def test_3():
    """Check for a valid stat - invalid stat TOTO"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3])})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError):
        _ = spookipy.StatisticsVertically(df,stats=['TOTO'])

def test_4():
    """Check for a valid percentiles - invalid percentiles None"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3])})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError):
        _ = spookipy.StatisticsVertically(df,stats='PERCENTILES', percentiles=None)

def test_5():
    """Check for a valid percentiles - invalid percentiles empty list"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3])})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError):
        _ = spookipy.StatisticsVertically(df,stats='PERCENTILES', percentiles=[])

def test_6():
    """Check for a valid percentiles - invalid percentiles list of str"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3])})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError):
        _ = spookipy.StatisticsVertically(df,stats='PERCENTILES', percentiles=['12'])

def test_7():
    """Check for a valid threshold - invalid threshold_operators None"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3])})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError):
        _ = spookipy.StatisticsVertically(df,stats='THRESHOLDS')

def test_8():
    """Check for a valid threshold - invalid threshold_operators invalid value"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3])})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError):
        _ = spookipy.StatisticsVertically(df,stats='THRESHOLDS', threshold_operators=[], threshold_values=[])

def test_9():
    """Check for a valid threshold - invalid threshold_operators invalid operator"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3])})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError):
        _ = spookipy.StatisticsVertically(df,stats='THRESHOLDS', threshold_operators=['TO'], threshold_values=[1])

def test_10():
    """Check for a valid threshold - invalid threshold_values invalid value"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3])})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError):
        _ = spookipy.StatisticsVertically(df,stats='THRESHOLDS', threshold_operators=['GE'], threshold_values=[])

def test_11():
    """Check for a valid threshold - invalid threshold_operators and threshold_values of different lenghts"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3])})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError):
        _ = spookipy.StatisticsVertically(df,stats='THRESHOLDS', threshold_operators=['GE','LE'], threshold_values=[1])

def test_12():
    """Check for a valid nomvar - invalid nomvar"""
    df = pd.DataFrame({'nomvar': np.array(['TT','UU','VV']),'ip1':np.array([1,2,3]),'ip2':np.array([1,2,3]),'ip3':np.array([1,2,3]), 'grid':'123', 'forecast_hour':12})
    # compute StatisticsVerticallyy
    with pytest.raises(spookipy.StatisticsVerticallyError):
        _ = spookipy.StatisticsVertically(df,nomvar = 'TO', stats='MEAN')

# def test_13(plugin_test_dir):
#     """Check for a valid nomvar - invalid nomvar"""
#     source0  = glob.glob('/fs/site4/eccc/oth/nlab_central/ron000/wxelements/archives/sample/2021090512_024_*')

#     src_df0 = fstpy.StandardFileReader(source0).to_pandas()
#     # compute StatisticsVerticallyy
#     # with pytest.raises(spookipy.StatisticsVerticallyError):
#     df = spookipy.StatisticsVertically(
#         src_df0, 
#         nomvar = 'PR', 
#         stats = ['MEAN','STD','PERCENTILES','INTERPERCENTILES','THRESHOLDS'],
#         percentiles = list(range(0,105,5)),
#         interpercentiles_lower = [10,25], 
#         interpercentiles_upper = [90,75], 
#         threshold_operators = ['LT','LT','EQ','GE','GE'],
#         threshold_values = [-10,-5,0,5,10],
#         ).compute()
#     # print(df[fstpy.BASE_COLUMNS].drop(columns='d').to_string())
#     assert(True)
