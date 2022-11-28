Description:
~~~~~~~~~~~~

-  Limit the minimum of a field to the specified value

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  A meteorological field

Result(s):
~~~~~~~~~~

-  The meteorological field of which no value is less than the specified value

Algorithm:
~~~~~~~~~~

.. code-block:: text

         For F, a given field of size N, composed of n elements (n = 1,N)

         For z, a value given by the "value" key, designated as the lower boundary of the field F

         For each point n=1,N do

            If F(n) < z then
               F(n) = z
            End if

         End do

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, minimum, borne/bound, inférieur/lower

Usage:
~~~~~~

.. code:: python

   import os
   import fstpy
   import spookipy

   spooki_dir     = os.environ['SPOOKI_DIR']
   spooki_out_dir = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/SetLowerBoundary/testsFiles/inputFile.std')
   output_file = (f'{spooki_out_dir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   res_df = spookipy.SetLowerBoundary(df, value=1.).compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginSetLowerBoundary.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginSetLowerBoundary.html>`_
