import ctypes
import os

import numpy as np
import numpy.ctypeslib as ctl

path_lib = os.path.dirname(os.path.abspath(__file__)) + '/libwindmodulus.so'
lib = ctypes.cdll.LoadLibrary(path_lib)
lib.wind_modulus_cpp.argtypes = [
                                   ctl.ndpointer(np.float32, 
                                          flags='aligned, c_contiguous'),
                                   ctl.ndpointer(np.float32, 
                                          flags='aligned, c_contiguous'),
                                   ctypes.c_int
]

def wind_modulus_cpp(a:np.array, b:np.array):
       shape = a.shape
       size = a.size
       lib.wind_modulus_cpp.restype = ctl.ndpointer(np.float32, 
                                          flags='aligned, c_contiguous',
                                          shape=shape)

       flag_fortran = a.flags['F_CONTIGUOUS']
       dtype = a.dtype

       # make sure a has the right format for the cpp function
       if not a.flags['C_CONTIGUOUS']:
              a = np.ascontiguousarray(a,dtype='float32')
       elif a.dtype != "float32":
              a = a.astype("float32")

       # make sure b has the right format for the cpp function
       if not b.flags['C_CONTIGUOUS']:
              b = np.ascontiguousarray(b,dtype='float32')
       elif b.dtype != "float32":
              b = b.astype("float32")

       c = lib.wind_modulus_cpp(a,b,size)

       # c has the same format as a (order and dtype)
       if flag_fortran:
              c = np.asfortranarray(c,dtype=dtype)
       elif c.dtype != dtype:
              c = c.astype(dtype)

       return c
