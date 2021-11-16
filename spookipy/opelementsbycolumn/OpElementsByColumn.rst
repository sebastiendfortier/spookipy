Description:
============

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

    python3
    
    import os
    import fstpy.all as fstpy
    import spookipy.all as spooki

    spooki_dir = os.environ['SPOOKI_DIR']

    user = os.environ['USER']

    df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MultiplyElementsByPoint/testsFiles/inputFile.std').to_pandas()

    res_df = spooki.OpElementsByColumn(df,
                                        operator=np.prod,
                                        operation_name='MultiplyElementsByPoint',
                                        exception_class=MultiplyElementsByPointError,
                                        group_by_forecast_hour=True,
                                        group_by_level=True,
                                        nomvar_out='MUEP',
                                        etiket='MULEPT').compute()

    fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

