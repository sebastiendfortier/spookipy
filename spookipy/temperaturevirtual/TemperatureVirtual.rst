Description:
~~~~~~~~~~~~

-  Calculates the virtual temperature as a function of temperature and water vapour mixing ratio.
-  The virtual temperature is used to account for the presence of water vapour and may be interpreted as a proxy for density. 

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  Air Temperature, TT
  
   *and* one of the following fields:

-  Specific Humidity, HU
-  Water vapour mixing ratio, QV
-  Dew point temperature, TD 
-  Dew point depression, ES
-  Relative Humidity, HR

Result(s):
~~~~~~~~~~

-  Virtual temperature, VT (deg C)

Algorithm:
~~~~~~~~~~

.. code-block:: text

    If necessary, calculate the water vapour mixing ratio, QV (kg kg⁻¹) with the 
    WaterVapourMixingRatio plug-in

    For QV the water vapour mixing ratio (kg kg-1) 
    For TT the air temperature in deg K
    The virtual temperature (deg K) is calculated as: 

    VT(deg K) = TT*[(1+QV/epsilon)/(1+QV)]
    VT(deg C) = VT(deg K) - 273.15

    Where epsilon is the ratio of Rd (the gas constant for dry air; Rd = 287.05 J kg-1 K-1) and 
    Rv (the gas constant for water vapour; Rv = 461.51 J kg-1 K-1).

Reference:
~~~~~~~~~~

-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud
   Physics, 3rd Ed. Butterworth Heinemann, 290 pp.
-  `Analysis of virtual temperature <https://wiki.cmc.ec.gc.ca/wiki/RPT/Analyse_de_la_temp%C3%A9rature_virtuelle>`__
   

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, température/temperature, humidité/humidity

Usage:
~~~~~~

.. code:: python

   python3

   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/TemperatureVirtual/testsFiles/inputFile.std').to_pandas()
   df = fstpy.select_with_meta(df, ['TT', 'HU'])
   
   res_df = spooki.TemperatureVirtual(df).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : Neil Taylor
-  Coded by : `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginTemperatureVirtual.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html//pluginTemperatureVirtual.html>`_
