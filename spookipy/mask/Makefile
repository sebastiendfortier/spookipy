# Minimal makefile
#
all: lib interface

lib:
	f2py3 -c -m fmask fmask.f90

interface:
	f2py3 -h fmask.pyf fmask.f90 -m fmask

clean:
	rm -f *.pyf *.so
