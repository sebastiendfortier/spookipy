English
-------

**Description:**

-  Arithmetic mean for each point of all the fields received

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  At least 2 different fields

\*Result(s):\*

-  The mean of the fields received from input named "MEAN"

\*Algorithm:\*

    For N fields Fn , (n=1,N)

    The arithmetic mean of the N fields received from input is expressed
    for each point (i,j,k) as :

    :math:`\mbox{ $MEAN(i,j,k) = \frac {\sum_{n=1}^{N} F_n(i,j,k)}{N}$}`

**Reference:**

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, moyenne/mean, average

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ArithmeticMeanByPoint/testsFiles/inputFile.std] >>
                [ArithmeticMeanByPoint] >>
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

 
