English
-------

**Description:**

-  Merging of all the similar grids received by the plug-in.
-  Grids are similar when their projection type and their size along X
   and along Y are identical.
-  If at least one grid is not similar to the other available grids, the
   plug-in fails.

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  At least one field from input

\*Result(s):\*

-  All the fields on a single grid

\*Algorithm:\*

-  Does not apply

\*Reference:\*

-  None

\*Keywords:\*

-  UTILITAIRE/UTILITY, grille/grid, similaire/similar, merge/fusion

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd     --input $SPOOKI_DIR/pluginsRelatedStuff/GridMergeSimilar/testsFiles/inputFile.std] >>
                [GetDictionaryInformation --dataBase STATIONS --table STATIONSFB --outputAttribute FictiveStationFlag ] >>
                [GridMergeSimilar] >> [PrintIMO]"
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

 
