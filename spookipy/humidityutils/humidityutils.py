# -*- coding: utf-8 -*-
import fstpy.all as fstpy

# TDPACK
# CONSTANTE POUR NOUS PERMETTRE DE SWITCHER LA CORRECTION POUR LA CONSTANTE DE CONVERSION
# des unites KELVIN et CELSIUS
# Raison: Actuellement, il y a une inconsistance avec la librairie TDPACK; la constante utilisee pour la conversion est
#         273.16 alors que dans SPOOKI elle etait de 273.15  On utise donc la constante de TDPACK en lui enlevant un
#         offset de 0.01.  Lorsque la librairie TDPACK aura ete modifiee, on utilisera un offset de 0.
#
AEW1=6.1094
AEW2=17.625
AEW3=243.04
AEI1=6.1121
AEI2=22.587
AEI3=273.86
epsilon=0.6219800221014

TDPACK_OFFSET_FIX=0.01

def get_temp_phase_switch(caller_class:str, error_calss:Exception, ice_water_phase_both:bool, temp_phase_switch:float, temp_phase_switch_unit:str, rpn:bool) -> float:
    kelvin = fstpy.get_unit_by_name('kelvin')
    celsius = fstpy.get_unit_by_name('celsius')
    celsius_to_kelvin = fstpy.get_converter(celsius,kelvin)
    kelvin_to_celsius = fstpy.get_converter(kelvin,celsius)
    if ice_water_phase_both:
        if temp_phase_switch != -99999:
            if temp_phase_switch < -273.15 or temp_phase_switch > 273.16:
                raise error_calss(caller_class + ' - temp_phase_switch not within range [-273.15,273.16]')
            else:
                if rpn:
                    if temp_phase_switch_unit == 'celsius':
                        temp_phase_switch = celsius_to_kelvin(temp_phase_switch)
                else:
                    temp_phase_switch = kelvin_to_celsius(temp_phase_switch)
        else:
            raise error_calss(caller_class + ' - temp_phase_switch must be defined when using ice_water_phase_both')
    else:
        raise error_calss(caller_class + ' - temp_phase_switch must not be defined when using ice_water_phase_both') 
    return temp_phase_switch
 