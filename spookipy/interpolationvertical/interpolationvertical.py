# -*- coding: utf-8 -*-
import fstpy.all as fstpy
import numpy as np
import pandas as pd
from ..plugin import Plugin


class InterpolationVerticalError(Exception):
    pass

class InterpolationVertical(Plugin):

    def __init__(self, df: pd.DataFrame):
        super().__init__(df)


    def compute(self) -> pd.DataFrame:
        pass