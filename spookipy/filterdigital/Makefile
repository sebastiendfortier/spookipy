# Minimal makefile
#
all: lib interface

lib:
	f2py3 -c -m stenfilt stenfilt.f90

interface:
	f2py3 -h stenfilt.pyf stenfilt.f90 -m stenfilt

clean:
	rm -f *.pyf *.so
