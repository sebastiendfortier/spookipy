# Python interface to the f_stenfilt Fortran subroutine using ctypes
import ctypes
import os

import numpy as np
from numpy.ctypeslib import ndpointer

# Load the shared library
# Adjust the path as needed - this assumes the library is in the same directory
_libpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libstenfilt.so")
_lib = ctypes.CDLL(_libpath)

# Define the function signature for f_stenfilt
_lib.f_stenfilt.argtypes = [
    ndpointer(ctypes.c_float, flags="F_CONTIGUOUS"),  # slab
    ctypes.c_int,  # NI
    ctypes.c_int,  # NJ
    ctypes.c_int,  # Npass
    ndpointer(ctypes.c_int, flags="F_CONTIGUOUS"),  # list
    ctypes.c_int,  # L
    ndpointer(ctypes.c_float, flags="F_CONTIGUOUS"),  # res
]
_lib.f_stenfilt.restype = None  # void return type


def f_stenfilt(slab, ni, nj, npass, list, list_len):
    """
    Python wrapper for the Fortran f_stenfilt function.

    Parameters:
    -----------
    slab : 2D numpy array of floats
        Input data to be filtered
    ni : int
        X dimension of data
    nj : int
        Y dimension of data
    npass : int
        Number of filter passes
    list : numpy array of ints
        List of filter numbers
    list_len : int
        Dimension of the list

    Returns:
    --------
    res : 2D numpy array of floats
        Filtered data
    """
    # Ensure input arrays are in the correct format
    slab_c = np.asfortranarray(slab, dtype=np.float32)
    list_c = np.ascontiguousarray(list, dtype=np.int32)

    # Create output array
    res = np.empty_like(slab_c, dtype=np.float32, order="F")

    # Call the Fortran function
    _lib.f_stenfilt(slab_c, ni, nj, npass, list_c, list_len, res)

    return res
