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

   import os
   import fstpy
   import spookipy

   spooki_dir     = os.environ['SPOOKI_DIR']
   spooki_out_dir = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/SubtractElementsVertically/testsFiles/inputFile.std')
   output_file = (f'{spooki_out_dir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   res_df = spookipy.SubtractElementsVertically(df, direction='ascending').compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author   : `Hatem Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
             `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginSubtractElementsVertically.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginSubtractElementsVertically.html>`_
