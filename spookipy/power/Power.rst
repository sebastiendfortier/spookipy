Description:
~~~~~~~~~~~~

-  Powers each element of a field by a given value

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  A meteorological field

Result(s):
~~~~~~~~~~

-  The meteorological field to which the given value has
   powered each element

Algorithm:
~~~~~~~~~~

.. code-block:: text

            For F, a field of n elements

            For z, a value given by the "value" key

            for each point do

               F(n) = F(n) **  z        n >= 1

            end do

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, exponent/power 

Usage:
~~~~~~

.. code:: python

   import os
   import fstpy
   import spookipy

   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/PowerElementBy/testsFiles/inputFile.std')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   res_df = spookipy.PowerElementBy(df, value=10.).compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()

Contacts:
~~~~~~~~~

-  Author   : Steven Chia Ah-Lan
-  Coded by : Steven Chia Ah-Lan
-  Support  : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__



Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <https://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginPower.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginPower.html>`_
