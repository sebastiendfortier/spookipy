Description:
~~~~~~~~~~~~

-  Calculation of the George-K index, a severe weather index used
   for forecasting thunderstorm (George, 1960).
-  This index takes into account the vertical lapse rate and the
   humidity at low levels.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  Air température (TT) at 850 mb, 700 mb and 500 mb
   and one of the following fields at 850 mb and 700 mb:
-  Specific humidity, HU
-  Water vapour mixing ratio, QV
-  Relative humidity, HR
-  Dew point temperature, TD
-  Dew point depression, ES
   Note: : Make sure to provide the dependencies listed above
   to this plug-in or the plug-in results
   called by the plug-in (see the section "this plug-in uses").
   For more details on this alternative use,
   see the `documentation
   page. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__

Result(s):
~~~~~~~~~~

-  George-K index, KI (scalar, without units)

Algorithm:
~~~~~~~~~~

.. code-block:: text

         For TT850, TT700 and TT500, the air temperature (deg C) at 850mb, 700mb and 500mb respectively.
         For TD850 and TD700, the dew point temperature (deg C) at 850mb and 700mb respectively.

         *If the input fields are the specific humidity, HU (kg/kg) or
               the water vapour mixing ratio, QV (kg/kg) or
               the relative humidity, HR (fraction) or
               the dew point depression, ES (deg C or deg K) and the air temperature, TT (deg C):

               Calculate the dew point temperature, TD (deg C) with TemperatureDewPoint plug-in with --iceWaterPhase WATER.

               KI = (TT850 - TT500) + TD850 - (TT700 - TD700)
               where KI is the George-K index (scalar)

         *If  the input fields are the dew point temperature, TD (deg C) and the air temperature, TT (deg C):

               KI = (TT850 - TT500) + TD850 - (TT700 - TD700)
               where KI is the George-K index (scalar)

Reference:
~~~~~~~~~~

-  George, J.J., 1960; Weather Forecasting for Aeronautics,
   Academic Press
-  Bluestein, 1993; Synoptic-Dynamic Meteorology in Midlatitudes,
   Oxford University Press, Vol 2, 594pp.
-  `Wikipedia:
   K-index <http://en.wikipedia.org/wiki/K-index_(meteorology)>`__

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, indice/index, George, violent/severe, orage/thunderstorm, convection, stabilité/stability

Usage:
~~~~~~

.. code:: python
   
   import os
   import fstpy
   import spookipy

   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/GeorgeKIndex/testsFiles/inputFile.std')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   res_df = spookipy.GeorgeKIndex(df).compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : George Karaganis
-  Coded by : `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginGeorgeKIndex.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginGeorgeKIndex.html>`_
