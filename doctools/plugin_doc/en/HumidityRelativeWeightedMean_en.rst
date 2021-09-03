English
-------

**Description:**

-  Calculation of the weighted mean of relative humidity in the lower
   troposphere and separately in the middle troposphere. This is an
   aviation product. The lower tropospheric calculation uses the levels
   at 1000, 925 and 850 hPa while the middle tropospheric calculation
   uses the levels at 850, 700 and 500 hPa.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Specific humidity, HU, at 1000, 925, 850, 700 and 500 hPa
-  Temperature, TT, at 1000, 925, 850, 700 and 500 hPa

\*Result(s):\*

-  Relative humidity, HR (fraction)

\*Algorithm:\*

.. code:: example

    For HU1000, HU925, HU850, HU700 and HU500, specific humidity (kg/kg) at 1000, 925, 850, 700 and 500 hPa respectively.
    For HUs1000, HUs925, HUs850, HUs700 and HUs500, saturation specific humidity (kg/kg) at 1000, 925, 850, 700 and 500 hPa respectively.
    For HRL, the lower tropospheric relative humidity and HRM, the middle tropospheric relative humidity.

    HRL = (HU1000 + 2*HU925 + HU850) / (HUs1000 + 2*HUs925 + HUs850)

    HRM = (HU850 + 2*HU700 + HU500) / (HUs850 + 2*HUs700 + HUs500)

    The saturation specific humidity (HUs) is calculated by replacing the TD (dew point temperature) field by TT in the HumiditySpecific plug-in.

    The user can choose the highest value that the HR field can have with the --capped option.

**Reference:**

-  Does not apply

\*Keywords:\*

-  MÉTÉO/WEATHER, température/temperature, humidité/humidity,
   pondéré/weighted

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/HumidityRelativeWeightedMean/testsFiles/inputFile.std] >>
                [HumidityRelativeWeightedMean] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Marc Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Coded by : `Simon
   Voyer-Poitras <https://wiki.cmc.ec.gc.ca/wiki/User:Voyerpoitrass>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
