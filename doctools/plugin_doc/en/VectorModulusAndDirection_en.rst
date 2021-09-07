English
-------

**Description:**

-  Calculation of the modulus and the direction of a vector
-  The direction of the vector can be calculated with the trigonometric
   convention or with the meteorological convention (where the vector is
   coming from with respect to north)

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  A component of a vector along the X axis
-  A component of the same vector along the Y axis \*/\ Notes:/*

   -  Be certain to have selected, beforehand, only the components of
      the vector of which we want to calculate the modulus and the
      direction.
   -  The components received from the dependencies must be named in
      alphabetical order to be associated correctly with the components
      along the X and Y axis, respectively.

\*Result(s):\*

-  The vector modulus, MOD, which has the same units as the dependencies
-  The vector direction, DIR (deg)

\*Algorithm:\*

    | For MOD, the modulus of a vector with horizontal components x and
      y :
    |    MOD   =   :math:`\sqrt{(x^2 + y^2)}`
    | For DIR, the direction of that same vector :
    |    If the direction is calculated with the trigonometric
      convention (--orientationType TRIG), then :
    |      DIR   =   :math:`\frac{180}{\pi}` atan2(y,x)
    |      if DIR < 0, DIR = DIR + 360
    |    If the direction is calculated with the meteorological
      convention (--orientationType WIND), then :
    |      the gduvfwd function of the EZSCINT library is used to
      calculate the direction of where the vector is coming from with
      respect to north

**Reference:**

-  `EZSCINT library of
   RMNLIB <https://wiki.cmc.ec.gc.ca/wiki/Librmn/ezscint>`__

\*Keywords:\*

-  UTILITAIRE/UTILITY, module/modulus, vitesse/speed, direction, angle,
   vecteur/vector

\*Usage:\*

-  TRIG : trigonometric convention
-  WIND : where the vector is coming from with respect to north
   (meteorological convention)

\*Call example:\*

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindModulusAndDirection/testsFiles/inputFile.std] >>
                [VectorModulusAndDirection --orientationType WIND] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  

\*Contacts:\*

-  Author : `Maryse
   Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
