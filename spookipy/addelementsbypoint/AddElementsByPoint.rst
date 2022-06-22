Description:
~~~~~~~~~~~~

-  Add, for each point, the values of all the fields received

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  At least 2 different fields

Result(s):
~~~~~~~~~~

-  A field named "ADEP" with the result of the sum of the fields
   received from input

Algorithm:
~~~~~~~~~~

-  ADEP[i,j,k] = A[i,j,k] + B[i,j,k] + ...

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, accumuler/accumulate, ajout/add, somme/sum

Usage:
~~~~~~



.. code:: python

   python3
   
   import os
   import fstpy
   import spookipy

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/AddElementsByPoint/testsFiles/inputFile.std').to_pandas()

   res_df = spookipy.AddElementsByPoint(df).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()

Results validation:
~~~~~~~~~~~~~~~~~~~

Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginAddElementsByPoint.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginAddElementsByPoint.html>`_
