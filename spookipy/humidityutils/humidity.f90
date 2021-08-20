
subroutine svp (tt, ni, nj, tempPhaseSwitch, iceWaterPhaseBoth)
implicit none

   real,    intent(inout) :: tt(ni ,nj)
   integer, intent(in)    :: ni, nj
   real,    intent(in)    :: tempPhaseSwitch
   logical, intent(in)    :: iceWaterPhaseBoth

   real, parameter :: TDPACK_OFFSET_FIX=0.01
   real, parameter :: AEw1 = 6.1094
   real, parameter :: AEw2 = 17.625
   real, parameter :: AEw3 = 243.05
   real, parameter :: AEi1 = 6.1121
   real, parameter :: AEi2 = 22.587
   real, parameter :: AEi3 = 273.86

   integer i,j

   do i=1, ni
         do j=1, nj
            tt(i,j) = tt(i,j)-TDPACK_OFFSET_FIX
            if ( .not. iceWaterPhaseBoth .or. (iceWaterPhaseBoth .and. tt(i,j) > tempPhaseSwitch) ) then
               tt(i,j) = AEw1 * exp((AEw2 * tt(i,j)) / (AEw3 + tt(i,j)))
            else
               tt(i,j) = AEi1 * exp((AEi2 * tt(i,j)) / (AEi3 + tt(i,j)))
            endif
         enddo
   enddo
   end

subroutine svprpn (tt, ni, nj, tempPhaseSwitch, iceWaterPhaseBoth)
   implicit none

      real,    intent(inout) :: tt(ni ,nj)
      integer, intent(in)    :: ni, nj
      real,    intent(in)    :: tempPhaseSwitch
      logical, intent(in)    :: iceWaterPhaseBoth

      integer i,j

      real foewa,foew

      do i=1, ni
            do j=1, nj
               if ( .not. iceWaterPhaseBoth .or. (iceWaterPhaseBoth .and. tt(i,j) > tempPhaseSwitch) ) then
                  tt(i,j) = foewa(tt(i,j),tempPhaseSwitch) / 100.0
               else
                  tt(i,j) = foew(tt(i,j),tempPhaseSwitch) / 100.0
               endif
            enddo
      enddo
      end


subroutine vpprtdrpn (td, ni, nj, tempPhaseSwitch)
   implicit none

      real,    intent(inout) :: td(ni ,nj)
      integer, intent(in)    :: ni, nj
      real,    intent(in)    :: tempPhaseSwitch
      integer i,j

      real foewa
      do i=1, ni
            do j=1, nj
                  td(i,j) = foewa(td(i,j),tempPhaseSwitch) / 100.0
            enddo
      enddo
      end

subroutine vpprhu (hu, ni, nj, tempPhaseSwitch)
   implicit none

      real,    intent(inout) :: hu(ni ,nj)
      integer, intent(in)    :: ni, nj
      real,    intent(in)    :: tempPhaseSwitch
      integer i,j

      real foewa
      do i=1, ni
            do j=1, nj
               hu(i,j) = max(hu(i,j) , 10e-15)
               hu(i,j) = foewa(td(i,j),tempPhaseSwitch) / 100.0
            enddo
      enddo
      end

function fomult(ddd)
   real, intent (in) :: ddd
   real, parameter :: ttns1  = 610.78
   real :: fomult
   fomult = real(ttns1*ddd)
end function fomult

function foewf(ttt,trpl)
   real, intent (in) :: ttt
   real, intent (in) :: trpl
   real, parameter :: ttns3w = 17.269
   real, parameter :: ttns3i = 21.875
   real, parameter :: ttns4w = 35.86
   real, parameter :: ttns4i = 7.66
   real :: foewf
   foewf = real(dmin1(dsign(Dble(ttns3w),                                   &
   Dble(ttt)-Dble(trpl)),dsign                                         &
   (Dble(ttns3i),Dble(ttt)-Dble(trpl)))*dabs(Dble(ttt)-Dble(trpl))/    &
   (Dble(ttt)-ttns4w+dmax1(0.d0,dsign                                  &
   (Dble(ttns4w-ttns4i),Dble(trpl)-Dble(ttt)))))
end function foewf


function foew(ttt,trpl)
   real, intent (in) :: ttt
   real, intent (in) :: trpl
   real :: foew
   real fomult, foewf
   foew = real(fomult(real(dexp(Dble(foewf(ttt,trpl))))))
end function foew

function foewaf(ttt,trpl)
   real, intent (in) :: ttt
   real, intent (in) :: trpl
   real, parameter :: ttns3w = 17.269
   real, parameter :: ttns4w = 35.86
   real :: foewaf
   foewaf = real(ttns3w*(Dble(ttt)-Dble(trpl))/(Dble(ttt)-ttns4w))
end function foewaf

function foewa(ttt,trpl)
   real, intent (in) :: ttt
   real, intent (in) :: trpl
   real :: foewa
   real fomult, foewaf
   foewa = real(fomult(real(dexp(Dble(foewaf(ttt,trpl))))))
end function foewa


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
