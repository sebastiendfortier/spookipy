Description:
~~~~~~~~~~~~

-  Generic plugin used by other plugins to apply specific operations on a column of data

Iteration method:
~~~~~~~~~~~~~~~~~

-  Column-by-Column

Dependencies:
~~~~~~~~~~~~~

-  At least 1 3d field

Result(s):
~~~~~~~~~~

-  A 2d field with the result of the operation

Algorithm:
~~~~~~~~~~

-  Does not apply

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, generique/generic, colonne/column

Usage:
~~~~~~

.. code:: python

    import os
    import fstpy
    import spookipy
    import numpy as np

    class MultiplyElementsByPointError(Exception):
        pass

    spooki_dir  = os.environ['SPOOKI_DIR']
    tmpdir      = os.environ['BIG_TMPDIR']

    input_file  = (f'{spooki_dir}/pluginsRelatedStuff/MultiplyElementsByPoint/testsFiles/inputFile.std')
    output_file = (f'{tmpdir}/outputFile.std')

    df = fstpy.StandardFileReader(input_file).to_pandas()

    res_df = spookipy.OpElementsByColumn(df,
                                        operator=np.prod,
                                        operation_name='MultiplyElementsByPoint',
                                        exception_class=MultiplyElementsByPointError,
                                        group_by_forecast_hour=True,
                                        group_by_level=True,
                                        nomvar_out='MUEP',
                                        etiket='MULEPT').compute()

    fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author   : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support  : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

