# -*- coding: utf-8 -*-
import os
import rpnpy.librmn.all as rmn

HOST_NUM = os.getenv("TRUE_HOST")[-1]
USER = os.getenv("USER")
TEST_PATH = "/fs/site%s/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"%HOST_NUM
TMP_PATH = "/fs/site%s/eccc/cmd/w/%s/spooki_tmpdir/"%(HOST_NUM,USER)

def convip(df,nomvar='',style=rmn.CONVIP_ENCODE):
    def convertip(df,i):
        ip1 = df.at[i,'ip1']
        (val, kind) = rmn.convertIp(rmn.CONVIP_DECODE, int(ip1))
        if kind != -1:
            df.at[i,'ip1'] = rmn.convertIp(style, val, kind)

    for i in df.index:
        if nomvar != '':
            if df.at[i,'nomvar'] == nomvar:
                convertip(df,i)
        else:
            convertip(df,i)
    return df        