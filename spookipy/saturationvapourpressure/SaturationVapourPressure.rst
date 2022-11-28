Description:
~~~~~~~~~~~~

-  Calculates the saturation vapour pressure as a function of temperature.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  Air temperature, TT

Result(s):
~~~~~~~~~~

-  Saturation vapour pressure, SVP (hPa)

Algorithm:
~~~~~~~~~~

.. code-block:: text

         -If the --RPN key is NOT activated:

            For the air temperature, TT (deg C)
            For the temperature at which to switch from saturation over water to saturation 
            over ice, TPL (deg C)
            For the saturation vapour pressure, SVP (hPa)

            If TT > TPL or --iceWaterPhase WATER
               SVP = AEw1*EXP[AEw2*TT/(AEw3 + TT)]
            else
               SVP = AEi1*EXP[AEi2*TT/(AEi3+TT)]

            where according to Alduchov and Eskridge (1996)
            AEw1=6.1094   AEi1=6.1121
            AEw2=17.625   AEi2=22.587
            AEw3=243.04   AEi3=273.86


         -If the --RPN key is activated:

            For the temperature, TT (deg K)
            For the temperature below which we calculate the saturation vapour pressure 
            with respect to ice, TPL (deg K)

            If TT > TPL or --iceWaterPhase WATER
               Call rpn function sfoewa.ftn90 to obtain the saturation vapour pressure, SVP (Pa)
            else
               Call rpn function sfoew.ftn90 to obtain the saturation vapour pressure, SVP (Pa)

            Convert SVP (Pa) to hPa:
               SVP(hPa)=SVP(Pa)/100.0

References:
~~~~~~~~~~~

-  `Alduchov, O. A., and R. E. Eskridge, 1996: Improved Magnus
   form approximation of saturation vapor pressure. ''J. Appl.
   Meteor.'', '''35''',
   601-609 <http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281996%29035%3C0601%3AIMFAOS%3E2.0.CO%3B2>`__
-  `Analysis of saturation vapour
   pressure <https://wiki.cmc.ec.gc.ca/wiki/RPT/en/Analysis_of_saturation_vapour_pressure>`__
-  `RPN thermodynamic
   library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, humidité/humidity, pression/pressure, saturation

Usage:
~~~~~~

.. code:: python

   import os
   import fstpy
   import spookipy

   spooki_dir     = os.environ['SPOOKI_DIR']
   spooki_out_dir = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/SaturationVapourPressure/testsFiles/inputFile.std')
   output_file = (f'{spooki_out_dir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   res_df = spookipy.SaturationVapourPressure(df, 
                                              ice_water_phase='both', 
                                              temp_phase_switch=0.01).compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author   : Neil Taylor
-  Coded by : `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support  : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginSaturationVapourPressure.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginSaturationVapourPressure.html>`_
