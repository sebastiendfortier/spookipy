# Minimal makefile
#
all: lib interface

lib:
	f2py3 -c -m tdpack tdpack.f90

interface:
	f2py3 --overwrite-signature -h tdpack.pyf tdpack.f90 -m tdpack

clean:
	rm *.pyf *.so *.mod
