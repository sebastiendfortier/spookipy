import argparse
import re
import warnings

import spookipy
import fstpy
import pandas as pd


from ..plugin import Plugin, PluginParser
from ..utils import initializer


class ReaderStdError(Exception):
    pass


class ReaderStd(Plugin):
    """
    Initializes an instance of the ReaderStd class.

    This constructor sets up the ReaderStd object with various parameters, including the input file,
    query conditions, and additional processing options. If `etiket_format` is provided, a warning is issued,
    as its functionality is not yet implemented.

    :param df: A Pandas DataFrame to initialize the instance with. If None, data will be loaded from input files.
    :type df: pd.DataFrame, optional
    :param input: Path to the input file or a list of files to be read.
    :type input: str, optional
    :param query: A query string to filter data from the input file(s).
    :type query: str, optional
    :param etiket_format: Format specification for etiket fields. (Currently not implemented.)
    :type etiket_format: str, optional
    :param group5005: Whether to apply special grouping for records labeled 5005.
    :type group5005: bool, optional
    :param reduce_df: Whether to apply a reduction operation on the final DataFrame.
    :type reduce_df: bool, optional

    :raises ReaderStdError: If the input parameter is None or invalid.
    """

    @initializer
    def __init__(
        self,
        df: pd.DataFrame = None,
        input: str = None,
        query: str = None,
        etiket_format: str = None,
        group5005=False,
        reduce_df=False,
    ):
        if etiket_format is not None:
            warnings.warn("etiket_format has yet to be implemented !")
        self.validate_params()
        # TODO etiket_format force la lecture en ce moment ex : [ReaderStd --input {sources[0]} --etiketFormat 1,6,1,3]

    def validate_params(self):
        """Validates the parameters provided during initialization.

        This method checks each parameter against predefined validation functions,
        ensuring that they conform to expected types and formats. If any validation
        fails, a `ReaderStdError` .

        :raises ReaderStdError: If any parameter validation fails"""

        if self.input is None:
            raise ReaderStdError("Input should not be empty!")

    def modify_5005(self):
        """Wrapper function for modfify_5005_record that adds ip_info and flag5005 columns"""

        df = fstpy.add_columns(df, "ip_info")
        df["flag5005"] = True
        spookipy.modify_5005_record(df)

    def compute(self) -> pd.DataFrame:
        """Abstract method that should implement the plugin's algorithm.

        :return: dataframe with the results
        :rtype: pd.DataFrame
        """

        df_list = []
        if not isinstance(self.input, list):
            self.input = [self.input]

        for path in self.input:
            if self.query:
                temp_df = fstpy.StandardFileReader(path, query=self.query).to_pandas()

            else:
                temp_df = fstpy.StandardFileReader(path).to_pandas()

            df_list.append(temp_df)

        if self.df is None:
            result_df = fstpy.safe_concatenate(df_list)

        else:
            self.get_dataframes()
            result_df = self.final_results(df_list, ReaderStd, copy_input=True, reduce_df=self.reduce_df)

        return fstpy.add_columns(result_df, "unit")

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

        parser = PluginParser(prog=ReaderStd.__name__, parents=[Plugin.base_parser], add_help=False)

        parser.add_argument(
            "--input",
            type=str,
            nargs="+",
            action=UniqueStore,
            dest="input",
            required=True,
            help="Output file name\nEx: --input /tmp/output.std",
        )
        parser.add_argument(
            "--query", type=str, dest="query", help="Simple query for entry file\nEx: --query nomvar=='UU'"
        )
        parser.add_argument("--silentFailure", type=str, help="Fail silently if verification is not a success.")
        parser.add_argument(
            "--etiketFormat",
            type=str,
            dest="etiket_format",
            help="Define etiket format(length of each part): RUNID,PDSLABEL,IMPLEMENTATION,MEMBER.Will be written back by WriterStd with the same format.",
        )
        for action in parser._actions:
            if action.dest == "copy_input":
                action.help = (
                    f"[Doesn't do anything.] {action.help} It is already the default behavior for {ReaderStd.__name__}"
                )

        parsed_arg = vars(parser.parse_args(args.split()))

        return parsed_arg
