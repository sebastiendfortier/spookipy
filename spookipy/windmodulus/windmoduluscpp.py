import ctypes

import numpy as np
import numpy.ctypeslib as ctl

lib = ctypes.cdll.LoadLibrary('windmodulus.so')
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
       return lib.wind_modulus_cpp(a,b,size)
