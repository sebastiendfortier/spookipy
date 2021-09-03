English
-------

**Description:**

-  Calculation of the horizontal wind deformation

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  UU wind component (along the X axis on the grid)
-  VV wind component (along the Y axis on the grid)

\*Result(s):\*

-  The wind deformation, DEF (s-1)

\*Algorithm:\*

-  ...

\*Reference:\*

-  See the definition of the deformation in the `Aviation
   package <http://iweb.cmc.ec.gc.ca/cmc/bibliotheque/PREVISIONS/f_7.pdf>`__
   (link in French only) and the `Ellrod&Knapp
   (1992) <http://iweb/~afsg003/doc/ClearAirTurbulence.pdf>`__ article.

\*Customizable condition:\*

-  N/A

\*Keywords:\*

-  MÉTÉO/WEATHER, vent/wind, déformation/deformation, turbulence,
   aviation

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/testsFiles/inputFile.std] >>
                [WindDeformation] >>
                [WriterStd --output /tmp/$USER/outputFile.std  --noUnitConversion]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Marc Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
