module tdpack
implicit none
   real*8,   parameter ::  AI = 0.2864887713087E4
   real*8,   parameter ::  AW = 0.3135012829948E04
   real*8,   parameter ::  BI = 0.1660931315020E0
   real*8,   parameter ::  BW = 0.2367075766316E1
   real*8,   parameter ::  CHLF = 0.3340000000000E6
   real*8,   parameter ::  CHLC = 0.2501000000000E7
   real*8,   parameter ::  CONSOL = 0.1367000000000E4
   real*8,   parameter ::  CONSOL2 = 0.1361000000000E4
   real*8,   parameter ::  CPD = 0.1005460000000E4
   real*8,   parameter ::  CPV = 0.1869460000000E4
   real*8,   parameter ::  CPI = 0.2115300000000E4
   real*8,   parameter ::  CPW = 0.4218000000000E4
   real*8,   parameter ::  DELTA = 0.6077686814144E0
   real*8,   parameter ::  EPS1 = 0.6219800221014E0
   real*8,   parameter ::  EPS2 = 0.3780199778986E0
   real*8,   parameter ::  GRAV = 0.9806160000000E1
   real*8,   parameter ::  KARMAN = 0.4000000000000E0
   real*8,   parameter ::  KNAMS = 0.5147910000000E0
   real*8,   parameter ::  OMEGA = 0.7292000000000E-4
   real*8,   parameter ::  PI = 3.14159265358979323846
   real*8,   parameter ::  RAUW = 0.1000000000000E4
   real*8,   parameter ::  RAYT = 0.6371220000000E7
   real*8,   parameter ::  RGASD = 0.2870500000000E3
   real*8,   parameter ::  RGASV = 0.4615100000000E3
   real*8,   parameter ::  RIC = 0.2000000000000E0
   real*8,   parameter ::  SLP = 0.6666666666667E-1
   real*8,   parameter ::  STEFAN = 0.5669800000000E-7
   real*8,   parameter ::  STLO = 0.6628486583943E-3
   real*8,   parameter ::  T1S = 0.2731600000000E3
   real*8,   parameter ::  T2S = 0.2581600000000E3
   real*8,   parameter ::  TCDK = 0.2731500000000E3
   real*8,   parameter ::  TGL = 0.2731600000000E3
   real*8,   parameter ::  TRPL = 0.2731600000000E3
   real*8,   parameter ::  CAPPA = (RGASD/CPD)
   real*8,   parameter ::  CVD = (CPD - RGASD)
   real*8,   parameter :: TTNS1 = 610.78
   real*8,   parameter :: TTNS3W = 17.269
   real*8,   parameter :: TTNS3I = 21.875
   real*8,   parameter :: TTNS4W = 35.86
   real*8,   parameter :: TTNS4I = 7.66
   real*8,   parameter :: AERK1W = 610.94
   real*8,   parameter :: AERK2W = 17.625
   real*8,   parameter :: AERK3W = 30.11
   real*8,   parameter :: AERK1I = 611.21
   real*8,   parameter :: AERK2I = 22.587
   real*8,   parameter :: AERK3I = -0.71
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
   ! real*8,   parameter :: ai_8 =  AI
   ! real*8,   parameter :: aw_8 =  AW
   ! real*8,   parameter :: bi_8 =  BI
   ! real*8,   parameter :: bw_8 =  BW
   ! real*8,   parameter :: cappa_8 =  CAPPA
   ! real*8,   parameter :: chlf_8 =  CHLF
   ! real*8,   parameter :: chlc_8 =  CHLC
   ! real*8,   parameter :: consol_8 =  CONSOL
   ! real*8,   parameter :: consol2_8 =  CONSOL2
   ! real*8,   parameter :: cpd_8 =  CPD
   ! real*8,   parameter :: cpv_8 =  CPV
   ! real*8,   parameter :: cpi_8 =  CPI
   ! real*8,   parameter :: cpw_8 =  CPW
   ! real*8,   parameter :: cvd_8 =  CVD
   ! real*8,   parameter :: delta_8 =  DELTA
   ! real*8,   parameter :: eps1_8 =  EPS1
   ! real*8,   parameter :: eps2_8 =  EPS2
   ! real*8,   parameter :: grav_8 =  GRAV
   ! real*8,   parameter :: karman_8 =  KARMAN
   ! real*8,   parameter :: knams_8 =  KNAMS
   ! real*8,   parameter :: omega_8 =  OMEGA
   ! real*8,   parameter :: pi_8 =  PI
   ! real*8,   parameter :: rauw_8 =  RAUW
   ! real*8,   parameter :: rayt_8 =  RAYT
   ! real*8,   parameter :: rgasd_8 =  RGASD
   ! real*8,   parameter :: rgasv_8 =  RGASV
   ! real*8,   parameter :: ric_8 =  RIC
   ! real*8,   parameter :: slp_8 =  SLP
   ! real*8,   parameter :: stefan_8 =  STEFAN
   ! real*8,   parameter :: stlo_8 =  STLO
   ! real*8,   parameter :: t1s_8 =  T1S
   ! real*8,   parameter :: t2s_8 =  T2S
   ! real*8,   parameter :: tcdk_8 =  TCDK
   ! real*8,   parameter :: tgl_8 =  TGL
   ! real*8,   parameter :: trpl_8 =  TRPL
   ! real*8,   parameter :: ttns1 =  TTNS1
   ! real*8,   parameter :: ttns3w =  TTNS3W
   ! real*8,   parameter :: ttns3i =  TTNS3I
   ! real*8,   parameter :: ttns4w =  TTNS4W
   ! real*8,   parameter :: ttns4i =  TTNS4I
   ! real*8,   parameter :: aerk1w =  AERK1W
   ! real*8,   parameter :: aerk2w =  AERK2W
   ! real*8,   parameter :: aerk3w =  AERK3W
   ! real*8,   parameter :: aerk1i =  AERK1I
   ! real*8,   parameter :: aerk2i =  AERK2I
   ! real*8,   parameter :: aerk3i =  AERK3I





   REAL*8, parameter :: CAPPA_= CAPPA
   REAL*8, parameter :: CHLC_ = CHLC
   REAL*8, parameter :: CHLF_ = CHLF
   REAL*8, parameter :: CPV_  = CPV
   REAL*8, parameter :: DELTA_= DELTA
   REAL*8, parameter :: EPS1_ = EPS1
   REAL*8, parameter :: EPS2_ = EPS2
   REAL*8, parameter :: TRPL_ = TRPL
   REAL*8, parameter :: CTE1_ = 17.625*(0.2731600000000E3-30.11)
   REAL*8, parameter :: CTE2_ = 22.587*(0.2731600000000E3+0.71)-17.625*(0.2731600000000E3-30.11)
   REAL*8, parameter :: CTE3_ = 2317
   REAL*8, parameter :: CTE4_ = 7.24
   REAL*8, parameter :: CTE5_ = 128.4


   real*8, parameter :: TDPACK_OFFSET_FIX=0.01
   real*8, parameter :: AEw1 = 6.1094
   real*8, parameter :: AEw2 = 17.625
   real*8, parameter :: AEw3 = 243.05
   real*8, parameter :: AEi1 = 6.1121
   real*8, parameter :: AEi2 = 22.587
   real*8, parameter :: AEi3 = 273.86

contains

function DIFTRPL_(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 DIFTRPL_
   DIFTRPL_ = ttt-TRPL_
end function

function FN1_(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FN1_
   FN1_ = ttt-AERK3W+dmax1(0.,dsign(AERK3W-AERK3I,Dble(-DIFTRPL_(ttt))))
end function

function MASKT(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 MASKT
   MASKT = dmax1(0.,dsign(1d0,Dble(DIFTRPL_(ttt))))
end function

function FOMULTS(ddd,ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8, intent(in) :: ddd
   REAL*8 FOMULTS
   FOMULTS=(AERK1W*MASKT(ttt)+(1.-MASKT(ttt))*AERK1I)*ddd
end function

function FOEWF(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FOEWF
   FOEWF=dmin1(dsign(AERK2W,Dble(DIFTRPL_(ttt))),dsign(AERK2I,Dble(DIFTRPL_(ttt))))*dabs(Dble(DIFTRPL_(ttt)))/FN1_(ttt)
end function

function FOEW(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FOEW
   FOEW=FOMULTS(dexp(Dble(FOEWF(ttt))),ttt)
end function

function FOEWAF(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FOEWAF
   FOEWAF=AERK2W*(DIFTRPL_(ttt))/(ttt-AERK3W)
end function

function FOEWA(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FOEWA
   FOEWA=AERK1W*dexp(Dble(FOEWAF(ttt)))
end function

function FODLE(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FODLE
   FODLE=(CTE1_+dmax1(0.,dsign(CTE2_,Dble(-DIFTRPL_(ttt)))))/(FN1_(ttt)**2.)
end function

function FOQST(ttt,prs)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8, intent(in) :: prs
   REAL*8 FOQST
   FOQST=EPS1_/(dmax1(1.,prs/FOEW(ttt))-EPS2_)
end function

function FOQSTX(prs,ddd)
   implicit none
   REAL*8, intent(in) :: prs
   REAL*8, intent(in) :: ddd
   REAL*8 FOQSTX
   FOQSTX=EPS1_/(dmax1(1.,prs/ddd)-EPS2_)
end function

function FOQSA(ttt,prs)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8, intent(in) :: prs
   REAL*8 FOQSA
   FOQSA=EPS1_/(dmax1(1.,prs/FOEWA(ttt))-EPS2_)
end function

function FQSMX(ttt,prs,fff)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8, intent(in) :: prs
   REAL*8, intent(in) :: fff
   REAL*8 FQSMX
   FQSMX=EPS1_/(dmax1(1.,prs/FESMX(ttt,fff))-EPS2_)
end function

function FQSMXX(fesmx8,prs)
   implicit none
   REAL*8, intent(in) :: fesmx8
   REAL*8, intent(in) :: prs
   REAL*8 FQSMXX
   FQSMXX = EPS1_/(dmax1(1.,prs/fesmx8)-EPS2_)
end function

function FODQS(qst,ttt)
   implicit none
   REAL*8, intent(in) :: qst
   REAL*8, intent(in) :: ttt
   REAL*8 FODQS
   FODQS = qst*(1.+DELTA_*Dble(qst))*FODLE(ttt)
end function

function FOEFQ(qqq,prs)
   implicit none
   REAL*8, intent(in) :: qqq
   REAL*8, intent(in) :: prs
   REAL*8 FOEFQ
   FOEFQ=dmin1(prs,(Dble(qqq)*Dble(prs))/(EPS1_+EPS2_*Dble(qqq)))
end function

function FOQFE(eee,prs)
   implicit none
   REAL*8, intent(in) :: eee
   REAL*8, intent(in) :: prs
   REAL*8 FOQFE
   FOQFE=dmin1(1.,EPS1_*eee/(Dble(prs)-EPS2_*Dble(eee)))
end function

function FOTVT(ttt,qqq)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8, intent(in) :: qqq
   REAL*8 FOTVT
   FOTVT=ttt*(1.+DELTA_*Dble(qqq))
end function

function FOTTV(tvi,qqq)
   implicit none
   REAL*8, intent(in) :: tvi
   REAL*8, intent(in) :: qqq
   REAL*8 FOTTV
   FOTTV=tvi/(1.+DELTA_*Dble(qqq))
end function

function FOTVHT(ttt,qqq,qqh)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8, intent(in) :: qqq
   REAL*8, intent(in) :: qqh
   REAL*8 FOTVHT
   FOTVHT=ttt*(1.+DELTA_*Dble(qqq)-Dble(qqh))
end function

function FOTTVH(tvi,qqq,qqh)
   implicit none
   REAL*8, intent(in) :: tvi
   REAL*8, intent(in) :: qqq
   REAL*8, intent(in) :: qqh
   REAL*8 FOTTVH
   FOTTVH=tvi/(1.+DELTA_*Dble(qqq)-Dble(qqh))
end function

function FODQA(qst,ttt)
   implicit none
   REAL*8, intent(in) :: qst
   REAL*8, intent(in) :: ttt
   REAL*8 FODQA
   FODQA=qst*(1.+DELTA_*Dble(qst))*FODLA(ttt)
end function

function FDQSMX(qsm,dlemx)
   implicit none
   REAL*8, intent(in) :: qsm
   REAL*8, intent(in) :: dlemx
   REAL*8 FDQSMX
   FDQSMX=qsm*(1.+DELTA_*Dble(qsm))*Dble(dlemx)
end function

function FOHR(qqq,ttt,prs)
   implicit none
   REAL*8, intent(in) :: qqq
   REAL*8, intent(in) :: ttt
   REAL*8, intent(in) :: prs
   REAL*8 FOHR
   FOHR=dmin1(prs,FOEFQ(qqq,prs))/FOEW(ttt)
end function

function FOHRX(qqq,prs,ddd)
   implicit none
   REAL*8, intent(in) :: qqq
   REAL*8, intent(in) :: prs
   REAL*8, intent(in) :: ddd
   REAL*8 FOHRX
   FOHRX=dmin1(prs,FOEFQ(qqq,prs))/ddd
end function

function FOLV(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FOLV
   FOLV=CHLC_-(CTE3_*DIFTRPL_(ttt))
end function

function FOLS(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FOLS
   FOLS = CHLC_+CHLF_+(CPV_-(CTE4_*ttt+CTE5_))*DIFTRPL_(ttt)
end function

function FOPOIT(t00,pr0,pf)
   implicit none
   REAL*8, intent(in) :: t00
   REAL*8, intent(in) :: pr0
   REAL*8, intent(in) :: pf
   REAL*8 FOPOIT
   FOPOIT = t00*((Dble(pr0)/Dble(pf))**-(CAPPA_))
end function

function FOPOIP(t00,tf,pr0)
   implicit none
   REAL*8, intent(in) :: t00
   REAL*8, intent(in) :: tf
   REAL*8, intent(in) :: pr0
   REAL*8 FOPOIP
   FOPOIP=pr0*dexp(-(dlog(Dble(t00)/Dble(tf))/CAPPA_))
end function

function FODLA(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FODLA
   FODLA = CTE1_/((ttt-AERK3W)**2.)
end function

function FOHRA(qqq,ttt,prs)
   implicit none
   REAL*8, intent(in) :: qqq
   REAL*8, intent(in) :: ttt
   REAL*8, intent(in) :: prs
   REAL*8 FOHRA
   FOHRA = dmin1(prs,FOEFQ(qqq,prs))/FOEWA(ttt)
end function

function FESIF(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FESIF
   FESIF = AERK2I*DIFTRPL_(ttt)/(ttt-AERK3I)
end function

function FESI(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FESI
   FESI = AERK1I*dexp(Dble(FESIF(ttt)))
end function

function FDLESI(ttt)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8 FDLESI
   FDLESI=AERK2I*(TRPL_-AERK3I)/((ttt-AERK3I)**2.)
end function

function FESMX(ttt,fff)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8, intent(in) :: fff
   REAL*8 FESMX
   FESMX=(1.-fff)*FOEWA(ttt)+Dble(fff)*FESI(ttt)
end function

function FESMXX(fff,fesi8,foewa8)
   implicit none
   REAL*8, intent(in) :: fff
   REAL*8, intent(in) :: fesi8
   REAL*8, intent(in) :: foewa8
   REAL*8 FESMXX
   FESMXX=(1.-fff)*foewa8+Dble(fff)*fesi8
end function

function FDLESMX(ttt,fff,ddff)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8, intent(in) :: fff
   REAL*8, intent(in) :: ddff
   REAL*8 FDLESMX
   FDLESMX=((1.-fff)*FOEWA(ttt)*FODLA(ttt)+Dble(fff)*FESI(ttt)*FDLESI(ttt)+Dble(ddff)*(FESI(ttt)-FOEWA(ttt)))/FESMX(ttt,fff)
end function

function FDLESMXX(ttt,fff,ddff,foewa8,fesi8,fesmx8)
   implicit none
   REAL*8, intent(in) :: ttt
   REAL*8, intent(in) :: fff
   REAL*8, intent(in) :: ddff
   REAL*8, intent(in) :: foewa8
   REAL*8, intent(in) :: fesi8
   REAL*8, intent(in) :: fesmx8
   REAL*8 FDLESMXX
   FDLESMXX=((1.-fff)*foewa8*FODLA(ttt)+Dble(fff)*fesi8*FDLESI(ttt)+Dble(ddff)*(fesi8-foewa8))/fesmx8
end function


function shuahr(hu,tt,px,swph)
   implicit none
   REAL*8, intent(in) :: hu
   REAL*8, intent(in) :: tt
   REAL*8, intent(in) :: px
   logical, intent(in) :: swph
   REAL*8 shuahr
   if (swph) then
      shuahr = FOHR(hu,tt,px)
   else
      shuahr = FOHRA(hu,tt,px)
   endif
end function

function sesahu(es,tt,px,swph)
   implicit none
   REAL*8, intent(in) :: es
   REAL*8, intent(in) :: tt
   REAL*8, intent(in) :: px
   logical, intent(in) :: swph
   REAL*8 e,td
   REAL*8 sesahu
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
   REAL*8, intent(in) :: es
   REAL*8, intent(in) :: tt
   REAL*8, intent(in) :: px
   logical, intent(in) :: swph
   REAL*8 hu
   REAL*8 sesahr
   hu = sesahu(es,tt,px,swph)
   sesahr = shuahr(hu,tt,px,swph)
end function

function shrahu(hr, tt, px, swph)
   implicit none
   REAL*8, intent(in) :: hr
   REAL*8, intent(in) :: tt
   REAL*8, intent(in) :: px
   logical, intent(in) :: swph
   REAL*8 hrtt,e
   REAL*8 shrahu
   hrtt = hr * tt
   if (swph) then
      if (px < hrtt) then
         e = px
      else
         e = hrtt
      endif
   else
      if (px < hrtt) then
         e = px
      else
         e = hrtt
      endif

   endif
   shrahu = FOEFQ(e,px)
end function

function shuaes(hu, tt, px, swph)
   implicit none
   REAL*8, intent(in) :: hu
   REAL*8, intent(in) :: tt
   REAL*8, intent(in) :: px
   logical, intent(in) :: swph
   REAL*8 e,cte,td,hutmp
   REAL*8 shuaes
   hutmp = hu
   if (hu <= 0.0000000001) then
      hutmp = 0.0000000001
   end if
   e = FOEFQ(hutmp,px)
   cte = dlog(e/TTNS1)
   td = (cte*TTNS4W - TTNS3W*TRPL)/(cte - TTNS3W)
   if (swph) then
      if (td < TRPL) then
         td = (TTNS4I*cte - TTNS3I*TRPL)/(cte - TTNS3I)
      endif
   endif
   shuaes = tt-td
end function

function shraes(hr, tt, px, swph)
   implicit none
   REAL*8, intent(in) :: hr
   REAL*8, intent(in) :: tt
   REAL*8, intent(in) :: px
   logical, intent(in) :: swph
   REAL*8 hu
   REAL*8 shraes
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
   REAL svp_water_from_tt
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
   REAL svp_ice_from_tt
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
   rpn_svp_water = FOEWA(Dble(tt)) / 100.
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
   rpn_svp_ice = FOEW(Dble(tt)) / 100.
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
   vppr_water_td = AEw1 * exp((AEw2 * td) / (AEw3 + td))
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
   vppr_ice_td =( AEi1 * exp((AEi2 * td)) / (AEi3 + td))
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
            res(i,j) = FOEFQ(Dble(hu(i,j)), Dble(px(i,j))) / 100.
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
   rpn_vppr_water_from_td = FOEWA(Dble(td)) / 100.
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
   rpn_vppr_ice_from_td = FOEW(Dble(td)) / 100.
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
   td_water_from_vppr = (AEw3 * log(tmpvppr/AEw1) ) / ( AEw2 - log(tmpvppr/AEw1))
end function

!
! Calculates the temperature dew point (Ice Phase) as a function of vapour pressure.
! @param vppr   Vapour pressure (hPa)
! @return 		 Temperature dew point, TD (celsius)
!
function td_ice_from_vppr(vppr)
   implicit none
   REAL, intent(in) :: vppr
   REAL tmpvppr,td_ice_from_vppr
   tmpvppr = max(vppr, 10E-15)
   td_ice_from_vppr =  (AEi3 * log(tmpvppr/AEi1) ) / ( AEi2 - log(tmpvppr/AEi1))
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
         res(i,j) = shrahu(Dble(hr(i,j)), Dble(tt(i,j)), Dble(px(i,j)), swph)
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
         res(i,j) = max(shraes(Dble(hr(i,j)), Dble(tt(i,j)), Dble(px(i,j)), swph),0.)
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
         res(i,j) = max(shuaes(Dble(hu(i,j)), Dble(tt(i,j)), Dble(px(i,j)), swph),0.)
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



end module tdpack
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
