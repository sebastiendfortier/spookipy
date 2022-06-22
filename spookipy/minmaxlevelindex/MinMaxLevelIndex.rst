Description:
~~~~~~~~~~~~

-  Finds the index of the maximum and/or minimum value in the column or part of it.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Column by column

Dependencies:
~~~~~~~~~~~~~

-  Meteorological field (3D)
   
   If the -bounded key is activated:
-  Field of indices of the lower limit, KBAS
-  Field of indices of the upper limit, KTOP

Result(s):
~~~~~~~~~~

-  The meteorological field (3D) received as input
-  A field with the indices, KMIN (2D), for which the value of the meteorological field is minimum
   *and/or*
-  A field with the indices, KMAX (2D), for which the value of the meteorological field is maximum

Algorithm:
~~~~~~~~~~

.. code-block:: text

   If the key --bounded is not activated :
         KBAS = lowest level in the column
         KTOP = highest level in the column

   For each column and for the levels between KBAS and KTOP:
   (this is done from bottom to top or from top to bottom depending on the "--direction" option)

         If (minMax = MIN or BOTH)
            Loop for k between KBAS and KTOP
               If min > VAR[k] then 
                  min = VAR[k]
                  KMIN = k
               End if
            End loop
         End if

         If (minMax = MAX or BOTH)
            Loop for k between KBAS and KTOP
               If max < VAR[k] then 
                  max = VAR[k] 
                  KMAX = k
               End if
            End loop
         End if


   Notes:

   -  If several identical values of the max or min are found in a column, the first occurrence will 
      be considered the min or the max. Depending on the "--direction" option, it will be
      the highest or lowest occurrence in the sample.
   -  When the values of KBAS and KTOP are equal to -1 (fields needed when using the "--bounded" option),
      the column will be ignored and the returned value will be -1.

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~
-  UTILITAIRE/UTILITY, minimum, maximum, niveau/level, vertical, borné/bounded

Usage:
~~~~~~

.. code:: python

   python3
   
   import os
   import fstpy
   import spookipy

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MinMaxLevelIndex/testsFiles/inputFile.std').to_pandas()

   res_df = spookipy.MinMaxLevelIndex(df, min=True, nomvar="UU", ascending=True).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


.. code:: python

   python3
   
   import os
   import fstpy
   import spookipy

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MinMaxLevelIndex/testsFiles/inputFile.std').to_pandas()

   minidx_df = spookipy.SetConstantValue(df, min_index=True, nomvar_out='KBAS', bi_dimensionnal=True).compute()

   maxidx_df = spookipy.SetConstantValue(df, max_index=True, nomvar_out='KTOP', bi_dimensionnal=True).compute()

   all_df = pd.concat([df,minidx_df,maxidx_df], ignore_index=True)

   res_df = spookipy.MinMaxLevelIndex(all_df, nomvar="UU", min=True, ascending=True).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Daniel Figueras <https://wiki.cmc.ec.gc.ca/wiki/User:Figuerasd>`__ / `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ / Jonathan Cameron / `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginMinMaxLevelIndex.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginMinMaxLevelIndex.html>`_
