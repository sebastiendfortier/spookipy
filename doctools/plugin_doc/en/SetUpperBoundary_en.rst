English
-------

**Description:**

-  Limit the maximum of a field to the specified value

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  A meteorological field

\*Result(s):\*

-  The meteorological field of which no value is greater than the
   specified value

\*Algorithm:\*

.. code:: example

    For F, a given field of dimension N, composed of n elements (n = 1,N)
    For z, a value given by the "value" key, designated as upper boundary of field F
       For each point n=1,N do

           If F(n) > z then
              F(n) = z
           End if

      End do

**Reference:**

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, maximum, borne/bound, supérieur/upper

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SetUpperBoundary/testsFiles/inputFile.std] >>
                [SetUpperBoundary --value 1 ] >>
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

Units tests

| **Uses:**
| **Used by:**

 
