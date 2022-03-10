Description:
~~~~~~~~~~~~

-  Humidex calculation. The humidex index aims to quantify the discomfort caused by a combination of heat and humidity.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  Air surface temperature, TTC and one of the following fields at the surface:

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

    For TTC, the air temperature valid at the surface level (deg C).
    For TD, the dew point temperature (deg C). It can be calculated with the TemperatureDewPoint plugin.
    For :math:`{e_{s}(TD)}`, the partial vapour pressure
    (hPa) at saturation. It can be calculated with the SaturationVapourPressure plugin using TD instead of TTC and with the option –iceWaterPhase WATER

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
- `Scribe specifications <https://wiki.cmc.ec.gc.ca/images/0/0d/SITS14_specs.pdf>`__

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

    df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/Humidex/testsFiles/inputFile.std').to_pandas()

    res_df = spooki.Humidex(df).compute()

    fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()

Contacts:
~~~~~~~~~

-  Author : `Agnieszka Barszcz <https://wiki.cmc.ec.gc.ca/wiki/Agn%C3%A8s_Barszcz>`__
-  Coded by : `Philippe Lachapelle <https://wiki.cmc.ec.gc.ca/wiki/User:lachapellep>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginHumidex.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginHumidex.html>`_
