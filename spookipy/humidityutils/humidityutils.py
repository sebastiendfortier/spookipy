# -*- coding: utf-8 -*-
import warnings
import fstpy.all as fstpy
import numpy as np


def get_temp_phase_switch(
        error_class: type,
        ice_water_phase_both: bool,
        temp_phase_switch: float,
        temp_phase_switch_unit: str,
        rpn: bool) -> float:
    """Gets the phase switch temperature from the provided parameters

    :param error_class: Exception to raise
    :type error_class: type
    :param ice_water_phase: ice water phase value ['both','water']
    :type ice_water_phase: str
    :param temp_phase_switch: phase switch temperature value
    :type temp_phase_switch: float
    :param temp_phase_switch_unit: phase switch temperature unit
    :type temp_phase_switch_unit: str
    :param rpn: flag to choose between rpn or regular method
    :type rpn: bool
    :return: phase switch temperature
    :rtype: float
    """
    if ice_water_phase_both:
        validate_temp_phase_switch(error_class, temp_phase_switch)
        if rpn:
            if temp_phase_switch_unit == 'celsius':
                temp_phase_switch = fstpy.unit_convert_array(
                    np.array([temp_phase_switch], dtype=np.float32), 'celsius', 'kelvin')[0]
        elif temp_phase_switch_unit == 'kelvin':
            temp_phase_switch = fstpy.unit_convert_array(
                np.array([temp_phase_switch], dtype=np.float32), 'kelvin', 'celsius')[0]
    return temp_phase_switch


def validate_temp_phase_switch_unit(
        error_class: type,
        temp_phase_switch_unit: str):
    
    valid_units = ['celsius', 'kelvin']
    if temp_phase_switch_unit not in valid_units:
        raise error_class(
            f'Invalid unit {temp_phase_switch_unit} not in {valid_units}')


def validate_ice_water_phase(error_class: type, ice_water_phase: str):
    """Validates that the ice water phase in either water or both

    :param error_class: exception to raise
    :type error_class: type
    :param ice_water_phase: ice water phase
    :type ice_water_phase: str
    :raises error_class: raised exception
    """
    phases = ['both', 'water']
    if ice_water_phase not in phases:
        raise error_class(f'Invalid {ice_water_phase} not in {phases}')


def validate_temp_phase_switch(error_class: type, temp_phase_switch: float):
    """Validates that the phase switch temperature is between  -273.15 and 273.16

    :param error_class: exception to raise
    :type error_class: type
    :param temp_phase_switch: phase switch temperature
    :type temp_phase_switch: float
    :raises error_class: raised exception
    """
    if temp_phase_switch is None:
        # can happen when using rpn
        return
    if temp_phase_switch < -273.15 or temp_phase_switch > 273.16:
        raise error_class(
            f'Temp_phase_switch {temp_phase_switch} not within range [-273.15,273.16]\n')


def validate_parameter_combinations(
        error_class: type,
        ice_water_phase: str,
        temp_phase_switch: float,
        default_temp_phase_switch: float = None,
        rpn: bool = False):
    """Validate the paramter combinations

    :param error_class: Exception to raise
    :type error_class: type
    :param ice_water_phase: ice water phase value ['both','water']
    :type ice_water_phase: str
    :param temp_phase_switch: phase switch temperature value
    :type temp_phase_switch: float
    :param default_temp_phase_switch: default value of phase switch temperature for this plugin (default None)
    :type default_temp_phase_switch: float
    :raises error_class: Cannot use ice_water_phase="water" with temp_phase_switch
    :raises error_class: Cannot use ice_water_phase without setting temp_phase_switch
    :raises error_class: Cannot use temp_phase_switch without setting ice_water_phase
    """
    if (ice_water_phase == 'water') and not (temp_phase_switch is None or temp_phase_switch == default_temp_phase_switch):
        raise error_class(
            'Cannot use ice_water_phase="water" with temp_phase_switch\n temp_phase_switch = {}, default_temp_phase_switch = {}, -> {}'.format(temp_phase_switch,default_temp_phase_switch,temp_phase_switch is default_temp_phase_switch))

    if (not (ice_water_phase is None) and (ice_water_phase != 'water')) and (
            temp_phase_switch is None) and (not rpn):
        raise error_class(
            'Cannot use ice_water_phase without setting temp_phase_switch\n')

    if not (temp_phase_switch is None) and (ice_water_phase is None):
        raise error_class(
            'Cannot use temp_phase_switch without setting ice_water_phase\n')

def validate_rpn(
        temp_phase_switch: float,
        temp_phase_switch_unit: str,
        rpn: bool):
    """Raise warning if rpn is used with temp_phase_switch

    :param temp_phase_switch: phase switch temperature value
    :type temp_phase_switch: float
    :param temp_phase_switch_unit: phase switch temperature unit
    :type temp_phase_switch_unit: str
    :param rpn: use rpn
    :type rpn: bool
    """
    if not rpn:
        return
    if temp_phase_switch is not None or temp_phase_switch_unit is not None:
        warnings.warn("temp_phase_switch and temp_phase_switch_unit will be ignore while using rpn.")

def validate_humidity_parameters(
        error_class: type,
        ice_water_phase: str,
        temp_phase_switch: float,
        temp_phase_switch_unit: str,
        default_temp_phase_switch: float = None,
        rpn: bool = False):
    """validate the humidity plugin parameters. Validates the paramter combinations, the phase switch temperature unit and value and the ice water phase value

    :param error_class: Exception to raise
    :type error_class: type
    :param ice_water_phase: ice water phase value ['both','water']
    :type ice_water_phase: str
    :param temp_phase_switch: phase switch temperature value
    :type temp_phase_switch: float
    :param temp_phase_switch_unit: phase switch temperature unit
    :type temp_phase_switch_unit: str
    :param default_temp_phase_switch: default value of phase switch temperature for this plugin (default None)
    :type default_temp_phase_switch: float
    :param rpn: use rpn (default: False)
    :type rpn: bool
    """
    validate_parameter_combinations(
        error_class, ice_water_phase, temp_phase_switch, default_temp_phase_switch, rpn)
    validate_temp_phase_switch_unit(error_class, temp_phase_switch_unit)
    validate_ice_water_phase(error_class, ice_water_phase)
    validate_rpn(temp_phase_switch, temp_phase_switch_unit, rpn)
