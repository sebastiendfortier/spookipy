English
-------

**Description:**

-  Find the minimum and/or the maximum value of all the fields available
   for each point on the same grid

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Meteorological fields on the same grid

\*Result(s):\*

-  A field of values, MIN
   **and/or**
-  A field of values, MAX

\*Algorithme:\*

    For the fields A (i,j,k), B (i,j,k), C(i,j,k),....

    MIN(i,j,k) = min( A(i,j,k), B(i,j,k), C(i,j,k), ...)

    MAX(i,j,k) = max( A(i,j,k), B(i,j,k), C(i,j,k), ...)

**Reference:**

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, minimum, maximum

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ArithmeticMinMaxByPoint/testsFiles/inputFile.std] >>
                [ArithmeticMinMaxByPoint --minMax BOTH] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Daniel
   Figueras <https://wiki.cmc.ec.gc.ca/wiki/User:Figuerasd>`__
-  Coded by : `Simon
   Voyer-Poitras <https://wiki.cmc.ec.gc.ca/wiki/User:Voyerpoitrass>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
