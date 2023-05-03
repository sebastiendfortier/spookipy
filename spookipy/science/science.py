# -*- coding: utf-8 -*-
import numpy as np

"""scientific functions"""

TDPACK_OFFSET_FIX = 0.01
EPS1 = 0.6219800221014E0
EPS2 = 0.3780199778986E0
TRPL = 0.2731600000000E3
AERK1W = 610.94
AERK2W = 17.625
AERK3W = 30.11
AERK1I = 611.21
AERK2I = 22.587
AERK3I = -0.71
AEw1 = 6.1094
AEw2 = 17.625
AEw3 = 243.05
AEi1 = 6.1121
AEi2 = 22.587
AEi3 = 273.86
TCDK = 273.15   # conversion Celsius a kelvin


def sign(a, b):
    return np.where(b < 0, -1 * np.abs(a), np.abs(a))


def DIFTRPL(ttt):
    return (ttt - TRPL)

def convert_celsius_to_kelvin(ttt):
    return (ttt - TCDK)

# #define _FN1(ttt)              (_DBLE(ttt)-AERK3W+_DMAX1(_ZERO,_DSIGN(AERK3W-AERK3I,-_DIFTRPL(ttt))))


def FN1(ttt):
    tmp = sign(AERK3W - AERK3I, -DIFTRPL(ttt))
    return (ttt - AERK3W + np.where(0. > tmp, 0., tmp))

# #define MASKT(ttt)             _DMAX1(_ZERO,_DSIGN(_ONE,_DIFTRPL(ttt)))


def MASKT(ttt):
    tmp = sign(1., DIFTRPL(ttt))
    return np.where(0. > tmp, 0., tmp)


# #define FOMULTS(ddd,ttt)       ((AERK1W*MASKT(ttt)+(_ONE-MASKT(ttt))*AERK1I)*ddd)
def FOMULTS(ddd, ttt):
    return ((AERK1W * MASKT(ttt) + (1. - MASKT(ttt)) * AERK1I) * ddd)

# #define FOEWF(ttt)             (_DMIN1(_DSIGN(AERK2W,_DIFTRPL(ttt)),_DSIGN(AERK2I,_DIFTRPL(ttt)))*_DABS(_DIFTRPL(ttt))/_FN1(ttt))


def FOEWF(ttt):
    tmp1 = sign(AERK2W, DIFTRPL(ttt))
    tmp2 = sign(AERK2I, DIFTRPL(ttt))
    return np.where(tmp1 < tmp2, tmp1, tmp2) * np.abs(DIFTRPL(ttt)) / FN1(ttt)

# #define FOEW(ttt)              (FOMULTS(_DEXP(FOEWF(ttt)),ttt))


def FOEW(ttt):
    return FOMULTS(np.exp(FOEWF(ttt)), ttt)


# #define FOEWAF(ttt)            (AERK2W*(_DIFTRPL(ttt))/(_DBLE(ttt)-AERK3W))
def FOEWAF(ttt):
    return (AERK2W * (DIFTRPL(ttt)) / (ttt - AERK3W))

# #define FOEWA(ttt)             (AERK1W*_DEXP(FOEWAF(ttt)))


def FOEWA(ttt):
    return (AERK1W * np.exp(FOEWAF(ttt)))


# #define FOQFE(eee,prs)         (_DMIN1(_ONE,_EPS1*_DBLE(eee)/(_DBLE(prs)-_EPS2*_DBLE(eee))))
def FOQFE(eee, prs):
    tmp = EPS1 * eee / (prs - EPS2 * eee)
    return np.where(1.0 < tmp, 1.0, tmp)


# #define FOEFQ(qqq,prs)         (_DMIN1(_DBLE(prs),(_DBLE(qqq)*_DBLE(prs))/(_EPS1+_EPS2*_DBLE(qqq))))
def FOEFQ(qqq, prs):
    tmp = (qqq * prs) / (EPS1 + EPS2 * qqq)
    return np.where(prs < tmp, prs, tmp)


# #define FOHR(qqq,ttt,prs)      (_DMIN1(_DBLE(prs),FOEFQ(qqq,prs))/FOEW(ttt))
def FOHR(qqq, ttt, prs):
    tmp = FOEFQ(qqq, prs)
    return (np.where(prs < tmp, prs, tmp) / FOEW(ttt))


# #define FOHRA(qqq,ttt,prs)     (_DMIN1(_DBLE(prs),FOEFQ(qqq,prs))/FOEWA(ttt))
def FOHRA(qqq, ttt, prs):
    tmp = FOEFQ(qqq, prs)
    return (np.where(prs < tmp, prs, tmp) / FOEWA(ttt))


def shuahr(hu:np.ndarray, tt:np.ndarray, px:np.ndarray, swph:bool) -> np.ndarray:
    """Converts HU to HR

    :param hu: humidity specific
    :type hu: np.ndarray
    :param tt: air temperature
    :type tt: np.ndarray
    :param px: pressure
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: humidity relative
    :rtype: np.ndarray
    """
    if (swph):
        return FOHR(hu, tt, px)
    else:
        return FOHRA(hu, tt, px)


def sesahu(es:np.ndarray, tt:np.ndarray, px:np.ndarray, swph:bool) -> np.ndarray:
    """Converts ES to HU

    :param es: dew point depression
    :type es: np.ndarray
    :param tt: air temperature
    :type tt: np.ndarray
    :param px: pressure
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: humidity specific
    :rtype: np.ndarray
    """
    td = tt - es
    if (swph):
        e = FOEW(td)
    else:
        e = FOEWA(td)
    return FOQFE(e, px)


def sesahr(es:np.ndarray, tt:np.ndarray, px:np.ndarray, swph:bool) -> np.ndarray:
    """Converts ES to HR

    :param es: dew point depression
    :type es: np.ndarray
    :param tt: air temperature
    :type tt: np.ndarray
    :param px: pressure
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: humidity relative
    :rtype: np.ndarray
    """
    hu = sesahu(es, tt, px, swph)
    return shuahr(hu, tt, px, swph)


def shrahu(hr:np.ndarray, tt:np.ndarray, px:np.ndarray, swph:bool) -> np.ndarray:
    """Converts HR to HU

    :param hr: humidity relative
    :type hr: np.ndarray
    :param tt: air temperature
    :type tt: np.ndarray
    :param px: pressure
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: humidity specific
    :rtype: np.ndarray
    """
    if (swph):
        tmp = hr * FOEW(tt)
        # e = np.min(px,hr * FOEW(tt))
        e = np.where(px < tmp, px, tmp)
    else:
        tmp = hr * FOEWA(tt)
        # e = np.min(px,hr * FOEWA(tt))
        e = np.where(px < tmp, px, tmp)
    return FOQFE(e, px)


def shuaes(hu:np.ndarray, tt:np.ndarray, px:np.ndarray, swph:bool) -> np.ndarray:
    """Converts HU to ES

    :param hu: humidity specific
    :type hu: np.ndarray
    :param tt: air temperature
    :type tt: np.ndarray
    :param px: pressure
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: dew point depression
    :rtype: np.ndarray
    """
    petit = 0.0000000001
    alpha = np.log(AERK1W / AERK1I)
    e = FOEFQ(np.where(petit > hu, petit, hu), px)
    cte = np.log(e / AERK1W)
    td = (AERK3W * cte - AERK2W * TRPL) / (cte - AERK2W)
    if swph:
        td = np.where(td < TRPL, ((AERK3I * (cte + alpha) - AERK2I * TRPL)) / (cte + alpha - AERK2I), td)
    return (tt - td)


def shraes(hr:np.ndarray, tt:np.ndarray, px:np.ndarray, swph:bool) -> np.ndarray:
    """Converts HR to ES

    :param hr: humidity relative
    :type hr: np.ndarray
    :param tt: air temperature
    :type tt: np.ndarray
    :param px: pressure
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: dew point depression
    :rtype: np.ndarray
    """
    hu = shrahu(hr, tt, px, swph)
    return shuaes(hu, tt, px, swph)


#
# Calculates the saturation vapour pressure (Water phase) as a def of temperature.:
# @param tt  Air temperature (celsius)
# @return  Saturation vapour pressure, SVP (hPa)
#
def svp_water_from_tt(tt:np.ndarray) -> np.ndarray:
    """Calculates the saturation vapour pressure (Water phase) as a def of temperature.

    :param tt: air temperature (celsius)
    :type tt: np.ndarray
    :return: saturation vapour pressure (hPa)
    :rtype: np.ndarray
    """
    return AEw1 * np.exp((AEw2 * tt) / (AEw3 + tt))


#
# Calculates the saturation vapour pressure (ice phase) as a def of temperature.:
# @param tt  Air temperature (celsius)
# @return  Saturation vapour pressure, SVP (hPa)
# /
def svp_ice_from_tt(tt:np.ndarray) -> np.ndarray:
    """Calculates the saturation vapour pressure (ice phase) as a def of temperature

    :param tt: air temperature (celsius)
    :type tt: np.ndarray
    :return: saturation vapour pressure (hPa)
    :rtype: np.ndarray
    """
    return AEi1 * np.exp((AEi2 * tt) / (AEi3 + tt))


#
# Calculates the saturation vapour pressure as a def of temperature.:
# @param tt     Air temperature (celsius)
# @param tpl    temperature at which to change from the ice phase to the water phase (celsius).
# @param swph   A boolean representing if we consider both ice and water phase.
# @return  Saturation vapour pressure, SVP (hPa)
# /
def svp_from_tt(tt:np.ndarray, tpl:float, swph:bool) -> np.ndarray:
    """Calculates the saturation vapour pressure as a def of temperature

    :param tt: air temperature (celsius)
    :type tt: np.ndarray
    :param tpl: temperature at which to change from the ice phase to the water phase (celsius)
    :type tpl: float
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: saturation vapour pressure (hPa)
    :rtype: np.ndarray
    """
    return np.where(
        not swph or (
            swph and tt > tpl),
        svp_water_from_tt(tt),
        svp_ice_from_tt(tt))


#
# Calculates the saturation vapour pressure (water phase) using RPN TdPack as a def of temperature.:
# @param tt  Air temperature (kelvin)
# @return  Saturation vapour pressure, SVP (hPa)
#
def rpn_svp_water(tt:float) -> float:
    """Calculates the saturation vapour pressure (water phase) using RPN TdPack as a def of temperature

    :param tt: air temperature (kelvin)
    :type tt: float
    :return: saturation vapour pressure (hPa)
    :rtype: float
    """
    return FOEWA(tt) / 100.


#
# Calculates the saturation vapour pressure (ice phase) using RPN TdPack as a def of temperature.:
# @param tt  Air temperature (kelvin)
# @return  Saturation vapour pressure, SVP (hPa)
# /
def rpn_svp_ice(tt:float) -> float:
    """Calculates the saturation vapour pressure (ice phase) using RPN TdPack as a def of temperature

    :param tt: air temperature (kelvin)
    :type tt: float
    :return: saturation vapour pressure (hPa)
    :rtype: float
    """
    # RPN returns Saturation vapour pressure in Pascal and we want output to be HectoPascal.
    # return rpn::libphy::sfoew(tt) / 100.0f
    return FOEW(tt) / 100.


#
# Calculates the saturation vapour pressure using RPN TdPack as a def of temperature.:
# @param tt     Air temperature (kelvin)
# @param tpl    temperature at which to change from the ice phase to the water phase (kelvin).
# @param swph   A boolean representing if we consider both ice and water phase.
# @return  Saturation vapour pressure, SVP (hPa)
# /
def rpn_svp_from_tt(tt:np.ndarray, tpl:float, swph:bool) -> np.ndarray:
    """Calculates the saturation vapour pressure using RPN TdPack as a def of temperature

    :param tt: air temperature (kelvin)
    :type tt: np.ndarray
    :param tpl: temperature at which to change from the ice phase to the water phase (kelvin)
    :type tpl: float
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: saturation vapour pressure (hPa)
    :rtype: np.ndarray
    """
    return np.where(
        not swph or (
            swph and tt > tpl),
        rpn_svp_water(tt),
        rpn_svp_ice(tt))


#
# Calculates the vapour pressure as a def of relative humidity and saturation vapour pressure.:
# @param hr   Relative humidity, in decimal (between 0 and 1)
# @param svp  saturation vapour pressure, in hPa
# @return     Vapour pressure, in hPa
# /
def vppr_from_hr(hr:np.ndarray, svp:np.ndarray) -> np.ndarray:
    """Calculates the vapour pressure as a def of relative humidity and saturation vapour pressure

    :param hr: relative humidity
    :type hr: np.ndarray
    :param svp: saturation vapour pressure (hPa)
    :type svp: np.ndarray
    :return: vapour pressure (hPa)
    :rtype: np.ndarray
    """
    res = np.where(hr > 10E-15, hr, 10E-15)  # np.max(hr, 10E-15)
    return res * svp


#
# Calculates the vapour pressure as a def of specific humidity and pressure.:
# @param hu   Specific humidity, in kg/kg
# @param px   Pressure, in hPa
# @return     Vapour pressure, in hPa
# /
def vppr_from_hu(hu:np.ndarray, px:np.ndarray) -> np.ndarray:
    """Calculates the vapour pressure as a def of specific humidity and pressure

    :param hu: specific humidity (kg/kg)
    :type hu: np.ndarray
    :param px: pressure (hPa)
    :type px: np.ndarray
    :return: vapour pressure (hPa)
    :rtype: np.ndarray
    """
    res = np.where(hu > 10E-15, hu, 10E-15)  # np.max(hu, 10E-15)
    return (res * px) / (EPS1 + res * (1. - EPS1))


#
# Calculates the vapour pressure as a def of mixing ratio and pressure.:
# @param qv   Mixing ratio, in kg/kg
# @param px   Pressure, in hPa
# @return     Vapour pressure, in hPa
# /
def vppr_from_qv(qv:np.ndarray, px:np.ndarray) -> np.ndarray:
    """Calculates the vapour pressure as a def of mixing ratio and pressure

    :param qv: water vapour mixing ratio (kg/kg)
    :type qv: np.ndarray
    :param px: pressure (hPa)
    :type px: np.ndarray
    :return: vapour pressure (hPa)
    :rtype: np.ndarray
    """
    res = np.where(qv > 10E-15, qv, 10E-15)  # np.max(qv, 10E-15)
    return (res * px) / (EPS1 + res)

#
# Calculates the vapour pressure (water phase) as a def of temperature dew point.:
# @param td   temperature dew point, in celsius
# @return     Vapour pressure, in hPa
# /


def vppr_water_td(td:np.ndarray) -> np.ndarray:
    """Calculates the vapour pressure (water phase) as a def of temperature dew point

    :param td: temperature dew point (celsius)
    :type td: np.ndarray
    :return: vapour pressure (hPa)
    :rtype: np.ndarray
    """
    return AEw1 * np.exp(((AEw2 * td) / (AEw3 + td)))


#
# Calculates the vapour pressure (ice phase) as a def of temperature dew point.:
# @param td   temperature dew point, in celsius
# @return     Vapour pressure, in hPa
# /

def vppr_ice_td(td:np.ndarray) -> np.ndarray:
    """Calculates the vapour pressure (ice phase) as a def of temperature dew point

    :param td: temperature dew point (celsius)
    :type td: np.ndarray
    :return: vapour pressure (hPa)
    :rtype: np.ndarray
    """
    return AEi1 * np.exp(((AEi2 * td) / (AEi3 + td)))


#
# Calculates the vapour pressure as a def of temperature dew point.:
# @param td     temperature dew point, in celsius
# @param tt     Air temperature (celsius)
# @param tpl    temperature at which to change from the ice phase to the water phase (celsius).
# @param swph   A boolean representing if we consider both ice and water phase.
# @return     Vapour pressure, in hPa
# /
def vppr_from_td(td:np.ndarray, tt:np.ndarray, tpl:float, swph:bool) -> np.ndarray:
    """Calculates the vapour pressure as a def of temperature dew point

    :param td: temperature dew point (celsius)
    :type td: np.ndarray
    :param tt: air temperature (celsius)
    :type tt: np.ndarray
    :param tpl: temperature at which to change from the ice phase to the water phase (celsius)
    :type tpl: float
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: vapour pressure (hPa)
    :rtype: np.ndarray
    """
    return np.where(
        not swph or (
            swph and tt > tpl),
        vppr_water_td(td),
        vppr_ice_td(td))


#
# Calculates the vapour pressure using RPN TdPack as a def of specific humidity and pressure.:
# @param hu   Specific humidity, in kg/kg
# @param px   Pressure, in Pa
# @return     Vapour pressure, in hPa
# /
def rpn_vppr_from_hu(hu:float, px:float) -> float:
    """Calculates the vapour pressure using RPN TdPack as a def of specific humidity and pressure

    :param hu: specific humidity (kg/kg)
    :type hu: float
    :param px: pressure (Pa)
    :type px: float
    :return: vapour pressure (hPa)
    :rtype: float
    """
    return FOEFQ(hu, px) / 100.


#
# Calculates the vapour pressure (water phase) as a def of temperature dew point.:
# @param td   temperature dew point, in kelvin
# @return     Vapour pressure, in hPa
#
def rpn_vppr_water_from_td(td:float) -> float:
    """Calculates the vapour pressure (water phase) using RPN TdPack as a def of temperature dew point

    :param td: temperature dew point (kelvin)
    :type td: float
    :return: vapour pressure (hPa)
    :rtype: float
    """
    # RPN returns vapour pressure in Pascal and we want output to be HectoPascal.
    # return rpn::libphy::sfoewa(td) / 100.0d0f
    return FOEWA(td) / 100.


#
# Calculates the vapour pressure (ice phase) as a def of temperature dew point.:
# @param td   temperature dew point, in kelvin
# @return     Vapour pressure, in hPa
#
def rpn_vppr_ice_from_td(td:float) -> float:
    """Calculates the vapour pressure (ice phase) using RPN TdPack as a def of temperature dew point

    :param td: temperature dew point (kelvin)
    :type td: float
    :return: vapour pressure (hPa)
    :rtype: float
    """
    # RPN returns vapour pressure in Pascal and we want output to be HectoPascal.
    # return rpn::libphy::sfoew(td) / 100.0d0f
    return FOEW(td) / 100.


#
# Calculates the vapour pressure as a def of temperature dew point.:
# @param td   temperature dew point, in kelvin
# @param tt     Air temperature (kelvin)
# @param tpl    temperature at which to change from the ice phase to the water phase (kelvin).
# @param swph   A boolean representing if we consider both ice and water phase.
# @return     Vapour pressure, in hPa
# /
def rpn_vppr_from_td(td:np.ndarray, tt:np.ndarray, tpl:float, swph:bool) -> np.ndarray:
    """Calculates the vapour pressure using RPN TdPack as a def of temperature dew point

    :param td: temperature dew point (kelvin)
    :type td: np.ndarray
    :param tt: air temperature (kelvin)
    :type tt: np.ndarray
    :param tpl: temperature at which to change from the ice phase to the water phase (kelvin)
    :type tpl: float
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: vapour pressure (hPa)
    :rtype: np.ndarray
    """
    return np.where(
        not swph or (
            swph and tt > tpl),
        rpn_vppr_water_from_td(td),
        rpn_vppr_ice_from_td(td))


def td_from_es(tt:np.ndarray, es:np.ndarray) -> np.ndarray:
    """Calculates the temperature dew point from the dew point depression

    :param tt: air temperature (celsius)
    :type tt: np.ndarray
    :param es: dew point depression (celsius)
    :type es: np.ndarray
    :return: temperature dew point (celsius)
    :rtype: np.ndarray
    """
    return np.where(es < 0., tt, tt - es)


#
# Calculates the temperature dew point (Water Phase) as a def of vapour pressure.:
# @param vppr   Vapour pressure (hPa)
# @return 		 temperature dew point, TD (celsius)
#
def td_water_from_vppr(vppr:np.ndarray) -> np.ndarray:
    """Calculates the temperature dew point (Water Phase) as a def of vapour pressure

    :param vppr: vapour pressure (hPa)
    :type vppr: np.ndarray
    :return: temperature dew point (celsius)
    :rtype: np.ndarray
    """
    tmpvppr = np.where(vppr > 10E-15, vppr, 10E-15)  # np.max(vppr, 10E-15)
    # RPN returns vapour pressure in Pascal and we want output to be HectoPascal.
    # return rpn::libphy::sfoewa(td) / 100.0d0f
    return ((AEw3 * np.log(tmpvppr / AEw1)) / (AEw2 - np.log(tmpvppr / AEw1)))


#
# Calculates the temperature dew point (Ice Phase) as a def of vapour pressure.:
# @param vppr   Vapour pressure (hPa)
# @return 		 temperature dew point, TD (celsius)
#
def td_ice_from_vppr(vppr:np.ndarray) -> np.ndarray:
    """Calculates the temperature dew point (Ice Phase) as a def of vapour pressure

    :param vppr: vapour pressure (hPa)
    :type vppr: np.ndarray
    :return: temperature dew point (celsius)
    :rtype: np.ndarray
    """
    tmpvppr = np.where(vppr > 10E-15, vppr, 10E-15)  # np.max(vppr, 10E-15)
    return ((AEi3 * np.log(tmpvppr / AEi1)) / (AEi2 - np.log(tmpvppr / AEi1)))


def td_from_vppr(tt:np.ndarray, vppr:np.ndarray, tpl:float, swph:bool) -> np.ndarray:
    """Calculates the temperature dew point from the  vapour pressure

    :param tt: air temperature (celsius)
    :type tt: np.ndarray
    :param vppr: vapour pressure (hPa)
    :type vppr: np.ndarray
    :param tpl: temperature at which to change from the ice phase to the water phase (kelvin)
    :type tpl: float
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: temperature dew point (celsius)
    :rtype: np.ndarray
    """
    return np.where(
        not swph or (
            swph and tt > tpl),
        td_water_from_vppr(vppr),
        td_ice_from_vppr(vppr))


def rpn_hu_from_hr(tt:np.ndarray, hr:np.ndarray, px:np.ndarray, swph:bool) -> np.ndarray:
    """Calculates the specific humidity using RPN TdPack from the relative humidity

    :param tt: air temperature (kelvin)
    :type tt: np.ndarray
    :param hr: relative humidity
    :type hr: np.ndarray
    :param px: pressure (Pa)
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: specific humidity
    :rtype: np.ndarray
    """
    return shrahu(hr, tt, px, swph)


def rpn_es_from_hr(tt:np.ndarray, hr:np.ndarray, px:np.ndarray, swph:bool) -> np.ndarray:
    """Calculates the dew point depression using RPN TdPack from the relative humidity

    :param tt: air temperature (kelvin)
    :type tt: np.ndarray
    :param hr: relative humidity
    :type hr: np.ndarray
    :param px: pressure (Pa)
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: dew point depression (celsius)
    :rtype: np.ndarray
    """

    return np.maximum(shraes(hr, tt, px, swph), 0.0)


def rpn_es_from_hu(tt:np.ndarray, hu:np.ndarray, px:np.ndarray, swph:bool) ->np.ndarray:
    """Calculates the dew point depression using RPN TdPack from the specific humidity

    :param tt: air temperature (kelvin)
    :type tt: np.ndarray
    :param hu: specific humidity (kg/kg)
    :type hu: np.ndarray
    :param px: pressure (Pa)
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: dew point depression (celsius)
    :rtype: np.ndarray
    """
    tmp = shuaes(hu, tt, px, swph)
    return np.where(tmp > 0., tmp, 0.)  # np.max(shuaes(hu, tt, px, swph),0.)


def hu_from_qv(qv:np.ndarray) -> np.ndarray:
    """Calculates the specific humidity from the water vapour mixing ratio

    :param qv: water vapour mixing ratio (kg/kg)
    :type qv: np.ndarray
    :return: specific humidity (kg/kg)
    :rtype: np.ndarray
    """
    tmpqv = np.where(qv > 10E-15, qv, 10E-15)  # np.max(qv,10E-15)
    return tmpqv / (tmpqv + 1.)


# def td_from_hr(tt:np.ndarray, hr:np.ndarray) -> np.ndarray:
#     """[summary]

#     :param tt: [description]
#     :type tt: np.ndarray
#     :param hr: [description]
#     :type hr: np.ndarray
#     :return: [description]
#     :rtype: np.ndarray
#     """
#     vara = 17.625
#     varb = 243.04
#     hrtmp = hr
#     hrtmp = np.where(hrtmp > 1., 1., hrtmp)
#     hrtmp = np.where(hrtmp < 10E-15, 10E-15, hrtmp)
#     term = (vara * tt) / (varb + tt) + np.log(hrtmp)
#     return (varb * term) / (vara - term)


def hr_from_svp_vppr(svp:np.ndarray, vppr:np.ndarray) -> np.ndarray:
    """Calculates the relative humidity from saturation vapour pressure and vapour pressure

    :param svp: saturation vapour pressure (hPa)
    :type svp: np.ndarray
    :param vppr: vapour pressure (hPa)
    :type vppr: np.ndarray
    :return: relative humidity
    :rtype: np.ndarray
    """
    return vppr / svp


def rpn_hr_from_es(tt:np.ndarray, es:np.ndarray, px:np.ndarray, swph:bool) -> np.ndarray:
    """Calculates the relative humidity using RPN TdPack from the dew point depression

    :param tt: air temperature (kelvin)
    :type tt: np.ndarray
    :param es: dew point depression (celsius)
    :type es: np.ndarray
    :param px: pressure (Pa)
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: relative humidity
    :rtype: np.ndarray
    """
    return sesahr(es, tt, px, swph)


def rpn_hr_from_hu(tt:np.ndarray, hu:np.ndarray, px:np.ndarray, swph:bool):
    """Calculates the relative humidity using RPN TdPack from the specific humidity

    :param tt: air temperature (kelvin)
    :type tt: np.ndarray
    :param hu: specific humidity
    :type hu: np.ndarray
    :param px: pressure (Pa)
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: relative humidity
    :rtype: np.ndarray
    """
    return shuahr(hu, tt, px, swph)


def hu_from_vppr(vppr:np.ndarray, px:np.ndarray) -> np.ndarray:
    """Calculates the specific humidity from the vapour pressure

    :param vppr: vapour pressure (hPa)
    :type vppr: np.ndarray
    :param px: pressure (hPa)
    :type px: np.ndarray
    :return: specific humidity
    :rtype: np.ndarray
    """
    return (EPS1 * vppr) / (px - (1. - EPS1) * vppr)


def rpn_hu_from_es(tt:np.ndarray, es:np.ndarray, px:np.ndarray, swph:bool) -> np.ndarray:
    """Calculates the specific humidity using RPN TdPack from the dew point depression

    :param tt: air temperature (kelvin)
    :type tt: np.ndarray
    :param es: dew point depression (celsius)
    :type es: np.ndarray
    :param px: pressure (Pa)
    :type px: np.ndarray
    :param swph: boolean representing if we consider both ice and water phase
    :type swph: bool
    :return: specific humidity
    :rtype: np.ndarray
    """
    return sesahu(es, tt, px, swph)


def hmx_from_svp(tt:np.ndarray, svp:np.ndarray) -> np.ndarray:
    """Calculates the humidex from the saturation vapour pressure

    :param tt: air temperature (celsius)
    :type tt: np.ndarray
    :param svp: saturation vapour pressure (hPa)
    :type svp: np.ndarray
    :return: humidex
    :rtype: np.ndarray
    """
    resultat = tt + (0.55555 * (svp - 10.))
    return np.where(resultat > tt, resultat, tt)


def qv_from_hu(hu:np.ndarray)->np.ndarray:
    """Calculates the water vapour mixing ratio from the specific humidity

    :param hu: specific humidity (kg/kg)
    :type hu: np.ndarray
    :return: water vapour mixing ratio (g/kg)
    :rtype: np.ndarray
    """
    hutmp = np.where(hu > 10E-15, hu, 10E-15)  # np.max(hu,10E-15)
    return (hutmp / (1. - hutmp)) * 1000.


def qv_from_vppr(vppr:np.ndarray, px:np.ndarray) -> np.ndarray:
    """Calculates the water vapour mixing ratio from the vapour pressure

    :param vppr: vapour pressure (Pa)
    :type vppr: np.ndarray
    :param px: pressure (Pa)
    :type px: np.ndarray
    :return: water vapour mixing ratio (g/kg)
    :rtype: np.ndarray
    """
    return np.where(px < 10E-15, 0., EPS1 * (vppr / (px - vppr)) * 1000.)

def vt_from_qv(tt:np.ndarray, qv:np.ndarray) -> np.ndarray:
    """Calculates the virtual temperature from the water vapour mixing ratio

    :param tt: air temperature (kelvin)
    :type tt: np.ndarray
    :param qv: water vapour mixing ratio (kg/kg)
    :type qv: np.ndarray
    :return: virtual temperature (celsius)
    :rtype: np.ndarray
    """

    qvtmp = np.where(qv > 10E-15, qv, 10E-15)

    return ( ( tt * ((1. + (qvtmp/EPS1))/(1. + qvtmp)) ) - TCDK)
    

def es_from_td(tt:np.ndarray, td:np.ndarray) -> np.ndarray:
    """Calculates the dew point depression from the temperature dew point

    :param tt: air temperature (celsius)
    :type tt: np.ndarray
    :param td: temperature dew point (celsius)
    :type td: np.ndarray
    :return: dew point depression (celsius)
    :rtype: np.ndarray
    """
    tmp = tt - td
    return np.where(tmp > 0., tmp, 0.)

    
