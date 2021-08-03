# -*- coding: utf-8 -*-
import fstpy.all as fstpy
import numpy as np
from rpnpy.utils.tdpack import FOEWA, FOEW, FOEFQ, FOQFE, TRPL ,FOHR, FOHRA
import math
# TDPACK
# CONSTANTE POUR NOUS PERMETTRE DE SWITCHER LA CORRECTION POUR LA CONSTANTE DE CONVERSION
# des unites KELVIN et CELSIUS
# Raison: Actuellement, il y a une inconsistance avec la librairie TDPACK; la ante utilisee pour la conversion est
#         273.16 alors que dans SPOOKI elle etait de 273.15  On utise donc la ante de TDPACK en lui enlevant un
#         offset de 0.01.  Lorsque la librairie TDPACK aura ete modifiee, on utilisera un offset de 0.
#
TDPACK_OFFSET_FIX=0.01
AEW1=6.1094
AEW2=17.625
AEW3=243.04+TDPACK_OFFSET_FIX
AEI1=6.1121
AEI2=22.587
AEI3=273.86

epsilon=0.6219800221014



ttns1  = 610.78
ttns3w = 17.269
ttns3i = 21.875
ttns4w = 35.86
ttns4i =  7.66



def shuahr(hu,tt,px,ice_water_phase_both):
    hu = hu.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    if ice_water_phase_both:
        return FOHR(hu,tt,px)
    else:
        return FOHRA(hu,tt,px)

def sesahu(es,tt,px,ice_water_phase_both):
    es = es.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    td = tt - es
    if ice_water_phase_both:
        e = FOEW(td)
    else:
        e = FOEWA(td)
    return FOQFE(e,px)

def sesahr(es,tt,px,ice_water_phase_both):
    es = es.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    hu = sesahu(es,tt,px,ice_water_phase_both)
    return shuahr(hu,tt,px,ice_water_phase_both)

def shrahu(hr, tt, px, ice_water_phase_both):
    hr = hr.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    hrtt = hr * tt
    if ice_water_phase_both:
        tt = FOEW(tt)
        e = np.where(px < hrtt, px, hrtt)
    else:
        tt = FOEWA(tt)
        e = np.where(px < hrtt, px, hrtt)
    return FOEFQ(e,px)


def shuaes(hu, tt, px, ice_water_phase_both):
    hu = hu.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    hu = np.where(hu > 0.0000000001, hu, 0.0000000001)
    e = FOEFQ(hu,px)
    cte = np.log(e/ttns1)
    td = (cte*ttns4w - ttns3w*TRPL)/(cte - ttns3w)
    if ice_water_phase_both:
        td = np.where(td < TRPL,((ttns4i*cte - ttns3i*TRPL)/(cte - ttns3i)),td)
    return tt-td

def shraes(hr, tt, px, ice_water_phase_both):
    hr = hr.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    hu = shrahu(hr,tt,px,ice_water_phase_both)
    return shuaes(hu,tt,px,ice_water_phase_both)

def rpn_calc_dew_point_depression_hu(tt,hu,px,ice_water_phase_both):
    hu = hu.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    es = shuaes(hu, tt, px, ice_water_phase_both)
    return np.where(es> 0.0,es,0.0).astype(np.float32)

def rpn_calc_dew_point_depression_hr(tt,hr,px,ice_water_phase_both):
    hr = hr.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    es = shraes(hr, tt, px, ice_water_phase_both)
    return np.where(es> 0.0,es,0.0).astype(np.float32)

def rpn_calc_vapour_pressure_hu(hu, px):
    hu = hu.astype(np.float64)
    px = px.astype(np.float64)
    return (FOEFQ(hu, px) / 100.0).astype(np.float32)

def calc_vapour_pressure_hu(hu, px):
    hu = hu.astype(np.float64)
    px = px.astype(np.float64)
    epsilon1 = 0.621980
    hu = np.where(hu > 10e-15, hu, 10e-15)
    return ((hu * px)/( hu * (1-epsilon1) + epsilon1)).astype(np.float32)

def calc_vapour_pressure_qv(qv, px):
    qv = qv.astype(np.float64)
    px = px.astype(np.float64)
    epsilon1 = 0.621980
    qv = np.where(qv > 10e-15, qv, 10e-15)
    return  ((qv * px) / (qv + epsilon1)).astype(np.float32)

def calc_vapour_pressure_hr(hr, svp):
    hr = hr.astype(np.float64)
    svp = svp.astype(np.float64)
    hr = np.where(hr > 10e-15, hr, 10e-15)
    return (hr * svp).astype(np.float32)

def calc_temperature_dew_point_es(tt,es):
    es = es.astype(np.float64)
    tt = tt.astype(np.float64)
    return np.where(es < 0.0,tt,tt-es).astype(np.float32)

def calc_temperature_dew_point_water_vppr(vppr):
    vppr = vppr.astype(np.float64)
    vppr = np.where(vppr > 10e-15,vppr,10e-15)
    return (  np.log(vppr/AEW1) * AEW3 ) / ( AEW2 - np.log(vppr/AEW1) ).astype(np.float32)

def calc_temperature_dew_point_ice_vppr(vppr):
    vppr = vppr.astype(np.float64)
    vppr = np.where(vppr > 10e-15,vppr,10e-15)
    return ( np.log(vppr/AEI1) * AEI3 ) / ( AEI2 - np.log(vppr/AEI1) ).astype(np.float32)


def calc_temperature_dew_point_vppr(tt,vppr,temp_phase_switch, ice_water_phase_both):
    tt = tt.astype(np.float64)
    vppr = vppr.astype(np.float64)
    tdw=calc_temperature_dew_point_water_vppr(vppr)
    tdi=calc_temperature_dew_point_ice_vppr(vppr)
    if ice_water_phase_both:
        return np.where(tt > temp_phase_switch,tdw,tdi).astype(np.float32)
    else:
        return tdw.astype(np.float32)


def rpn_calc_vapour_pressure_water_td(td):
    td = td.astype(np.float64)
    return (FOEWA(td) / 100.0).astype(np.float32)


def rpn_calc_vapour_pressure_ice_td(td):
    td = td.astype(np.float64)
    return (FOEW(td) / 100.0).astype(np.float32)

def rpn_calc_vapour_pressure_both_td(tt,td,temp_phase_switch):
    tt = tt.astype(np.float64)
    td = td.astype(np.float64)
    vpprw = rpn_calc_vapour_pressure_water_td(td)
    vppri = rpn_calc_vapour_pressure_ice_td(td)
    return np.where(tt > temp_phase_switch,vpprw,vppri).astype(np.float32)

def rpn_calc_vapour_pressure_td(td,tt,temp_phase_switch, ice_water_phase_both):
    tt = tt.astype(np.float64)
    td = td.astype(np.float64)
    if not ice_water_phase_both:
        return  rpn_calc_vapour_pressure_water_td(td).astype(np.float32)
    else:
        return rpn_calc_vapour_pressure_both_td(tt,td,temp_phase_switch).astype(np.float32)

def calc_vapour_pressure_water_td(td):
    td = td.astype(np.float64)
    return (np.exp((td * AEW2) / (td + AEW3)) * AEW1).astype(np.float32)

def calc_vapour_pressure_ice_td(td):
    td = td.astype(np.float64)
    return (np.exp((td * AEI2) / (td + AEI3)) * AEI1).astype(np.float32)

def calc_vapour_pressure_both_td(tt,td,temp_phase_switch):
    tt = tt.astype(np.float64)
    td = td.astype(np.float64)
    vpprw = calc_vapour_pressure_water_td(td)
    vppri = calc_vapour_pressure_ice_td(td)
    return np.where(tt > temp_phase_switch,vpprw,vppri).astype(np.float32)

def calc_vapour_pressure_td(td,tt,temp_phase_switch, ice_water_phase_both):
    tt = tt.astype(np.float64)
    td = td.astype(np.float64)
    if not ice_water_phase_both:
        return  calc_vapour_pressure_water_td(td).astype(np.float32)
    else:
        return calc_vapour_pressure_both_td(tt,td,temp_phase_switch).astype(np.float32)


def rpn_calc_humidity_specific_hr(hr,tt,px,ice_water_phase_both):
    hr = hr.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    return shrahu(hr,tt,px,ice_water_phase_both).astype(np.float32)

def rpn_calc_humidity_specific_es(es,tt,px,ice_water_phase_both):
    es = es.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    return sesahu(es,tt,px,ice_water_phase_both).astype(np.float32)

def calc_dew_point_depression_td(tt,td):
    tt = tt.astype(np.float64)
    td = td.astype(np.float64)
    res = tt - td
    return np.where(res > 0.0, res, 0.0).astype(np.float32)

def calc_humidity_specific_qv(qv):
    qv = qv.astype(np.float64)
    qv = np.where(qv > 10e-15,qv,10e-15)
    return (qv / (qv+1)).astype(np.float32)

def calc_humidity_specific_vppr(vppr,px):
    vppr = vppr.astype(np.float64)
    px = px.astype(np.float64)
    epsilon1 = 0.621980
    return (vppr * epsilon1) / (px - vppr * (1-epsilon1)).astype(np.float32)



def rpn_calc_saturation_vapour_pressure_water(tt):
    tt = tt.astype(np.float64)
    return (FOEWA(tt) / 100.0).astype(np.float32)

def rpn_calc_saturation_vapour_pressure_ice(tt):
    tt = tt.astype(np.float64)
    return (FOEW(tt) / 100.0).astype(np.float32)


def rpn_calc_saturation_vapour_pressure(tt, temp_phase_switch, ice_water_phase_both):
    tt = tt.astype(np.float64)
    svpw = rpn_calc_saturation_vapour_pressure_water(tt)
    svpi = rpn_calc_saturation_vapour_pressure_ice(tt)
    if ice_water_phase_both:
        return np.where(tt > temp_phase_switch,svpw,svpi).astype(np.float32)
    else:
        return svpw.astype(np.float32)

def calc_saturation_vapour_pressure_water(tt):
    tt = tt.astype(np.float64)
    return AEW1 * np.exp((AEW2 * tt) / (AEW3 + tt)).astype(np.float32)


def calc_saturation_vapour_pressure_ice(tt) :
    tt = tt.astype(np.float64)
    return AEI1 * np.exp((AEI2 * tt) / (AEI3 + tt)).astype(np.float32)

def calc_saturation_vapour_pressure(tt, temp_phase_switch, ice_water_phase_both):
    tt = tt.astype(np.float64)
    svpw = calc_saturation_vapour_pressure_water(tt)
    svpi = calc_saturation_vapour_pressure_ice(tt)
    if ice_water_phase_both:
        return np.where(tt > temp_phase_switch,svpw,svpi).astype(np.float32)
    else:
        return svpw.astype(np.float32)

def calc_humidity_relative_svp_vppr(svp,vppr):
    svp = svp.astype(np.float64)
    vppr = vppr.astype(np.float64)
    return (vppr/svp).astype(np.float32)

def rpn_calc_humidity_relative_hu(hu,tt,px,ice_water_phase_both):
    hu = hu.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    return shuahr(hu, tt, px, ice_water_phase_both).astype(np.float32)

def rpn_calc_humidity_relative_es(es,tt,px,ice_water_phase_both):
    es = es.astype(np.float64)
    tt = tt.astype(np.float64)
    px = px.astype(np.float64)
    return sesahr(es, tt, px, ice_water_phase_both).astype(np.float32)


def calc_water_vapour_mixing_ratio_hu(hu):
    hu = hu.astype(np.float64)
    hu = np.where(hu > 10e-15,hu,10e-15)
    return ((hu / (1 - hu)) * 1000.0).astype(np.float32)

def calc_water_vapour_mixing_ratio_px_vppr(px,vppr):
    px = px.astype(np.float64)
    vppr = vppr.astype(np.float64)
    epsilon1 = 0.621980
    px_minus_vppr = px - vppr
    qv = epsilon1 * (vppr / (px - vppr)) * 1000.0
    return np.where(px_minus_vppr< 10e-15,0,qv).astype(np.float32)



def calc_humidex(tt,svp):
    tt = tt.astype(np.float64)
    svp = svp.astype(np.float64)
    resultat = tt + (0.55555 * (svp - 10))
    return np.where(resultat > tt,resultat,tt).astype(np.float32)

def get_temp_phase_switch(error_class:Exception, ice_water_phase_both:bool, temp_phase_switch:float, temp_phase_switch_unit:str, rpn:bool) -> float:
    if ice_water_phase_both:
        validate_temp_phase_switch(error_class,temp_phase_switch)
        if rpn:
            if temp_phase_switch_unit == 'celsius':
                temp_phase_switch = fstpy.unit_convert_array(np.array([temp_phase_switch],dtype='float32'), 'celsius','kelvin')[0]
        elif temp_phase_switch_unit == 'kelvin':
            temp_phase_switch = fstpy.unit_convert_array(np.array([temp_phase_switch],dtype='float32'), 'kelvin','celsius')[0]
    return temp_phase_switch

def validate_temp_phase_switch_unit(error_class:Exception,temp_phase_switch_unit:str):
    valid_units = ['celsius','kelvin']
    if temp_phase_switch_unit not in valid_units:
            raise error_class(f'Invalid unit {temp_phase_switch_unit} not in {valid_units}')

def validate_ice_water_phase(error_class:Exception,ice_water_phase:str):
    phases = ['both','water']
    if ice_water_phase not in phases:
        raise error_class(f'Invalid {ice_water_phase} not in {phases}')

def validate_temp_phase_switch(error_class:Exception,temp_phase_switch:float):
    if temp_phase_switch < -273.15 or temp_phase_switch > 273.16:
        raise error_class('Temp_phase_switch {temp_phase_switch} not within range [-273.15,273.16]')

def validate_parameter_combinations(error_class:Exception,ice_water_phase:str,temp_phase_switch:float):
    if (ice_water_phase=='water') and not (temp_phase_switch is None):
        raise error_class('Cannot use ice_water_phase="water" with temp_phase_switch\n')

    if (not (ice_water_phase is None) and (ice_water_phase!='water')) and (temp_phase_switch is None):
        raise error_class('Cannot use ice_water_phase without setting temp_phase_switch\n')

    if not (temp_phase_switch is None) and (ice_water_phase is None):
        raise error_class('Cannot use temp_phase_switch without setting ice_water_phase\n')

def validate_humidity_parameters(error_class:Exception,ice_water_phase:str,temp_phase_switch:float,temp_phase_switch_unit:str):
    validate_parameter_combinations(error_class,ice_water_phase,temp_phase_switch)
    validate_temp_phase_switch_unit(error_class,temp_phase_switch_unit)
    validate_ice_water_phase(error_class,ice_water_phase)
