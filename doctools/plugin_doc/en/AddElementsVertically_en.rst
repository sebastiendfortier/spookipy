English
-------

**Description:**

-  Addition of all the values of a field in the vertical

\*Iteration method:\*

-  Column-by-column

\*Dependencies:\*

-  At least one 3D field

\*Result(s):\*

-  A 2D field of the same name as the input field

\*Algorithm:\*

.. code:: example

    Add column by column all the values of a field in the vertical :

    A = A[k] + A[k+1] + A[k+2] + ...

**Reference:**

-  None

\*Keywords:\*

-  UTILITAIRE/UTILITY, accumuler/accumulate, addition,
   verticale/vertical

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/AddElementsVertically/testsFiles/inputFile.std] >>
                [AddElementsVertically] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Marc Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Coded by : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
