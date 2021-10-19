# Minimal makefile
#
all: lib interface

lib:
	f2py3 -c -m fortran_function fortran_function.f90

interface:
	f2py3 -h fortran_function.pyf fortran_function.f90 -m fortran_function

clean:
	rm -f *.pyf *.so
