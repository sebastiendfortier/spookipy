# Minimal makefile
#
all: lib interface

lib:
	f2py3 -c -m svp svp.f90

interface:
	f2py3 --overwrite-signature -h svp.pyf svp.f90 -m svp

clean:
	rm -f *.pyf *.so
