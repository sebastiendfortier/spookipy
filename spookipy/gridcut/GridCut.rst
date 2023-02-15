Description:
~~~~~~~~~~~~

Cuts a piece out of a grid, defined by its upper left hand corner
and lower right hand corner.
Notes:

-  This plug-in allows for the creation of a completely
   autonomous grid.
-  If one desires to merge several grids, these grids must have
   been cut by this plug-in in the same SPOOKI execution.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point by point.

Dependencies:
~~~~~~~~~~~~~

-  One or several field(s) on one or several input grid(s).

Result(s):
~~~~~~~~~~

-  The input fields on a piece of the grid, with the same input
   metadata.

Algorithm:
~~~~~~~~~~

-  The input grids are referenced, as well as their data and
   their descriptors.
-  The output grids are created by copying the input grid
   parameters and by modifying the dimensions.
-  The desired data is copied.

Reference:
~~~~~~~~~~

-  N/A

Keywords:
~~~~~~~~~

-  SYSTÈME/SYSTEM, grille/grid, découpage/cut, sélection/select

Usage:
~~~~~~

.. code:: python

   import os
   import fstpy
   import spookipy

   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/GridCut/testsFiles/inputFile.std')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   res_df = spookipy.GridCut(df, 
                             start_point=(5,16), 
                             end_point=(73,42)).compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()
         

Contacts:
~~~~~~~~~

-  Author : `Maximilien Martin <https://wiki.cmc.ec.gc.ca/wiki/User:Martinm>`__
-  Coded by : `Maximilien Martin <https://wiki.cmc.ec.gc.ca/wiki/User:Martinm>`__ / `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginGridCut.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginGridCut.html>`_
