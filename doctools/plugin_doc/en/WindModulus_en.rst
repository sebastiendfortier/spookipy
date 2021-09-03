English
-------

**Description:**

-  Calculation of the wind modulus from its 2 horizontal components.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  UU component of the wind (along the X axis of the grid).
-  VV component of the wind (along the Y axis of the grid).

\*Result(s):\*

-  Wind modulus, UV, in the same units as the dependencies.

\*Algorithm:\*

-  Calls the
   `WindModulusAndDirection <pluginWindModulusAndDirection.html>`__
   plug-in.
-  The wind having 2 components, calls the
   `VectorModulusAndDirection <pluginVectorModulusAndDirection.html>`__
   plug-in.
-  Conserves only the result of the modulus, MOD, into the UV variable.

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  MÉTÉO/WEATHER, module/modulus, vent/wind, vitesse/speed

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindModulusAndDirection/testsFiles/inputFile.std] >>
                [WindModulus] >>
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

 
