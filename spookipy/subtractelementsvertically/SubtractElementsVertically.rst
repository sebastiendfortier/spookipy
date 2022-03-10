Description:
~~~~~~~~~~~~

-  From a field value for a chosen level (either the lowest or the highest), subtract the values from all the other levels of the same field.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Column-by-column

Dependencies:
~~~~~~~~~~~~~

-  At least one 3D field

Result(s):
~~~~~~~~~~

-  A 2D field with the same name as the input field

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

-  UTILITAIRE/UTILITY, soustraire/subtract, soustraction/subtraction, verticale/vertical


Usage:
~~~~~~

.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/SubtractElementsVertically/testsFiles/inputFile.std').to_pandas()

   res_df = spooki.SubtractElementsVertically(df, direction='ascending').compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Hatem Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
   `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginSubtractElementsVertically.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginSubtractElementsVertically.html>`_
