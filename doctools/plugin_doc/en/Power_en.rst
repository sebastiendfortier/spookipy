English
-------

**Description:**

-  Raise to the power each element of a field

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  A meteorological field

\*Result(s):\*

-  The meteorological field of which the value at each point has been
   raised to the power.

\*Algorithm:\*

-  Apply the function :math:`\mathbf z^{value} ` to each element (z) of
   the given field

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, puissance/power, point

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Power/testsFiles/inputFile.std] >>
                [Power --value 3] >>
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

`Unit tests <PowerTests_8cpp.html>`__

| **Uses:**
| **Used by:**

 
