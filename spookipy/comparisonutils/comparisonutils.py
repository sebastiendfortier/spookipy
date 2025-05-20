# -*- coding: utf-8 -*-


class ComparisonUtilsError(Exception):
    pass


def _eq_(value, threshold, epsilon=0.00001):
    return abs(value - threshold) <= epsilon


def _ne_(value, threshold, epsilon=0.00001):
    return not _eq_(value, threshold, epsilon)


def _ge_(value, threshold, epsilon=0.00001):
    return (value > threshold) or _eq_(value, threshold, epsilon)


def _lt_(value, threshold, epsilon=0.00001):
    return not _ge_(value, threshold, epsilon)


def _le_(value, threshold, epsilon=0.00001):
    return value < threshold or _eq_(value, threshold, epsilon)


def _gt_(value, threshold, epsilon=0.00001):
    return not _le_(value, threshold, epsilon)
