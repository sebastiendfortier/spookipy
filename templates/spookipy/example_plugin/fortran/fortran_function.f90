! example of a fortran function that can be converted to a python module with f2py

subroutine fortran_function (a, b, ni, nj, res)
    implicit none
    real, intent(in)    :: a(ni,nj)
    real, intent(in)    :: b(ni,nj)
    real, intent(out)   :: res(ni,nj)
    integer, intent(in) :: ni,nj
    res = (a**2+b**2)**0.5
end subroutine    
