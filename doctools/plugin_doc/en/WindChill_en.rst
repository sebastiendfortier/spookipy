English
-------

**Description:**

-  Calculation of the equivalent temperature associated to the wind
   chill factor at the surface.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Air temperature, TT, at the surface
-  UU wind component (along the X axis of the grid), at the surface
-  VV wind component (along the Y axis of the grid), at the surface
   ***Note:*** : Be sure to provide the dependencies mentioned above to
   this plug-in or the results of
   the plug-ins called by this plug-in (See the "this plug-in uses"
   section). For more details on this
   alternative use, see the
   `documentation <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__
   page.

\*Result(s):\*

-  Wind chill factor, RE (deg C)

\*Algorithm:\*

    For TT(1), the surface temperature (deg C) and UV(1), the surface
    wind modulus (km.h-1) (respectively, at 2 meters and 10 meters),
    the wind chill factor RE (no units) is calculated according to the
    Osczevski-Bluestein equation, as :
    if TT(1) <= 0 et UV(1) >= 5 then :
        RE = :math:`\mathrm{13.1200 + 0.6215*TT(1) + (0.3965*TT(1) -
    11.3700)*UV(1)^{0.16}}`
    else
        RE = TT

**Reference:**

-  [[http://journals.ametsoc.org/doi/abs/10.1175/BAMS-86-10-1453][The
   new wind chill equivalent temperature chart. Osczevski, R. and
   Bluestein, M., Amer. Meteor. Soc., 2005]]
-  `Wikipédia : wind chill
   factor <http://en.wikipedia.org/wiki/Wind_chill>`__

\*Keywords:\*

-  MÉTÉO/WEATHER, vent/wind, facteuréolien/windchill, facteur/factor,
   refroidissement/chill

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindChill/testsFiles/inputFile.std] >>
                [WindChill] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Marc
   Besner <https://wiki.cmc.ec.gc.ca/wiki/User:Besnerm>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__, `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Unit tests

| **Uses:**
| **Used by:**

 
