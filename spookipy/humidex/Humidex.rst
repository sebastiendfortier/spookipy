Description:
~~~~~~~~~~~~

-  Humidex calculation. The humidex index aims to quantify the discomfort caused by a combination of heat and humidity.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  Air surface temperature, TT 

   **and one of the following fields:**

-  Specific humidity, HU
-  Relative humidity, HR
-  Water vapour mixing ratio, QV
-  Dew point temperature, TD
-  Dew point depression, ES

Result(s):
~~~~~~~~~~

-  Humidex index, HMX (scalar, unitless)

Algorithm:
~~~~~~~~~~

    For the air temperature valid at the surface level, TTC (deg C)

    For the dew point temperature, TD (deg C). It can be calculated with the TemperatureDewPoint plugin.

    For the partial vapour pressure at saturation, :math:`{e_{s}(TD)}` (hPa). It can be calculated 
    with the SaturationVapourPressure plugin using TD instead of TTC and with the
    option –iceWaterPhase WATER

    Compute the Humidex:

    :math:`{res = TTC + (0.5555) * (e_{s}(TD) - 10)}`
    
.. code-block:: text

        If res > TTC 
           HMX = res
        Else 
           HMX = TTC 
        End if

Reference:
~~~~~~~~~~

- `Description of the humidex by ECCC <http://ec.gc.ca/meteo-weather/default.asp?lang=En&amp;n=6C5D4990-1#humidex>`__
- `Scribe specifications <https://wiki.cmc.ec.gc.ca/w/images/0/0d/SITS14_specs.pdf>`__

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, température/temperature, humidité/humidity


Usage:
~~~~~~

.. code:: python
    
    import os
    import fstpy
    import spookipy

    spooki_dir  = os.environ['SPOOKI_DIR']
    tmpdir      = os.environ['BIG_TMPDIR']

    input_file  = (f'{spooki_dir}/pluginsRelatedStuff/Humidex/testsFiles/inputFile.std')
    output_file = (f'{tmpdir}/outputFile.std')

    df = fstpy.StandardFileReader(input_file).to_pandas()   

    res_df = spookipy.Humidex(df).compute()

    fstpy.StandardFileWriter(output_file, res_df).to_fst()

Contacts:
~~~~~~~~~

-  Author   : `Agnieszka Barszcz <https://wiki.cmc.ec.gc.ca/wiki/Agn%C3%A8s_Barszcz>`__
-  Coded by : `Philippe Lachapelle <https://wiki.cmc.ec.gc.ca/wiki/User:lachapellep>`__
-  Support  : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginHumidex.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginHumidex.html>`_
