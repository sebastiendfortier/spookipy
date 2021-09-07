English
-------

**Description:**

-  Calculation of the vertical wind shear between two levels, with a
   centered difference.

\*Iteration method:\*

-  Column-by-column

| \*Dependencies:\*
| Two vertical levels:

-  UU, wind component along the X axis.
-  VV, wind component along the Y axis.
-  GZ, geopotential height.

\*Result(s):\*

-  BS, vertical wind shear between two levels in 1/s
   If using the option "--outputComponents YES":
-  BSU, BS component along the X axis in 1/s
-  BSV, BS component along the Y axis in 1/s

\*Algorithm:\*

    | For UU and VV, the wind components in m/s.
    | For GZ, the geopotential height in meters.
    | For BS, the wind vertical shear in 1/s.
    | For BSU and BSV, the wind vertical shear components in 1/s.
    | For each level, K:

    | :math:` BS_{(K)}` =
      :math:`\mathrm{\sqrt{(BSU)_{(K)}^2 + (BSV)_{(K)}^2}}`
    | where
    | :math:`\mathrm{ BSU_{(K)}\; =\; \frac{[UU_{(K+1)} \, - \,
      UU_{(K-1)}]}{[GZ_{(K+1)} \, - \, GZ_{(K-1)}] }}`
    | and
    | :math:`\mathrm{ BSV_{(K)} \; =\; \frac{[VV_{(K+1)} \, - \,
      VV_{(K-1)}]}{[GZ_{(K+1)} \, - \, GZ_{(K-1)}] }}`
    | Note:

    -  The vertical wind shear is calculated with a centered difference.
       For example, for UU and N levels:
       For the 1st level:
       :math:`\mathrm{BSU_{(1)} \; =\; \frac{[UU_{(2)} \, - \,
        UU_{(1)}]}{[GZ_{(2)} \, - \, GZ_{(1)}] }}`
       For the last level:
       :math:`\mathrm{BSU_{(N)} \; =\; \frac{[UU_{(N)} \, - \,
        UU_{(N-1)}]}{[GZ_{(N)} \, - \, GZ_{(N-1)}] }}`

**Reference:**

-  `Package de
   l'aviation <http://iweb/~afsypst/pluginsRelatedStuff/WindVerticalShear/reference/PackageAviation.pdf>`__

\*Customizable condition:\*

-  N/A

\*Keywords:\*

-  MÉTÉO/WEATHER, cisaillement/shear, vent/wind, vertical, turbulence,
   aviation

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindVerticalShear/testsFiles/inputFile.std] >>
                [WindVerticalShear] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Marc Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Coded by : `Luc
   Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__,
   `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
