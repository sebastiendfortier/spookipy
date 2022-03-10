Description:
~~~~~~~~~~~~

-  Finds the maximum and/or minimum value in the column or part of it.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Column by column

Dependencies:
~~~~~~~~~~~~~

-  Meteorological field (3D)
  
   If the bounded key is activated:
-  Field of indices of the lower limit, KBAS
-  Field of indices of the upper limit, KTOP

Result(s):
~~~~~~~~~~

-  A field with the values, KMIN (2D), for which the value of the
   meteorological field is minimum
   *and/or*
-  A field with the values, KMAX (2D), for which the value of the
   meteorological field is maximum

Algorithm:
~~~~~~~~~~

.. code-block:: text

    Call to MinMaxLevelIndex plugin:

    df=MinMaxLevelIndex(self.df,
                        nomvar=self.nomvar, 
                        ascending=True, 
                        min=self.min, 
                        max=self.max,
                        bounded=self.bounded,
                        nomvar_min_idx= "_MIN",
                        nomvar_min_val= min_out,
                        nomvar_max_idx= "_MAX",
                        nomvar_max_val= max_out,
                        value_to_return=True).compute()

   Notes:

   -  If several identical values of the max or min are found in a column, the first occurrence 
      will be considered the min or the max. Depending on the "direction" option (ascending or not), 
      it will be the highest or lowest occurrence in the sample.
   -  When the values of KBAS and KTOP are equal to -1 (fields needed when using 
      the "bounded" option), the column will be ignored and the returned value will be -1.

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
   import fstpy.all as fstpy
   import spookipy.all as spooki

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MinMaxVertically/testsFiles/inputFile.std').to_pandas()

   res_df = spooki.MinMaxVertically(df, nomvar="TT", max=True, ascending=False).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MinMaxVertically/testsFiles/inputFile.std').to_pandas()

   tt_df = fstpy.select_with_meta(df, ['TT'])

   minidx_df = spooki.SetConstantValue(tt_df, min_index=True, nomvar_out='KBAS', bi_dimensionnal=True).compute()

   maxidx_df = spooki.SetConstantValue(tt_df, max_index=True, nomvar_out='KTOP', bi_dimensionnal=True).compute()

   all_df = pd.concat([df,minidx_df,maxidx_df], ignore_index=True)

   res_df = spooki.MinMaxVertically(all_df, nomvar="TT", min=True, max=True, bounded=True).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__ 
-  Coded by : `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Does not apply
