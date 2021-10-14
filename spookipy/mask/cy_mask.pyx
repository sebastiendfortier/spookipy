# -*- coding: utf-8 -*-
import cython

def validate(int c1, float v1, float t1):
    if (c1 == 0) and ( v1 < t1):
        return True
    elif (c1 == 1) and ( v1 <= t1):
        return True
    elif (c1 == 2) and ( (v1 >= t1 - 0.4 ) and (v1 <= t1 + 0.4) ):
        return True
    elif (c1 == 3) and ( v1 >= t1):
        return True
    elif (c1 == 4) and ( v1 > t1):
        return True
    else: # c1 == 5
        if ( v1 != t1):
            return True
    return False

def cy_mask(float v):
    cdef float vtmp = v
    v = 0.
    print(vtmp)
    print(v)
    