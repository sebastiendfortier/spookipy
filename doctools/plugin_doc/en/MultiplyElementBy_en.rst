English
-------

**Description:**

-  Multiplies each element of a field by a given value

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  A meteorological field

\*Result(s):\*

-  The meteorological field to which the given value has multiplied each
   element

\*Algorithm:\*

.. code:: example

    For F, a field of n elements

    For z, a value given by the "value" key

    for each point do

        F(n) = F(n) *  z        n >= 1

    end do

**Reference:**

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, multiplier/multiply

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MultiplyElementBy/testsFiles/inputFile.std] >>
                [MultiplyElementBy --value 10] >>
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

 
