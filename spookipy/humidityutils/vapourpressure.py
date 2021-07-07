# -*- coding: utf-8 -*-
import math
from .humidityutils import AEI1, AEI2, AEI3, AEW1, AEW2, AEW3, epsilon
from rpnpy.utils.tdpack import FOEWA, FOEW, FOEFQ
#
#  Calculates the vapour pressure as a function of relative humidity and saturation vapour pressure.
#  @param hr   Relative humidity, in decimal (between 0 and 1)
#  @param svp  saturation vapour pressure, in hPa
#  @return     Vapour pressure, in hPa
#
def calc_vapour_pressure_hr( hr:float,  svp:float) -> float:
    hr = max(hr, 10e-15)
    return hr * svp


#
#  Calculates the vapour pressure as a function of specific humidity and pressure.
#  @param hu   Specific humidity, in kg/kg
#  @param px   Pressure, in hPa
#  @return     Vapour pressure, in hPa
#
def calc_vapour_pressure_hu( hu:float,  px:float) -> float: 

    hu = max(hu, 10e-15)
    return (hu *  px)/(epsilon + hu *  (1-epsilon))


#
#  Calculates the vapour pressure as a function of mixing ratio and pressure.
#  @param qv   Mixing ratio, in kg/kg
#  @param px   Pressure, in hPa
#  @return     Vapour pressure, in hPa
#
def calc_vapour_pressure_qv( qv:float,  px:float) -> float: 

    qv = max(qv, 10e-15)
    return  (qv * px) / (epsilon + qv)


#
#  Calculates the vapour pressure (Water phase) as a function of temperature dew point.
#  @param td   Temperature dew point, in celsius
#  @return     Vapour pressure, in hPa
#
def calc_vapour_pressure_water_td( td:float) -> float: 
	return AEW1 *  math.exp((AEW2 *  td) / (AEW3 + td))


#
#  Calculates the vapour pressure (Ice phase) as a function of temperature dew point.
#  @param td   Temperature dew point, in celsius
#  @return     Vapour pressure, in hPa
#
def calc_vapour_pressure_td( td:float) -> float: 
	return AEI1 *  math.exp((AEI2 *  td) / (AEI3 + td))


#
#  Calculates the vapour pressure as a function of temperature dew point.
#  @param td     Temperature dew point, in celsius
#  @param tt     Air temperature (celsius)
#  @param tpl    Temperature at which to change from the ice phase to the water phase (celsius).
#  @param swph   A boolean representing if we consider both ice and water phase.
#  @return     Vapour pressure, in hPa
#
def metacalc_vapour_pressure_td( td:float,  tt:float,  tpl:float, swph:bool) -> float:
	#if( (tt > tpl) || !swph )
    if ( not swph or (swph and tt > tpl) ):
    	return  calc_vapour_pressure_water_td(td)
    else:
    	return calc_vapour_pressure_td(td)
	


#
#  Calculates the vapour pressure using RPN TdPack as a function of specific humidity and pressure.
#  @param hu   Specific humidity, in kg/kg
#  @param px   Pressure, in Pa
#  @return     Vapour pressure, in hPa
#
def rpncalc_vapour_pressure_hu( hu:float,  px:float) -> float: 
    #RPN returns vapour pressure in Pascal and we want output to be HectoPascal.
    #return rpn::libphy::sfoefq(hu, px) / 100.0f
    return FOEFQ(hu, px) / 100.0


#
#  Calculates the vapour pressure (Water phase) as a function of temperature dew point.
#  @param td   Temperature dew point, in kelvin
#  @return     Vapour pressure, in hPa
#
def rpncalc_vapour_pressure_water_td( td:float) -> float: 
    #RPN returns vapour pressure in Pascal and we want output to be HectoPascal.
    #return rpn::libphy::sfoewa(td) / 100.0f
    return FOEWA(td) / 100.0


#
#  Calculates the vapour pressure (Ice phase) as a function of temperature dew point.
#  @param td   Temperature dew point, in kelvin
#  @return     Vapour pressure, in hPa
#
def rpncalc_vapour_pressure_td( td:float) -> float:

    #RPN returns vapour pressure in Pascal and we want output to be HectoPascal.
    #return rpn::libphy::sfoew(td) / 100.0f
    return FOEW(td) / 100.0


#
#  Calculates the vapour pressure as a function of temperature dew point.
#  @param td   Temperature dew point, in kelvin
#  @param tt     Air temperature (kelvin)
#  @param tpl    Temperature at which to change from the ice phase to the water phase (kelvin).
#  @param swph   A boolean representing if we consider both ice and water phase.
#  @return     Vapour pressure, in hPa
#
def rpncalc_vapour_pressure_td( td:float,  tt:float,  tpl:float, swph:bool) -> float:

    #if( (tt > tpl) || !swph )
    if ( not swph or (swph and tt > tpl) ):
        return  rpncalc_vapour_pressure_water_td(td)
    else:
        return rpncalc_vapour_pressure_td(td)
	

