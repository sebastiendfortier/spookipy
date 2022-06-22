Description:
~~~~~~~~~~~~

-  Limit the maximum of a field to the specified value

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  A meteorological field

Result(s):
~~~~~~~~~~

-  The meteorological field of which no value is greater than the specified value

Algorithm:
~~~~~~~~~~

.. code-block:: text

      For F, a given field of dimension N, composed of n elements (n = 1,N)
      For z, a value given by the "value" key, designated as upper boundary of field F
         For each point n=1,N do

               If F(n) > z then
                  F(n) = z
               End if

         End do

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, maximum, borne/bound, supérieur/upper

Usage:
~~~~~~

.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/SetUpperBoundary/testsFiles/inputFile.std').to_pandas()

   res_df = spookipy.SetUpperBoundary(df, value=1.).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginSetUpperBoundary.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginSetUpperBoundary.html>`_
