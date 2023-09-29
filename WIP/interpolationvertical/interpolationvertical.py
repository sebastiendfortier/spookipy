# -*- coding: utf-8 -*-
import fstpy
import numpy as np
import pandas as pd
from ..plugin import Plugin


class InterpolationVerticalError(Exception):
    pass

class InterpolationVertical(Plugin):

    def __init__(self, df: pd.DataFrame):
        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)


    def compute(self) -> pd.DataFrame:
        pass
