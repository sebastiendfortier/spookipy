English
-------

**Description:**

-  Calculation at each point of the first field to the power of the
   second field

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  2 fields on the same grid with different names

\*Result(s):\*

-  First field to the power of the second field, POEP

\*Algorithm:\*

.. code:: example

    For the fields A identified by --baseFieldName and B identified by --exponentFieldName and grouped by --groupBy

    For each group:

    If the two fields are 2D:
    a) POEP[i,j]   = A[i,j]   ^ B[i,j]

    If one of the fields is 3D:
    b) POEP[i,j,k] = A[i,j,k] ^ B[i,j,k]
    c) POEP[i,j,k] = A[i,j,k] ^ B[i,j]
    d) POEP[i,j,k] = A[i,j]   ^ B[i,j,k]

**Reference:**

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, grille/grid, point, puissance/power,
   produit/product

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/PowerElementsByPoint/testsFiles/inputFile.std] >>
                [PowerElementsByPoint --baseFieldName UU --exponentFieldName POW] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Michael
   Powers <https://wiki.cmc.ec.gc.ca/wiki/User:Powersm>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
