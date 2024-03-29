Description:
~~~~~~~~~~~~

-  Calculation of the pressure field.  The plugin will detect the vertical coordinate, make sure 
   to provide the necessary metadata such as !!, PT, P0, etc. 
-  The definition of the different coordinates are available in this
   `document. <https://wiki.cmc.ec.gc.ca/w/images/0/01/Spooki_-_Definitions_coordvert.pdf>`__
-  Possibility to calculate the pressure in the case of a
   `standard atmosphere <https://en.wikipedia.org/wiki/International_Standard_Atmosphere>`__
   (constant pression ).

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  Any field on a set of given vertical levels

Result(s):
~~~~~~~~~~

-  Pressure field PX (hPa or mb), on all the given levels

Algorithm:
~~~~~~~~~~

-  `<https://wiki.cmc.ec.gc.ca/w/images/5/5c/Spooki_-_Algorithme_du_plugin_Pressure.pdf>`__

Reference:
~~~~~~~~~~

-  Inspired from the r.hy2pres utility of the RMNLIB library of RPN

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, pression/pressure, niveau/level, coordonnée/coordinate, r.hy2pres

Usage:
~~~~~~

.. code:: python
   
   import os
   import fstpy
   import spookipy

   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/Pressure/testsFiles/inputFile.std')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   res_df = spookipy.Pressure(df, reference_field='TT').compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author   : `Sandrine Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support  : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginPressure.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginPressure.html>`_
