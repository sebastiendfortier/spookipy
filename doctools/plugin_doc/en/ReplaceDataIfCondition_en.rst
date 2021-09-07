English
-------

**Description:**

-  For each element of a field, remplaces the values that coressponds to
   a given condition by value parameter

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  A meteorological field

\*Result(s):\*

-  The field with values that correspond to condition replaced by the
   value parameter

\*Algorithm:\*

-  For each vlaue of a field, if ( x corresponds to condition ) replace
   the value by the given value in parameter

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, remplacer/replace

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderCsv --input $SPOOKI_DIR/pluginsRelatedStuff/ReplaceDataIfCondition/testsFiles/simple_input.csv] >>
                [ReplaceDataIfCondition --condition <1 --value -999.0] >>
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

 
