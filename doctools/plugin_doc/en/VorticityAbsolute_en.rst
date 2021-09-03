English
-------

**Description:**

-  Calculation of the absolute vorticity.

\*Iteration method:\*

-  Point by point

\*Dependencies:\*

-  Wind component along the X-axis of the grid, UU
-  Wind component along the Y-axis of the grid, VV

\*Result(s):\*

-  Absolute vorticity, QQ (1/s)

\*Algorithm:\*

    | Call the plug-in to obtain the Coriolis parameter, CORP (1/s).
    | For UU (m/s) and VV (m/s), respectively the wind components along
      the X-axis and Y-axis.
    | For :math:`\varphi` (radians), the latitude.
    | Make a derivative off-center on a regional grid for the borders.
    | Calculate the absolute vorticity, QQ (1/s), with the following
      formula:
    | :math:`\mathrm{QQ_{i,j} = ( VV_{i+1,j} - VV_{i-1,j} ) / ( X_{i+1,j} -
      X_{i-1,j} ) - ( UU_{i,j+1} * cos\varphi_{i,j+1} - UU_{i,j-1} *
      cos\varphi_{i,j-1} ) / ( ( Y_{i,j+1} - Y_{i,j-1} ) * cos\varphi_{i,j}
      ) + CORP_{i,j}}`

**Reference:**

-  "An Introduction to Dynamic Meteorology", Holton, James R.

\*Keywords:\*

-  MÉTÉO/WEATHER, vent/wind, tourbillon/vorticity, absolute/absolu,
   Coriolis

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/VorticityAbsolute/testsFiles/inputFile.std] >>
                [VorticityAbsolute] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
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

 
