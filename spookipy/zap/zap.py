import logging
import fstpy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Union
import re
import warnings

from ..plugin import Plugin, PluginParser
from ..utils import initializer, round_half_down, type_of_field_to_typ_var1, get_cf_unit_string


class ZapError(Exception):
    pass


DATYP = ["X", "R", "I", "S", "E", "F", "A", "Z", "i", "e", "f"]

VALID_FLAGS = {
    "FILTERED": "filtered",
    "INTERPOLATED": "interpolated",
    "ZAPPED": "zapped",
    "UNITCONVERTED": "unit_converted",
    "BOUNDED": "bounded",
    "ENSEMBLEEXTRAINFO": "ensemble_extra_info",
    "ALL_FLAGS": "all_flags",
}

VERTICAL_LEVEL_CHOICES = set(fstpy.LEVELTYPES["label"])

TYPE_OF_FIELD = {
    "FORECAST",
    "ANALYSIS",
    "CLIMATOLOGY",
    "VARIOUS",
    "RAW_STATION_DATA",
    "MONTHLY_ERROR",
    "VARIOUS_CONSTANTS",
    "VERIFICATION_MATRIX_CONTINGENCY_TABLE",
    "OBSERVATION",
    "DIAGNOSTIC_QPF",
    "VARIOUS_SCORES",
    "TIME_SERIE",
    "MASK",
}

TYPE_OF_FIELD_CHOICES = TYPE_OF_FIELD.union({f"{field}_MASKED" for field in TYPE_OF_FIELD})

IMPLEMENTATION_TYPES_CHOICES = {"EXPERIMENTAL": "X", "PARALLEL": "P", "OPERATIONAL": "N"}


def split_metadata(df):
    no_meta_df = df.loc[~df.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY"])].copy()
    meta_df = df.loc[df.nomvar.isin(["^^", ">>", "^>", "!!", "!!SF", "HY"])].copy()
    return meta_df, no_meta_df


def warn_deprecated_forecast_hour_only():
    warnings.warn(
        "Parameter forecast_hour_only is deprecated and will have no effect on your resulting operation; "
        "use length_of_time_step (deet) and time_step_number (npas), or opt to use forecast_hour instead"
        "(forecast_hour will update time_step_number automatically)",
        DeprecationWarning,
    )


class Zap(Plugin):
    """Allows renaming one or more value(s) of field attribute(s) in the internal memory structure
    without affecting the data itself.

    :param df: Input dataframe
    :type df: pd.DataFrame
    :param type_of_field: New type of field (FORECAST, ANALYSIS, CLIMATOLOGY, etc.)
    :type type_of_field: str, optional
    :param nomvar: Variable name
    :type nomvar: str, optional
    :param run: New name for the run (2 characters)
    :type run: str, optional
    :param ensemble_member: New ensemble member number (3 characters)
    :type ensemble_member: str, optional
    :param implementation: New mode of operation (EXPERIMENTAL, PARALLEL, OPERATIONAL)
    :type implementation: str, optional
    :param date_of_observation: New date of origin
    :type date_of_observation: datetime, optional
    :param vertical_level: New vertical level
    :type vertical_level: float, optional
    :param vertical_level_type: New vertical level type (SIGMA, HYBRID, etc.)
    :type vertical_level_type: str, optional
    :param forecast_hour: New forecast hour
    :type forecast_hour: Union[float, timedelta], optional
    :param forecast_hour_only (deprecated): New forecast hour (no timestep adjustment)
    :type forecast_hour_only: Union[float, timedelta], optional
    :param user_defined_index: New index defined by user
    :type user_defined_index: int, optional
    :param nbits_for_data_storage: New number of bits for data storage
    :type nbits_for_data_storage: str, optional
    :param unit: New unit
    :type unit: str, optional
    :param modification_flag: Modification flags to set/unset
    :type modification_flag: Dict[str, bool], optional
    :param metadata_zappable: Allow metadata to be modified
    :type metadata_zappable: bool, optional
    :param label: New product definition section label
    :type label: str, optional
    :param length_of_time_step: New length of time step (DEET)
    :type length_of_time_step: int, optional
    :param time_step_number: New time step number (NPAS)
    :type time_step_number: int, optional
    :param etiket_format: New etiket format (ex. 2,6,1,3,K)
    :type etiket_format: str, optional
    :param do_not_flag_as_zapped: Disables zapped flag
    :type do_not_flag_as_zapped: bool, optional
    """

    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        type_of_field: str = None,
        nomvar: str = None,
        run: str = None,
        ensemble_member: str = None,
        etiket_format: str = None,
        implementation: str = None,
        date_of_observation: datetime = None,
        vertical_level: float = None,
        vertical_level_type: str = None,
        forecast_hour: Union[float, timedelta] = None,
        forecast_hour_only: Union[float, timedelta] = None,
        user_defined_index: int = None,
        nbits_for_data_storage: str = None,  # nbits
        unit: str = None,
        modification_flag: Dict[str, bool] = {},
        metadata_zappable: bool = False,
        label: str = None,
        length_of_time_step: int = None,  # deet
        time_step_number: int = None,  # npas
        do_not_flag_as_zapped: bool = False,
    ):
        if forecast_hour_only is not None:
            warn_deprecated_forecast_hour_only()

        self.df = fstpy.reduce_columns(self.df)
        super().__init__(self.df)
        self.validate_parameters()

    def validate_modification_flags(self):
        """Validate modification flags"""
        if self.modification_flag is not None:
            # Validate flag names
            for flag in self.modification_flag:
                if flag not in VALID_FLAGS and flag != "ALL_FLAGS":
                    raise ZapError(f"Invalid modification flag: {flag}")

            # Validate flag values are boolean
            for value in self.modification_flag.values():
                if not isinstance(value, bool):
                    raise ZapError("Modification flag values must be True or False")

    def validate_parameters(self):
        """Validate all input parameters"""
        if self.type_of_field is not None and self.type_of_field not in TYPE_OF_FIELD_CHOICES:
            raise ZapError(f"Invalid type_of_field: {self.type_of_field}")

        if self.run is not None and len(self.run) != 2:
            raise ZapError("Run parameter must be 2 characters")

        if self.ensemble_member is not None and self.ensemble_member != "" and len(self.ensemble_member) != 3:
            raise ZapError("Ensemble member must be 3 characters")

        if self.implementation is not None and self.implementation not in IMPLEMENTATION_TYPES_CHOICES:
            raise ZapError(f"Invalid implementation type: {self.implementation}")

        if self.vertical_level is not None and self.vertical_level < 0:
            raise ZapError("Vertical level must be positive")

        if self.vertical_level_type is not None and self.vertical_level_type not in VERTICAL_LEVEL_CHOICES:
            raise ZapError(f"Invalid vertical level type: {self.vertical_level_type}")

        if self.user_defined_index is not None and self.user_defined_index < 0:
            raise ZapError("User defined index must be positive")

        if self.length_of_time_step is not None:
            if self.length_of_time_step < 0 or self.length_of_time_step > 16777215:
                raise ZapError("Length of time step must be between 0 and 16777215")

        if self.time_step_number is not None:
            if self.time_step_number < 0 or self.time_step_number > 16777215:
                raise ZapError("Time step number must be between 0 and 16777215")

        # Validate forecast hours are not negative
        if self.forecast_hour is not None:
            if not isinstance(self.forecast_hour, timedelta):
                self.forecast_hour = timedelta(seconds=round(self.forecast_hour * 3600))
            if self.forecast_hour.total_seconds() < 0:
                raise ZapError("Forecast hour must be positive")

        if self.nbits_for_data_storage is not None:
            datypstr = self.nbits_for_data_storage[0]
            nbits_str = self.nbits_for_data_storage[1:]
            if datypstr not in DATYP:
                raise ZapError(f"{datypstr} not in {DATYP}")
            try:
                nbits = int(nbits_str)
                if not 0 < nbits < 65:
                    raise ZapError(
                        f"Invalid value for --nbits_for_data_storage, value must be between 1 and 64: {nbits}"
                    )
            except ValueError:
                raise ZapError(
                    f"Invalid value for --nbits_for_data_storage, characters following the first should be a number between 1 and 64: {nbits_str}"
                )

        if self.unit is not None:
            # validate and convert to cf-units string if necessary
            try:
                self.unit = get_cf_unit_string(self.unit, "Zap", ZapError)
            except ZapError as e:
                raise ZapError(f"Invalid value for unit parameter: {e}") from None

        if self.etiket_format is not None:
            pattern = r"^(\d+),(\d+),(\d+),(\d+),(K|D)$"
            match = re.match(pattern, self.etiket_format)
            if not match:
                raise ZapError(
                    f"Invalid value for --etiket_format. The given format should contain 5 comma-separated values, the first four being numbers summing up to a maximum of 12 and the last one being either K (keep) or D (discard): {self.etiket_format}"
                )
            numbers = [int(match.group(i)) for i in range(1, 5)]
            numbers_sum = sum(numbers)
            if numbers_sum > 12:
                raise ZapError(
                    f"Invalid value for --etiket_format. The sum of the first four numbers must not surpass 12 ({numbers[0]}+{numbers[1]}+{numbers[2]}+{numbers[3]}={numbers_sum}): {self.etiket_format}"
                )

        # Validate modification flags
        self.validate_modification_flags()

    def compute(self) -> pd.DataFrame:
        """Apply the zap modifications to the dataframe

        :return: Modified dataframe
        :rtype: pd.DataFrame
        """
        logging.info("Zap - compute")

        if not self.metadata_zappable:
            modifiable_df = self.no_meta_df
            if self.etiket_format is not None:
                modifiable_df["etiket_format"] = self.etiket_format

                modifiable_df = fstpy.add_columns(modifiable_df, columns=["etiket"])

                modifiable_df = fstpy.reduce_parsed_etiket_columns(modifiable_df)
        else:
            modifiable_df = self.df
            if self.etiket_format is not None:
                self.meta_df["etiket_format"] = self.etiket_format
                modifiable_df["etiket_format"] = self.etiket_format

                self.meta_df = fstpy.add_columns(self.meta_df, columns=["etiket"])
                modifiable_df = fstpy.add_columns(modifiable_df, columns=["etiket"])

                self.meta_df = fstpy.reduce_parsed_etiket_columns(self.meta_df)
                modifiable_df = fstpy.reduce_parsed_etiket_columns(modifiable_df)

        modifiable_df = fstpy.add_columns(modifiable_df, columns=["flags"])
        if self.modification_flag:
            for flag, value in self.modification_flag.items():
                if flag == "ALL_FLAGS":
                    for col in VALID_FLAGS.values():
                        modifiable_df[col] = value
                    if not value:
                        modifiable_df["multiple_modifications"] = False
                else:
                    modifiable_df[VALID_FLAGS[flag]] = value
        else:
            modifiable_df["zapped"] = True

        if self.do_not_flag_as_zapped:
            modifiable_df["zapped"] = False

        modifiable_df = fstpy.reduce_flag_values(modifiable_df)

        # Apply modifications based on parameters
        if self.type_of_field is not None:
            modifiable_df["typvar"] = type_of_field_to_typ_var1(self.type_of_field, Zap.__name__, ZapError)

        if self.nomvar is not None:
            modifiable_df["nomvar"] = self.nomvar

        if self.run is not None:
            modifiable_df = fstpy.add_columns(modifiable_df, columns=["etiket"])
            modifiable_df["run"] = self.run
            modifiable_df = fstpy.reduce_parsed_etiket_columns(modifiable_df)

        if self.ensemble_member is not None:
            modifiable_df = fstpy.add_columns(modifiable_df, columns=["etiket"])
            modifiable_df["ensemble_member"] = self.ensemble_member
            modifiable_df = fstpy.reduce_parsed_etiket_columns(modifiable_df)

        if self.implementation is not None:
            modifiable_df = fstpy.add_columns(modifiable_df, columns=["etiket"])
            modifiable_df["implementation"] = IMPLEMENTATION_TYPES_CHOICES[self.implementation]
            modifiable_df = fstpy.reduce_parsed_etiket_columns(modifiable_df)

        if self.date_of_observation is not None:
            if self.metadata_zappable:
                meta_df, no_meta_df = split_metadata(modifiable_df)

                no_meta_df = fstpy.add_columns(no_meta_df, columns=["dateo"])
                no_meta_df["date_of_observation"] = self.date_of_observation
                no_meta_df = fstpy.reduce_decoded_date_column(no_meta_df)

                modifiable_df = fstpy.safe_concatenate([meta_df, no_meta_df])
            else:
                modifiable_df = fstpy.add_columns(modifiable_df, columns=["dateo"])
                modifiable_df["date_of_observation"] = self.date_of_observation
                modifiable_df = fstpy.reduce_decoded_date_column(modifiable_df)

        if self.vertical_level is not None or self.vertical_level_type is not None:
            if self.metadata_zappable:
                meta_df, no_meta_df = split_metadata(modifiable_df)

                no_meta_df = fstpy.add_columns(no_meta_df, columns=["ip_info"])
                if self.vertical_level is not None:
                    no_meta_df["level"] = self.vertical_level
                if self.vertical_level_type is not None:
                    level_type = fstpy.LEVELTYPES.loc[fstpy.LEVELTYPES.label == self.vertical_level_type].kind
                    no_meta_df["ip1_kind"] = int(level_type)
                no_meta_df = fstpy.update_ip1_from_level(no_meta_df)
                modifiable_df = fstpy.safe_concatenate([meta_df, no_meta_df])
            else:
                modifiable_df = fstpy.add_columns(modifiable_df, columns=["ip_info"])
                if self.vertical_level is not None:
                    modifiable_df["level"] = self.vertical_level
                if self.vertical_level_type is not None:
                    level_type = fstpy.LEVELTYPES.loc[fstpy.LEVELTYPES.label == self.vertical_level_type].kind
                    modifiable_df["ip1_kind"] = level_type
                modifiable_df = fstpy.reduce_ip_info_columns(modifiable_df)

        ip2_changed = False
        if self.length_of_time_step is not None:
            if self.metadata_zappable:
                meta_df, no_meta_df = split_metadata(modifiable_df)

                no_meta_df["deet"] = self.length_of_time_step

                modifiable_df = fstpy.safe_concatenate([meta_df, no_meta_df])
            else:
                modifiable_df["deet"] = self.length_of_time_step
            ip2_changed = True

        if self.time_step_number is not None:
            if self.metadata_zappable:
                meta_df, no_meta_df = split_metadata(modifiable_df)

                no_meta_df["npas"] = self.time_step_number

                modifiable_df = fstpy.safe_concatenate([meta_df, no_meta_df])
            else:
                modifiable_df["npas"] = self.time_step_number
            ip2_changed = True

        if self.forecast_hour is not None:

            def process_forecast_hour(df):
                df = fstpy.add_columns(df, columns=["forecast_hour"])
                df["forecast_hour"] = self.forecast_hour
                df = fstpy.reduce_forecast_hour_column(df)
                grouped = df.groupby(["deet", "npas"])
                grouped.apply(self.validate_fh)
                return df

            if self.metadata_zappable:
                meta_df, no_meta_df = split_metadata(modifiable_df)

                no_meta_df = process_forecast_hour(no_meta_df)

                modifiable_df = fstpy.safe_concatenate([meta_df, no_meta_df])
            else:
                modifiable_df = process_forecast_hour(modifiable_df)
            ip2_changed = True

        if ip2_changed:
            if self.metadata_zappable:
                meta_df, no_meta_df = split_metadata(modifiable_df)

                no_meta_df["ip2"] = modifiable_df.apply(
                    lambda row: round_half_down(row["deet"] * row["npas"] / 3600), axis=1
                )

                modifiable_df = fstpy.safe_concatenate([meta_df, no_meta_df])
            else:
                modifiable_df["ip2"] = modifiable_df.apply(
                    lambda row: round_half_down(row["deet"] * row["npas"] / 3600), axis=1
                )

        if self.user_defined_index is not None:
            modifiable_df["ip3"] = self.user_defined_index

        if self.nbits_for_data_storage is not None:
            datyp = self.nbits_for_data_storage[0]
            nbits = int(self.nbits_for_data_storage[1:])
            modifiable_df["datyp"] = fstpy.get_data_type_value(datyp)
            modifiable_df["nbits"] = nbits

        if self.unit is not None:
            modifiable_df = fstpy.add_columns(modifiable_df, columns=["unit"])
            modifiable_df["unit"] = self.unit

        if self.label is not None:
            modifiable_df = fstpy.add_columns(modifiable_df, columns=["etiket"])
            modifiable_df["label"] = self.label
            modifiable_df = fstpy.reduce_parsed_etiket_columns(modifiable_df)

        if not self.metadata_zappable:
            modifiable_df = fstpy.safe_concatenate([self.meta_df, modifiable_df])

        modifiable_df = fstpy.remove_all_expanded_columns(modifiable_df)

        return modifiable_df

    def validate_fh(self, group):
        expected_fh = (group["deet"] * group["npas"]) / 3600
        actual_fh = self.forecast_hour.total_seconds() / 3600
        if not np.allclose(actual_fh, expected_fh):
            raise ZapError(
                f"Forecast hour validation failed for group: {group.name}. Expected: {expected_fh.iloc[0]}, Actual: {actual_fh}"
            )

    @staticmethod
    def parse_config(args: str) -> dict:
        """Parse command line arguments

        :param args: Arguments to parse
        :type args: str
        :return: Parsed arguments
        :rtype: dict
        """
        parser = PluginParser(prog=Zap.__name__, parents=[Plugin.base_parser], add_help=False)

        parser.add_argument(
            "--dateOfOrigin", type=str, dest="date_of_observation", help="New date of origin (YYYYMMDDHHMMSS)."
        )
        parser.add_argument(
            "--ensembleMember",
            type=str,
            dest="ensemble_member",
            help="New ensemble member number (3 characters) or _NONE_ to suppress the current value.",
        )
        parser.add_argument("--fieldName", type=str, dest="nomvar", help="New field name.")
        parser.add_argument(
            "--forecastHour",
            type=str,
            dest="forecast_hour",
            help="New forecast hour (the number of timesteps will be adjusted accordingly) warning not precise for decimal time.",
        )
        parser.add_argument(
            "--forecastHourOnly",
            type=str,
            dest="forecast_hour_only",
            help="DEPRECATED (use a forecastHour or a combination of timeStepNumber(npas) and lenghtOfTimeStep(deet) instead)",
        )
        parser.add_argument(
            "--implementation", type=str, choices=list(IMPLEMENTATION_TYPES_CHOICES), help="New mode of operation."
        )
        parser.add_argument(
            "--lengthOfTimeStep",
            type=int,
            dest="length_of_time_step",
            help="New lenghtOfTimeStep (deet) defined by user.",
        )
        parser.add_argument(
            "--metadataZappable",
            action="store_true",
            dest="metadata_zappable",
            help="Allows metadata to be modified. Use with Caution.",
        )
        parser.add_argument(
            "--modificationFlag",
            type=str,
            dest="modification_flag",
            help="Permits changing value of a modification flag, overrides default zapped flag.",
        )
        parser.add_argument(
            "--nbitsForDataStorage",
            type=str,
            dest="nbits_for_data_storage",
            help="New number of bits for data storage. Ex: --nbitsForDataStorage R16",
        )
        parser.add_argument("--pdsLabel", type=str, dest="label", help="New product definition section label.")
        parser.add_argument("--run", type=str, help="New name for the run (2 characters).")
        parser.add_argument("--tag", type=str, help="DEPRECATED. No longer supported.")
        parser.add_argument(
            "--timeStepNumber", type=int, dest="time_step_number", help="New timeStepNumber (npas) defined by user."
        )
        parser.add_argument(
            "--typeOfField",
            type=str,
            choices=list(TYPE_OF_FIELD_CHOICES),
            dest="type_of_field",
            help="New type of field. Note: You can append '_MASKED' to each of the choices to set a masked field.",
        )
        parser.add_argument("--unit", type=str, help="New unit.")
        parser.add_argument(
            "--userDefinedIndex",
            type=int,
            dest="user_defined_index",
            help="New index defined by user.",
        )
        parser.add_argument("--verticalLevel", type=float, dest="vertical_level", help="New vertical level.")
        parser.add_argument(
            "--verticalLevelType",
            type=str,
            choices=list(VERTICAL_LEVEL_CHOICES),
            dest="vertical_level_type",
            help="New vertical level type.",
        )
        parser.add_argument(
            "--doNotFlagAsZapped", action="store_true", dest="do_not_flag_as_zapped", help="Disables zapped flag."
        )

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg.get("date_of_observation"):
            date = parsed_arg["date_of_observation"]
            if not bool(re.fullmatch(r"\d{14}", date)):
                raise ZapError(
                    "Date should be represented by INTEGER[0 to +infinity] Ex: --dateOfOrigin 20050308000000"
                )
            try:
                parsed_arg["date_of_observation"] = datetime.strptime(date, "%Y%m%d%H%M%S")
            except ValueError:
                raise ZapError(f"{date} should be represented in this format (YYYYMMDDHHMMSS)")

        if parsed_arg.get("ensemble_member"):
            if parsed_arg["ensemble_member"] == "_NONE_":
                parsed_arg["ensemble_member"] = ""
            elif len(parsed_arg["ensemble_member"]) != 3:
                raise ZapError("Ensemble member must be 3 characters or _NONE_")

        if parsed_arg.get("forecast_hour"):
            if ":" in parsed_arg["forecast_hour"]:
                h, m, s = map(int, parsed_arg["forecast_hour"].split(":"))
                parsed_arg["forecast_hour"] = timedelta(hours=h, minutes=m, seconds=s)
            else:
                parsed_arg["forecast_hour"] = float(parsed_arg["forecast_hour"])

        if parsed_arg.get("forecast_hour_only"):
            warn_deprecated_forecast_hour_only()

        if parsed_arg.get("modification_flag"):
            flags = {}
            for flag_pair in parsed_arg["modification_flag"].split(","):
                flag, value = flag_pair.split("=")
                if flag in VALID_FLAGS and value.upper() in ["TRUE", "FALSE"]:
                    flags[flag] = value.upper() == "TRUE"
                else:
                    raise ZapError(
                        f"Error while parsing --modificationFlag {parsed_arg['modification_flag']} : '{flag}={value}' is not a valid pair."
                    )
            parsed_arg["modification_flag"] = flags

        if parsed_arg.get("nbits_for_data_storage"):
            datypstr = parsed_arg["nbits_for_data_storage"][0]
            nbits_str = parsed_arg["nbits_for_data_storage"][1:]
            if datypstr not in DATYP:
                raise ZapError(f"Invalid value for --nbitsForDataStorage, datyp {datypstr} not in {DATYP}")
            try:
                nbits = int(nbits_str)
                if not 0 < nbits < 65:
                    raise ZapError(f"Invalid value for --nbitsForDataStorage, value must be between 1 and 64: {nbits}")
            except ValueError:
                raise ZapError(
                    f"Invalid value for --nbitsForDataStorage, characters following the first should be a number between 1 and 64: {nbits_str}"
                )

        if parsed_arg.get("run"):
            if len(parsed_arg["run"]) != 2:
                raise ZapError("Run parameter must be 2 characters")

        if parsed_arg.get("unit"):
            try:
                parsed_arg["unit"] = get_cf_unit_string(parsed_arg["unit"], "Zap", ZapError)
            except ZapError as e:
                raise ZapError(f"While parsing --unit: {e}") from None
        return parsed_arg
