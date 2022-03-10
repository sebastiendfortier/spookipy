Description:
~~~~~~~~~~~~

-  Calculates the thermodynamic temperature of the dew point, a
   mesure of the atmospheric humidity.
-  Temperature at which the air must be cooled, at constant
   pressure and humidity content, to become saturated.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  Air temperature, TT
   and one of the following fields:
-  Dew point depression, ES
-  Specific humidity, HU
-  Relative humidity, HR
-  Water vapour mixing ratio, QV

Result(s):
~~~~~~~~~~

-  Dew point temperature, TD (deg C)

Algorithm:
~~~~~~~~~~

.. code-block:: text

   -If the --RPN key is NOT activated:

         *If the input fields are the specific humidity, HU (kg/kg) or
         the water vapour mixing ratio, QV (kg/kg) or
         the relative humidity, HR (fraction) and the air temperature, TT (deg C):

            For TPL, the temperature at which we must change from the saturation with respect to water to the saturation with respect to ice (deg C)
            Calculate the vapour pressure, VPPR (hPa) with the VapourPressure plug-in
            Calculate the dew point temperature, TD (deg C):

            If TT > TPL or --iceWaterPhase WATER
               TD= ( AEw3 * ln(VPPR/AEw1) ) / ( AEw2 - ln (VPPR/AEw1) )
            else
               TD= ( AEi3 * ln(VPPR/AEi1) ) / ( AEi2 - ln (VPPR/AEi1) )

            where according to Alduchov and Eskridge (1996)
               AEw1=6.1094   AEi1=6.1121
               AEw2=17.625   AEi2=22.587
               AEw3=243.04   AEi3=273.86

         *If the input fields are the dew point depression, ES (deg C or deg K) and the air temperature, TT (deg C):

            TD = TT - ES   (if ES < 0.0 , ES = 0.0)
            where TD is the dew point temperature (deg C)


   -If the --RPN key is activated:

         *If the input fields are the specific humidity, HU (kg/kg) or
         the water vapour mixing ratio, QV (kg/kg) or
         the relative humidity, HR (fraction) and the air temperature TT (deg C):

            Calculate the dew point depression, ES (deg C or deg K) with the DewPointDepression plug-in (with the same keys and their arguments)

            TD = TT - ES  (if ES < 0.0 , ES = 0.0)
            where TD is the dew point temperature (deg C)

         *If the input fields are TT (deg C) and ES (deg C or deg K):

            TD = TT - ES  (if ES < 0.0 , ES = 0.0)
            where TD is the dew point temperature (deg C)


   Notes:  - When the input field is ES or HR, the phase change will presumably happen at the same time in the input field as in output field.
            - When several fields of the dependencies and TT are available in the input, the calculation will be done with the field that has the most number of levels in common with TT, in order of preference (in case of equality)
               with HU followed by QV, HR and finally ES.
            - When the --RPN key is activate and the attribut to --iceWaterPhase is BOTH, -temperaturePhaseSwitch is no accepted and 273.16K (the triple point of water) is assigned to the shuaes.ftn90 and shraes.ftn90 functions which are called by the DewPointDepression plug-in.

Reference:
~~~~~~~~~~

-  (FRENCH) `Wikipédia : point de rosée <http://fr.wikipedia.org/wiki/Point_de_rosée>`__
-  `Alducho v, O. A., and R. E. Eskridge, 1996: Improved Magnus
   form approximation of saturation vapor pressure. J. Appl. Meteor., 35, 601-609. <http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281996%29035%3C0601%3AIMFAOS%3E2.0.CO%3B2>`__
-  `Lawrence, M. G., 2005: The relationship between relative humidity and the dewpoint temperature in moist air: A simple
   conversion and applications. Bull. Amer. Meteor. Soc., 86, 225-233. <http://journals.ametsoc.org/doi/pdf/10.1175/BAMS-86-2-225>`__
-  `RPN thermodynamic library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, température/temperature, pointderosée/dewpoint, humidité/humidity

Usage:
~~~~~~



.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/TemperatureDewPoint/testsFiles/inputFile.std').to_pandas()

   res_df = spooki.TemperatureDewPoint(df, ice_water_phase='both', temp_phase_switch=-40, temp_phase_switch_unit='celsius').compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Coded by : `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__ / Jonathan Cameron
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginTemperatureDewPoint.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginTemperatureDewPoint.html>`_
