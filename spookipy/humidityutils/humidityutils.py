# -*- coding: utf-8 -*-
import warnings
import fstpy
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
        explicit_temp_phase_switch: bool = False,
        rpn: bool = False):
    """Validate the paramter combinations

    :param error_class: Exception to raise
    :type error_class: type
    :param ice_water_phase: ice water phase value ['both','water']
    :type ice_water_phase: str
    :param temp_phase_switch: phase switch temperature value
    :type temp_phase_switch: float
    :param explicit_temp_phase_switch: is phase switch temperature set explicitly for this plugin (default False)
    :type explicit_temp_phase_switch: bool
    :raises error_class: Cannot use ice_water_phase="water" with temp_phase_switch
    :raises error_class: Cannot use ice_water_phase without setting temp_phase_switch
    :raises error_class: Cannot use temp_phase_switch without setting ice_water_phase
    """
    if (ice_water_phase == 'water') and temp_phase_switch is not None and explicit_temp_phase_switch:
        raise error_class(
            'Cannot use ice_water_phase="water" with temp_phase_switch\n')

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
        warnings.warn("temp_phase_switch and temp_phase_switch_unit will be ignored while using rpn.")

def validate_humidity_parameters(
        error_class: type,
        ice_water_phase: str,
        temp_phase_switch: float,
        temp_phase_switch_unit: str,
        explicit_temp_phase_switch: bool = False,
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
    :param explicit_temp_phase_switch: is phase switch temperature set explicitly for this plugin (default False)
    :type explicit_temp_phase_switch: bool
    :param rpn: use rpn (default: False)
    :type rpn: bool
    """
    validate_parameter_combinations(
        error_class, ice_water_phase, temp_phase_switch, explicit_temp_phase_switch, rpn)
    validate_temp_phase_switch_unit(error_class, temp_phase_switch_unit)
    validate_ice_water_phase(error_class, ice_water_phase)
    validate_rpn(temp_phase_switch, temp_phase_switch_unit, rpn)

def mandatory_ice_water_phase_when_using_temp_phase_switch(
        error_class: type,
        explicit_params: list):
    """Raise exception if 

    :param error_class: Exception to raise
    :type error_class: type
    :param explicit_params: list of parameters explicitly used in the plugin
    :type explicit_params: list()
    :raises error_class: Need to set ice_water_phase when temp_phase_switch is set explicitly
    """
    if ("ice_water_phase" not in explicit_params) and ("temp_phase_switch" in explicit_params):
        raise error_class(
            'Need to set ice_water_phase when temp_phase_switch is set explicitly\n')

def mandatory_temp_phase_switch_when_using_ice_water_phase_both(
        error_class: type,
        explicit_params: list,
        ice_water_phase: str,
        rpn: bool = False,
        mandatory_even_with_rpn: bool = False):
    """Raise exception if 

    :param error_class: Exception to raise
    :type error_class: type
    :param explicit_params: list of parameters explicitly used in the plugin
    :type explicit_params: list()
    :type ice_water_phase: str
    :param temp_phase_switch: phase switch temperature value
    :param rpn: use rpn (default: False)
    :type rpn: bool
    :raises error_class: Need to set temp_phase_switch when ice_water_phase is set explicitly to both
    """
    if (("temp_phase_switch" not in explicit_params) and 
        ("ice_water_phase" in explicit_params) and
        (ice_water_phase == 'both') and
        (not rpn or mandatory_even_with_rpn)):

        raise error_class(
            'Need to set temp_phase_switch when ice_water_phase is set explicitly to both\n')
