English
-------

**Description:**

-  From a field value for a chosen level (either the lowest or the
   highest), subtract the values from all the other levels of the same
   field.

\*Iteration method:\*

-  Column-by-column

\*Dependencies:\*

-  At least one 3D field

\*Result(s):\*

-  A 2D field with the same name as the input field

\*Algorithm:\*

.. code:: example

    For k the chosen level

      If direction = "ASCENDING" then
          A = A[k] - A[k+1] - A[k+2] - ...
      Else
          A = A[k] - A[k-1] - A[k-2] - ...
      End if

**Reference:**

-  None

\*Keywords:\*

-  UTILITAIRE/UTILITY, soustraire/subtract, soustraction/subtraction,
   verticale/vertical

\*Usage:\*

**Call example:**

.. code:: example

    ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SubtractElementsVertically/testsFiles/inputFile.std] >>
                    [SubtractElementsVertically --direction ASCENDING] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
      ...

**Results validation:**

**Contacts:**

-  Author : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
