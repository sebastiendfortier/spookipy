# -*- coding: utf-8 -*-
import argparse
import pandas as pd
import fstpy
import re

from enum import Enum
from datetime import datetime, timedelta
from typing import List, Tuple, Union
from ..plugin import Plugin, PluginParser
from ..utils import (
    initializer,
    validate_list_of_nomvar,
    validate_nomvar,
    type_of_field_to_typ_var1,
    VERTICAL_LEVEL_CHOICES,
    COORDINATE_CHOICES,
    TYPE_OF_FIELD_CHOICES,
    METADATA_FIELD_CHOICES,
)
from ..configparsingutils import apply_lambda_to_list, convert_time_range, convert_time


class SelectError(Exception):
    pass


class Select(Plugin):
    """
    A plugin for selecting and filtering fields from an internal DataFrame based on specified parameters.

    This class allows for various filtering criteria including date ranges, ensemble members,
    field names, and matrix sizes, enabling flexible data manipulation and analysis.

    :param df: Input DataFrame containing the data to be filtered.
    :type df: pd.DataFrame
    :param coordinate_type: Types of coordinates to include in the selection.
    :type coordinate_type: str
    :param date_of_observation: List of observation dates or date ranges for filtering.
    :type date_of_observation: List[Union[datetime, Tuple[datetime, datetime]]]
    :param date_of_validity: List of validity dates or date ranges for filtering.
    :type date_of_validity: List[Union[datetime, Tuple[datetime, datetime]]]
    :param exclude: Flag to exclude certain metadata from the selection.
    :type exclude: bool
    :param fail_msg: Message to display on failure.
    :type fail_msg: str, optional
    :param forecast_hour: Ranges of forecast hours for filtering.
    :type forecast_hour: List[Union[timedelta, Tuple[timedelta, timedelta]]]
    :param loose_match: Flag to enable loose matching of field names.
    :type loose_match: bool
    :param label: list of labels to include in this selection.
    :type label: str or list[str]
    :param metadata_nomvar: List of metadata fields to consider during filtering.
    :type metadata_nomvar: str or list[str]
    :param no_metadata: If True, metadata will be ignored in filtering operations.
    :type no_metadata: bool
    :param nomvar: List of field names to select from the DataFrame.
    :type nomvar: str or list[str]
    :param nofail: If True, will not raise an error on failure.
    :type nofail: bool
    :param silent_failure: If True, suppress error messages during execution.
    :type silent_failure: bool
    :param type_of_field: Types of fields to include in the selection.
    :type type_of_field: list[str]
    :param user_defined_index: Custom index values for filtering.
    :type user_defined_index: List[Union[int, Tuple[int, int]]]
    :param vertical_level: Vertical levels to consider in filtering.
    :type vertical_level: Union[List[Union[float, Tuple[float, float]]], str]
    :param vertical_level_type: Types of vertical levels for filtering.
    :type vertical_level_type: str
    :param x_axis_matrix_size: Specifications for the x-axis matrix size.
    :type x_axis_matrix_size: List[Union[int, Tuple[int, int]]]
    :param y_axis_matrix_size: Specifications for the y-axis matrix size.
    :type y_axis_matrix_size: List[Union[int, Tuple[int, int]]]
    :param reduce_df: Indicates whether to minimize the size of the DataFrame after filtering; defaults to True.
    :type reduce_df: bool, optional
    :param copy_input: If True, a copy of the input DataFrame will be utilized.
    :type copy_input: bool
    """

    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        coordinate_type: "str" = None,
        date_of_observation: "List[Union[datetime, Tuple[datetime, datetime]]]" = None,
        date_of_validity: "List[Union[datetime, Tuple[datetime, datetime]]]" = None,
        ensemble_member: "list[str]" = None,
        exclude=False,
        fail_msg: "str" = None,
        forecast_hour: "List[Union[timedelta, Tuple[timedelta, timedelta]]]" = None,
        loose_match=False,
        label: "list[str]" = None,
        metadata_nomvar: "list[str]" = None,
        no_metadata=False,
        nofail=False,
        nomvar: "list[str]" = None,
        silent_failure=False,
        type_of_field: "list[str]" = None,
        user_defined_index: "List[Union[int, Tuple[int, int]]]" = None,
        vertical_level: "Union[List[Union[float, Tuple[float, float]]], str]" = None,
        vertical_level_type: "str" = None,
        x_axis_matrix_size: "List[Union[int, Tuple[int, int]]]" = None,
        y_axis_matrix_size: "List[Union[int, Tuple[int, int]]]" = None,
        copy_input=False,
        reduce_df=True,
    ):
        self.main_query = []
        self.metadata_query = []
        self.single_query_df = pd.DataFrame
        self.result_meta_df = pd.DataFrame
        self.result_no_meta_df = pd.DataFrame
        self.count_distinct_dict = {
            "date_of_validity": None,
            "date_of_observation": None,
            "nomvar": None,
            "ni": None,
            "nj": None,
            "etiket": None,
            "forecast_hour": None,
            "ip3": None,
            "typvar": None,
            "vctype": None,
            "level": None,
            "ip1_kind": None,
            "follow_topography": None,
            "label": None,
            "surface": None,
        }

        # preliminary selection that reduces the amount of work that add_columns has to do.
        if self.nomvar and not self.exclude and not self.loose_match and not self.nofail:
            self.prepare_data()

        required_fields = [
            self.date_of_observation,
            self.date_of_validity,
            self.forecast_hour,
            self.label,
            self.type_of_field,
            self.vertical_level,
            self.vertical_level_type,
            self.coordinate_type,
        ]
        if any(required_fields):
            self.df = fstpy.add_columns(self.df)
        super().__init__(self.df)

        self.result_df = self.no_meta_df
        self.validate_params()

    def validate_params(self):
        """Validates the parameters provided during initialization.

        This method checks each parameter against predefined validation functions,
        ensuring that they conform to expected types and formats. If any validation
        fails, a `SelectError` is raised with an optional custom failure message.

        :raises SelectError: If any parameter validation fails, with an optional custom failure message.
        """
        ensure_list_attributes(self)
        try:
            if self.nomvar:
                validate_list_of_nomvar(self.nomvar, Select.__name__, SelectError)

            if self.coordinate_type:
                validate_coordinate_type(self.coordinate_type, Select.__name__, SelectError)

            if self.date_of_observation:
                validate_list_type(self.date_of_observation, datetime, Select.__name__, SelectError)

            if self.date_of_validity:
                validate_list_type(self.date_of_validity, datetime, Select.__name__, SelectError)

            if self.x_axis_matrix_size:
                validate_list_type(self.x_axis_matrix_size, int, Select.__name__, SelectError)
                validate_item_range(self.x_axis_matrix_size, Select.__name__, SelectError, 1)

            if self.y_axis_matrix_size:
                validate_list_type(self.y_axis_matrix_size, int, Select.__name__, SelectError)
                validate_item_range(self.y_axis_matrix_size, Select.__name__, SelectError, 1)

            if self.ensemble_member:
                validate_list_ensemble_member(self.ensemble_member, Select.__name__, SelectError)

            if self.forecast_hour:
                validate_list_type(self.forecast_hour, timedelta, Select.__name__, SelectError)
                validate_item_range(self.forecast_hour, Select.__name__, SelectError, timedelta(0))

            if self.label:
                validate_list_label(self.label, Select.__name__, SelectError)

            if self.metadata_nomvar:
                validate_list_metadata_nomvar(self.metadata_nomvar, "Select", SelectError)

            if self.user_defined_index:
                validate_list_type(self.user_defined_index, int, Select.__name__, SelectError)
                validate_item_range(self.user_defined_index, Select.__name__, SelectError, 0)

            if self.vertical_level:
                self.vertical_level = validate_vertical_level(self.vertical_level, Select.__name__, SelectError)

            if self.vertical_level_type:
                self.vertical_level_type = validate_vertical_level_type(
                    self.vertical_level_type, Select.__name__, SelectError
                )

            if self.type_of_field:
                validate_list_type_field(self.type_of_field, Select.__name__, SelectError)

        except SelectError:
            if self.fail_msg:
                raise SelectError(self.fail_msg)
            else:
                raise

    def prepare_data(self):
        """Filters the DataFrame based on only nomvar to reduce the amount of data that add_columns is called upon.

        This method selects fields and modifies self.df directly.
        """
        nomvar_to_keep = self.nomvar + METADATA_FIELD_CHOICES
        self.df = self.df[self.df.nomvar.isin(nomvar_to_keep)]
        self.df = fstpy.metadata_cleanup(self.df)

    #### MAIN QUERY BUILDER ####
    def compute(self) -> pd.DataFrame:
        """Filters the DataFrame based on specified criteria and returns the resulting DataFrame.

        This method builds queries based on the provided parameters and applies them to the internal DataFrame.
        It checks distinct values and handles both metadata and non-metadata queries to produce the final result.

        :return: A filtered DataFrame containing the selected fields based on the input parameters.
        :rtype: pd.DataFrame
        """

        single_attribute_query = None
        try:
            if self.date_of_validity:
                single_attribute_query = self.query_builder("date_of_validity", self.date_of_validity)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("date_of_validity")

            if self.date_of_observation:
                single_attribute_query = self.query_builder("date_of_observation", self.date_of_observation)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("date_of_observation")

            if self.nomvar:
                single_attribute_query = self.query_builder("nomvar", self.nomvar)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("nomvar")

            if self.x_axis_matrix_size:
                single_attribute_query = self.query_builder("ni", self.x_axis_matrix_size)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("ni")

            if self.y_axis_matrix_size:
                single_attribute_query = self.query_builder("nj", self.y_axis_matrix_size)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("nj")

            if self.ensemble_member:
                single_attribute_query = self.query_builder("etiket", self.ensemble_member)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("etiket")

            if self.forecast_hour:
                single_attribute_query = self.query_builder("forecast_hour", self.forecast_hour)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("forecast_hour")

            if self.label:
                single_attribute_query = self.query_builder("label", self.label)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("etiket")

            if self.user_defined_index:
                single_attribute_query = self.query_builder("ip3", self.user_defined_index)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("ip3")

            if self.type_of_field:
                single_attribute_query = self.query_builder("typvar", self.type_of_field)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("typvar")

            if self.coordinate_type:
                # converting vctype to string for it to be queryable
                self.no_meta_df["vctype_string"] = self.no_meta_df["vctype"].apply(str)
                single_attribute_query = self.query_builder("vctype_string", self.coordinate_type)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("vctype")

            if self.vertical_level and isinstance(self.vertical_level[0], bool):
                single_attribute_query = "surface == True"
                self.query_df([single_attribute_query])
                min_surface_level = (
                    self.result_df.groupby(["nomvar", "grid", "dateo", "datev"])["level"].min().reset_index()
                )
                self.result_df = self.result_df.merge(
                    min_surface_level, on=["nomvar", "grid", "level", "dateo", "datev"]
                )

                if self.loose_match:
                    self.main_query.pop()
                self.check_distinct_values()
                self.update_distinct_values("level")

            if self.vertical_level and not isinstance(self.vertical_level[0], bool):
                single_attribute_query = self.query_builder("level", self.vertical_level)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("surface")

            if self.vertical_level_type and isinstance(self.vertical_level_type[0], bool):
                single_attribute_query = self.query_builder("follow_topography", self.vertical_level_type)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("follow_topography")

            if self.vertical_level_type and not isinstance(self.vertical_level_type[0], bool):
                single_attribute_query = self.query_builder("ip1_kind", self.vertical_level_type)
                self.query_df(single_attribute_query)
                self.check_distinct_values()
                self.update_distinct_values("ip1_kind")

            if self.metadata_nomvar:
                single_attribute_query = self.query_builder("nomvar", self.metadata_nomvar)
                self.query_meta_df(single_attribute_query)

            r = pd.DataFrame()

            ### Different use case conditions ###
            if self.no_metadata:
                self.meta_df = pd.DataFrame()

            # --nometadata only and no queries
            if not self.main_query and self.no_metadata:
                r = self.final_results(
                    [self.no_meta_df], SelectError, copy_input=self.copy_input, reduce_df=self.reduce_df
                )

            # default case with queries and potentiel no metadata or modified meta
            elif self.main_query:
                r = self.final_results(
                    [self.result_df], SelectError, copy_input=self.copy_input, reduce_df=self.reduce_df
                )
                if "vctype_string" in r.columns:
                    r = r.drop("vctype_string", axis=1)

            # case when we want to exclude only metadata
            elif not self.main_query and self.exclude and self.metadata_query:
                r = self.final_results(
                    [self.no_meta_df], SelectError, copy_input=self.copy_input, reduce_df=self.reduce_df
                )

            # case where only metadata is left
            elif not self.main_query and self.metadata_query and not self.exclude:
                r = self.meta_df

            # loose match condition
            if self.loose_match:
                self.main_query = " | ".join(self.main_query)
                self.result_df = self.no_meta_df.query(self.main_query)

                if self.vertical_level and isinstance(self.vertical_level[0], bool):
                    self.loose_match_surface()

                if self.result_df.empty:
                    raise SelectError(f"[{Select.__name__}[('{self.main_query}')]] - SELECTION FAILED!")

                r = self.final_results(
                    [self.result_df, self.meta_df], SelectError, copy_input=self.copy_input, reduce_df=self.reduce_df
                )

                if "vctype_string" in r.columns:
                    r = r.drop("vctype_string", axis=1)

        except SelectError:
            if self.nofail:
                return pd.DataFrame
            elif self.silent_failure:
                raise SelectError()
            elif self.fail_msg:
                raise SelectError(self.fail_msg)
            else:
                raise

        return r

    def query_builder(self, column_name: str, list_of_data: list):
        """Constructs query conditions based on specified column and data list.

        This method generates query conditions for a specified column using the provided list of data values.
        Each data value is processed to create individual conditions.

        :param column_name: The name of the column to apply the query to.
        :type column_name: str
        :param list_of_data: A list of data values or conditions for filtering the DataFrame.
        :type list_of_data: list
        :param self: The instance of the current class, providing context for the query.
        :return: A list of query conditions.
        :rtype: list
        """
        query_conditions = []
        list_of_data = [list_of_data] if isinstance(list_of_data, str) else list_of_data

        for data in list_of_data:
            condition = statement_builder(data, column_name)
            query_conditions.append(condition)

        return query_conditions

    def statement_builder(data, column_name):
        """Constructs a query statement based on provided data and column name.

        This method builds a query statement string for a given column based on the provided data,
        which can be a single value or a range (tuple). Special cases for specific columns are also handled.

        :param data: The data to build the statement for, which can be a single value or a tuple for ranges.
        :type data: Union[str, tuple]
        :param column_name: The name of the column to apply the condition to.
        :type column_name: str
        :param self: The instance of the current class, providing context for the query.
        :return: A query statement string.
        :rtype: str
        """

        if isinstance(data, tuple):
            # interval case
            interval_start = data[0]
            interval_end = data[1]
            statement = f"{column_name} >= '{interval_start}' & {column_name} <= '{interval_end}'"
            if isinstance(interval_start, (int, float)):
                statement = f"{column_name} >= {min(interval_end, interval_start)} & {column_name} <= {max(interval_end, interval_start)}"

        else:
            # non interval case
            statement = f"{column_name} == '{data}'"
            if isinstance(data, (int, float, bool)):
                statement = f"{column_name} == {data}"

        if column_name == "label":
            statement = label_satement_builder(data)
        if column_name == "etiket":
            statement = ensemble_member_statement_builder(data)

        return statement

    def query_df(self, list_statements: list):
        """Executes a series of query statements on the DataFrame.

        This method applies the given query statements to the DataFrame, taking into account
        the exclusion flag. The results are concatenated and any duplicates are removed.

        :param list_statements: A list of query statements to apply to the DataFrame.
        :type list_statements: list
        :param self: The instance of the current class, providing context for the query.
        :raises SelectError: If any query execution fails and no exclusion is specified.
        """

        temp_df = pd.DataFrame
        for statement in list_statements:
            if self.exclude:
                continue

            self.single_query_df = self.result_df.query(statement)
            if (self.single_query_df).empty and not self.exclude:
                raise SelectError(f"[{Select.__name__}[('{statement}')]] - SELECTION FAILED!")

            temp_df = fstpy.safe_concatenate([self.single_query_df, temp_df])

        query = " | ".join(list_statements)
        query = f"({query})"

        if self.exclude:
            temp_df = self.no_meta_df.query(f"~({query})")

        self.result_df = fstpy.dataframe.drop_duplicates(temp_df)
        self.main_query.append(query)

    def query_meta_df(self, list_meta_statements: list):
        """Executes a series of metadata query statements on the metadata DataFrame.

        This method applies the provided metadata query statements to the metadata DataFrame.
        It handles exclusions and loose matching as specified in the class.

        :param list_meta_statements: A list of metadata query statements to apply.
        :type list_meta_statements: list
        :param self: The instance of the current class, providing context for the query.
        :raises SelectError: If any metadata query execution fails and no exclusion or loose match is specified.
        """
        query_conditions = []
        temp_df = pd.DataFrame

        for statement in list_meta_statements:
            self.single_query_df = self.meta_df.query(statement)
            if (self.single_query_df).empty and not self.exclude and not self.loose_match:
                raise SelectError(f"[{Select.__name__}[('{statement}')]] - SELECTION FAILED!")

            query_conditions.append(statement)
            temp_df = fstpy.safe_concatenate([self.single_query_df, temp_df])

        query = " | ".join(query_conditions)
        query = f"({query})"

        if self.exclude:
            temp_df = self.meta_df.query(f"~({query})")

        if self.loose_match:
            temp_df = self.meta_df.query(f"({query})")

        self.meta_df = fstpy.dataframe.drop_duplicates(temp_df)
        self.metadata_query.append(query)

    def loose_match_surface(self):
        """Executes a loose match on surface data.

        This method filters the `no_meta_df` DataFrame to include only rows where
        the 'surface' column is True. It calculates the minimum 'level' for each
        unique 'nomvar' (name) and merges this information back into the DataFrame
        to select all entries corresponding to that minimum level. The resulting
        DataFrame is concatenated with `result_df`, and duplicates are removed.
        The method also updates the `main_query` attribute to reflect the surface condition.

        :param self: The instance of the current class, providing context for the operation.
        :raises SelectError: If any errors occur during the processing of the DataFrame.
        :return: None: Modifies `result_df` and `main_query` attributes in place."""

        temp_df = self.no_meta_df.query("surface == True")

        min_surface_level = temp_df.groupby(["nomvar", "grid", "dateo", "datev"])["level"].min().reset_index()
        temp_df = self.no_meta_df.merge(min_surface_level, on=["nomvar", "grid", "level", "dateo", "datev"])

        temp_df = fstpy.safe_concatenate([self.result_df, temp_df])
        self.result_df = fstpy.dataframe.drop_duplicates(temp_df)
        self.main_query = self.main_query + " | (surface == True)"

    def check_distinct_values(self):
        """Validates that the distinct values in the result DataFrame match expected counts.

        This method checks whether the number of unique values in each specified column of the result
        DataFrame matches the previously recorded counts. If there is a discrepancy, a `SelectError` is raised.

        :raises SelectError: If the distinct value counts do not match expected values.
        """
        for column in self.count_distinct_dict:
            if self.count_distinct_dict[column]:
                if self.result_df[column].nunique() != self.count_distinct_dict[column]:
                    raise SelectError(f"[{Select.__name__}[('{self.main_query}')]] - SELECTION FAILED!")

    def update_distinct_values(self, column_name):
        """Updates the count of distinct values for a specified DataFrame column.

        This method checks the number of unique values in the specified column of the result DataFrame
        and updates the count in the internal dictionary.

        :param column_name: The name of the column to check for distinct values.
        :type column_name: str
        """
        self.count_distinct_dict[column_name] = self.result_df[column_name].nunique()

    @staticmethod
    def parse_config(args: str) -> dict:
        """method to translate spooki plugin parameters to python plugin parameters
        :param args: input unparsed arguments
        :type args: str
        :return: a dictionnary of converted parameters
        :rtype: dict
        """

        # Cette fonction a ete pris de https://stackoverflow.com/questions/23032514/argparse-disable-same-argument-occurrences
        class UniqueStore(argparse.Action):
            def __call__(self, parser, namespace, values, option_string):
                if getattr(namespace, self.dest, self.default) is not self.default:
                    parser.error(option_string + " appears several times.")
                setattr(namespace, self.dest, values)

        parser = PluginParser(prog=Select.__name__, parents=[Plugin.base_parser], add_help=False)
        parser.add_argument("--abort", type=str, dest="", help="")
        parser.add_argument(
            "--coordinateType", type=str, action=UniqueStore, dest="coordinate_type", help="Coordinate type."
        )
        parser.add_argument(
            "--dateOfOrigin",
            type=str,
            action=UniqueStore,
            dest="date_of_observation",
            help="List of origin dates. (YYYYMMDDHHMMSS).",
        )
        parser.add_argument(
            "--dateOfValidity",
            type=str,
            action=UniqueStore,
            dest="date_of_validity",
            help="List of validity dates. (YYYYMMDDHHMMSS).",
        )
        parser.add_argument(
            "--ensembleMember", type=str, action=UniqueStore, dest="ensemble_member", help="List of ensemble members."
        )
        parser.add_argument(
            "--exclude ",
            action="store_true",
            default=False,
            dest="exclude",
            help="Selects all the records except for those defined by the chosen parameters.",
        )
        parser.add_argument(
            "--failMsg",
            type=str,
            action=UniqueStore,
            dest="fail_msg",
            help="Message to be displayed when Select fails.",
        )
        parser.add_argument("--fieldName", type=str, action=UniqueStore, dest="nomvar", help="List of field names.")
        parser.add_argument(
            "--forecastHour",
            type=str,
            action=UniqueStore,
            dest="forecast_hour",
            help="List of forecast hours in decimal format 3.5 equals 3:30 or in HHH:MM:SS format.",
        )
        parser.add_argument(
            "--looseMatch",
            action="store_true",
            default=False,
            dest="loose_match",
            help="Selects all the records that match any of the chosen parameters.",
        )
        parser.add_argument(
            "--metadataFieldName",
            type=str,
            action=UniqueStore,
            dest="metadata_nomvar",
            help="List of metadata field names.",
        )
        parser.add_argument(
            "--noFail ",
            action="store_true",
            default=False,
            dest="nofail",
            help="Won't fail even if no match were found.",
        )
        parser.add_argument(
            "--noMetadata",
            action="store_true",
            default=False,
            dest="no_metadata",
            help=" No selection of metadata fields e.g. >>, ^^, HY, P0, P0LS, PT, E1, !!, !!SF",
        )
        parser.add_argument(
            "--pdsLabel", type=str, action=UniqueStore, dest="label", help="List of product definition section labels."
        )
        parser.add_argument(
            "--typeOfField", type=str, action=UniqueStore, dest="type_of_field", help="List of types of fields."
        )
        parser.add_argument(
            "--userDefinedIndex",
            type=str,
            action=UniqueStore,
            dest="user_defined_index",
            help="List of indices defined by user.",
        )
        parser.add_argument(
            "--verticalLevel", type=str, action=UniqueStore, dest="vertical_level", help="List of vertical levels."
        )
        parser.add_argument(
            "--verticalLevelType",
            type=str,
            action=UniqueStore,
            choices=VERTICAL_LEVEL_CHOICES,
            dest="vertical_level_type",
            help="Vertical level type.",
        )
        parser.add_argument(
            "--xAxisMatrixSize",
            type=str,
            action=UniqueStore,
            dest="x_axis_matrix_size",
            help="List of X axis matrix sizes.",
        )
        parser.add_argument(
            "--yAxisMatrixSize",
            type=str,
            action=UniqueStore,
            dest="y_axis_matrix_size",
            help="List of Y axis matrix sizes.",
        )
        parser.add_argument(
            "--silentFailure",
            action="store_true",
            dest="silent_failure",
            help="Fail silently if verification is not a success.",
        )

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg["coordinate_type"]:
            parsed_arg["coordinate_type"] = convert_coordinate_type(
                parsed_arg["coordinate_type"], Select.__name__, SelectError
            )

        if parsed_arg["date_of_observation"]:
            parsed_arg["date_of_observation"] = parsed_arg["date_of_observation"].split(",")
            parsed_arg["date_of_observation"] = apply_lambda_to_list(
                parsed_arg["date_of_observation"], lambda a: convert_dates(a, SelectError, "dateOfOrigin")
            )

        if parsed_arg["date_of_validity"]:
            parsed_arg["date_of_validity"] = parsed_arg["date_of_validity"].split(",")
            parsed_arg["date_of_validity"] = apply_lambda_to_list(
                parsed_arg["date_of_validity"], lambda a: convert_dates(a, SelectError, "dateOfValidity")
            )

        if parsed_arg["ensemble_member"]:
            parsed_arg["ensemble_member"] = parsed_arg["ensemble_member"].split(",")

        if parsed_arg["fail_msg"]:
            parsed_arg["fail_msg"] = parsed_arg["fail_msg"].replace("_", " ")

        if parsed_arg["forecast_hour"]:
            parsed_arg["forecast_hour"] = parsed_arg["forecast_hour"].split(",")
            parsed_arg["forecast_hour"] = apply_lambda_to_list(
                parsed_arg["forecast_hour"], lambda a: convert_forecast_hour(a, SelectError)
            )

        if parsed_arg["nomvar"]:
            parsed_arg["nomvar"] = parsed_arg["nomvar"].split(",")
            parsed_arg["nomvar"][:] = [item for item in parsed_arg["nomvar"] if item != ""]
            apply_lambda_to_list(parsed_arg["nomvar"], lambda a: validate_nomvar(a, Select.__name__, SelectError))

        if parsed_arg["metadata_nomvar"]:
            parsed_arg["metadata_nomvar"] = parsed_arg["metadata_nomvar"].split(",")
            validate_list_metadata_nomvar(parsed_arg["metadata_nomvar"], SelectError, "metadata_nomvar")

        if parsed_arg["label"]:
            parsed_arg["label"] = parsed_arg["label"].split(",")

        if parsed_arg["vertical_level"]:
            parsed_arg["vertical_level"] = parsed_arg["vertical_level"].split(",")
            if "SURFACE" not in parsed_arg["vertical_level"]:
                parsed_arg["vertical_level"] = apply_lambda_to_list(
                    parsed_arg["vertical_level"], lambda a: convert_floats(a, Select.__name__, SelectError)
                )

        if parsed_arg["type_of_field"]:
            parsed_arg["type_of_field"] = parsed_arg["type_of_field"].split(",")
            parsed_arg["type_of_field"] = [
                type_of_field_to_typ_var1(field, Select.__name__, SelectError) for field in parsed_arg["type_of_field"]
            ]

        if parsed_arg["user_defined_index"]:
            parsed_arg["user_defined_index"] = parsed_arg["user_defined_index"].split(",")
            parsed_arg["user_defined_index"] = apply_lambda_to_list(
                parsed_arg["user_defined_index"], lambda a: convert_ints(a, SelectError, "userDefinedIndex")
            )

        if parsed_arg["x_axis_matrix_size"]:
            parsed_arg["x_axis_matrix_size"] = parsed_arg["x_axis_matrix_size"].split(",")
            parsed_arg["x_axis_matrix_size"] = apply_lambda_to_list(
                parsed_arg["x_axis_matrix_size"], lambda a: convert_ints(a, SelectError, "xAxisMatrixSize")
            )

        if parsed_arg["y_axis_matrix_size"]:
            parsed_arg["y_axis_matrix_size"] = parsed_arg["y_axis_matrix_size"].split(",")
            parsed_arg["y_axis_matrix_size"] = apply_lambda_to_list(
                parsed_arg["y_axis_matrix_size"], lambda a: convert_ints(a, SelectError, "yAxisMatrixSize")
            )

        return parsed_arg


##### QUERY AND STATEMENT BUILDERS #####


def statement_builder(data, column_name):
    """Constructs a query statement based on provided data and column name.

    This method builds a query statement string for a given column based on the provided data,
    which can be a single value or a range (tuple). Special cases for specific columns are also handled.

    :param data: The data to build the statement for, which can be a single value or a tuple for ranges.
    :type data: Union[str, tuple]
    :param column_name: The name of the column to apply the condition to.
    :type column_name: str
    :param self: The instance of the current class, providing context for the query.
    :return: A query statement string.
    :rtype: str
    """

    if isinstance(data, tuple):
        # interval case
        interval_start = data[0]
        interval_end = data[1]
        statement = f"{column_name} >= '{interval_start}' & {column_name} <= '{interval_end}'"
        if isinstance(interval_start, (int, float)):
            statement = f"{column_name} >= {min(interval_end, interval_start)} & {column_name} <= {max(interval_end, interval_start)}"

    else:
        # non interval case
        statement = f"{column_name} == '{data}'"
        if isinstance(data, (int, float, bool)):
            statement = f"{column_name} == {data}"

    if column_name == "label":
        statement = label_satement_builder(data)
    if column_name == "etiket":
        statement = ensemble_member_statement_builder(data)

    return statement


### DATA CONVERTER FUNCTIONS AND VALIDATION FUNCTIONS ####


class LEVEL_TYPE_T(Enum):
    METER_SEA_LEVEL = 0
    SIGMA = 1
    MILLIBARS = 2
    ARBITRARY_CODE = 3
    METER_GROUND_LEVEL = 4
    HYBRID = 5
    THETA = 6
    MILLIBARS_NEW = 7
    NUMBER = 100
    LEVEL_TYPE_NOT_SET = 999


def convert_coordinate_type(type_of_coordinate, caller_class: str, error_class: type):
    """Converts a coordinate type string into its corresponding internal representation.

    :param type_of_coordinate: The string representation of the coordinate type.
    :type type_of_coordinate: str
    :return: The corresponding internal representation of the coordinate type.
    :rtype: str
    """
    if type_of_coordinate == "ETA_COORDINATE":
        return "ETA_1002"
    elif type_of_coordinate == "SIGMA_COORDINATE":
        return "SIGMA_1001"
    elif type_of_coordinate == "PRESSURE_COORDINATE":
        return "PRESSURE_2001"
    elif type_of_coordinate == "HYBRID_COORDINATE":
        return "HYBRID_5001"
    elif type_of_coordinate == "HYBRID_STAGGERED_COORDINATE":
        return "HYBRID_5002"
    elif type_of_coordinate == "HYBRID_5005_COORDINATE":
        return "HYBRID_5005"
    elif type_of_coordinate == "HYBRID_5100_COORDINATE":
        return "HYBRID_5100"
    elif type_of_coordinate == "UNKNOWN":
        return "UNKNOWN"
    else:
        raise error_class(
            f"WHILE CALLING {caller_class} - USE OF INVALID PARAMETER VALUE {type_of_coordinate}- VALID PARAMETER VALUES FOR --coordinateType ARE [ETA_COORDINATE|SIGMA_COORDINATE|PRESSURE_COORDINATE|HYBRID_COORDINATE|HYBRID_STAGGERED_COORDINATE|HYBRID_5005_COORDINATE|HYBRID_5100_COORDINATE]"
        )


def pattern_to_regex(pattern):
    """Converts a pattern with wildcards into a regular expression.

    :param pattern: The pattern string with '*' and '?' wildcards.
    :type pattern: str
    :return: The regular expression pattern.
    :rtype: str
    """
    # Escape special regex characters (except * and ?)
    pattern = re.escape(pattern)

    # Replace escaped wildcards with regex equivalents
    pattern = pattern.replace(r"\*", ".*")  # '*' becomes '.*' in regex
    pattern = pattern.replace(r"\?", ".")  # '?' becomes '.' in regex
    return f"{pattern}"  # Anchor to match the whole string


def convert_vertical_level_type(vertical_level_type: str):
    """Converts a vertical level type input into its corresponding internal representation.

    :param vertical_level_type: The vertical level type input to convert.
    :type vertical_level_type: str
    :return: The corresponding value for the vertical level type.
    :rtype: int
    """
    try:
        return LEVEL_TYPE_T[vertical_level_type].value
    except KeyError:
        raise SelectError(
            "WHILE CALLING Select - USE OF INVALID PARAMETER VALUE - VALID PARAMETER VALUES FOR --verticalLevelType ARE [SIGMA|MILLIBARS|HYBRID|THETA|METER_GROUND_LEVEL|METER_SEA_LEVEL|ARBITRARY_CODE]"
        )


def convert_topography_to_bool(data):
    """Converts a topography input into a boolean representation.

    :param data: The topography input, which indicates whether to follow topography.
    :type data: str
    :return: True if topography should be followed, False otherwise.
    :rtype: bool
    """
    topography = True
    if data == "NOTFOLLOWTOPOGRAPHY":
        topography = False
    return topography


def ensemble_member_statement_builder(ensemble_member):
    """Constructs a query string for filtering ensemble members.

    :param ensemble_member: The specific ensemble member suffix to filter by.
    :type ensemble_member: str
    :return: A query string that checks if the column values end with the specified member suffix.
    :rtype: str
    """
    return f"etiket.str.endswith('{ensemble_member}')"


def label_satement_builder(label):
    """Constructs a query string for filtering PDS labels.

    :param label: The pattern to match within the PDS label.
    :type label: str
    :return: A query string that checks if the column values contain the specified pattern.
    :rtype: str
    """
    label = pattern_to_regex(label)
    return f"label.str.match('{label}')"


def convert_forecast_hour(forecast_hour: str, error_class=Exception):
    """Converts forecast hour input into a suitable time format.

    :param forecast_hour: The forecast hour input, which can be a single value or a range.
    :type forecast_hour: str
    :return: The converted forecast hour.
    :rtype: Union[timedelta, Tuple[timedelta, timedelta]]
    :raises SelectError: If the input cannot be converted.
    """

    if "@" in forecast_hour:
        forecast_hour = convert_time_range(forecast_hour, error_class)
    else:
        forecast_hour = convert_time(forecast_hour, error_class)

    return forecast_hour


def convert_dates(date: str, error_class=Exception, arg_name=""):
    """Converts date input into a suitable datetime format.

    :param date: The date input, which can be a single value or a range.
    :type date: str
    :return: The converted date(s) as datetime objects.
    :rtype: Union[datetime, Tuple[datetime, datetime]]
    """

    if "@" in date:
        date = convert_date_range(date, error_class, arg_name)
    else:
        date = convert_date(date, error_class, arg_name)

    return date


def convert_date_range(range: str, error_class=Exception, arg_name=""):
    """Converts a date range string into two datetime objects.

    :param range: The date range string to convert.
    :type range: str
    :param error_class: The exception class to raise in case of errors.
    :type error_class: Exception, optional
    :return: A tuple of two datetime objects representing the start and end dates.
    :rtype: Tuple[datetime, datetime]
    """
    dates = range.split("@")
    if len(dates) != 2:
        raise error_class(
            "Range of date should represented by INTEGER[0 to +infinity] @ INTEGER[0 to +infinity]."
            f"Ex: --{arg_name} 20060308000000@20060718000000"
        )
    return (convert_date(dates[0], error_class), convert_date(dates[1], error_class))


def convert_date(date: str, error_class=Exception, arg_name=""):
    """Converts a date string into a datetime object.

    :param date: The date string to convert.
    :type date: str
    :param error_class: The exception class to raise in case of errors.
    :type error_class: Exception, optional
    :return: The converted date as a datetime object.
    :rtype: datetime
    """
    if not is_valid_length_and_digits(date):
        raise error_class(f"Date should be represented by INTEGER[0 to +infinity] Ex: --{arg_name} 20050308000000")
    try:
        converted_date = datetime.strptime(date, "%Y%m%d%H%M%S")
    except ValueError:
        raise error_class(f"{date} should be represented in this format (YYYYMMDDHHMMSS)")

    return converted_date


def is_valid_length_and_digits(date: str):
    """Validates if the date string is exactly 14 digits long.

    :param date: The date string to validate.
    :type date: str
    :return: True if the string is valid, False otherwise.
    :rtype: bool
    """
    # Check if the string contains exactly 14 digits
    return bool(re.fullmatch(r"\d{14}", date))


def convert_ints(data, error_class=Exception, arg_name=""):
    """Converts integer input into a suitable integer format.

    :param data: The integer input, which can be a single value or a range.
    :type data: str
    :return: The converted integer(s).
    :rtype: Union[int, Tuple[int, int]]
    """
    if "@" in data:
        data = convert_int_range(data, error_class, arg_name)
    else:
        data = convert_int(data, error_class, arg_name)

    return data


def convert_int_range(int_range_str, error_class=Exception, arg_name=""):
    """Converts an integer range string into two integer values.

    :param int_range_str: The integer range string to convert.
    :type int_range_str: str
    :return: A tuple of two integers representing the start and end of the range.
    :rtype: Tuple[int, int]
    """
    ints_str = int_range_str.split("@")
    if len(ints_str) != 2:
        raise error_class(
            f"Range of {arg_name} should be represented by INT[0 to +infinity] @ INT[0 to +infinity]. Ex: --{arg_name} 1@5"
        )
    return convert_int(ints_str[0]), convert_int(ints_str[1])


def convert_int(int_str, error_class=Exception, arg_name=""):
    """Converts a string representation of an integer into an actual integer.

    :param int_str: The string to convert.
    :type int_str: str
    :return: The converted integer.
    :rtype: int
    :raises SelectError: If the string cannot be converted to a positive integer.
    """
    try:
        value = int(int_str)
        if value < 0:
            raise error_class("Integer must be positive.")
        return value
    except (error_class, ValueError):
        raise error_class(f"{arg_name} should be represented by INT[0 to +infinity]. Ex: --{arg_name} 1")


def convert_floats(data, error_class=Exception, arg_name=""):
    """Converts float input into a suitable float format.

    :param data: The float input, which can be a single value or a range.
    :type data: str
    :return: The converted float(s).
    :rtype: Union[float, Tuple[float, float]]
    """
    if "@" in data:
        data = convert_float_range(data, error_class, arg_name)
    else:
        data = convert_float(data, error_class, arg_name)

    return data


def convert_float_range(float_range_str, error_class=Exception, arg_name=""):
    """Converts a float range string into two float values.

    :param float_range_str: The float range string to convert.
    :type float_range_str: str
    :return: A tuple of two floats representing the start and end of the range.
    :rtype: Tuple[float, float]
    """
    floats_str = float_range_str.split("@")
    if len(floats_str) != 2:
        raise error_class(
            f"Range of {arg_name} should be represented by FLOAT[0 to +infinity] @ FLOAT[0 to +infinity]. Ex: --{arg_name} 0.85@0.3"
        )
    return convert_float(floats_str[0]), convert_float(floats_str[1])


def convert_float(float_str, error_class=Exception, arg_name=""):
    """Converts a string representation of a float into an actual float.

    :param float_str: The string to convert.
    :type float_str: str
    :return: The converted float.
    :rtype: float
    :raises error_class: If the string cannot be converted to a float.
    """
    try:
        value = float(float_str)
        if value < 0:
            error_class(
                f"{arg_name} should be represented by FLOAT[0 to +infinity] or for --verticalLevel STRING[SURFACE]. Ex: --{arg_name} 1.0 or for --verticalLevel SURFACE"
            )
        return value
    except (error_class, ValueError):
        raise error_class(
            f"{arg_name} should be represented by FLOAT[0 to +infinity] or for --verticalLevel STRING[SURFACE]. Ex: --{arg_name} 1.0 or for --verticalLevel SURFACE"
        )


def validate_list_type_field(list_type_field: Union[List, str], caller_class: str, error_class: type):
    """
    Validates the elements of a list or a string to ensure they are valid strings.

    :param list_type_field: The list or string to validate.
    :type list_type_field: list|str
    :param caller_class: The name of the calling class for error messages.
    :type caller_class: str
    :param error_class: The error class to use for raising exceptions.
    :type error_class: type
    :raises error_class: If an element in the list is not a string or if an element is not in TYPE_OF_FIELD_CHOICES.
    """
    for type_field in list_type_field:
        if not isinstance(type_field, str):
            raise error_class(caller_class + " - type_of_field must be a string")
        if type_field not in TYPE_OF_FIELD_CHOICES:
            raise error_class(
                f"WHILE CALLING {caller_class} - USE OF INVALID PARAMETER VALUE - VALID PARAMETER VALUES FOR --typeOfField ARE {TYPE_OF_FIELD_CHOICES}"
            )


def validate_list_ensemble_member(list_ensemble_member: Union[List, str], caller_class: str, error_class: type):
    """Check that a ensembleMember has min 1 character

    :param list_ensemble_member: list_ensemble_member list of ensemble members to validate
    :type list_ensemble_member: str or list of str
    :param caller_class: a string that indicates the name of the caller class or method
    :type caller_class: str
    :param error_class: The exception to throw if ensembleMember lenght is < 1 or contains other than alphanumeric
    :type error_class: Exception
    :raises error_class: The class of the exception

    MyError: MyClass - ensembleMember must be a string
    """
    for ensemble_member in list_ensemble_member:
        if not isinstance(ensemble_member, str):
            raise error_class(caller_class + " - ensembleMember must be a string")
        pattern = r"^[^\s]+$"
        if not re.match(pattern, ensemble_member):
            raise error_class(caller_class + " - ensembleMember must be 1 or more alphanumeric characters.")


def validate_list_metadata_nomvar(list_metadata_nomvar: Union[List, str], caller_class: str, error_class: type):
    """Check that a ensembleMember is within valid METADATA_FIELD_CHOICES

    :param list_metadata_nomvar:list_metadata_nomvar list of metadata_nomvar
    :type list_metadata_nomvar: str
    :param caller_class: a string that indicates the name of the caller class or method
    :type caller_class: str
    :param error_class: The exception to throw if metdataFieldName is not within valid METADATA_FIELD_CHOICES
    :type error_class: Exception
    :raises error_class: The class of the exception

    MyError: MyClass -metdataFieldName must be a string
    """
    for metadata in list_metadata_nomvar:
        if not isinstance(metadata, str):
            raise error_class(caller_class + " - metadataFieldName must be a string")
        if metadata not in METADATA_FIELD_CHOICES:
            raise error_class(
                f"WHILE CALLING {caller_class} - USE OF INVALID PARAMETER VALUE - VALID PARAMETER VALUES FOR --metadataFieldName ARE {METADATA_FIELD_CHOICES}"
            )


def validate_coordinate_type(coordinate_type: "str", caller_class: str, error_class: type):
    """Validates the coordinate type input.
    Checks if the coordinate type is a string and converts it using the appropriate conversion function.

    :param coordinate_type: The coordinate type to validate.
    :type coordinate_type: str
    :param caller_class: The class name or context for the validation error message.
    :param error_class: Exception class for errors.
    :raises error_class: If validation fails.
    """
    if coordinate_type not in COORDINATE_CHOICES:
        raise error_class(
            f"WHILE CALLING {caller_class} - USE OF INVALID PARAMETER VALUE {coordinate_type} - VALID PARAMETER VALUES FOR --coordinateType ARE {COORDINATE_CHOICES}"
        )


def validate_vertical_level_type(vertical_level_type: "str", caller_class: str, error_class: type):
    """Validates the vertical level type input.
    Checks if the vertical level type is a valid string from predefined choices and converts it
    if necessary, handling special cases for topography.

    :param vertical_level_type: The vertical level type to validate.
    :type vertical_level_type: str
    :param caller_class: The class name or context for the validation error message.
    :param error_class: Exception class for errors.
    :raises error_class: If validation fails.
    :return: The processed vertical level type.
    """
    if not isinstance(vertical_level_type, str) or vertical_level_type not in VERTICAL_LEVEL_CHOICES:
        raise error_class(f"{caller_class} - {str(vertical_level_type)} needs to be a valid verticalLevelType str")

    elif vertical_level_type == "NOTFOLLOWTOPOGRAPHY" or vertical_level_type == "FOLLOWTOPOGRAPHY":
        vertical_level_type = convert_topography_to_bool(vertical_level_type)
        vertical_level_type = [vertical_level_type]
    else:
        vertical_level_type = convert_vertical_level_type(vertical_level_type)

    if isinstance(vertical_level_type, int):
        vertical_level_type = [vertical_level_type]

    return vertical_level_type


def validate_list_label(list_labels: list, caller_class: str, error_class: type):
    """Validates a list of PDS labels.
    Checks if the input is a list of strings.

    :param list_labels: The list of PDS labels to validate.
    :type list_labels: list
    :param caller_class: The class name or context for the validation error message.
    :param error_class: Exception class for errors.
    :raises error_class: If validation fails.
    """
    for label in list_labels:
        if not isinstance(label, str):
            raise error_class(f"{caller_class} - {str(list_labels)} needs to be a str")


def validate_vertical_level(
    levels: Union[List[Union[float, Tuple[float, float]]], str], caller_class: str, error_class: type
):
    """Validates vertical level inputs.

    Checks if the levels are either a string (only 'SURFACE' is allowed) or a list of floats or tuples of floats.

    :param levels: The vertical levels to validate, can be a list or a single string.
    :type levels: Union[List[Union[float, Tuple[float, float]]], str]
    :param caller_class: The class name or context for the validation error message.
    :param error_class: Exception class for errors.
    :raises error_class: If validation fails.
    :return: The validated vertical level levels.
    """


def validate_vertical_level(
    levels: Union[List[Union[float, Tuple[float, float], str]], str], caller_class: str, error_class: type
):
    """Validates vertical level inputs.

    Checks if the levels are either 'SURFACE' (as a string or in a list) or a list of floats or tuples of floats.

    :param levels: The vertical levels to validate.
    :type levels: Union[List[Union[float, Tuple[float, float], str]], str]
    :param caller_class: The class name or context for the validation error message.
    :param error_class: Exception class for errors.
    :raises error_class: If validation fails.
    :return: The validated vertical levels.
    """

    # Check for SURFACE first
    if len(levels) == 1 and levels[0] == "SURFACE":
        return [True]

    # Check if there are any strings in the list - these are not allowed except for SURFACE
    if any(isinstance(item, str) for item in levels):
        raise error_class(
            f"{caller_class} - {str(levels)} only SURFACE is valid string for --verticalLevel, otherwise use floats"
        )

    # If not SURFACE, validate as list of floats
    validate_list_type(levels, float, caller_class, error_class)
    validate_item_range(levels, caller_class, error_class, 0)

    return levels


def validate_list_type(values, data_type: type, caller_class: str, error_class: type):
    """Validates the type of list elements.

    Checks if the values are either of a specified data type or tuples containing
    two elements of that data type.

    :param values: The value(s) to validate, which can be a single value or a list of values.
    :type values: Union[List[Union[data_type, Tuple[data_type, data_type]]], data_type]
    :param data_type: The expected type of the elements in the list.
    :type data_type: type
    :param caller_class: The class name or context for the validation error message.
    :param error_class: Exception class for errors.
    :raises error_class: If any value is not of the specified data type or a valid tuple.
    :return: A list containing the validated values.
    :rtype: List[Union[data_type, Tuple[data_type, data_type]]
    """

    for value in values:
        # Validate that the value is either of the expected type or a valid tuple
        if isinstance(value, data_type):
            continue
        elif isinstance(value, tuple) and len(value) == 2:
            if not all(isinstance(v, data_type) for v in value):
                raise error_class(
                    f"{caller_class} - Tuple elements must be of type {data_type.__name__}. Invalid tuple: {value}"
                )
        else:
            raise error_class(
                f"{caller_class} - Each item must be of type {data_type.__name__} or a tuple of two elements of type {data_type.__name__}. Invalid value: {value}"
            )


def validate_item_range(list, caller_class: str, error_class: type, min_range=None, max_range=None):
    """Validates the range of items in a list.

    Checks if the items are within specified minimum and maximum ranges, allowing for
    tuples of two values to be validated as well.

    :param list: The list of values to validate, which can include tuples.
    :type list: List[Union[float, Tuple[float, float]]]
    :param caller_class: The class name or context for the validation error message.
    :param error_class: Exception class for errors.
    :param min_range: The minimum allowed value. Defaults to None.
    :type min_range: Optional[float]
    :param max_range: The maximum allowed value. Defaults to None.
    :type max_range: Optional[float]
    :raises error_class: If any value or tuple of values is outside the specified range.
    :return: None. This function raises an exception if validation fails.
    """

    for value in list:
        if isinstance(value, tuple) and len(value) == 2:
            val1, val2 = value
            if min_range is not None and (val1 < min_range or val2 < min_range):
                raise error_class(
                    f"{caller_class}: {value} tuple should have both values greater or equal to {min_range}"
                )
            if max_range is not None and (val1 > max_range or val2 > max_range):
                raise error_class(
                    f"{caller_class}: {value} tuple should have both values smaller or equal to {max_range}"
                )
            continue

        if min_range is not None and value < min_range:
            raise error_class(f"{caller_class}: {value} should be greater or equal than {min_range}")
        if max_range is not None and value > max_range:
            raise error_class(f"{caller_class}: {value} should be smaller or equal than {max_range}")


def ensure_list_attributes(self):
    """
    Ensures that certain attributes of the object are lists. If an attribute is not a list, it converts it to a list.

    :param self: The object instance.
    :type self: object
    :return: None. This function modifies the object's attributes in place.
    :rtype: None
    """
    attributes = [
        "date_of_observation",
        "date_of_validity",
        "metadata_nomvar",
        "label",
        "x_axis_matrix_size",
        "y_axis_matrix_size",
        "forecast_hour",
        "user_defined_index",
        "ensemble_member",
        "type_of_field",
        "list_of_nomvar",
        "vertical_level",
    ]

    for attr in attributes:
        # searches for self + attr returns None if not found
        value = getattr(self, attr, None)
        if value is not None and not isinstance(value, list):
            setattr(self, attr, [value])
