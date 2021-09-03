English
-------

**Description:**

-  Calculation of the Coriolis parameter.

\*Iteration method:\*

-  Point by point

\*Dependencies:\*

-  A field on a grid known by SPOOKI.

\*Result(s):\*

-  Coriolis parameter, CORP (1/s)

\*Algorithm:\*

    | For OMEGA = 7.2921 \* 10\*\*-5 (1/s) and :math:`\varphi`
      (radians), the latitude.
    | Calculate the Coriolis parameter, CORP (1/s), with the following
      formula:
    | CORP = 2 \* OMEGA \* sin( :math:`\varphi`)

**Reference:**

-  "An Introduction to Dynamic Meteorology", Holton, James R.

\*Keywords:\*

-  MÉTÉO/WEATHER, Coriolis, paramètre/parameter

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/CoriolisParameter/testsFiles/inputFile.std] >>
                [CoriolisParameter] >>
                [WriterStd --output /tmp/$USER/outputFile.std --noUnitConversion]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Simon
   Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Coded by : `Simon
   Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Unit tests

| **Uses:**
| **Used by:**

 
