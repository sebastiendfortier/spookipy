English
-------

**Description:**

-  calculation. The humidex index aims to quantify the discomfort caused
   by a combination of heat and humidity.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  | Air surface temperature, TTC
   | **and** one of the following fields at the surface:

   -  Specific humidity, HU
   -  Relative humidity, HR
   -  Water vapour mixing ratio, QV
   -  Dew point temperature, TD
   -  Dew point depression, ES

\*Result(s):\*

-  index, HMX (scalar, unitless)

\*Algorithm:\*

.. code:: example

    TTC is the Temperature [Celsius Degrees]
    Calculate TD with the TemperatureDewPoint plugin.
    ES(TT) is the Saturation Vapour Pressure. This value can be obtained with the SaturationVapourPressure plugin by using TD instead of TTC with the option --iceWaterPhase WATER

    We calculate the Humidex:

    HMX = TTC + (0.5555) * (ES(TT) - 10)
    if HMX > TTC
       result = HMX
    else
       result = TTC

**Reference:**

`Description of the humidex by
ECCC <http://ec.gc.ca/meteo-weather/default.asp?lang=En&amp;n=6C5D4990-1#humidex>`__

`Scribe
specifications <https://wiki.cmc.ec.gc.ca/images/0/0d/SITS14_specs.pdf>`__

**Keywords:**

-  MÉTÉO/WEATHER, température/temperature, humidité/humidity

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Humidex/testsFiles/inputFile.std] >>
                [Humidex] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Agnieszka
   Barszcz <https://wiki.cmc.ec.gc.ca/wiki/Agn%C3%A8s_Barszcz>`__
-  Coded by : `Philippe
   Lachapelle <https://wiki.cmc.ec.gc.ca/wiki/User:lachapellep>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
