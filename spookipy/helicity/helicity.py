# -*- coding: utf-8 -*-
from ..plugin import Plugin
from ..utils import create_empty_result, get_existing_result, get_intersecting_levels, get_plugin_dependencies, existing_results, final_results
import pandas as pd
import fstpy.all as fstpy
import numpy as np
import sys


class HelicityError(Exception):
    pass


class Helicity(Plugin):
    plugin_mandatory_dependencies = {
        'UU':{'nomvar':'UU','unit':'knot'},
        'VV':{'nomvar':'VV','unit':'knot'},
    }
    plugin_result_specifications = {
        'UV':{'nomvar':'UV','etiket':'WNDMOD','unit':'knot'}
        }

    def __init__(self,df:pd.DataFrame):
        self.df = df
        #ajouter forecast_hour et unit
        self.validate_input()

    # might be able to move
    def validate_input(self):
        if self.df.empty:
            raise  HelicityError('No data to process')

        self.df = fstpy.metadata_cleanup(self.df)

        self.meta_df = self.df.loc[self.df.nomvar.isin(["^^",">>","^>", "!!", "!!SF", "HY","P0","PT"])].reset_index(drop=True)

        self.df = fstpy.add_composite_columns(self.df,True,'numpy', attributes_to_decode=['unit','forecast_hour','ip_info'])

         #check if result already exists
        self.existing_result_df = get_existing_result(self.df,self.plugin_result_specifications)

        if self.existing_result_df.empty:
            self.dependencies_df = get_plugin_dependencies(self.df,None,self.plugin_mandatory_dependencies)
            if self.dependencies_df.empty:
                raise HelicityError('No data to process')
            self.fhour_groups=self.dependencies_df.groupby(by=['grid','forecast_hour'])


    def compute(self) -> pd.DataFrame:
        if not self.existing_result_df.empty:
            return existing_results('Helicity',self.existing_result_df,self.meta_df)

        sys.stdout.write('Helicity - compute\n')
        df_list = []
        for _,current_fhour_group in self.fhour_groups:
            current_fhour_group = get_intersecting_levels(current_fhour_group,self.plugin_mandatory_dependencies)
            if current_fhour_group.empty:
                sys.stderr.write('Helicity - no intersecting levels found')
                continue
            current_fhour_group = fstpy.load_data(current_fhour_group)
            uu_df = current_fhour_group.loc[current_fhour_group.nomvar=="UU"].reset_index(drop=True)
            vv_df = current_fhour_group.loc[current_fhour_group.nomvar=="VV"].reset_index(drop=True)
            uv_df = create_empty_result(vv_df,self.plugin_result_specifications['UV'],copy=True)


            for i in uv_df.index:
                uu = uu_df.at[i,'d']
                vv = vv_df.at[i,'d']
                # uv_df.at[i,'d'] = wind_modulus(uu,vv)

            df_list.append(uv_df)

        return final_results(df_list,HelicityError, self.meta_df)

    # struct helicity
    # {
    #     helicity(boost::function<void (void)> f): _f(f) {}
    #     void operator()
    #     (
    #             const vector<IFlatSlice<float>::iterator> & UUNcarrot,
    #             const vector<IFlatSlice<float>::iterator> & VVNcarrot,
    #             const vector<IFlatSlice<float>::iterator> & GZcarrot,
    #             const float & CX,
    #             const float & CY,
    #             const float & Z2,
    #             float & HL
    #     )
    #     {
    #         SPOOKI_ASSERT(UUNcarrot.size() == VVNcarrot.size());
    #         _f();
    #         size_t UUNSize(UUNcarrot.size());
    #         const float & UUNZ1(*(UUNcarrot[0])), UUNZ2(*(UUNcarrot[size_t(Z2)]));
    #         const float & VVNZ1(*(VVNcarrot[0])), VVNZ2(*(VVNcarrot[size_t(Z2)]));
    #         const float & GZZ1(*(GZcarrot[0])), GZZ2(*(GZcarrot[size_t(Z2)]));
    #         float HL1 = ((VVNZ2 - VVNZ1) *  CX) - ((UUNZ2 - UUNZ1) * CY) ;
    #         float HL0(0);

    #         for (size_t Z(0); Z <= (size_t)Z2; ++Z)
    #         {
    #             if((Z + 1) == ((size_t)Z2 + 1) or Z + 1 > UUNSize)
    #             {
    #                 break;
    #             }
    #             const float & UUNZ(*(UUNcarrot[Z])), UUNZP(*(UUNcarrot[Z + 1])), VVNZ(*(VVNcarrot[Z])), VVNZP(*(VVNcarrot[Z + 1]));
    #             HL0 += (UUNZP * VVNZ) - (UUNZ * VVNZP);
    #         }

    #         HL = (HL0 + HL1)*(300/(GZZ2-GZZ1));
    #     }
    #     boost::function<void (void)> _f;
    # };
