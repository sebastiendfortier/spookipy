English
-------

**Description:**

-  Calculates the square root of each element in a given field

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  A meteorological field

\*Result(s):\*

-  The meteorological field of which the value at each point is the
   square root of the field from input

\*Algorithm:\*

-  Apply the function :math:` \sqrt{z} ` to each value (z) of the given
   field

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, racine/root, carré/square, point

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SquareRoot/testsFiles/inputFile.std] >>
                [SquareRoot --noFieldNameTag] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
