! Modified version of f_stenfilt with ISO_C_BINDING for ctypes
module f_stenfilt_mod
  use iso_c_binding
  implicit none
  
  contains
  
  ! Add bind(C) and explicit C types for interoperability
  subroutine f_stenfilt(slab, NI, NJ, Npass, list, L, res) bind(C, name='f_stenfilt')
    use iso_c_binding
    implicit none

    integer(c_int), value :: NI, NJ
    integer(c_int), value :: L
    integer(c_int), intent(in) :: list(L)
    integer(c_int), value :: Npass
    real(c_float), intent(in) :: slab(NI, NJ)
    real(c_float), intent(out) :: res(NI, NJ)
    
    real(c_float) :: facteur(-8:8,10)
    real(c_float) :: temp
    integer(c_int) :: k, I, J
    integer(c_int) :: nb_elm
    integer(c_int) :: pass
    integer(c_int) :: nb_elem, istart, iend
    real(c_float) :: sum
    real(c_float) :: result1(ni), result2(nj)

    res = slab

    nb_elem = (L+1)/2
    istart = -nb_elem + 1
    iend = nb_elem - 1

    do j=1, nb_elem
      do I=istart, iend
        facteur(i,j) = 0.0
      enddo
    enddo

    do j=1, nb_elem-1
      sum = 0.0
      do i=-j, j
        sum = sum + REAL(list(I+nb_elem))
      enddo

      do i=-j,j
!            print *,i,nb_elem-j
!            print *,((i .ge. 4) .and. (i .le. 9)),((nb_elem-j .ge. -4)
!     &      .and. (nb_elem-j .le. 4))
!            print ("A10,f8.6"),"facteur = ",
!     &      (1.0*REAL(list(i+nb_elem)) / sum)      
        facteur(i,nb_elem-j) = 1.0*REAL(list(i+nb_elem)) / sum
!            print ("A,I,A,I,A,f8.6"),"facteur(",i,",",nb_elem-j,") = ",
!     &      facteur(i,nb_elem-j)
         enddo        
      enddo
!      print *,"display facteur"
      do I=istart,iend
        do J=1,nb_elem
!        print ("A8,I2,A1,I2,A4,f8.6"),"facteur(",i,",",j,") = ",
!     &      facteur(i,j)      
      enddo
    enddo
!      print *,"compute"   
    do pass=1, Npass
      do J=1, NJ
        do I=2, NI-1
          temp = 0.0
          nb_elm = min(I-1,NI-I,L/2)
          do k = -nb_elm, nb_elm
!                   print *,k,(L/2+1)-nb_elm
!                  print ("f8.6"),slab(I+k,J)
!                  print ("f8.6"),facteur(k,(L/2+1)-nb_elm)
!                  print ("f10.8"),facteur(k,(L/2+1)-nb_elm)          
            temp = temp + res(I+k,J) * facteur(k,(L/2+1)-nb_elm)
          enddo
!               print ("f10.8"),temp          
          result1(I) = temp
        enddo
        do I=2, NI-1
          res(I,J) = result1(I)
        enddo
      enddo

      do I=1, NI
        do J=2, NJ-1
          temp=0.0
          nb_elm = min(J-1,NJ-J,L/2)
          do k = -nb_elm, nb_elm
!                 print *,k,(L/2+1)-nb_elm
!                  print ("f10.8"),facteur(k,(L/2+1)-nb_elm)
            temp = temp + res(I,J+k) * facteur(k,(L/2+1)-nb_elm)
!                  print ("f8.6,A1,f8.6"),slab(I,J+k),",",
!     &            facteur(k,(L/2+1)-nb_elm)            
          enddo
!               print ("f10.8"),temp
          result2(J) = temp
        enddo
        do J=2, NJ-1
          res(I,J) = result2(J)
        enddo
      enddo
    enddo
!      print *,min_i,min_j,max_i,max_j
!      print *,(3+1)/2,(9+ 1)/2,(18 + 1)/2,(1 + 1)/2
!      print *,l
    return
  end subroutine f_stenfilt
  
end module f_stenfilt_mod

