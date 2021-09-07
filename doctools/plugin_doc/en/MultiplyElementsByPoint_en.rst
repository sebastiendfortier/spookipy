English
-------

**Description:**

-  Multiplication of the values of all the fields received at each point

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  At least 2 different fields

\*Result(s):\*

-  A field named "MUEP" with the result of the multiplication of the
   input fields

\*Algorithm:\*

-  MUEP[i,j,k] = A[i,j,k] \* B[i,j,k] \* ...

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, grille/grid, point, multiplier/multiply,
   produit/product

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MultiplyElementsByPoint/testsFiles/inputFile.std] >>
                [MultiplyElementsByPoint] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
