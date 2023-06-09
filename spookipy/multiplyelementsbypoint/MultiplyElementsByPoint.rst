Description:
~~~~~~~~~~~~

-  Multiplication of the values of all the fields received at each point

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  At least 2 different fields

Result(s):
~~~~~~~~~~

-  A field named "MUEP" with the result of the multiplication of the input fields

Algorithm:
~~~~~~~~~~

-  MUEP[i,j,k] = A[i,j,k] \* B[i,j,k] \* ...

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, grille/grid, point, multiplier/multiply, produit/product

Usage:
~~~~~~

.. code:: python

   import os
   import fstpy
   import spookipy

   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/MultiplyElementsByPoint/testsFiles/inputFile.std')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   res_df = spookipy.MultiplyElementsByPoint(df).compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author   : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ / `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support  : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginMultiplyElementsByPoint.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginMultiplyElementsByPoint.html>`_
