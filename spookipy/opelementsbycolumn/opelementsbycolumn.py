# -*- coding: utf-8 -*-
import logging

import datetime
import fstpy
import numpy as np
import pandas as pd

from ..plugin import Plugin
from ..utils import (
    create_empty_result,
    get_3d_array,
    find_intersecting_levels,
    initializer,
    validate_nomvar,
    LevelIntersectionError,
)


class OpElementsByColumnError(Exception):
    pass


class OpElementsByColumn(Plugin):
    """Generic plugin used by other plugins to apply specific operations on a column of data

    :param df: input DataFrame
    :type df: pd.DataFrame
    :param operator: function to apply on a column of data
    :type operator: function
    :param operation_name: name of operation to display for logging, defaults to 'OpElementsByColumn'
    :type operation_name: str, optional
    :param exception_class: exception to raise, defaults to OpElementsByColumnError
    :type exception_class: type, optional
    :param group_by_forecast_hour: group fields by forecast hour, defaults to False
    :type group_by_forecast_hour: bool, optional
    :param group_by_level: group fields by level, defaults to False
    :type group_by_level: bool, optional
    :param nomvar_out: nomvar to apply to results, defaults to None
    :type nomvar_out: str, optional
    :param plugin_nomvar_out: nomvar from the calling plugin, to apply to results, defaults to 'OPEC'
    :type nomvar_out: str, optional
    :param unit: unit to apply to results, defaults to '1' (dimensionless)
    :type unit: str, optional
    :param label: label to apply to results, defaults to None (keep the same label)
    :type label: str, optional
    :param copy_input: Indicates that the input fields will be returned with the plugin results , defaults to False
    :type copy_input: bool, optional
    :param reduce_df: Indicates to reduce the dataframe to its minimum, defaults to True
    :type reduce_df: bool, optional
    """

    @initializer
    def __init__(
        self,
        df: pd.DataFrame,
        operator,
        operation_name="OpElementsByColumn",
        exception_class=OpElementsByColumnError,
        group_by_forecast_hour=False,
        group_by_level=False,
        group_by_nomvar=False,
        group_by_ensemble_member=False,
        plugin_nomvar_out="OPEC",
        nomvar_out=None,
        unit="1",
        label=None,
        copy_input=False,
        reduce_df=True,
    ):
        if self.nomvar_out is not None:
            if self.group_by_nomvar:
                raise self.exception_class(
                    self.operation_name + " - cannot use nomvar_out option with group_by_nomvar \n"
                )
        else:
            self.nomvar_out = plugin_nomvar_out

        validate_nomvar(self.nomvar_out, self.operation_name, self.exception_class)

        self.plugin_result_specifications = {"ALL": {"nomvar": self.nomvar_out, "unit": self.unit}}

        if self.label:
            self.plugin_result_specifications["ALL"]["label"] = self.label

        self.df = fstpy.metadata_cleanup(self.df)
        super().__init__(self.df)
        self.prepare_groups()

    def prepare_groups(self):
        if len(self.no_meta_df) == 1:
            raise self.exception_class(self.operation_name + " - not enough records to process, need at least 2")

        self.no_meta_df = fstpy.add_columns(
            self.no_meta_df, columns=["forecast_hour", "ip_info", "unit", "flags", "etiket"]
        )

        # Groupement seulement sur la grille pour determiner les groupes avec niveaux communs
        grouping = ["grid"]
        self.groups = self.no_meta_df.groupby(by=grouping[0])

        all_group_df = pd.DataFrame()
        for _, current_group in self.groups:
            # Un seul champ dans le groupe
            if len(current_group.index) == 1:
                continue

            try:
                group_df = find_intersecting_levels(current_group)
            except LevelIntersectionError:
                raise self.exception_class(self.operation_name + " - not enough records to process, need at least 2")
            else:
                if not (group_df.empty):
                    all_group_df = pd.safe_concat([all_group_df, group_df])
                else:
                    logging.warning(
                        f"\n\nNo common levels for this group: \n{current_group[['nomvar', 'typvar', 'ni', 'nj', 'nk', 'ip1']]} \n"
                    )

        # Formation des groupes selon les criteres demandes a l'appel
        if self.group_by_nomvar:
            grouping.append("nomvar")

        if self.group_by_forecast_hour:
            items_to_add = ["datev", "dateo"]
            grouping.extend(items_to_add)

        if self.group_by_level:
            grouping.append("level")

        if self.group_by_ensemble_member:
            grouping.append("ensemble_member")

        if not (all_group_df.empty):
            self.groups = all_group_df.groupby(by=grouping)
        else:
            raise self.exception_class(self.operation_name + " -  invalid input !")

    def compute(self) -> pd.DataFrame:
        logging.info("OpElementsByColumn - compute")
        # holds data from all the groups
        df_list = []
        for _, current_group in self.groups:
            current_group.sort_values(by=["nomvar", "dateo", "datev"], inplace=True)
            if len(current_group.index) == 1:
                logging.warning("need more than one field for this operation - skipping")
                continue

            if self.group_by_nomvar:
                self.plugin_result_specifications["ALL"]["nomvar"] = current_group.iloc[0].nomvar
                if not self.group_by_forecast_hour:
                    self.plugin_result_specifications["ALL"]["ip2"] = [0]
                    self.plugin_result_specifications["ALL"]["forecast_hour"] = datetime.timedelta(0)
                    self.plugin_result_specifications["ALL"]["npas"] = [0]

            # Si champs masque avec son mask, on ne veut pas conserver les flags pour le typvar lors de la multiplication
            # Reproduction du comportement en CPP
            if self.operation_name == "MultiplyElementsByPoint":
                if current_group["masked"].any() and current_group["masks"].any():
                    # On veut conserver le 1er caractere du typvar d'un des champs masques et non d'un mask
                    self.plugin_result_specifications["ALL"]["typvar"] = current_group.loc[
                        current_group["masked"] == True, "typvar"
                    ].iloc[0]
                    self.plugin_result_specifications["ALL"]["masked"] = False
                    self.plugin_result_specifications["ALL"]["masks"] = False

            res_df = create_empty_result(current_group, self.plugin_result_specifications["ALL"])

            array_3d = get_3d_array(current_group)

            if np.issubdtype(self.operator(array_3d, axis=0).dtype, np.integer):
                res_df["datyp"] = 2
                res_df.at[0, "d"] = self.operator(array_3d, axis=0).astype(np.int32)
            elif np.issubdtype(self.operator(array_3d, axis=0).dtype, np.floating):
                res_df["datyp"] = 5
                res_df.at[0, "d"] = self.operator(array_3d, axis=0).astype(np.float32)

            # Met le nombre de bits a 32 pour eviter les erreurs de conversion
            res_df["nbits"] = 32

            df_list.append(res_df)

        return self.final_results(df_list, self.exception_class, copy_input=self.copy_input, reduce_df=self.reduce_df)
