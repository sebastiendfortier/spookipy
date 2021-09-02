module science
implicit none
   ! real,   parameter ::  AI = 0.2864887713087E4
   ! real,   parameter ::  AW = 0.3135012829948E0
   ! real,   parameter ::  BI = 0.1660931315020E0
   ! real,   parameter ::  BW = 0.2367075766316E1
   ! real,   parameter ::  CHLF = 0.3340000000000E6
   ! real,   parameter ::  CHLC = 0.2501000000000E7
   ! real,   parameter ::  CONSOL = 0.1367000000000E4
   ! real,   parameter ::  CONSOL2 = 0.1361000000000E4
   ! real,   parameter ::  CPD = 0.1005460000000E4
   ! real,   parameter ::  CPV = 0.1869460000000E4
   ! real,   parameter ::  CPI = 0.2115300000000E4
   ! real,   parameter ::  CPW = 0.4218000000000E4
   ! real,   parameter ::  DELTA = 0.6077686814144E0
   real*8,   parameter ::  EPS1 = 0.6219800221014E0
   real*8,   parameter ::  EPS2 = 0.3780199778986E0
   ! real,   parameter ::  GRAV = 0.9806160000000E1
   ! real,   parameter ::  KARMAN = 0.4000000000000E0
   ! real,   parameter ::  KNAMS = 0.5147910000000E0
   ! real,   parameter ::  OMEGA = 0.7292000000000E-4
   ! real,   parameter ::  PI = 3.14159265358979323846
   ! real,   parameter ::  RAUW = 0.1000000000000E4
   ! real,   parameter ::  RAYT = 0.6371220000000E7
   ! real,   parameter ::  RGASD = 0.2870500000000E3
   ! real,   parameter ::  RGASV = 0.4615100000000E3
   ! real,   parameter ::  RIC = 0.2000000000000E0
   ! real,   parameter ::  SLP = 0.6666666666667E-1
   ! real,   parameter ::  STEFAN = 0.5669800000000E-7
   ! real,   parameter ::  STLO = 0.6628486583943E-3
   ! real,   parameter ::  T1S = 0.2731600000000E3
   ! real,   parameter ::  T2S = 0.2581600000000E3
   ! real,   parameter ::  TCDK = 0.2731500000000E3
   ! real,   parameter ::  TGL = 0.2731600000000E3
   real*8,   parameter ::  TRPL = 0.2731600000000E3
   ! real,   parameter ::  CAPPA = (RGASD/CPD)
   ! real,   parameter ::  CVD = (CPD - RGASD)
   ! real,   parameter :: TTNS1 = 610.78
   ! real,   parameter :: TTNS3W = 17.269
   ! real,   parameter :: TTNS3I = 21.875
   ! real,   parameter :: TTNS4W = 35.86
   ! real,   parameter :: TTNS4I = 7.66
   real*8,   parameter :: AERK1W = 610.94
   real*8,   parameter :: AERK2W = 17.625
   real*8,   parameter :: AERK3W = 30.11
   real*8,   parameter :: AERK1I = 611.21
   real*8,   parameter :: AERK2I = 22.587
   real*8,   parameter :: AERK3I = -0.71
   ! real, parameter :: CTE1 = (AERK2W*(TRPL-AERK3W))
   ! real, parameter :: CTE2 = (AERK2I*(TRPL-AERK3I)-CTE1)
   ! real, parameter :: CTE3 = 2317
   ! real, parameter :: CTE4 = 7.24
   ! real, parameter :: CTE5 = 128.4


   ! real, parameter :: TDPACK_OFFSET_FIX=0.01
   real*8, parameter :: AEw1 = 6.1094
   real*8, parameter :: AEw2 = 17.625
   real*8, parameter :: AEw3 = 243.05
   real*8, parameter :: AEi1 = 6.1121
   real*8, parameter :: AEi2 = 22.587
   real*8, parameter :: AEi3 = 273.86

contains


function DIFTRPL(ttt)
   implicit none
   real*8, intent(in) :: ttt
   real*8 DIFTRPL
   DIFTRPL=(ttt-TRPL)
end function
! #define _FN1(ttt)              (_DBLE(ttt)-AERK3W+_DMAX1(_ZERO,_DSIGN(AERK3W-AERK3I,-_DIFTRPL(ttt))))
function FN1(ttt)
   implicit none
   real*8, intent(in) :: ttt
   real*8 FN1
   FN1=(ttt-AERK3W+dmax1(0d0,dsign(AERK3W-AERK3I,-DIFTRPL(ttt))))
end function
! #define MASKT(ttt)             _DMAX1(_ZERO,_DSIGN(_ONE,_DIFTRPL(ttt)))
function MASKT(ttt)
   implicit none
   real*8, intent(in) :: ttt
   real*8 MASKT
   MASKT=dmax1(0d0,dsign(1d0,DIFTRPL(ttt)))
end function
! #define FOMULTS(ddd,ttt)       ((AERK1W*MASKT(ttt)+(_ONE-MASKT(ttt))*AERK1I)*ddd)
function FOMULTS(ddd,ttt)
   implicit none
   real*8, intent(in) :: ddd
   real*8, intent(in) :: ttt
   real*8 FOMULTS
   FOMULTS=((AERK1W*MASKT(ttt)+(1d0-MASKT(ttt))*AERK1I)*ddd)
end function
! #define FOEWF(ttt)             (_DMIN1(_DSIGN(AERK2W,_DIFTRPL(ttt)),_DSIGN(AERK2I,_DIFTRPL(ttt)))*_DABS(_DIFTRPL(ttt))/_FN1(ttt))
function FOEWF(ttt)
   implicit none
   real*8, intent(in) :: ttt
   real*8 FOEWF
   FOEWF=dmin1(dsign(AERK2W,DIFTRPL(ttt)),DSIGN(AERK2I,DIFTRPL(ttt)))*dabs(DIFTRPL(ttt))/FN1(ttt)
end function
! #define FOEW(ttt)              (FOMULTS(_DEXP(FOEWF(ttt)),ttt))
function FOEW(ttt)
   implicit none
   real*8, intent(in) :: ttt
   real*8 FOEW
   FOEW=FOMULTS(dexp(FOEWF(ttt)),ttt)
end function

! #define FOEWAF(ttt)            (AERK2W*(_DIFTRPL(ttt))/(_DBLE(ttt)-AERK3W))
function FOEWAF(ttt)
   implicit none
   real*8, intent(in) :: ttt
   real*8 FOEWAF
   FOEWAF=(AERK2W*(DIFTRPL(ttt))/(ttt-AERK3W))
end function
! #define FOEWA(ttt)             (AERK1W*_DEXP(FOEWAF(ttt)))
function FOEWA(ttt)
   implicit none
   real*8, intent(in) :: ttt
   real*8 FOEWA
   FOEWA=(AERK1W*dexp(FOEWAF(ttt)))
end function

! #define FOQFE(eee,prs)         (_DMIN1(_ONE,_EPS1*_DBLE(eee)/(_DBLE(prs)-_EPS2*_DBLE(eee))))
function FOQFE(eee,prs)
   implicit none
   real*8, intent(in) :: eee
   real*8, intent(in) :: prs
   real*8 FOQFE
   FOQFE=(dmin1(1d0,EPS1*eee/(prs-EPS2*eee)))
end function

! #define FOEFQ(qqq,prs)         (_DMIN1(_DBLE(prs),(_DBLE(qqq)*_DBLE(prs))/(_EPS1+_EPS2*_DBLE(qqq))))
function FOEFQ(qqq,prs)
   implicit none
   real*8, intent(in) :: qqq
   real*8, intent(in) :: prs
   real*8 FOEFQ
   FOEFQ=(dmin1(prs,(qqq*prs)/(EPS1+EPS2*qqq)))
end function

! #define FOHR(qqq,ttt,prs)      (_DMIN1(_DBLE(prs),FOEFQ(qqq,prs))/FOEW(ttt))
function FOHR(qqq,ttt,prs)
   implicit none
   real*8, intent(in) :: qqq
   real*8, intent(in) :: ttt
   real*8, intent(in) :: prs
   real*8 FOHR
   FOHR=(dmin1(prs,FOEFQ(qqq,prs))/FOEW(ttt))
end function

! #define FOHRA(qqq,ttt,prs)     (_DMIN1(_DBLE(prs),FOEFQ(qqq,prs))/FOEWA(ttt))
function FOHRA(qqq,ttt,prs)
   implicit none
   real*8, intent(in) :: qqq
   real*8, intent(in) :: ttt
   real*8, intent(in) :: prs
   real*8 FOHRA
   FOHRA=(dmin1(prs,FOEFQ(qqq,prs))/FOEWA(ttt))
end function

function shuahr(hu,tt,px,swph)
   implicit none
   real*8, intent(in) :: hu
   real*8, intent(in) :: tt
   real*8, intent(in) :: px
   logical, intent(in) :: swph
   real*8 shuahr
   if (swph) then
      shuahr = FOHR(hu,tt,px)
   else
      shuahr = FOHRA(hu,tt,px)
   endif
end function


function sesahu(es,tt,px,swph)
   implicit none
   real*8, intent(in) :: es
   real*8, intent(in) :: tt
   real*8, intent(in) :: px
   logical, intent(in) :: swph
   real*8 e,td
   real*8 sesahu
   td = tt - es
   if (swph) then
      e = FOEW(td)
   else
      e = FOEWA(td)
   endif
   sesahu = FOQFE(e,px)
end function


function sesahr(es,tt,px,swph)
   implicit none
   real*8, intent(in) :: es
   real*8, intent(in) :: tt
   real*8, intent(in) :: px
   logical, intent(in) :: swph
   real*8 hu
   real*8 sesahr
   hu = sesahu(es,tt,px,swph)
   sesahr = shuahr(hu,tt,px,swph)
end function

function shrahu(hr, tt, px, swph)
   implicit none
   real*8, intent(in) :: hr
   real*8, intent(in) :: tt
   real*8, intent(in) :: px
   logical, intent(in) :: swph
   real*8 hrtt,e
   real*8 shrahu
   hrtt = hr * tt
   if (swph) then
      e = dmin1(px,hr * FOEW(tt))
   else
      e = dmin1(px,hr * FOEWA(tt))
   endif
   shrahu = FOQFE(e,px)
end function

function shuaes(hu, tt, px, swph)
   implicit none
   real*8, intent(in) :: hu
   real*8, intent(in) :: tt
   real*8, intent(in) :: px
   logical, intent(in) :: swph
   real*8 e,cte,td,hutmp,petit,alpha
   real*8 shuaes
   petit = 0.0000000001
   alpha = dlog(AERK1W/AERK1I)
   hutmp = hu
   e = FOEFQ(dmax1(petit,hu),px)
   cte = dlog(e/AERK1W)
   td = (AERK3W*cte - AERK2W*TRPL)/(cte - AERK2W)
   If (td .LT. trpl .AND. swph) THEN
      td = ((AERK3I*(cte + alpha) - AERK2I)*TRPL)/(cte + alpha - AERK2I)
   END IF !
   shuaes = (tt-td)
end function


function shraes(hr, tt, px, swph)
   implicit none
   real*8, intent(in) :: hr
   real*8, intent(in) :: tt
   real*8, intent(in) :: px
   logical, intent(in) :: swph
   real*8 hu
   real*8 shraes
   hu = shrahu(hr,tt,px,swph)
   shraes = shuaes(hu,tt,px,swph)
end function


!
! Calculates the saturation vapour pressure (Water phase) as a function of temperature.
! @param tt  Air temperature (celsius)
! @return  Saturation vapour pressure, SVP (hPa)
!
function svp_water_from_tt(tt)
   implicit none
   real*8,  intent(in) :: tt
   real*8 svp_water_from_tt
   svp_water_from_tt = AEw1 * dexp((AEw2 * tt) / (AEw3 + tt))
end function

!
! Calculates the saturation vapour pressure (ice phase) as a function of temperature.
! @param tt  Air temperature (celsius)
! @return  Saturation vapour pressure, SVP (hPa)
!/
function svp_ice_from_tt(tt)
   implicit none
   real*8,  intent(in) :: tt
   real*8 svp_ice_from_tt
   svp_ice_from_tt = AEi1 * dexp((AEi2 * tt) / (AEi3 + tt))
end function

!
! Calculates the saturation vapour pressure as a function of temperature.
! @param tt     Air temperature (celsius)
! @param tpl    Temperature at which to change from the ice phase to the water phase (celsius).
! @param swph   A boolean representing if we consider both ice and water phase.
! @return  Saturation vapour pressure, SVP (hPa)
!/
subroutine svp_from_tt(tt, ni, nj, tpl, swph, res)
   implicit none

   real*8,  intent(in)   :: tt(ni ,nj)
   real*8,  intent(out)  :: res(ni ,nj)
   integer, intent(in) :: ni, nj
   real*8,  intent(in)   :: tpl
   logical, intent(in) :: swph

   integer i,j

   do i=1, ni
      do j=1, nj
         if ( .not. swph .or. (swph .and. tt(i,j) > tpl) ) then
            res(i,j) = svp_water_from_tt(tt(i,j))
         else
            res(i,j) = svp_ice_from_tt(tt(i,j))
         endif
      enddo
   enddo
end subroutine



!
! Calculates the saturation vapour pressure (water phase) using RPN TdPack as a function of temperature.
! @param tt  Air temperature (kelvin)
! @return  Saturation vapour pressure, SVP (hPa)
!
function rpn_svp_water(tt)
   implicit none
   real*8,  intent(in) :: tt
   real*8 rpn_svp_water
   rpn_svp_water = FOEWA(tt) / 100.
end function

!
! Calculates the saturation vapour pressure (ice phase) using RPN TdPack as a function of temperature.
! @param tt  Air temperature (kelvin)
! @return  Saturation vapour pressure, SVP (hPa)
!/
function rpn_svp_ice(tt)
   implicit none
   real*8,  intent(in)    :: tt
   real*8 rpn_svp_ice
      !RPN returns Saturation vapour pressure in Pascal and we want output to be HectoPascal.
      !return rpn::libphy::sfoew(tt) / 100.0f
   rpn_svp_ice = FOEW(tt) / 100.
end function

!
! Calculates the saturation vapour pressure using RPN TdPack as a function of temperature.
! @param tt     Air temperature (kelvin)
! @param tpl    Temperature at which to change from the ice phase to the water phase (kelvin).
! @param swph   A boolean representing if we consider both ice and water phase.
! @return  Saturation vapour pressure, SVP (hPa)
!/
subroutine rpn_svp(tt, ni, nj, tpl,  swph, res)
   implicit none
   real*8,    intent(in)  :: tt(ni ,nj)
   real*8,    intent(out) :: res(ni ,nj)
   integer, intent(in)  :: ni, nj
   real*8,    intent(in)  :: tpl
   logical, intent(in)  :: swph
   integer i,j

   do i=1, ni
      do j=1, nj
         if ( .not. swph .or. (swph .and. tt(i,j) > tpl) ) then
            res(i,j) = rpn_svp_water(tt(i,j))
         else
            res(i,j) = rpn_svp_ice(tt(i,j))
         endif
      enddo
   enddo
end subroutine


!
! Calculates the vapour pressure as a function of relative humidity and saturation vapour pressure.
! @param hr   Relative humidity, in decimal (between 0 and 1)
! @param svp  saturation vapour pressure, in hPa
! @return     Vapour pressure, in hPa
!/
subroutine vppr_from_hr(hr, svp, ni, nj, res)
   implicit none
   real*8,  intent(in)     :: hr(ni ,nj)
   real*8,  intent(in)     :: svp(ni ,nj)
   real*8,    intent(out)  :: res(ni ,nj)
   integer, intent(in)   :: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = dmax1(hr(i,j), 10E-15)
         res(i,j) = res(i,j) * svp(i,j)
      enddo
   enddo
end subroutine

!
! Calculates the vapour pressure as a function of specific humidity and pressure.
! @param hu   Specific humidity, in kg/kg
! @param px   Pressure, in hPa
! @return     Vapour pressure, in hPa
!/
subroutine vppr_from_hu(hu, px, ni, nj, res)
   implicit none
   real*8,    intent(in)    :: hu(ni ,nj)
   real*8,    intent(in)    :: px(ni ,nj)
   real*8,    intent(out)   :: res(ni ,nj)
   integer, intent(in)    :: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = dmax1(hu(i,j), 10E-15)
         res(i,j) = (res(i,j) * px(i,j))/(EPS1 + res(i,j) * (1.-EPS1))
      enddo
   enddo
end subroutine

!
! Calculates the vapour pressure as a function of mixing ratio and pressure.
! @param qv   Mixing ratio, in kg/kg
! @param px   Pressure, in hPa
! @return     Vapour pressure, in hPa
!/
subroutine vppr_from_qv(qv, px, ni, nj, res)
   implicit none
   real*8,  intent(in)    :: qv(ni ,nj)
   real*8,  intent(in)    :: px(ni ,nj)
   real*8,  intent(out)   :: res(ni ,nj)
   integer, intent(in)  :: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = dmax1(qv(i,j), 10E-15)
         res(i,j) = (res(i,j) * px(i,j))/(EPS1 + res(i,j))
      enddo
   enddo
end subroutine

!
! Calculates the vapour pressure (water phase) as a function of temperature dew point.
! @param td   Temperature dew point, in celsius
! @return     Vapour pressure, in hPa
!/
function vppr_water_td(td)
   implicit none
   real*8,  intent(in) :: td
   real*8 vppr_water_td
   vppr_water_td = AEw1 * dexp(((AEw2 * td) / (AEw3 + td)))
end function


!
! Calculates the vapour pressure (ice phase) as a function of temperature dew point.
! @param td   Temperature dew point, in celsius
! @return     Vapour pressure, in hPa
!/

function vppr_ice_td(td)
   implicit none
   real*8,  intent(in) :: td
   real*8 vppr_ice_td
   vppr_ice_td = AEi1 * dexp(((AEi2 * td) / (AEi3 + td)))
end function

!
! Calculates the vapour pressure as a function of temperature dew point.
! @param td     Temperature dew point, in celsius
! @param tt     Air temperature (celsius)
! @param tpl    Temperature at which to change from the ice phase to the water phase (celsius).
! @param swph   A boolean representing if we consider both ice and water phase.
! @return     Vapour pressure, in hPa
!/
subroutine vppr_from_td(td, tt, ni, nj, tpl, swph, res)
   implicit none
   real*8,  intent(in)     :: td(ni ,nj)
   real*8,  intent(in )    :: tt(ni ,nj)
   real*8,  intent(out)    :: res(ni ,nj)
   integer, intent(in)   :: ni, nj
   real*8,    intent(in)   :: tpl
   logical,   intent(in) :: swph
   integer i,j

   do i=1, ni
      do j=1, nj
         if ( .not. swph .or. (swph .and. tt(i,j) > tpl) ) then
            res(i,j) = vppr_water_td(td(i,j))
         else
            res(i,j) = vppr_ice_td(td(i,j))
         endif
         ! if (res(i,j) .eq. 0.) then
         !    print *,td(i,j),tt(i,j)
         ! endif
      enddo
   enddo
end subroutine


!
! Calculates the vapour pressure using RPN TdPack as a function of specific humidity and pressure.
! @param hu   Specific humidity, in kg/kg
! @param px   Pressure, in Pa
! @return     Vapour pressure, in hPa
!/
subroutine rpn_vppr_from_hu(hu, px, ni, nj, res)
   implicit none
   real*8,  intent(in)    :: hu(ni ,nj)
   real*8,  intent(in)    :: px(ni ,nj)
   real*8,  intent(out)   :: res(ni ,nj)
   integer, intent(in)  :: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
            res(i,j) = FOEFQ(hu(i,j), px(i,j)) / 100.
      enddo
   enddo
   !RPN returns vapour pressure in Pascal and we want output to be HectoPascal.
   !return rpn::libphy::sfoefq(hu, px) / 100.0f

end subroutine

!
! Calculates the vapour pressure (water phase) as a function of temperature dew point.
! @param td   Temperature dew point, in kelvin
! @return     Vapour pressure, in hPa
!
function rpn_vppr_water_from_td(td)
   implicit none
   real*8,  intent(in) :: td
   real*8 rpn_vppr_water_from_td
   !RPN returns vapour pressure in Pascal and we want output to be HectoPascal.
   !return rpn::libphy::sfoewa(td) / 100.0d0f
   rpn_vppr_water_from_td = FOEWA(td) / 100.
end function

!
! Calculates the vapour pressure (ice phase) as a function of temperature dew point.
! @param td   Temperature dew point, in kelvin
! @return     Vapour pressure, in hPa
!
function rpn_vppr_ice_from_td(td)
   implicit none
   real*8,  intent(in) :: td
   real*8 rpn_vppr_ice_from_td
      !RPN returns vapour pressure in Pascal and we want output to be HectoPascal.
      !return rpn::libphy::sfoew(td) / 100.0d0f
   rpn_vppr_ice_from_td = FOEW(td) / 100.
end function

!
! Calculates the vapour pressure as a function of temperature dew point.
! @param td   Temperature dew point, in kelvin
! @param tt     Air temperature (kelvin)
! @param tpl    Temperature at which to change from the ice phase to the water phase (kelvin).
! @param swph   A boolean representing if we consider both ice and water phase.
! @return     Vapour pressure, in hPa
!/
subroutine rpn_vppr_from_td(td, tt, ni, nj, tpl, swph, res)
   implicit none
   real*8,  intent(in)    :: td(ni ,nj)
   real*8,  intent(in)    :: tt(ni ,nj)
   real*8,  intent(out)   :: res(ni ,nj)
   integer, intent(in)  :: ni, nj
   real*8,    intent(in)  :: tpl
   logical, intent(in)  :: swph
   integer i,j
   do i=1, ni
      do j=1, nj
         if ( .not. swph .or. (swph .and. tt(i,j) > tpl) ) then
            res(i,j) = rpn_vppr_water_from_td(td(i,j))
         else
            res(i,j) = rpn_vppr_ice_from_td(td(i,j))
         endif
      enddo
   enddo
end subroutine

subroutine td_from_es(tt,es,ni,nj,res)
   implicit none
   real*8,  intent(in)  :: tt(ni ,nj)
   real*8,  intent(in)  :: es(ni ,nj)
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         if (es(i,j) < 0.) then
            res(i,j) = tt(i,j)
         else
            res(i,j) = tt(i,j)-es(i,j)
         endif
      enddo
   enddo
end subroutine

!
! Calculates the temperature dew point (Water Phase) as a function of vapour pressure.
! @param vppr   Vapour pressure (hPa)
! @return 		 Temperature dew point, TD (celsius)
!
function td_water_from_vppr(vppr)
   implicit none
   real*8,  intent(in) :: vppr
   real*8 tmpvppr,td_water_from_vppr
   tmpvppr = dmax1(vppr, 10E-15)
   !RPN returns vapour pressure in Pascal and we want output to be HectoPascal.
   !return rpn::libphy::sfoewa(td) / 100.0d0f
   td_water_from_vppr = ((AEw3 * dlog(tmpvppr/AEw1) ) / ( AEw2 - dlog(tmpvppr/AEw1)))
end function

!
! Calculates the temperature dew point (Ice Phase) as a function of vapour pressure.
! @param vppr   Vapour pressure (hPa)
! @return 		 Temperature dew point, TD (celsius)
!
function td_ice_from_vppr(vppr)
   implicit none
   real*8, intent(in) :: vppr
   real*8 tmpvppr,td_ice_from_vppr
   tmpvppr = dmax1(vppr, 10E-15)
   td_ice_from_vppr =  ((AEi3 * dlog(tmpvppr/AEi1) ) / ( AEi2 - dlog(tmpvppr/AEi1)))
end function

subroutine td_from_vppr(tt,vppr,ni,nj,tpl,swph,res)
   implicit none
   real*8,  intent(in)  :: tt(ni ,nj)
   real*8,  intent(in)  :: vppr(ni ,nj)
   real*8,  intent(in)  :: tpl
   logical, intent(in):: swph
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         if ( .not. swph .or. (swph .and. tt(i,j) > tpl) ) then
            res(i,j) = td_water_from_vppr(vppr(i,j))
         else
            res(i,j) = td_ice_from_vppr(vppr(i,j))
         endif
      enddo
   enddo
end subroutine

subroutine rpn_hu_from_hr(tt,hr,px,ni,nj,swph,res)
   implicit none
   real*8,  intent(in)  :: tt(ni ,nj)
   real*8,  intent(in)  :: hr(ni ,nj)
   real*8,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = shrahu(hr(i,j), tt(i,j), px(i,j), swph)
      enddo
   enddo
end subroutine


subroutine rpn_es_from_hr(tt,hr,px,ni,nj,swph,res)
   implicit none
   real*8,  intent(in)  :: tt(ni ,nj)
   real*8,  intent(in)  :: hr(ni ,nj)
   real*8,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = dmax1(shraes(hr(i,j), tt(i,j), px(i,j), swph),0.)
      enddo
   enddo
end subroutine

subroutine rpn_es_from_hu(tt,hu,px,ni,nj,swph,res)
   implicit none
   real*8,  intent(in)  :: tt(ni ,nj)
   real*8,  intent(in)  :: hu(ni ,nj)
   real*8,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = dmax1(shuaes(hu(i,j), tt(i,j), px(i,j), swph),0.)
      enddo
   enddo
end subroutine

subroutine hu_from_qv(qv,ni,nj,res)
   implicit none
   real*8,  intent(in)  :: qv(ni ,nj)
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   real*8 tmpqv
   do i=1, ni
      do j=1, nj
         tmpqv= dmax1(qv(i,j),10E-15)
         res(i,j) = tmpqv / (tmpqv + 1.)
      enddo
   enddo
end subroutine

subroutine td_from_hr(tt,hr,ni,nj,res)
   implicit none
   real*8,  intent(in)  :: tt(ni ,nj)
   real*8,  intent(in)  :: hr(ni ,nj)
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   real*8,   parameter :: vara = 17.625
   real*8,   parameter :: varb = 243.04
   real*8 hrtmp,term

   do i=1, ni
      do j=1, nj
         hrtmp = hr(i,j)
         if (hrtmp > 1.) then
            hrtmp = 1.
         endif
         if (hrtmp < 10E-15) then
            hrtmp = 10E-15
         endif
         term = (vara * tt(i,j))/(varb + tt(i,j)) + dlog(hrtmp)
         res(i,j) = (varb * term) / (vara - term )
      enddo
   enddo
end subroutine


subroutine hr_from_svp_vppr(svp,vppr,ni,nj,res)
   implicit none
   real*8,  intent(in)  :: svp(ni ,nj)
   real*8,  intent(in)  :: vppr(ni ,nj)
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = vppr(i,j)/svp(i,j)
      enddo
   enddo
end subroutine


subroutine rpn_hr_from_es(tt,es,px,ni,nj,swph,res)
   implicit none
   real*8,  intent(in)  :: tt(ni ,nj)
   real*8,  intent(in)  :: es(ni ,nj)
   real*8,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = sesahr(es(i,j), tt(i,j), px(i,j), swph)
      enddo
   enddo
end subroutine

subroutine rpn_hr_from_hu(tt,hu,px,ni,nj,swph,res)
   implicit none
   real*8,  intent(in)  :: tt(ni ,nj)
   real*8,  intent(in)  :: hu(ni ,nj)
   real*8,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = shuahr(hu(i,j), tt(i,j), px(i,j), swph)
      enddo
   enddo
end subroutine


subroutine hu_from_vppr(vppr,px,ni,nj,res)
   implicit none
   real*8,  intent(in)  :: vppr(ni ,nj)
   real*8,  intent(in)  :: px(ni ,nj)
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = (EPS1 * vppr(i,j)) / (px(i,j) - (1.-EPS1)*vppr(i,j))
      enddo
   enddo
end subroutine


subroutine rpn_hu_from_es(tt,es,px,ni,nj,swph,res)
   implicit none
   real*8,  intent(in)  :: tt(ni ,nj)
   real*8,  intent(in)  :: es(ni ,nj)
   real*8,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = sesahu(es(i,j), tt(i,j), px(i,j), swph)
      enddo
   enddo
end subroutine


subroutine hmx_from_svp(tt,svp,ni,nj,res)
   implicit none
   real*8,  intent(in)  :: tt(ni ,nj)
   real*8,  intent(in)  :: svp(ni ,nj)
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   real*8 resultat
   integer i,j
   do i=1, ni
      do j=1, nj
         resultat = tt(i,j) + (0.55555 * (svp(i,j) - 10.))
         if (resultat > tt(i,j)) then
            res(i,j) = resultat
         else
            res(i,j) = tt(i,j)
         endif
      enddo
   enddo
end subroutine

subroutine qv_from_hu(hu,ni,nj,res)
   implicit none
   real*8,  intent(in)  :: hu(ni ,nj)
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   real*8 hutmp
   integer i,j
   do i=1, ni
      do j=1, nj
         hutmp = dmax1(hu(i,j),10d-15)
         res(i,j) = (hutmp / (1. - hutmp)) * 1000d0
      enddo
   enddo
end subroutine

subroutine qv_from_vppr(vppr,px,ni,nj,res)
   implicit none
   real*8,  intent(in)  :: vppr(ni ,nj)
   real*8,  intent(in)  :: px(ni ,nj)
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         if (px(i,j) < 10E-15) then
            res(i,j) = 0.
         else
            res(i,j) = EPS1 * (vppr(i,j) / (px(i,j) - vppr(i,j))) * 1000.
         endif
      enddo
   enddo
end subroutine

subroutine es_from_td(tt,td,ni,nj,res)
   implicit none
   real*8,  intent(in)  :: tt(ni ,nj)
   real*8,  intent(in)  :: td(ni ,nj)
   real*8,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = dmax1(tt(i,j) - td(i,j), 0.)
      enddo
   enddo
end subroutine

end module science
