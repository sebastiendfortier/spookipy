English
-------

**Description:**

-  Verifies if the number of levels of one or more field(s) satisfies
   one of the following criteria :

   -  number equal to the specified number of levels
   -  number less than or equal to the specified maximum number of
      levels
   -  number greater than or equal to the specified minimum number of
      levels
   -  number of levels identical for all the input fields
   -  number of levels identical for each input grid

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  At least one field

\*Result(s):\*

-  The result is posted in the standard output (STDOUT).
   ***Note:*** No data is output from this plug-in.

\*Algorithm:\*

-  Does not apply

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  SYSTÈME/SYSTEM, niveau/level, minimum, maximum, exact, identique/same

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/CheckNumberOfLevels/testsFiles/inputFile.std] >>
                [CheckNumberOfLevels --minimum 1] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Luc
   Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
-  Coded by : `Luc
   Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
