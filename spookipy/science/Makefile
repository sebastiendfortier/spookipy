# Minimal makefile
#
all: lib interface

lib:
	f2py3 -c -m science science.f90

interface:
	f2py3 --overwrite-signature -h science.pyf science.f90 -m science

clean:
	rm -f *.pyf *.so *.mod
