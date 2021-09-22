# Minimal makefile
#
all: lib interface

lib:
	f2py3 -c -m f_mask f_mask.f90

interface:
	f2py3 -h f_mask.pyf f_mask.f90 -m f_mask

clean:
	rm -f *.pyf *.so
