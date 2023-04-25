Description:
~~~~~~~~~~~~

-  Associates, to each vertical level index given, a value of one
   or many 3D meteorological fields given in input.

   **Note:** The numbering of the indices starts at zero

Iteration method:
~~~~~~~~~~~~~~~~~

-  Column by column

Dependencies:
~~~~~~~~~~~~~

-  A field of vertical level indexes (2D)
-  One or many meteorological field(s) (3D)

Result(s):
~~~~~~~~~~

-  Meteorological field(s) (2D) which the values correspond to
   those of the vertical levels specified by the index field

Algorithm:
~~~~~~~~~~

.. code-block:: text

   For IND, a 2D field of vertical level indexes, where the index numbering starts at 0.

   For each 3D meteorological field, CHP3D, given in input, do :
         For each i,j
            If IND(i,j) = -1
               CHP2D(i,j) = -1
            Else If IND(i,j) is valid
               CHP2D(i,j) = CHP3D(i,j,IND(i,j))
            Else
               Error message:  INVALID INDEX TO MATCH - OUT OF RANGE!
            End if
         End loop on i,j
   End loop on the fields

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, associer/match, niveau/level, vertical

Usage:
~~~~~~

.. code:: python

   import os
   import fstpy
   import spookipy

   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/MatchLevelIndexToValue/testsFiles/inputFile.std')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   res_df = spookipy.MatchLevelIndexToValue(df).compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__, `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginMatchLevelIndexToValue.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginMatchLevelIndexToValue.html>`_
