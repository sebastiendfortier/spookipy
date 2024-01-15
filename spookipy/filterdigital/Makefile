# Minimal makefile
#
all: clean lib interface

lib:
	f2py -c -m f_stenfilt f_stenfilt.f90

interface:
	f2py --overwrite-signature -h f_stenfilt.pyf f_stenfilt.f90 -m f_stenfilt

clean:
	rm -f *.pyf *.so
