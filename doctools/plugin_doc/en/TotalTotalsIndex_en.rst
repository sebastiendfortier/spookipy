English
-------

**Description:**

-  Calculation of the Total Totals index, a severe weather index used
   for forecasting thunderstorms (Miller, 1972).
-  This combined index is a measure of the vertical lapse rate and of
   the humidity at low levels.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Air temperature (TT) at 850 mb and 500 mb
   **and** one of the following fields at 850 mb:
-  Specific Humidity, HU
-  Water vapour mixing ratio, QV
-  Relative Humidity, HR
-  Dew point temperature, TD
-  Dew point depression, ES

\*Result(s):\*

-  Total Totals index, TTI (scalar, without units)

\*Algorithm:\*

.. code:: example

    For TT850 and TT500, the air temperature (deg C) at 850 mb and 500 mb respectively.
    For TD850, the dew point temperature (deg C) at 850 mb.

    *If the input fields are the specific humidity, HU (kg/kg) or
        the water vapour mixing ratio, QV (kg/kg) or
        the relative humidity, HR (fraction) or
        the dew point depression, ES (deg C or deg K) and the air temperature, TT (deg C):

        Calculate the dew point temperature, TD (deg C) with TemperatureDewPoint plug-in with --iceWaterPhase WATER.

        The Total Totals index is calculated as :
          TTI = TT850 + TD850 - 2*(TT500)

    *If the input fields are the dew point temperature, TD (deg C) and the air temperature, TT (deg C):

        The Total Totals index is calculated as :
          TTI = TT850 + TD850 - 2*(TT500)

**Reference:**

-  Djurik,D 1994:Weather Analysis, Prentice-Hall.
-  `Wikipedia : Total Totals index (link only in
   French) <http://fr.wikipedia.org/wiki/Indice_total-total>`__

\*Customizable condition:\*

-  Height for bottom and top levels in mb

\*Keywords:\*

-  MÉTÉO/WEATHER, stabilité/stability, indice/index, total,
   violent/severe, orage/thunderstorm, convection

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/TotalTotalsIndex/testsFiles/inputFile.std] >>
                [TotalTotalsIndex] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `George
   Karaganis <https://wiki.cmc.ec.gc.ca/wiki/User:Karaganisg>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
