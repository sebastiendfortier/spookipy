Description:
~~~~~~~~~~~~

-  Multiplies each element of a field by a given value

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  A meteorological field

Result(s):
~~~~~~~~~~

-  The meteorological field to which the given value has
   multiplied each element

Algorithm:
~~~~~~~~~~

.. code-block:: text

            For F, a field of n elements

            For z, a value given by the "value" key

            for each point do

               F(n) = F(n) *  z        n >= 1

            end do

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, multiplier/multiply

Usage:
~~~~~~



.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MultiplyElementBy/testsFiles/inputFile.std').to_pandas()

   res_df = spookipy.MultiplyElementBy(df, value=10.).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()

Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__



Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginMultiplyElementBy.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginMultiplyElementBy.html>`_
