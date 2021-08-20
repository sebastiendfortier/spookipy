module science
implicit none
   real,   parameter ::  AI = 0.2864887713087E4
   real,   parameter ::  AW = 0.3135012829948E0
   real,   parameter ::  BI = 0.1660931315020E0
   real,   parameter ::  BW = 0.2367075766316E1
   real,   parameter ::  CHLF = 0.3340000000000E6
   real,   parameter ::  CHLC = 0.2501000000000E7
   real,   parameter ::  CONSOL = 0.1367000000000E4
   real,   parameter ::  CONSOL2 = 0.1361000000000E4
   real,   parameter ::  CPD = 0.1005460000000E4
   real,   parameter ::  CPV = 0.1869460000000E4
   real,   parameter ::  CPI = 0.2115300000000E4
   real,   parameter ::  CPW = 0.4218000000000E4
   real,   parameter ::  DELTA = 0.6077686814144E0
   real,   parameter ::  EPS1 = 0.6219800221014E0
   real,   parameter ::  EPS2 = 0.3780199778986E0
   real,   parameter ::  GRAV = 0.9806160000000E1
   real,   parameter ::  KARMAN = 0.4000000000000E0
   real,   parameter ::  KNAMS = 0.5147910000000E0
   real,   parameter ::  OMEGA = 0.7292000000000E-4
   real,   parameter ::  PI = 3.14159265358979323846
   real,   parameter ::  RAUW = 0.1000000000000E4
   real,   parameter ::  RAYT = 0.6371220000000E7
   real,   parameter ::  RGASD = 0.2870500000000E3
   real,   parameter ::  RGASV = 0.4615100000000E3
   real,   parameter ::  RIC = 0.2000000000000E0
   real,   parameter ::  SLP = 0.6666666666667E-1
   real,   parameter ::  STEFAN = 0.5669800000000E-7
   real,   parameter ::  STLO = 0.6628486583943E-3
   real,   parameter ::  T1S = 0.2731600000000E3
   real,   parameter ::  T2S = 0.2581600000000E3
   real,   parameter ::  TCDK = 0.2731500000000E3
   real,   parameter ::  TGL = 0.2731600000000E3
   real,   parameter ::  TRPL = 0.2731600000000E3
   real,   parameter ::  CAPPA = (RGASD/CPD)
   real,   parameter ::  CVD = (CPD - RGASD)
   real,   parameter :: TTNS1 = 610.78
   real,   parameter :: TTNS3W = 17.269
   real,   parameter :: TTNS3I = 21.875
   real,   parameter :: TTNS4W = 35.86
   real,   parameter :: TTNS4I = 7.66
   real,   parameter :: AERK1W = 610.94
   real,   parameter :: AERK2W = 17.625
   real,   parameter :: AERK3W = 30.11
   real,   parameter :: AERK1I = 611.21
   real,   parameter :: AERK2I = 22.587
   real,   parameter :: AERK3I = -0.71
   real, parameter :: CTE1 = (AERK2W*(TRPL-AERK3W))
   real, parameter :: CTE2 = (AERK2I*(TRPL-AERK3I)-CTE1)
   real, parameter :: CTE3 = 2317
   real, parameter :: CTE4 = 7.24
   real, parameter :: CTE5 = 128.4


   real, parameter :: TDPACK_OFFSET_FIX=0.01
   real, parameter :: AEw1 = 6.1094
   real, parameter :: AEw2 = 17.625
   real, parameter :: AEw3 = 243.05
   real, parameter :: AEi1 = 6.1121
   real, parameter :: AEi2 = 22.587
   real, parameter :: AEi3 = 273.86

contains

function DIFTRPL_(ttt)
   implicit none
   real, intent(in) :: ttt
   real DIFTRPL_
   DIFTRPL_ = ttt-TRPL
end function

function FN1_(ttt)
   implicit none
   real, intent(in) :: ttt
   real FN1_
   FN1_ = ttt-AERK3W+max(0.,sign(AERK3W-AERK3I,-DIFTRPL_(ttt)))
end function

function MASKT(ttt)
   implicit none
   real, intent(in) :: ttt
   real MASKT
   MASKT = max(0.,sign(1.,DIFTRPL_(ttt)))
end function

function FOMULTS(ddd,ttt)
   implicit none
   real, intent(in) :: ttt
   real, intent(in) :: ddd
   real FOMULTS
   FOMULTS=(AERK1W*MASKT(ttt)+(1.-MASKT(ttt))*AERK1I)*ddd
end function

function FOEWF(ttt)
   implicit none
   real, intent(in) :: ttt
   real FOEWF
   FOEWF=min(sign(AERK2W,DIFTRPL_(ttt)),sign(AERK2I,DIFTRPL_(ttt)))*abs(DIFTRPL_(ttt))/FN1_(ttt)
end function

function FOEW(ttt)
   implicit none
   real, intent(in) :: ttt
   real FOEW
   FOEW=FOMULTS(exp(FOEWF(ttt)),ttt)
end function

function FOEWAF(ttt)
   implicit none
   real, intent(in) :: ttt
   real FOEWAF
   FOEWAF=AERK2W*(DIFTRPL_(ttt))/(ttt-AERK3W)
end function

function FOEWA(ttt)
   implicit none
   real, intent(in) :: ttt
   real FOEWA
   FOEWA=AERK1W*exp(FOEWAF(ttt))
end function

function FODLE(ttt)
   implicit none
   real, intent(in) :: ttt
   real FODLE
   FODLE=(CTE1+max(0.,sign(CTE2,-DIFTRPL_(ttt))))/(FN1_(ttt)**2.)
end function

function FOQST(ttt,prs)
   implicit none
   real, intent(in) :: ttt
   real, intent(in) :: prs
   real FOQST
   FOQST=EPS1/(max(1.,prs/FOEW(ttt))-EPS2)
end function

function FOQSTX(prs,ddd)
   implicit none
   real, intent(in) :: prs
   real, intent(in) :: ddd
   real FOQSTX
   FOQSTX=EPS1/(max(1.,prs/ddd)-EPS2)
end function

function FOQSA(ttt,prs)
   implicit none
   real, intent(in) :: ttt
   real, intent(in) :: prs
   real FOQSA
   FOQSA=EPS1/(max(1.,prs/FOEWA(ttt))-EPS2)
end function

function FQSMX(ttt,prs,fff)
   implicit none
   real, intent(in) :: ttt
   real, intent(in) :: prs
   real, intent(in) :: fff
   real FQSMX
   FQSMX=EPS1/(max(1.,prs/FESMX(ttt,fff))-EPS2)
end function

function FQSMXX(fesmx8,prs)
   implicit none
   real, intent(in) :: fesmx8
   real, intent(in) :: prs
   real FQSMXX
   FQSMXX = EPS1/(max(1.,prs/fesmx8)-EPS2)
end function

function FODQS(qst,ttt)
   implicit none
   real, intent(in) :: qst
   real, intent(in) :: ttt
   real FODQS
   FODQS = qst*(1.+DELTA*qst)*FODLE(ttt)
end function

function FOEFQ(qqq,prs)
   implicit none
   real, intent(in) :: qqq
   real, intent(in) :: prs
   real FOEFQ
   FOEFQ=min(prs,(qqq*prs)/(EPS1+EPS2*qqq))
end function

function FOQFE(eee,prs)
   implicit none
   real, intent(in) :: eee
   real, intent(in) :: prs
   real FOQFE
   FOQFE=min(1.,EPS1*eee/(prs-EPS2*eee))
end function

function FOTVT(ttt,qqq)
   implicit none
   real, intent(in) :: ttt
   real, intent(in) :: qqq
   real FOTVT
   FOTVT=ttt*(1.+DELTA*qqq)
end function

function FOTTV(tvi,qqq)
   implicit none
   real, intent(in) :: tvi
   real, intent(in) :: qqq
   real FOTTV
   FOTTV=tvi/(1.+DELTA*qqq)
end function

function FOTVHT(ttt,qqq,qqh)
   implicit none
   real, intent(in) :: ttt
   real, intent(in) :: qqq
   real, intent(in) :: qqh
   real FOTVHT
   FOTVHT=ttt*(1.+DELTA*qqq-qqh)
end function

function FOTTVH(tvi,qqq,qqh)
   implicit none
   real, intent(in) :: tvi
   real, intent(in) :: qqq
   real, intent(in) :: qqh
   real FOTTVH
   FOTTVH=tvi/(1.+DELTA*qqq-qqh)
end function

function FODQA(qst,ttt)
   implicit none
   real, intent(in) :: qst
   real, intent(in) :: ttt
   real FODQA
   FODQA=qst*(1.+DELTA*qst)*FODLA(ttt)
end function

function FDQSMX(qsm,dlemx)
   implicit none
   real, intent(in) :: qsm
   real, intent(in) :: dlemx
   real FDQSMX
   FDQSMX=qsm*(1.+DELTA*qsm)*dlemx
end function

function FOHR(qqq,ttt,prs)
   implicit none
   real, intent(in) :: qqq
   real, intent(in) :: ttt
   real, intent(in) :: prs
   real FOHR
   FOHR=min(prs,FOEFQ(qqq,prs))/FOEW(ttt)
end function

function FOHRX(qqq,prs,ddd)
   implicit none
   real, intent(in) :: qqq
   real, intent(in) :: prs
   real, intent(in) :: ddd
   real FOHRX
   FOHRX=min(prs,FOEFQ(qqq,prs))/ddd
end function

function FOLV(ttt)
   implicit none
   real, intent(in) :: ttt
   real FOLV
   FOLV=CHLC-(CTE3*DIFTRPL_(ttt))
end function

function FOLS(ttt)
   implicit none
   real, intent(in) :: ttt
   real FOLS
   FOLS = CHLC+CHLF+(CPV-(CTE4*ttt+CTE5))*DIFTRPL_(ttt)
end function

function FOPOIT(t00,pr0,pf)
   implicit none
   real, intent(in) :: t00
   real, intent(in) :: pr0
   real, intent(in) :: pf
   real FOPOIT
   FOPOIT = t00*((pr0/pf)**-(CAPPA))
end function

function FOPOIP(t00,tf,pr0)
   implicit none
   real, intent(in) :: t00
   real, intent(in) :: tf
   real, intent(in) :: pr0
   real FOPOIP
   FOPOIP=pr0*exp(-(log(t00/tf)/CAPPA))
end function

function FODLA(ttt)
   implicit none
   real, intent(in) :: ttt
   real FODLA
   FODLA = CTE1/((ttt-AERK3W)**2.)
end function

function FOHRA(qqq,ttt,prs)
   implicit none
   real, intent(in) :: qqq
   real, intent(in) :: ttt
   real, intent(in) :: prs
   real FOHRA
   FOHRA = min(prs,FOEFQ(qqq,prs))/FOEWA(ttt)
end function

function FESIF(ttt)
   implicit none
   real, intent(in) :: ttt
   real FESIF
   FESIF = AERK2I*DIFTRPL_(ttt)/(ttt-AERK3I)
end function

function FESI(ttt)
   implicit none
   real, intent(in) :: ttt
   real FESI
   FESI = AERK1I*exp(FESIF(ttt))
end function

function FDLESI(ttt)
   implicit none
   real, intent(in) :: ttt
   real FDLESI
   FDLESI=AERK2I*(TRPL-AERK3I)/((ttt-AERK3I)**2.)
end function

function FESMX(ttt,fff)
   implicit none
   real, intent(in) :: ttt
   real, intent(in) :: fff
   real FESMX
   FESMX=(1.-fff)*FOEWA(ttt)+fff*FESI(ttt)
end function

function FESMXX(fff,fesi8,foewa8)
   implicit none
   real, intent(in) :: fff
   real, intent(in) :: fesi8
   real, intent(in) :: foewa8
   real FESMXX
   FESMXX=(1.-fff)*foewa8+fff*fesi8
end function

function FDLESMX(ttt,fff,ddff)
   implicit none
   real, intent(in) :: ttt
   real, intent(in) :: fff
   real, intent(in) :: ddff
   real FDLESMX
   FDLESMX=((1.-fff)*FOEWA(ttt)*FODLA(ttt)+fff*FESI(ttt)*FDLESI(ttt)+ddff*(FESI(ttt)-FOEWA(ttt)))/FESMX(ttt,fff)
end function

function FDLESMXX(ttt,fff,ddff,foewa8,fesi8,fesmx8)
   implicit none
   real, intent(in) :: ttt
   real, intent(in) :: fff
   real, intent(in) :: ddff
   real, intent(in) :: foewa8
   real, intent(in) :: fesi8
   real, intent(in) :: fesmx8
   real FDLESMXX
   FDLESMXX=((1.-fff)*foewa8*FODLA(ttt)+fff*fesi8*FDLESI(ttt)+ddff*(fesi8-foewa8))/fesmx8
end function


function shuahr(hu,tt,px,swph)
   implicit none
   real, intent(in) :: hu
   real, intent(in) :: tt
   real, intent(in) :: px
   logical, intent(in) :: swph
   real shuahr
   if (swph) then
      shuahr = FOHR(hu,tt,px)
   else
      shuahr = FOHRA(hu,tt,px)
   endif
end function

function sesahu(es,tt,px,swph)
   implicit none
   real, intent(in) :: es
   real, intent(in) :: tt
   real, intent(in) :: px
   logical, intent(in) :: swph
   real e,td
   real sesahu
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
   real, intent(in) :: es
   real, intent(in) :: tt
   real, intent(in) :: px
   logical, intent(in) :: swph
   real hu
   real sesahr
   hu = sesahu(es,tt,px,swph)
   sesahr = shuahr(hu,tt,px,swph)
end function

function shrahu(hr, tt, px, swph)
   implicit none
   real, intent(in) :: hr
   real, intent(in) :: tt
   real, intent(in) :: px
   logical, intent(in) :: swph
   real hrtt,e
   real shrahu
   hrtt = hr * tt
   if (swph) then
      e = min(px,hr * FOEW(tt))
   else
      e = min(px,hr * FOEWA(tt))
   endif
   shrahu = FOQFE(e,px)
end function

function shuaes(hu, tt, px, swph)
   implicit none
   real, intent(in) :: hu
   real, intent(in) :: tt
   real, intent(in) :: px
   logical, intent(in) :: swph
   real e,cte,td,hutmp
   real shuaes,petit
   petit = 0.0000000001
   hutmp = hu
   e = FOEFQ(max(petit,hu),px)
   cte = alog(e/TTNS1)
   td = (TTNS4W*CTE - TTNS3W*TRPL)/(CTE - TTNS3W)
   if(td .lt. TRPL .and. swph) then
      td = (TTNS4I*CTE - TTNS3I*TRPL)/(CTE - TTNS3I)
   end if
   shuaes = tt-td
end function

function shraes(hr, tt, px, swph)
   implicit none
   real, intent(in) :: hr
   real, intent(in) :: tt
   real, intent(in) :: px
   logical, intent(in) :: swph
   real hu
   real shraes
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
   real,  intent(in) :: tt
   real svp_water_from_tt
   svp_water_from_tt = AEw1 * exp((AEw2 * tt) / (AEw3 + tt))
end function

!
! Calculates the saturation vapour pressure (ice phase) as a function of temperature.
! @param tt  Air temperature (celsius)
! @return  Saturation vapour pressure, SVP (hPa)
!/
function svp_ice_from_tt(tt)
   implicit none
   real,  intent(in) :: tt
   real svp_ice_from_tt
   svp_ice_from_tt = AEi1 * exp((AEi2 * tt) / (AEi3 + tt))
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

   real,  intent(in)   :: tt(ni ,nj)
   real,  intent(out)  :: res(ni ,nj)
   integer, intent(in) :: ni, nj
   real,  intent(in)   :: tpl
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
   real,  intent(in) :: tt
   real rpn_svp_water
   rpn_svp_water = FOEWA(tt) / 100.
end function

!
! Calculates the saturation vapour pressure (ice phase) using RPN TdPack as a function of temperature.
! @param tt  Air temperature (kelvin)
! @return  Saturation vapour pressure, SVP (hPa)
!/
function rpn_svp_ice(tt)
   implicit none
   real,  intent(in)    :: tt
   real rpn_svp_ice
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
   real,    intent(in)  :: tt(ni ,nj)
   real,    intent(out) :: res(ni ,nj)
   integer, intent(in)  :: ni, nj
   real,    intent(in)  :: tpl
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
   real,  intent(in)     :: hr(ni ,nj)
   real,    intent(out)  :: res(ni ,nj)
   real,  intent(in)     :: svp(ni ,nj)
   integer, intent(in)   :: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = max(hr(i,j), 10E-15)
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
   real,    intent(in)    :: hu(ni ,nj)
   real,    intent(out)   :: res(ni ,nj)
   real,    intent(in)    :: px(ni ,nj)
   integer, intent(in)    :: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = max(hu(i,j), 10E-15)
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
   real,  intent(in)    :: qv(ni ,nj)
   real,  intent(out)   :: res(ni ,nj)
   real,  intent(in)    :: px(ni ,nj)
   integer, intent(in)  :: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = max(qv(i,j), 10E-15)
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
   real,  intent(in) :: td
   real vppr_water_td
   vppr_water_td = AEw1 * exp(((AEw2 * td) / (AEw3 + td)))
end function


!
! Calculates the vapour pressure (ice phase) as a function of temperature dew point.
! @param td   Temperature dew point, in celsius
! @return     Vapour pressure, in hPa
!/

function vppr_ice_td(td)
   implicit none
   real,  intent(in) :: td
   real vppr_ice_td
   vppr_ice_td = AEi1 * exp(((AEi2 * td) / (AEi3 + td)))
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
   real,  intent(in)     :: td(ni ,nj)
   real,  intent(out)    :: res(ni ,nj)
   real,  intent(in )    :: tt(ni ,nj)
   integer, intent(in)   :: ni, nj
   real,    intent(in)   :: tpl
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
   real,  intent(in)    :: hu(ni ,nj)
   real,  intent(in)    :: px(ni ,nj)
   real,  intent(out)   :: res(ni ,nj)
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
   real,  intent(in) :: td
   real rpn_vppr_water_from_td
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
   real,  intent(in) :: td
   real rpn_vppr_ice_from_td
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
   real,  intent(in)    :: td(ni ,nj)
   real,  intent(in)    :: tt(ni ,nj)
   real,  intent(out)   :: res(ni ,nj)
   integer, intent(in)  :: ni, nj
   real,    intent(in)  :: tpl
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
   real,  intent(in)  :: tt(ni ,nj)
   real,  intent(in)  :: es(ni ,nj)
   real,  intent(out) :: res(ni ,nj)
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
   real,  intent(in) :: vppr
   real tmpvppr,td_water_from_vppr
   tmpvppr = max(vppr, 10E-15)
   !RPN returns vapour pressure in Pascal and we want output to be HectoPascal.
   !return rpn::libphy::sfoewa(td) / 100.0d0f
   td_water_from_vppr = ((AEw3 * log(tmpvppr/AEw1) ) / ( AEw2 - log(tmpvppr/AEw1)))
end function

!
! Calculates the temperature dew point (Ice Phase) as a function of vapour pressure.
! @param vppr   Vapour pressure (hPa)
! @return 		 Temperature dew point, TD (celsius)
!
function td_ice_from_vppr(vppr)
   implicit none
   real, intent(in) :: vppr
   real tmpvppr,td_ice_from_vppr
   tmpvppr = max(vppr, 10E-15)
   td_ice_from_vppr =  ((AEi3 * log(tmpvppr/AEi1) ) / ( AEi2 - log(tmpvppr/AEi1)))
end function

subroutine td_from_vppr(tt,vppr,ni,nj,tpl,swph,res)
   implicit none
   real,  intent(in)  :: tt(ni ,nj)
   real,  intent(in)  :: vppr(ni ,nj)
   real,  intent(in)  :: tpl
   logical, intent(in):: swph
   real,  intent(out) :: res(ni ,nj)
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
   real,  intent(in)  :: tt(ni ,nj)
   real,  intent(in)  :: hr(ni ,nj)
   real,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real,  intent(out) :: res(ni ,nj)
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
   real,  intent(in)  :: tt(ni ,nj)
   real,  intent(in)  :: hr(ni ,nj)
   real,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = max(shraes(hr(i,j), tt(i,j), px(i,j), swph),0.)
      enddo
   enddo
end subroutine

subroutine rpn_es_from_hu(tt,hu,px,ni,nj,swph,res)
   implicit none
   real,  intent(in)  :: tt(ni ,nj)
   real,  intent(in)  :: hu(ni ,nj)
   real,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = max(shuaes(hu(i,j), tt(i,j), px(i,j), swph),0.)
      enddo
   enddo
end subroutine

subroutine hu_from_qv(qv,ni,nj,res)
   implicit none
   real,  intent(in)  :: qv(ni ,nj)
   real,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   real tmpqv
   do i=1, ni
      do j=1, nj
         tmpqv= max(qv(i,j),10E-15)
         res(i,j) = tmpqv / (tmpqv + 1.)
      enddo
   enddo
end subroutine

subroutine td_from_hr(tt,hr,ni,nj,res)
   implicit none
   real,  intent(in)  :: tt(ni ,nj)
   real,  intent(in)  :: hr(ni ,nj)
   real,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   real,   parameter :: vara = 17.625
   real,   parameter :: varb = 243.04
   real hrtmp,term

   do i=1, ni
      do j=1, nj
         hrtmp = hr(i,j)
         if (hrtmp > 1.) then
            hrtmp = 1.
         endif
         if (hrtmp < 10E-15) then
            hrtmp = 10E-15
         endif
         term = (vara * tt(i,j))/(varb + tt(i,j)) + log(hrtmp)
         res(i,j) = (varb * term) / (vara - term )
      enddo
   enddo
end subroutine


subroutine hr_from_svp_vppr(svp,vppr,ni,nj,res)
   implicit none
   real,  intent(in)  :: svp(ni ,nj)
   real,  intent(in)  :: vppr(ni ,nj)
   real,  intent(out) :: res(ni ,nj)
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
   real,  intent(in)  :: tt(ni ,nj)
   real,  intent(in)  :: es(ni ,nj)
   real,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real,  intent(out) :: res(ni ,nj)
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
   real,  intent(in)  :: tt(ni ,nj)
   real,  intent(in)  :: hu(ni ,nj)
   real,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real,  intent(out) :: res(ni ,nj)
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
   real,  intent(in)  :: vppr(ni ,nj)
   real,  intent(in)  :: px(ni ,nj)
   real,  intent(out) :: res(ni ,nj)
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
   real,  intent(in)  :: tt(ni ,nj)
   real,  intent(in)  :: es(ni ,nj)
   real,  intent(in)  :: px(ni ,nj)
   logical, intent(in):: swph
   real,  intent(out) :: res(ni ,nj)
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
   real,  intent(in)  :: tt(ni ,nj)
   real,  intent(in)  :: svp(ni ,nj)
   real,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   real resultat
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
   real,  intent(in)  :: hu(ni ,nj)
   real,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   real hutmp
   integer i,j
   do i=1, ni
      do j=1, nj
         hutmp = max(hu(i,j),10E-15)
         res(i,j) = (hutmp / (1. - hutmp)) * 1000.
      enddo
   enddo
end subroutine

subroutine qv_from_vppr(vppr,px,ni,nj,res)
   implicit none
   real,  intent(in)  :: vppr(ni ,nj)
   real,  intent(in)  :: px(ni ,nj)
   real,  intent(out) :: res(ni ,nj)
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
   real,  intent(in)  :: tt(ni ,nj)
   real,  intent(in)  :: td(ni ,nj)
   real,  intent(out) :: res(ni ,nj)
   integer, intent(in):: ni, nj
   integer i,j
   do i=1, ni
      do j=1, nj
         res(i,j) = max(tt(i,j) - td(i,j), 0.)
      enddo
   enddo
end subroutine

end module science
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! real,   parameter :: ai =  AI
   ! real,   parameter :: aw =  AW
   ! real,   parameter :: bi =  BI
   ! real,   parameter :: bw =  BW
   ! real,   parameter :: cappa =  CAPPA
   ! real,   parameter :: chlf =  CHLF
   ! real,   parameter :: chlc =  CHLC
   ! real,   parameter :: consol =  CONSOL
   ! real,   parameter :: consol2 =  CONSOL2
   ! real,   parameter :: cpd =  CPD
   ! real,   parameter :: cpv =  CPV
   ! real,   parameter :: cpi =  CPI
   ! real,   parameter :: cpw =  CPW
   ! real,   parameter :: cvd =  CVD
   ! real,   parameter :: delta =  DELTA
   ! real,   parameter :: eps1 =  EPS1
   ! real,   parameter :: eps2 =  EPS2
   ! real,   parameter :: grav =  GRAV
   ! real,   parameter :: karman =  KARMAN
   ! real,   parameter :: knams =  KNAMS
   ! real,   parameter :: omega =  OMEGA
   ! real,   parameter :: pi =  PI
   ! real,   parameter :: rauw =  RAUW
   ! real,   parameter :: rayt =  RAYT
   ! real,   parameter :: rgasd =  RGASD
   ! real,   parameter :: rgasv =  RGASV
   ! real,   parameter :: ric =  RIC
   ! real,   parameter :: slp =  SLP
   ! real,   parameter :: stefan =  STEFAN
   ! real,   parameter :: stlo =  STLO
   ! real,   parameter :: t1s =  T1S
   ! real,   parameter :: t2s =  T2S
   ! real,   parameter :: tcdk =  TCDK
   ! real,   parameter :: tgl =  TGL
   ! real,   parameter :: trpl =  TRPL
   ! real,   parameter :: ai_8 =  AI
   ! real,   parameter :: aw_8 =  AW
   ! real,   parameter :: bi_8 =  BI
   ! real,   parameter :: bw_8 =  BW
   ! real,   parameter :: cappa_8 =  CAPPA
   ! real,   parameter :: chlf_8 =  CHLF
   ! real,   parameter :: chlc_8 =  CHLC
   ! real,   parameter :: consol_8 =  CONSOL
   ! real,   parameter :: consol2_8 =  CONSOL2
   ! real,   parameter :: cpd_8 =  CPD
   ! real,   parameter :: cpv_8 =  CPV
   ! real,   parameter :: cpi_8 =  CPI
   ! real,   parameter :: cpw_8 =  CPW
   ! real,   parameter :: cvd_8 =  CVD
   ! real,   parameter :: delta_8 =  DELTA
   ! real,   parameter :: eps1_8 =  EPS1
   ! real,   parameter :: eps2_8 =  EPS2
   ! real,   parameter :: grav_8 =  GRAV
   ! real,   parameter :: karman_8 =  KARMAN
   ! real,   parameter :: knams_8 =  KNAMS
   ! real,   parameter :: omega_8 =  OMEGA
   ! real,   parameter :: pi_8 =  PI
   ! real,   parameter :: rauw_8 =  RAUW
   ! real,   parameter :: rayt_8 =  RAYT
   ! real,   parameter :: rgasd_8 =  RGASD
   ! real,   parameter :: rgasv_8 =  RGASV
   ! real,   parameter :: ric_8 =  RIC
   ! real,   parameter :: slp_8 =  SLP
   ! real,   parameter :: stefan_8 =  STEFAN
   ! real,   parameter :: stlo_8 =  STLO
   ! real,   parameter :: t1s_8 =  T1S
   ! real,   parameter :: t2s_8 =  T2S
   ! real,   parameter :: tcdk_8 =  TCDK
   ! real,   parameter :: tgl_8 =  TGL
   ! real,   parameter :: trpl_8 =  TRPL
   ! real,   parameter :: ttns1 =  TTNS1
   ! real,   parameter :: ttns3w =  TTNS3W
   ! real,   parameter :: ttns3i =  TTNS3I
   ! real,   parameter :: ttns4w =  TTNS4W
   ! real,   parameter :: ttns4i =  TTNS4I
   ! real,   parameter :: aerk1w =  AERK1W
   ! real,   parameter :: aerk2w =  AERK2W
   ! real,   parameter :: aerk3w =  AERK3W
   ! real,   parameter :: aerk1i =  AERK1I
   ! real,   parameter :: aerk2i =  AERK2I
   ! real,   parameter :: aerk3i =  AERK3I
