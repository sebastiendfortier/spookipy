Description:
~~~~~~~~~~~~

-  

Iteration method:
~~~~~~~~~~~~~~~~~

-  Column-by-column

Dependencies:
~~~~~~~~~~~~~

-  At least one 3D field

Result(s):
~~~~~~~~~~

-  A 2D field with the stat name for each requested stat

Algorithm:
~~~~~~~~~~

.. code-block:: text

         For k the chosen level

            If direction = "ASCENDING" then
               A = A[k] - A[k+1] - A[k+2] - ...
            Else
               A = A[k] - A[k-1] - A[k-2] - ...
            End if

Reference:
~~~~~~~~~~

-  None

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, soustraire/subtract, statistique/statistic, verticale/vertical


Usage:
~~~~~~

.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/SubtractElementsVertically/testsFiles/inputFile.std').to_pandas()

   res_df = spookipy.SubtractElementsVertically(df, direction='ascending').compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : Ronald Frenette
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Does not apply
