English
-------

**Description:**

-  Calculation of the wind modulus and the wind direction.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  UU wind component (along the X axis).
-  VV wind component (along the Y axis).

\*Result(s):\*

-  Wind modulus, UV, same units as the dependencies.
-  Meteorological wind direction, WD (deg).

\*Algorithm:\*

-  The wind, having 2 components, calls the
   `VectorModulusAndDirection <pluginVectorModulusAndDirection.html>`__
   plug-in with the --orientationType WIND parameter key.

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  MÉTÉO/WEATHER, vent/wind, module/modulus, direction, angle

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindModulusAndDirection/testsFiles/inputFile.std] >>
                [WindModulusAndDirection] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Maryse
   Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Unit tests

| **Uses:**
| **Used by:**

 
