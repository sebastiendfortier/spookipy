Description:
~~~~~~~~~~~~

-  Calculation of the pressure field for a given vertical coordinate.
-  The definition of the different coordinates are available in this
   `document. <https://wiki.cmc.ec.gc.ca/images/0/01/Spooki_-_Definitions_coordvert.pdf>`__
-  Possibility to calculate the pressure in the case of a
   `standard atmosphere <https://en.wikipedia.org/wiki/International_Standard_Atmosphere>`__
   (constant pression ).
-  Others types of vertical coordinates could be added and documented in the future.

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

-  `<https://wiki.cmc.ec.gc.ca/images/5/5c/Spooki_-_Algorithme_du_plugin_Pressure.pdf>`__

Reference:
~~~~~~~~~~

-  Inspired from the r.hy2pres utility of the RMNLIB library of RPN

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, pression/pressure, niveau/level, coordonnée/coordinate, r.hy2pres

Usage:
~~~~~~


.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/Pressure/testsFiles/inputFile.std').to_pandas()

   res_df = spooki.Pressure(df, reference_field='TT').compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Sandrine Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginPressure.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginPressure.html>`_
