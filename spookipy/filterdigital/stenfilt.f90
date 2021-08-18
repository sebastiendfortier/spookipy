!     ***************************************************************
!     *                        F I L T R E                          *
!     * Object :                                                    *
!     *         To filter data.                                     *
!     *                                                             *
!     * Arguments :                                                 *
!     *            IN /  ni    : x dimension of data                *
!     *            IN /  nj    : y dimension of data                *
!     *            IN /  Npass : nombre de passes pour le filtrage  *
!     *            IN /  list  : list des nombres de filtre        *
!     *            IN /  L     : dimension de la list              *
!     *         IN/OUT/  slab  : les donnees a filtrer              *
!     *                                                             *
!     ***************************************************************
      subroutine filtre (slab, NI, NJ, Npass, list, L)
      implicit none

      integer NI, NJ
      integer l,list(L)
      real,intent(inout) :: slab(NI ,NJ)
      real facteur(-8:8,10)
      real temp
      integer k,I,J
      integer nb_elm
      integer Npass, pass
      integer nb_elem, istart, iend
      real sum
      real result1(ni), result2(nj)

!      print *,NI,NJ,Npass,L
!      do I=1,L
!         print *,list(I)
!      enddo
!      do J=1,NJ
!         do I=1,NI
!            print *,slab(I,J)
!         enddo
!      enddo
      nb_elem = (l+1)/2
      istart = -nb_elem + 1
      iend = nb_elem -1

      do j=1, nb_elem
          do I=istart,iend
!            print *,i,j
            facteur(i,j) = 0.0
!            print ("A,I,A,I,A,f5.2"),"facteur(",i,",",j,") = ",
!     &      facteur(i,j)
          enddo
      enddo
!      do I=istart,iend
!        do J=1,nb_elem
!	        facteur(i,j) = 0.0
!        enddo
!      enddo
!      print *,"fill facteur"
      do j=1, nb_elem-1
         sum = 0.0
         do i=-j,j
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
                  temp = temp + slab(I+k,J) * facteur(k,(L/2+1)-nb_elm)
               enddo
!               print ("f10.8"),temp
               result1(I) = temp
            enddo
            do I=2, NI-1
               slab(I,J) = result1(I)
            enddo
         enddo

         do I=1, NI
            do J=2, NJ-1
               temp=0.0
               nb_elm = min(J-1,NJ-J,L/2)
               do k = -nb_elm, nb_elm
!                 print *,k,(L/2+1)-nb_elm
!                  print ("f10.8"),facteur(k,(L/2+1)-nb_elm)
                  temp = temp + slab(I,J+k) * facteur(k,(L/2+1)-nb_elm)
!                  print ("f8.6,A1,f8.6"),slab(I,J+k),",",
!     &            facteur(k,(L/2+1)-nb_elm)
               enddo
!               print ("f10.8"),temp
               result2(J) = temp
            enddo
            do J=2, NJ-1
               slab(I,J) = result2(J)
            enddo
         enddo
      enddo
!      print *,min_i,min_j,max_i,max_j
!      print *,(3+1)/2,(9+ 1)/2,(18 + 1)/2,(1 + 1)/2
!      print *,l
      return
      end
