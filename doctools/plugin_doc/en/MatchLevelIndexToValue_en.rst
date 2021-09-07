English
-------

**Description:**

-  Associates, to each vertical level index given, a value of one or
   many 3D meteorological fields given in input.
   ***Note:*** The numbering of the indices starts at zero

\*Iteration method:\*

-  Column by column

\*Dependencies:\*

-  A field of vertical level indexes, IND (2D)
-  One or many meteorological field(s) (3D)

\*Result(s):\*

-  Meteorological field(s) (2D) which the values correspond to those of
   the vertical levels specified by the index field IND

\*Algorithm:\*

.. code:: example

    For IND, a 2D field of vertical level indexes, where the index numbering starts at 0.

    For each 3D meteorological field, CHP3D, given in input, do :
        For each i,j
            CHP2D(i,j) = CHP3D(i,j,IND(i,j))
        End loop on i,j
    End loop on the fields

**Reference:**

-  None

\*Keywords:\*

-  UTILITAIRE/UTILITY, associer/match, niveau/level, vertical

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MatchLevelIndexToValue/testsFiles/inputFile.std] >>
                [MatchLevelIndexToValue] >>
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

 
