English
-------

**Description:**

-  Vertical arithmetic mean of each input field received

\*Iteration method:\*

-  Column-by-column

\*Dependencies:\*

-  At least one 3D field

\*Result(s):\*

-  2D field(s) averaged vertically, of the same name(s) as the input
   field(s) received

\*Algorithm:\*

    For F, a field with N levels

    For each column:

    :math:`\mbox{ $F = \frac {\sum_{k=0}^{N} F(k)}{N+1}$}`

**Reference:**

-  None

\*Keywords:\*

-  UTILITAIRE/UTILITY, moyenne/mean, verticale/vertical

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ArithmeticMeanElementsVertically/testsFiles/inputFile.std] >>
                [ArithmeticMeanElementsVertically] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
