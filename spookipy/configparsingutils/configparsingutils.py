from datetime import timedelta


def preprocess_negative_args(argv: list, flags: list) -> list:
    """function to switch the syntax of the argument with the --option=value format for non numeral values starting with -
    use this when you have an argument with a value that might start with -
    code taken from https://stackoverflow.com/a/64379138
    :param argv: list of arguments (split config)
    :type argv: list[str]
    :param flags: list of argument with a non numerical value that might start with a -
    :type flags: list[str]
    :return: list of argument ready to be parse with the parse
    :rtype: list[str]
    """
    result = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in flags and i + 1 < len(argv) and argv[i + 1].startswith("-"):
            arg = arg + "=" + argv[i + 1]
            i += 1
        result.append(arg)
        i += 1
    return result


def apply_lambda_to_list(my_list: list, my_lambda):
    """function to apply a lambda to a list
    :param my_list: list of element
    :type my_list: list
    :param my_lambda: lambda to apply
    :type my_lambda: lambda
    :return: list of results
    :rtype: list
    """
    return list(my_lambda(e) for e in my_list)


def convert_time_range(range: str, error_class=Exception):
    """function to convert string representing a time range in a tuple of datetime.timedelta
    :param range: range of time in the format 0@1 or 0:00:00@1:00:00
    :type range: str
    :param error_class: Exception to raise if the format is not recognized
    :type error_class: Exception (optional)
    :return: a tuple of two timedelta to represent the range
    :rtype: tuple(datetime.timedelta, datetime.timedelta)
    """
    times = range.split("@")
    if len(times) != 2:
        raise error_class(
            f"Range of time ({range}) should represented by INT[0 to +infinity] @ INT[0 to + infinity] ] or [ [0 to + infinity]:[0-59]:[0-59] @ [0 to + infinity]:[0-59]:[0-59] ]. Ex: 23@24 or 23:00:00@24:00:00"
        )
    return (convert_time(times[0]), convert_time(times[1]))


def convert_time(time: str, error_class=Exception):
    """function to convert string representing a time into a datetime.timedelta
    :param interval: interval of time in the format 1.5 or 1:30:00
    :type interval: str
    :param error_class: Exception to raise if the format is not recognized
    :type error_class: Exception (optional)
    :return: a timedelta
    :rtype: datetime.timedelta
    """
    t = time.split(":")
    if len(t) == 3:
        return timedelta(hours=float(t[0]), minutes=float(t[1]), seconds=float(t[2]))
    elif len(t) == 1:
        return timedelta(hours=float(t[0]))
    else:
        raise error_class(
            f"Times ({time}) need to be formatted with FLOAT[>0 to + infinity] or STRING[ [0 to + infinity]:[0-59]:[0-59] Ex: 3 or 3:00:00"
        )


def check_and_format_humidity_parsed_arguments(parsed_arg, error_class=Exception):
    if parsed_arg["ice_water_phase"] is not None:
        parsed_arg["ice_water_phase"] = parsed_arg["ice_water_phase"].lower()
    else:
        del parsed_arg["ice_water_phase"]

    if parsed_arg["temperaturePhaseSwitch"] is not None:
        parsed_arg["temp_phase_switch"] = float(parsed_arg["temperaturePhaseSwitch"][0:-1])
        parsed_arg["temp_phase_switch_unit"] = parsed_arg["temperaturePhaseSwitch"][-1]

        if parsed_arg["temp_phase_switch_unit"] == "C":
            parsed_arg["temp_phase_switch_unit"] = "celsius"
        elif parsed_arg["temp_phase_switch_unit"] == "K":
            parsed_arg["temp_phase_switch_unit"] = "kelvin"
        else:
            raise error_class(
                "--temperaturePhaseSwitch needs to be of types [ FLOAT[-273.15 to 273.16] + STRING [C|K] ], it is {}".format(
                    parsed_arg["temperaturePhaseSwitch"]
                )
            )
