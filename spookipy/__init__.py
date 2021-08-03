# -*- coding: utf-8 -*-
import pandas as pd

def __add__(self, other):
    return pd.concat([self,other],ignore_index=True)

