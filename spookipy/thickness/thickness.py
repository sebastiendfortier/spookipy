import logging
import fstpy

from ..plugin import Plugin, PluginParser
import pandas as pd
import numpy as np

from ..utils import (
    create_empty_result,
    existing_results,
    get_dependencies,
    get_existing_result,
    get_from_dataframe,
    initializer,
    DependencyError,
)


class ThicknessError(Exception):
    pass


class VctypesError(Exception):
    pass


class ParametersValuesError(Exception):
    pass


class Thickness(Plugin):
    """Check that the vertical coordinate type of the input field corresponds to the "coordinate_type" key passed as a parameter

    if so, look in the input field for the levels passed as a parameter and do at each point:

    DZ = ABS ( GZ(top) - GZ(base) )

    rename the values concerned (nomvar) without changing other values

    cordinate type from fstpy.VerticalCoordType:

    'SIGMA_1001': SIGMA_COORDINATE

    'ETA_1002': ETA_COORDINATE

    "PRESSURE_2001": PRESSURE_COORDINATE

    "HYBRID_5001": HYBRID_COORDINATE

    "HYBRID_5002": HYBRID_STAGGERED_COORDINATE

    "UNKNOWN": UNKNOWN,


    :param df: dataframe with the data
    :type df: pd.DataFrame
    :param base: Base of the thickness layer (model or pressure level)
    :type base: float
    :param top: Top of the thickness layer (model or pressure level)
    :type top: float
    :param coordinate_type: Type of vertical coordinate. choices: SIGMA_1001, ETA_1002, PRESSURE_2001,HYBRID_5001,UNKNOWN
    :type coordinate_type: str
    :param dependency_check: Indicates the plugin is being called from another one who checks dependencies , defaults to False
    :type dependency_check: bool, optional
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """

    computable_plugin = "DZ"

    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        base: float,
        top: float,
        coordinate_type: str,
        dependency_check=False,
        copy_input=False,
        reduce_df=True,
    ):
        self.plugin_mandatory_dependencies = [{"GZ": {"nomvar": "GZ", "unit": "dam"}}]

        self.plugin_result_specifications = {"DZ": {"nomvar": "DZ", "unit": "dam", "label": "THCKNS"}}

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
        self.verify_parameters_values()
        self.no_meta_df = fstpy.add_columns(self.no_meta_df, columns=["ip_info"])
        self.existing_result_df = get_existing_result(self.no_meta_df, self.plugin_result_specifications)
        self.groups = self.no_meta_df.groupby(["grid", "datev", "dateo", "vctype"])

    def verify_parameters_values(self):
        self.verify_top_base_values()
        self.verify_vctype()

    def verify_vctype(self):
        """Verify that the type of vertical coordinates is accurate

        :raises VctypesError: raises an error when the type of vertical coordinates is not accurate
        """

        if self.coordinate_type not in fstpy.vctype_dict.keys():
            raise VctypesError("The vctypes values in the dataframe are not supported")
        else:
            self.coordinate = fstpy.vctype_dict[self.coordinate_type]

    def verify_top_base_values(self):
        """Verify that the top and base values are not negative or equal to the other value"""

        if any(x <= 0 for x in [self.base, self.top]):
            raise ParametersValuesError("The base value or the top value is negative")
        elif self.base == self.top:
            raise ParametersValuesError("The base value is equal to the top value")
        else:
            return True

    def compute(self) -> pd.DataFrame:
        # If a row DZ already exists in the dataframe we return the result
        if not self.existing_result_df.empty:
            return existing_results("Thickness", self.existing_result_df, self.meta_df)

        logging.info("Thickness - compute")
        df_list = []

        try:
            # self.plugin_mandatory_dependencies[0]["GZ"]["vctype"]=self.coordinate
            gz_dict = self.plugin_mandatory_dependencies[0]["GZ"]
            gz_dict["vctype"] = self.coordinate

            dependencies_list = get_dependencies(
                self.groups, self.meta_df, "Thickness", self.plugin_mandatory_dependencies, intersect_levels=False
            )

        except DependencyError:
            if not self.dependency_check:
                raise DependencyError(f"{Thickness} - No matching dependencies found")

        else:
            for dependencies_df, _ in dependencies_list:
                gz_df = get_from_dataframe(dependencies_df, "GZ")
                gz_df.level = gz_df.level.astype("float32")
                gz_top_df = gz_df.loc[np.isclose(gz_df.level, self.top)]
                top_ip = gz_top_df.iloc[0].level
                gz_base_df = gz_df.loc[np.isclose(gz_df.level, self.base)]
                base_ip = gz_base_df.iloc[0].level

                if self.base < self.top:
                    b_inf = top_ip
                    b_sup = base_ip
                else:
                    b_inf = base_ip
                    b_sup = top_ip

                dz_df = create_result_container(gz_df, b_inf, b_sup, self.plugin_result_specifications)

                array = np.abs(gz_top_df.iloc[0].d - gz_base_df.iloc[0].d).astype(np.float32)
                dz_df["d"] = [array]

                df_list.append(dz_df)

        finally:
            return self.final_results(
                df_list,
                ThicknessError,
                dependency_check=self.dependency_check,
                copy_input=self.copy_input,
                reduce_df=self.reduce_df,
            )

    @staticmethod
    def parse_config(args: str) -> dict:
        parser = PluginParser(prog=Thickness.__name__, parents=[Plugin.base_parser], add_help=False)
        # parser.add_argument('--df',pd.DataFrame,help="dataframe with the data")
        parser.add_argument(
            "--base", type=float, dest="base", help="Base of the thickness layer (model or pressure level)"
        )
        parser.add_argument(
            "--top", type=float, dest="top", help="Top of the thickness layer (model or pressure level)"
        )
        parser.add_argument(
            "--coordinateType",
            type=str,
            dest="coordinate_type",
            choices=[
                "SIGMA_COORDINATE",
                "HYBRID_COORDINATE",
                "ETA_COORDINATE",
                "PRESSURE_COORDINATE",
                "UNKNOWN",
                "HYBRID_STAGGERED_COORDINATE",
            ],
            help="Type of vertical coordinate",
        )

        parsed_arg = vars(parser.parse_args(args.split()))

        if parsed_arg["base"] < 0:
            raise ThicknessError("The base of the thickness layer has to be positive")

        if parsed_arg["top"] < 0:
            raise ThicknessError("The top of the thickness layer has to be positive")

        if parsed_arg["coordinate_type"] == "SIGMA_COORDINATE":
            parsed_arg["coordinate_type"] = parsed_arg["coordinate_type"].replace("COORDINATE", "1001")

        if parsed_arg["coordinate_type"] == "ETA_COORDINATE":
            parsed_arg["coordinate_type"] = parsed_arg["coordinate_type"].replace("COORDINATE", "1002")

        if parsed_arg["coordinate_type"] == "PRESSURE_COORDINATE":
            parsed_arg["coordinate_type"] = parsed_arg["coordinate_type"].replace("COORDINATE", "2001")

        if parsed_arg["coordinate_type"] == "HYBRID_COORDINATE":
            parsed_arg["coordinate_type"] = parsed_arg["coordinate_type"].replace("COORDINATE", "5001")

        if parsed_arg["coordinate_type"] == "HYBRID_STAGGERED_COORDINATE":
            parsed_arg["coordinate_type"] = parsed_arg["coordinate_type"].replace("STAGGERED_COORDINATE", "5002")

        return parsed_arg


def create_result_container(df, b_inf, b_sup, result_specifications):
    ip1 = b_inf
    ip3 = b_sup
    kind = int(df.iloc[0].ip1_kind)

    inter = fstpy.Interval("ip1", ip1, ip3, kind)

    result_specifications["DZ"]["interval"] = inter
    res_df = create_empty_result(df, result_specifications["DZ"])

    return res_df
