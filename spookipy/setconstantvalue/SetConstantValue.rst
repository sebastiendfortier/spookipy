Description:
~~~~~~~~~~~~

-  Copies the input field and replace all its values by a given constant. Possibility to generate a 2D constant field from a 3D field.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  A meteorological field

Result(s):
~~~~~~~~~~

-  A copy (3D or 2D) of the meteorological field received from
   input containing the value received as parameter

Algorithm:
~~~~~~~~~~

-  Does not apply

Reference:
~~~~~~~~~~

-  None

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, constant, generate/produire

Usage:
~~~~~~



.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/SetConstantValue/testsFiles/inputFile.std').to_pandas()

   res_df = spooki.SetConstantValue(df, value=4.).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginSetConstantValue.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginSetConstantValue.html>`_
