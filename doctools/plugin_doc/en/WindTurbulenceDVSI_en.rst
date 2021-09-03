English
-------

**Description:**

-  Calculation of the turbulence index DVSI (Deformation Vertical Shear
   Index - developed by Ellrod)

\*Iteration method:\*

-  Element-by-element

\*Dependencies:\* Three vertical levels:

-  Wind component UU (along the X axis)
-  Wind component VV (along the Y axis)

Two vertical levels (lower and upper):

-  Geopotential height GZ.

\*Result(s):\*

-  The turbulence index (DVSI=Deformation Vertical Shear Index, variable
   of the index Ellrod) at each point on the grid

\*Algorithm:\*

-  DVSI = DEF x BS x correction where correction = \|UV\|/45.0 (using
   middle level) (\|UV\| = the wind modulus calculated by the plug-in)
   DEF = the deformation of the wind calculated by the plug-in (using
   middle level) BS = the vertical shear BS calculated by the plug-in
   (using lower and upper levels) UV is in m/s, DEF is in (m/s)/100km
   and BS is in (m/s)/km

\*Reference:\*

-  `Aviation
   package <http://iweb.cmc.ec.gc.ca/cmc/bibliotheque/PREVISIONS/f_7.pdf>`__
   and the article `Ellrod&Knapp
   (1992) <http://iweb/~afsg003/doc/ClearAirTurbulence.pdf>`__

\*Customizable condition:\*

-  N/A

\*Keywords:\*

-  MÉTÉO/WEATHER, turbulence, cisaillement/shear, vertical,
   déformation/deformation, vent/wind, aviation, dvsi, ellrod

\*Usage:\*

.. code:: example

.. code:: example

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindTurbulenceDVSI/testsFiles/inputFile.std] >>
                [WindTurbulenceDVSI] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
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

 
