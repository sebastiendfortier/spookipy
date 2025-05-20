# Makefile to compile the Fortran code into a shared library

FC = gfortran
FFLAGS = -fPIC -O2 -shared

# Target shared library
LIBRARY = libstenfilt.so

all: $(LIBRARY)

$(LIBRARY): f_stenfilt_mod.f90
	$(FC) $(FFLAGS) -o $@ $<

clean:
	rm -f *.so *.o *.mod

